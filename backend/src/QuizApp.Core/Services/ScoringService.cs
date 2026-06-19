using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public sealed class ScoringService
{
    public AnswerEvaluation ScoreAnswer(QuestionDefinition question, SubmittedAnswer submittedAnswer)
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

        var answersByQuestion = attempt.Answers.ToDictionary(answer => answer.QuestionId, StringComparer.OrdinalIgnoreCase);
        var assessmentItems = GetAssessmentItems(assessment);
        var orderedQuestions = attempt.QuestionOrder
            .Select(questionId => assessmentItems.First(item => string.Equals(item.Question.Id, questionId, StringComparison.OrdinalIgnoreCase)))
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
        var percentScore = totalQuestions == 0 ? 0 : Math.Round(correctCount * 100m / totalQuestions, 2);

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
            .Select(itemId => assessment.Items.First(item => string.Equals(item.Id, itemId, StringComparison.OrdinalIgnoreCase)))
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

        return new AttemptResults(
            attempt.Id,
            assessment.Id,
            assessment.Title,
            attempt.Mode,
            attempt.Status,
            easyCount + correctCount,
            totalItems,
            totalItems == 0 ? 0 : Math.Round((easyCount + correctCount) * 100m / totalItems, 2),
            attempt.Status is AttemptStatus.Completed,
            Array.Empty<QuestionResult>())
        {
            AssessmentType = assessment.AssessmentType,
            RecallSummary = new RecallDrillSummary(reviewedCount, easyCount, correctCount, needsReviewCount, forgotCount, weakTags),
            RecallItems = itemResults
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
}
