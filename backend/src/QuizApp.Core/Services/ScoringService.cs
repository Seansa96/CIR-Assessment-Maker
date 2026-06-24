using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public sealed class ScoringService
{
    private readonly ICodeQuestionScorer codeQuestionScorer;
    private readonly ISymbolicExpressionScorer symbolicExpressionScorer;
    private readonly ICircuitQuestionScorer circuitQuestionScorer;

    public ScoringService(
        ICodeQuestionScorer codeQuestionScorer,
        ISymbolicExpressionScorer symbolicExpressionScorer,
        ICircuitQuestionScorer circuitQuestionScorer)
    {
        this.codeQuestionScorer = codeQuestionScorer;
        this.symbolicExpressionScorer = symbolicExpressionScorer;
        this.circuitQuestionScorer = circuitQuestionScorer;
    }

    public async Task<AnswerEvaluation> ScoreQuestionAsync(QuestionDefinition question, SubmittedAnswer submittedAnswer, AppSettings settings, CancellationToken cancellationToken = default)
    {
        if (question.Type is QuestionType.Multipart)
        {
            return await ScoreMultipartQuestionAsync(question, submittedAnswer, settings, cancellationToken);
        }

        var evaluation = question.Type switch
        {
            QuestionType.Code => await codeQuestionScorer.ScoreAsync(question, submittedAnswer, settings, cancellationToken),
            QuestionType.SymbolicResponse => await symbolicExpressionScorer.ScoreAsync(question, submittedAnswer, settings, cancellationToken),
            QuestionType.Circuit => await circuitQuestionScorer.ScoreAsync(question, submittedAnswer, settings, cancellationToken),
            _ => ScoreSynchronousAnswer(question, submittedAnswer)
        };

        return evaluation with
        {
            EarnedPoints = evaluation.IsCorrect ? 1m : 0m,
            PossiblePoints = 1m
        };
    }

    private async Task<AnswerEvaluation> ScoreMultipartQuestionAsync(QuestionDefinition question, SubmittedAnswer submittedAnswer, AppSettings settings, CancellationToken cancellationToken)
    {
        var partEvaluations = new List<AnswerEvaluation>();
        var partAnswersDict = submittedAnswer.PartAnswers.ToDictionary(a => a.QuestionId, StringComparer.OrdinalIgnoreCase);

        var earnedPoints = 0m;
        var possiblePoints = 1m;
        var partWeight = question.Parts.Count > 0 ? 1m / question.Parts.Count : 0m;

        foreach (var part in question.Parts)
        {
            var partDef = new QuestionDefinition(
                Id: part.Id,
                Type: part.Type,
                Prompt: part.Prompt,
                Choices: part.Choices,
                Answer: part.Answer,
                Explanation: part.Explanation,
                Media: part.Media)
            {
                CodeQuestion = part.CodeQuestion,
                CircuitQuestion = part.CircuitQuestion
            };

            partAnswersDict.TryGetValue(part.Id, out var partSubmittedAnswer);
            if (partSubmittedAnswer is null)
            {
                partSubmittedAnswer = new SubmittedAnswer(part.Id, null, Array.Empty<string>(), null, null, null);
            }

            var partEval = await ScoreQuestionAsync(partDef, partSubmittedAnswer, settings, cancellationToken);
            var scaledEarned = partEval.IsCorrect ? partWeight : 0m;
            
            partEvaluations.Add(partEval with 
            { 
                EarnedPoints = scaledEarned,
                PossiblePoints = partWeight
            });
            earnedPoints += scaledEarned;
        }

        var isCorrect = earnedPoints >= possiblePoints - 0.0001m && earnedPoints <= possiblePoints + 0.0001m; // Floating point tolerance

        return new AnswerEvaluation(
            question.Id,
            isCorrect,
            question.Explanation,
            null)
        {
            EarnedPoints = earnedPoints,
            PossiblePoints = possiblePoints,
            PartEvaluations = partEvaluations
        };
    }

    private AnswerEvaluation ScoreSynchronousAnswer(QuestionDefinition question, SubmittedAnswer submittedAnswer)
    {
        var isCorrect = question.Type switch
        {
            QuestionType.MultipleChoice => string.Equals(question.Answer.ChoiceId, submittedAnswer.ChoiceId, StringComparison.OrdinalIgnoreCase),
            QuestionType.SelectAll => SameChoiceSet(question.Answer.ChoiceIds, submittedAnswer.ChoiceIds),
            QuestionType.FreeResponse => submittedAnswer.SelfCheckCorrect == true,
            QuestionType.NumericResponse => IsNumericCorrect(question.Answer.NumericValue, submittedAnswer.NumericValue, question.Answer.NumericTolerance),
            _ => false
        };

        return new AnswerEvaluation(
            question.Id,
            isCorrect,
            question.Explanation,
            DescribeExpectedAnswer(question));
    }

    public AttemptResults BuildResults(AssessmentDefinition assessment, Attempt attempt)
    {
        if (assessment.AssessmentType is AssessmentType.RecallDrill)
        {
            return BuildRecallResults(assessment, attempt);
        }

        if (assessment.AssessmentType is AssessmentType.ConceptLesson or AssessmentType.InteractiveExploration)
        {
            return BuildLearningResults(assessment, attempt);
        }

        var answersByQuestion = attempt.Answers.ToDictionary(answer => answer.QuestionId, StringComparer.OrdinalIgnoreCase);
        var assessmentItems = GetAssessmentItems(assessment);
        var orderedQuestions = attempt.QuestionOrder
            .Select(questionId => assessmentItems.FirstOrDefault(item => string.Equals(item.Question.Id, questionId, StringComparison.OrdinalIgnoreCase)))
            .OfType<AssessmentItem>()
            .ToList();

        var questionResults = orderedQuestions.Select(item =>
        {
            var question = item.Question;
            answersByQuestion.TryGetValue(question.Id, out var answer);
            var showFeedback = attempt.Status is AttemptStatus.Completed or AttemptStatus.Abandoned || attempt.Mode is AssessmentMode.Practice;
            var isPendingSelfCheck = question.Type is QuestionType.FreeResponse
                && answer?.Answer.FreeResponseText is not null
                && answer.Answer.SelfCheckCorrect is null;

            return new QuestionResult(
                question.Id,
                question.Prompt,
                question.Type,
                question.Media,
                answer?.Answer,
                showFeedback ? answer?.Evaluation?.IsCorrect : null,
                showFeedback ? question.Explanation : null,
                showFeedback ? DescribeExpectedAnswer(question) : null,
                showFeedback ? answer?.Evaluation?.CodeFeedback : null,
                showFeedback ? answer?.Evaluation?.SymbolicFeedback : null,
                showFeedback ? answer?.Evaluation?.CircuitFeedback : null)
            {
                Title = item.Step?.Title,
                Instruction = item.Step?.Instruction,
                Hint = item.Step?.Hint,
                ExampleId = item.Example?.Id,
                ExampleTitle = item.Example?.Title,
                Problem = item.Example?.Problem,
                KeyPoints = showFeedback ? question.Answer.KeyPoints : Array.Empty<string>(),
                IsPendingSelfCheck = isPendingSelfCheck
            };
        }).ToList();

        var correctCount = attempt.Answers.Count(answer => answer.Evaluation?.IsCorrect == true);
        var totalQuestions = attempt.QuestionOrder.Count;
        var earnedPoints = attempt.Answers.Sum(answer => answer.Evaluation?.EarnedPoints ?? 0m);
        var possiblePoints = (decimal)totalQuestions;
        var percentScore = possiblePoints == 0m ? 0m : Math.Round(earnedPoints * 100m / possiblePoints, 2);

        return new AttemptResults(
            attempt.Id,
            assessment.Id,
            assessment.Title,
            attempt.Mode,
            attempt.Status,
            correctCount,
            totalQuestions,
            percentScore,
            attempt.Status is AttemptStatus.Completed,
            questionResults)
        {
            AssessmentType = assessment.AssessmentType,
            EarnedPoints = earnedPoints,
            PossiblePoints = possiblePoints,
            HasPendingSelfChecks = questionResults.Any(question => question.IsPendingSelfCheck)
        };
    }

    public IReadOnlyList<QuestionDefinition> GetAttemptQuestions(AssessmentDefinition assessment)
    {
        return GetAssessmentItems(assessment).Select(item => item.Question).ToList();
    }

    public IReadOnlyList<RecallItemDefinition> GetRecallItems(AssessmentDefinition assessment)
    {
        return assessment.AssessmentType is AssessmentType.RecallDrill
            ? assessment.Items.ToList()
            : Array.Empty<RecallItemDefinition>();
    }

    private static AttemptResults BuildRecallResults(AssessmentDefinition assessment, Attempt attempt)
    {
        var recallAttempts = attempt.RecallItems.ToDictionary(item => item.ItemId, StringComparer.OrdinalIgnoreCase);
        var orderedItems = attempt.QuestionOrder
            .Select(itemId => assessment.Items.FirstOrDefault(item => string.Equals(item.Id, itemId, StringComparison.OrdinalIgnoreCase)))
            .OfType<RecallItemDefinition>()
            .ToList();
        var itemResults = orderedItems.Select(item =>
        {
            recallAttempts.TryGetValue(item.Id, out var recallAttempt);
            var answerRevealed = recallAttempt?.AnswerRevealed == true
                || attempt.Status is AttemptStatus.Completed or AttemptStatus.Abandoned;

            return new RecallItemResult(
                item.Id,
                item.Type,
                item.Prompt,
                recallAttempt?.UserResponse,
                answerRevealed,
                recallAttempt?.Rating ?? RecallRating.Unknown,
                answerRevealed ? item.Answer.Expected : null,
                answerRevealed ? item.Answer.ExpectedLatex : null,
                answerRevealed ? item.Answer.Aliases : Array.Empty<string>(),
                answerRevealed ? item.Explanation : null,
                item.Tags,
                item.Answer.Media);
        }).ToList();

        var easyCount = itemResults.Count(item => item.Rating is RecallRating.Easy);
        var correctCount = itemResults.Count(item => item.Rating is RecallRating.Correct);
        var needsReviewCount = itemResults.Count(item => item.Rating is RecallRating.NeedsReview);
        var forgotCount = itemResults.Count(item => item.Rating is RecallRating.ForgotCompletely);
        var weakTags = itemResults
            .Where(item => item.Rating is RecallRating.NeedsReview or RecallRating.ForgotCompletely)
            .SelectMany(item => item.Tags)
            .Where(tag => !string.IsNullOrWhiteSpace(tag))
            .GroupBy(tag => tag, StringComparer.OrdinalIgnoreCase)
            .OrderByDescending(group => group.Count())
            .ThenBy(group => group.Key)
            .Select(group => group.Key)
            .ToList();
        var reviewedCount = itemResults.Count(item => item.Rating is not RecallRating.Unknown);
        var totalItems = attempt.QuestionOrder.Count;
        var earnedPoints = (decimal)(easyCount + correctCount);
        var possiblePoints = (decimal)totalItems;

        return new AttemptResults(
            attempt.Id,
            assessment.Id,
            assessment.Title,
            attempt.Mode,
            attempt.Status,
            easyCount + correctCount,
            totalItems,
            possiblePoints == 0m ? 0m : Math.Round(earnedPoints * 100m / possiblePoints, 2),
            attempt.Status is AttemptStatus.Completed,
            Array.Empty<QuestionResult>())
        {
            AssessmentType = assessment.AssessmentType,
            EarnedPoints = earnedPoints,
            PossiblePoints = possiblePoints,
            RecallSummary = new RecallDrillSummary(reviewedCount, easyCount, correctCount, needsReviewCount, forgotCount, weakTags),
            RecallItems = itemResults
        };
    }

    private static AttemptResults BuildLearningResults(AssessmentDefinition assessment, Attempt attempt)
    {
        var progressBySection = attempt.LearningSections.ToDictionary(
            section => section.SectionId,
            StringComparer.OrdinalIgnoreCase);
        var answersByQuestion = attempt.Answers.ToDictionary(
            answer => answer.QuestionId,
            StringComparer.OrdinalIgnoreCase);
        var sections = assessment.AssessmentType is AssessmentType.ConceptLesson
            ? assessment.Lesson!.Sections.Select(section => new LearningItem(section.Id, section.Title, section.Required, section.Check)).ToList()
            : assessment.Exploration!.Sections.Select(section => new LearningItem(section.Id, section.Title, section.Required, section.Check)).ToList();

        var previousRequiredComplete = true;
        var sectionResults = new List<LearningSectionResult>();
        foreach (var section in sections)
        {
            progressBySection.TryGetValue(section.Id, out var progress);
            QuestionResult? checkResult = null;
            if (section.Check is not null)
            {
                answersByQuestion.TryGetValue(section.Check.Id, out var answer);
                checkResult = BuildQuestionResult(section.Check, answer, true);
            }

            var unlocked = previousRequiredComplete;
            sectionResults.Add(new LearningSectionResult(
                section.Id,
                section.Title,
                section.Required,
                progress?.Visited == true,
                progress?.InteractionChanged == true,
                progress?.Completed == true,
                unlocked,
                progress?.ControlValues ?? new Dictionary<string, System.Text.Json.JsonElement>(),
                checkResult));

            if (section.Required && progress?.Completed != true)
            {
                previousRequiredComplete = false;
            }
        }

        var requiredSections = sectionResults.Where(section => section.Required).ToList();
        var completedCount = requiredSections.Count(section => section.Completed);
        var totalCount = requiredSections.Count;
        var earnedPoints = (decimal)completedCount;
        var possiblePoints = (decimal)totalCount;
        return new AttemptResults(
            attempt.Id,
            assessment.Id,
            assessment.Title,
            attempt.Mode,
            attempt.Status,
            completedCount,
            totalCount,
            possiblePoints == 0m ? 0m : Math.Round(earnedPoints * 100m / possiblePoints, 2),
            attempt.Status is AttemptStatus.Completed,
            Array.Empty<QuestionResult>())
        {
            AssessmentType = assessment.AssessmentType,
            EarnedPoints = earnedPoints,
            PossiblePoints = possiblePoints,
            LearningSections = sectionResults
        };
    }

    private static QuestionResult BuildQuestionResult(
        QuestionDefinition question,
        AttemptAnswer? answer,
        bool showFeedback)
    {
        var isPendingSelfCheck = false;
        
        if (question.Type is QuestionType.Multipart)
        {
            isPendingSelfCheck = question.Parts.Any(part => 
                part.Type is QuestionType.FreeResponse 
                && answer?.Answer.PartAnswers.FirstOrDefault(pa => string.Equals(pa.QuestionId, part.Id, StringComparison.OrdinalIgnoreCase))?.FreeResponseText is not null
                && answer?.Answer.PartAnswers.FirstOrDefault(pa => string.Equals(pa.QuestionId, part.Id, StringComparison.OrdinalIgnoreCase))?.SelfCheckCorrect is null);
        }
        else
        {
            isPendingSelfCheck = question.Type is QuestionType.FreeResponse
                && answer?.Answer.FreeResponseText is not null
                && answer.Answer.SelfCheckCorrect is null;
        }

        var partResults = Array.Empty<QuestionResult>();
        if (question.Type is QuestionType.Multipart && question.Parts.Count > 0)
        {
            partResults = question.Parts.Select(part =>
            {
                var partAnswer = answer?.Answer.PartAnswers.FirstOrDefault(pa => string.Equals(pa.QuestionId, part.Id, StringComparison.OrdinalIgnoreCase));
                var partEval = answer?.Evaluation?.PartEvaluations.FirstOrDefault(pe => string.Equals(pe.QuestionId, part.Id, StringComparison.OrdinalIgnoreCase));
                
                var partDef = new QuestionDefinition(
                    Id: part.Id,
                    Type: part.Type,
                    Prompt: part.Prompt,
                    Choices: part.Choices,
                    Answer: part.Answer,
                    Explanation: part.Explanation,
                    Media: part.Media)
                {
                    CodeQuestion = part.CodeQuestion,
                    CircuitQuestion = part.CircuitQuestion
                };

                return BuildQuestionResult(partDef, partAnswer is not null ? new AttemptAnswer(part.Id, partAnswer, partEval, answer?.SubmittedAt ?? DateTimeOffset.UtcNow) : null, showFeedback);
            }).ToArray();
        }

        return new QuestionResult(
            question.Id,
            question.Prompt,
            question.Type,
            question.Media,
            answer?.Answer,
            showFeedback ? answer?.Evaluation?.IsCorrect : null,
            showFeedback ? question.Explanation : null,
            showFeedback ? DescribeExpectedAnswer(question) : null,
            showFeedback ? answer?.Evaluation?.CodeFeedback : null,
            showFeedback ? answer?.Evaluation?.SymbolicFeedback : null,
            showFeedback ? answer?.Evaluation?.CircuitFeedback : null)
        {
            KeyPoints = showFeedback ? question.Answer.KeyPoints : Array.Empty<string>(),
            IsPendingSelfCheck = isPendingSelfCheck,
            EarnedPoints = answer?.Evaluation?.EarnedPoints ?? 0m,
            PossiblePoints = answer?.Evaluation?.PossiblePoints ?? 1m,
            PartResults = partResults
        };
    }

    private static bool SameChoiceSet(IReadOnlyList<string> expected, IReadOnlyList<string> actual)
    {
        return expected.ToHashSet(StringComparer.OrdinalIgnoreCase)
            .SetEquals(actual.ToHashSet(StringComparer.OrdinalIgnoreCase));
    }

    private static string? DescribeExpectedAnswer(QuestionDefinition question)
    {
        return question.Type switch
        {
            QuestionType.MultipleChoice => question.Answer.ChoiceId,
            QuestionType.SelectAll => string.Join(", ", question.Answer.ChoiceIds),
            QuestionType.FreeResponse => question.Answer.Expected,
            QuestionType.NumericResponse => question.Answer.NumericValue?.ToString(),
            QuestionType.Code => "All code tests pass",
            QuestionType.SymbolicResponse => question.Answer.SymbolicExpectedLatex ?? question.Answer.ExpectedLatex,
            QuestionType.Circuit => "Circuit matching requirements",
            _ => null
        };
    }

    private static bool IsNumericCorrect(decimal? expected, decimal? actual, decimal? tolerance)
    {
        if (expected is null || actual is null || tolerance is null)
        {
            return false;
        }

        return Math.Abs(expected.Value - actual.Value) <= tolerance.Value;
    }

    private static IReadOnlyList<AssessmentItem> GetAssessmentItems(AssessmentDefinition assessment)
    {
        if (assessment.AssessmentType is AssessmentType.GuidedProject)
        {
            return Array.Empty<AssessmentItem>();
        }

        if (assessment.AssessmentType is AssessmentType.RecallDrill)
        {
            return Array.Empty<AssessmentItem>();
        }

        if (assessment.AssessmentType is AssessmentType.ConceptLesson)
        {
            return assessment.Lesson!.Sections
                .Where(section => section.Check is not null)
                .Select(section => new AssessmentItem(section.Check!, null, null))
                .ToList();
        }

        if (assessment.AssessmentType is AssessmentType.InteractiveExploration)
        {
            return assessment.Exploration!.Sections
                .Where(section => section.Check is not null)
                .Select(section => new AssessmentItem(section.Check!, null, null))
                .ToList();
        }

        if (assessment.AssessmentType is not AssessmentType.WorkedExample)
        {
            return assessment.Questions.Select(question => new AssessmentItem(question, null, null)).ToList();
        }

        return assessment.WorkedExamples
            .SelectMany(example => example.Steps.Select(step => new AssessmentItem(step.Question with { Id = step.Id }, example, step)))
            .ToList();
    }

    private sealed record AssessmentItem(
        QuestionDefinition Question,
        WorkedExampleDefinition? Example,
        WorkedExampleStepDefinition? Step);

    private sealed record LearningItem(
        string Id,
        string Title,
        bool Required,
        QuestionDefinition? Check);
}
