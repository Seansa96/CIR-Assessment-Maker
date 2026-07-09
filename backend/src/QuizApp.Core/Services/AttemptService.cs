using System.Security.Cryptography;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Core.Services;

public sealed class AttemptService
{
    private readonly IAssessmentRepository assessmentRepository;
    private readonly IAttemptRepository attemptRepository;
    private readonly IAttemptSessionStore attemptSessionStore;
    private readonly IGradeLogRepository gradeLogRepository;
    private readonly IGuidedProjectSessionRepository guidedProjectSessionRepository;
    private readonly ISettingsRepository settingsRepository;
    private readonly AssessmentValidator validator;
    private readonly ScoringService scoringService;

    public AttemptService(
        IAssessmentRepository assessmentRepository,
        IAttemptRepository attemptRepository,
        IAttemptSessionStore attemptSessionStore,
        IGradeLogRepository gradeLogRepository,
        IGuidedProjectSessionRepository guidedProjectSessionRepository,
        ISettingsRepository settingsRepository,
        AssessmentValidator validator,
        ScoringService scoringService)
    {
        this.assessmentRepository = assessmentRepository;
        this.attemptRepository = attemptRepository;
        this.attemptSessionStore = attemptSessionStore;
        this.gradeLogRepository = gradeLogRepository;
        this.guidedProjectSessionRepository = guidedProjectSessionRepository;
        this.settingsRepository = settingsRepository;
        this.validator = validator;
        this.scoringService = scoringService;
    }

    public async Task<Attempt> StartAsync(string assessmentId, AssessmentMode? mode, CancellationToken cancellationToken = default)
    {
        var assessment = await GetValidAssessmentAsync(assessmentId, cancellationToken);
        var settings = await settingsRepository.GetAsync(cancellationToken);
        var selectedMode = IsInstructionalAssessment(assessment.AssessmentType)
            ? AssessmentMode.Practice
            : mode ?? assessment.ModeDefault;
        var questionOrder = assessment.AssessmentType switch
        {
            AssessmentType.RecallDrill => scoringService.GetRecallItems(assessment).Select(item => item.Id).ToList(),
            AssessmentType.Glossary => scoringService.GetRecallItems(assessment).Select(item => item.Id).ToList(),
            AssessmentType.ConceptLesson => assessment.Lesson!.Sections.Select(section => section.Id).ToList(),
            AssessmentType.InteractiveExploration => assessment.Exploration!.Sections.Select(section => section.Id).ToList(),
            AssessmentType.DirectedProject => assessment.DirectedProject!.Phases.SelectMany(phase => phase.Steps).Select(step => step.Id).ToList(),
            _ => scoringService.GetAttemptQuestions(assessment).Select(question => question.Id).ToList()
        };

        if ((assessment.AssessmentType is AssessmentType.Glossary && assessment.RandomizeQuestions)
            || (!IsInstructionalAssessment(assessment.AssessmentType)
            && assessment.RandomizeQuestions
            && settings.DefaultQuestionOrder is QuestionOrderMode.Randomized))
        {
            Shuffle(questionOrder);
        }

        if (assessment.AssessmentType is AssessmentType.Quiz or AssessmentType.Test
            && assessment.AttemptQuestionCount is > 0
            && assessment.AttemptQuestionCount < questionOrder.Count)
        {
            questionOrder = questionOrder.Take(assessment.AttemptQuestionCount.Value).ToList();
        }

        var attempt = new Attempt(
            Guid.NewGuid().ToString("n"),
            assessment.Id,
            selectedMode,
            AttemptStatus.InProgress,
            questionOrder,
            Array.Empty<AttemptAnswer>(),
            DateTimeOffset.UtcNow,
            null,
            null,
            null);

        await SaveAttemptAsync(attempt, cancellationToken);
        return attempt;
    }

    public async Task<Attempt> SubmitAnswerAsync(string attemptId, SubmittedAnswer submittedAnswer, CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        var assessment = await GetValidAssessmentAsync(attempt.AssessmentId, cancellationToken);
        var questions = scoringService.GetAttemptQuestions(assessment);
        var question = questions.FirstOrDefault(candidate => string.Equals(candidate.Id, submittedAnswer.QuestionId, StringComparison.OrdinalIgnoreCase))
            ?? throw new InvalidOperationException($"Question '{submittedAnswer.QuestionId}' does not exist on this assessment.");
        var existingAnswer = attempt.Answers.LastOrDefault(answer => string.Equals(answer.QuestionId, submittedAnswer.QuestionId, StringComparison.OrdinalIgnoreCase));

        if (attempt.Status is not AttemptStatus.InProgress)
        {
            if (!CanUpdateCompletedFreeResponseSelfCheck(attempt, question, submittedAnswer, existingAnswer))
            {
                throw new InvalidOperationException("Can only submit answers to an in-progress attempt.");
            }
        }

        if (assessment.AssessmentType is AssessmentType.WorkedExample)
        {
            var currentStepId = GetCurrentWorkedExampleStepId(attempt);
            if (!string.Equals(currentStepId, submittedAnswer.QuestionId, StringComparison.OrdinalIgnoreCase))
            {
                throw new InvalidOperationException("Worked example steps must be completed in order.");
            }
        }

        if (assessment.AssessmentType is AssessmentType.ConceptLesson or AssessmentType.InteractiveExploration)
        {
            var section = GetLearningSections(assessment)
                .FirstOrDefault(candidate => string.Equals(candidate.Check?.Id, submittedAnswer.QuestionId, StringComparison.OrdinalIgnoreCase))
                ?? throw new InvalidOperationException($"Learning check '{submittedAnswer.QuestionId}' does not exist on this assessment.");
            EnsureLearningSectionUnlocked(assessment, attempt, section.Id);
        }

        var answerToScore = NormalizeSubmittedAnswer(question, submittedAnswer, existingAnswer);

        var settings = await settingsRepository.GetAsync(cancellationToken);
        var evaluation = await scoringService.ScoreQuestionAsync(question, answerToScore, settings, cancellationToken);
        var answers = attempt.Answers
            .Where(answer => !string.Equals(answer.QuestionId, submittedAnswer.QuestionId, StringComparison.OrdinalIgnoreCase))
            .Append(new AttemptAnswer(answerToScore.QuestionId, answerToScore, evaluation, DateTimeOffset.UtcNow))
            .ToList();

        var shouldCompleteWorkedExample = assessment.AssessmentType is AssessmentType.WorkedExample
            && IsResolved(new AttemptAnswer(answerToScore.QuestionId, answerToScore, evaluation, DateTimeOffset.UtcNow))
            && attempt.QuestionOrder.All(questionId => answers.Any(answer =>
                string.Equals(answer.QuestionId, questionId, StringComparison.OrdinalIgnoreCase)
                && IsResolved(answer)));
        var updatedAttempt = shouldCompleteWorkedExample
            ? attempt with { Answers = answers, Status = AttemptStatus.Completed, CompletedAt = DateTimeOffset.UtcNow, PausedAt = null }
            : attempt with { Answers = answers };
        await SaveAttemptAsync(updatedAttempt, cancellationToken);
        return updatedAttempt;
    }

    public async Task<Attempt> OverrideAnswerEvaluationAsync(
        string attemptId,
        string questionId,
        bool correct,
        CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        
        if (attempt.Status is not AttemptStatus.Completed and not AttemptStatus.InProgress)
        {
            throw new InvalidOperationException("Can only override answers on an in-progress or completed attempt.");
        }

        var existingAnswerIndex = attempt.Answers.ToList().FindLastIndex(answer => 
            string.Equals(answer.QuestionId, questionId, StringComparison.OrdinalIgnoreCase));
            
        var newAnswers = attempt.Answers.ToList();

        if (existingAnswerIndex < 0)
        {
            var dummySubmitted = new SubmittedAnswer(questionId, null, Array.Empty<string>(), null, null, null);
            var newAnswer = new AttemptAnswer(questionId, dummySubmitted, null, DateTimeOffset.UtcNow, correct);
            newAnswers.Add(newAnswer);
        }
        else
        {
            var existingAnswer = attempt.Answers[existingAnswerIndex];
            newAnswers[existingAnswerIndex] = existingAnswer with { UserOverriddenCorrect = correct };
        }

        Attempt updatedAttempt;
        if (attempt.Status is AttemptStatus.InProgress)
        {
            // For in-progress Worked Examples: auto-complete the attempt if all steps are now resolved.
            var assessment = await GetValidAssessmentAsync(attempt.AssessmentId, cancellationToken);
            var shouldComplete = assessment.AssessmentType is AssessmentType.WorkedExample
                && attempt.QuestionOrder.All(qId => newAnswers.Any(a =>
                    string.Equals(a.QuestionId, qId, StringComparison.OrdinalIgnoreCase)
                    && IsResolved(a)));
            updatedAttempt = shouldComplete
                ? attempt with { Answers = newAnswers, Status = AttemptStatus.Completed, CompletedAt = DateTimeOffset.UtcNow, PausedAt = null }
                : attempt with { Answers = newAnswers };
        }
        else
        {
            updatedAttempt = attempt with { Answers = newAnswers };
        }

        await SaveAttemptAsync(updatedAttempt, cancellationToken);
        return updatedAttempt;
    }

    public async Task<Attempt> UpdateLearningSectionStateAsync(
        string attemptId,
        string sectionId,
        bool visited,
        bool interactionChanged,
        IReadOnlyDictionary<string, System.Text.Json.JsonElement>? controlValues,
        CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        var assessment = await GetValidAssessmentAsync(attempt.AssessmentId, cancellationToken);
        EnsureLearningAssessment(assessment);
        EnsureLearningAttemptInProgress(attempt);
        var section = GetLearningSections(assessment)
            .FirstOrDefault(candidate => string.Equals(candidate.Id, sectionId, StringComparison.OrdinalIgnoreCase))
            ?? throw new InvalidOperationException($"Learning section '{sectionId}' does not exist on this assessment.");
        EnsureLearningSectionUnlocked(assessment, attempt, section.Id);

        var existing = attempt.LearningSections.FirstOrDefault(candidate =>
            string.Equals(candidate.SectionId, section.Id, StringComparison.OrdinalIgnoreCase));
        var updated = new LearningSectionAttempt(
            section.Id,
            visited || existing?.Visited == true,
            interactionChanged || existing?.InteractionChanged == true,
            existing?.Completed == true,
            controlValues ?? existing?.ControlValues ?? new Dictionary<string, System.Text.Json.JsonElement>(),
            DateTimeOffset.UtcNow);
        var updatedAttempt = attempt with
        {
            LearningSections = ReplaceLearningSection(attempt.LearningSections, updated)
        };
        await SaveAttemptAsync(updatedAttempt, cancellationToken);
        return updatedAttempt;
    }

    public async Task<Attempt> CompleteLearningSectionAsync(
        string attemptId,
        string sectionId,
        CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        var assessment = await GetValidAssessmentAsync(attempt.AssessmentId, cancellationToken);
        EnsureLearningAssessment(assessment);
        EnsureLearningAttemptInProgress(attempt);
        var section = GetLearningSections(assessment)
            .FirstOrDefault(candidate => string.Equals(candidate.Id, sectionId, StringComparison.OrdinalIgnoreCase))
            ?? throw new InvalidOperationException($"Learning section '{sectionId}' does not exist on this assessment.");
        EnsureLearningSectionUnlocked(assessment, attempt, section.Id);

        var existing = attempt.LearningSections.FirstOrDefault(candidate =>
            string.Equals(candidate.SectionId, section.Id, StringComparison.OrdinalIgnoreCase));
        if (assessment.AssessmentType is AssessmentType.InteractiveExploration
            && existing?.InteractionChanged != true)
        {
            throw new InvalidOperationException("Change at least one exploration control before continuing.");
        }
        if (section.Check is not null && !attempt.Answers.Any(answer =>
            string.Equals(answer.QuestionId, section.Check.Id, StringComparison.OrdinalIgnoreCase)
            && IsResolved(answer)))
        {
            throw new InvalidOperationException("Complete the section check correctly before continuing.");
        }

        var completedSection = new LearningSectionAttempt(
            section.Id,
            true,
            existing?.InteractionChanged == true,
            true,
            existing?.ControlValues ?? new Dictionary<string, System.Text.Json.JsonElement>(),
            DateTimeOffset.UtcNow);
        var learningSections = ReplaceLearningSection(attempt.LearningSections, completedSection);
        var requiredComplete = GetLearningSections(assessment)
            .Where(candidate => candidate.Required)
            .All(candidate => learningSections.Any(progress =>
                string.Equals(progress.SectionId, candidate.Id, StringComparison.OrdinalIgnoreCase)
                && progress.Completed));
        var updatedAttempt = requiredComplete && assessment.AssessmentType is not AssessmentType.Glossary
            ? attempt with
            {
                LearningSections = learningSections,
                Status = AttemptStatus.Completed,
                CompletedAt = DateTimeOffset.UtcNow,
                PausedAt = null
            }
            : attempt with { LearningSections = learningSections };
        await SaveAttemptAsync(updatedAttempt, cancellationToken);
        return updatedAttempt;
    }

    public async Task<Attempt> UpdateDirectedProjectStepStateAsync(
        string attemptId,
        string stepId,
        bool visited,
        bool completed,
        IReadOnlyList<string> completedChecklistItemIds,
        string? notes,
        CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        var assessment = await GetValidAssessmentAsync(attempt.AssessmentId, cancellationToken);
        
        if (assessment.AssessmentType is not AssessmentType.DirectedProject)
        {
            throw new InvalidOperationException("Only directed projects use directed project step state.");
        }
        
        if (attempt.Status is not AttemptStatus.InProgress)
        {
            throw new InvalidOperationException("Directed project state can only be changed on an in-progress attempt.");
        }

        var stepExists = assessment.DirectedProject!.Phases.SelectMany(p => p.Steps).Any(s => string.Equals(s.Id, stepId, StringComparison.OrdinalIgnoreCase));
        if (!stepExists)
        {
            throw new InvalidOperationException($"Directed project step '{stepId}' does not exist on this assessment.");
        }

        var existing = attempt.DirectedProjectSteps.FirstOrDefault(candidate =>
            string.Equals(candidate.StepId, stepId, StringComparison.OrdinalIgnoreCase));
            
        var updated = new DirectedProjectStepAttempt(
            stepId,
            visited || existing?.Visited == true,
            completed || existing?.Completed == true,
            completedChecklistItemIds,
            notes ?? existing?.Notes,
            DateTimeOffset.UtcNow);

        var updatedAttempt = attempt with
        {
            DirectedProjectSteps = attempt.DirectedProjectSteps
                .Where(s => !string.Equals(s.StepId, stepId, StringComparison.OrdinalIgnoreCase))
                .Append(updated)
                .ToList()
        };
        await SaveAttemptAsync(updatedAttempt, cancellationToken);
        return updatedAttempt;
    }

    public async Task<Attempt> CompleteDirectedProjectStepAsync(
        string attemptId,
        string stepId,
        CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        var assessment = await GetValidAssessmentAsync(attempt.AssessmentId, cancellationToken);
        
        if (assessment.AssessmentType is not AssessmentType.DirectedProject)
        {
            throw new InvalidOperationException("Only directed projects use directed project step state.");
        }

        if (attempt.Status is not AttemptStatus.InProgress)
        {
            throw new InvalidOperationException("Directed project state can only be changed on an in-progress attempt.");
        }

        var stepExists = assessment.DirectedProject!.Phases.SelectMany(p => p.Steps).Any(s => string.Equals(s.Id, stepId, StringComparison.OrdinalIgnoreCase));
        if (!stepExists)
        {
            throw new InvalidOperationException($"Directed project step '{stepId}' does not exist on this assessment.");
        }

        var existing = attempt.DirectedProjectSteps.FirstOrDefault(candidate =>
            string.Equals(candidate.StepId, stepId, StringComparison.OrdinalIgnoreCase));
            
        var updated = new DirectedProjectStepAttempt(
            stepId,
            true,
            true,
            existing?.CompletedChecklistItemIds ?? Array.Empty<string>(),
            existing?.Notes,
            DateTimeOffset.UtcNow);

        var directedProjectSteps = attempt.DirectedProjectSteps
            .Where(s => !string.Equals(s.StepId, stepId, StringComparison.OrdinalIgnoreCase))
            .Append(updated)
            .ToList();

        var requiredComplete = assessment.DirectedProject!.Phases
            .Where(p => p.Required)
            .SelectMany(p => p.Steps)
            .All(s => directedProjectSteps.Any(ds => string.Equals(ds.StepId, s.Id, StringComparison.OrdinalIgnoreCase) && ds.Completed));

        var updatedAttempt = requiredComplete
            ? attempt with
            {
                DirectedProjectSteps = directedProjectSteps,
                Status = AttemptStatus.Completed,
                CompletedAt = DateTimeOffset.UtcNow,
                PausedAt = null
            }
            : attempt with { DirectedProjectSteps = directedProjectSteps };

        await SaveAttemptAsync(updatedAttempt, cancellationToken);
        return updatedAttempt;
    }


    public async Task<Attempt> RevealRecallItemAsync(string attemptId, string itemId, string? userResponse, CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        var assessment = await GetValidAssessmentAsync(attempt.AssessmentId, cancellationToken);
        if (assessment.AssessmentType is not AssessmentType.RecallDrill and not AssessmentType.Glossary)
        {
            throw new InvalidOperationException("Only recall drill and glossary attempts can reveal recall answers.");
        }

        if (attempt.Status is not AttemptStatus.InProgress)
        {
            throw new InvalidOperationException("Can only reveal recall answers on an in-progress attempt.");
        }

        EnsureGlossaryStudyComplete(assessment, attempt);
        var item = scoringService.GetRecallItems(assessment).FirstOrDefault(candidate => string.Equals(candidate.Id, itemId, StringComparison.OrdinalIgnoreCase))
            ?? throw new InvalidOperationException($"Recall item '{itemId}' does not exist on this assessment.");
        if (!attempt.QuestionOrder.Contains(item.Id, StringComparer.OrdinalIgnoreCase))
        {
            throw new InvalidOperationException($"Recall item '{itemId}' is not part of this attempt.");
        }

        var existing = attempt.RecallItems.FirstOrDefault(candidate => string.Equals(candidate.ItemId, item.Id, StringComparison.OrdinalIgnoreCase));
        var response = item.Type is RecallItemType.Flashcard
            ? existing?.UserResponse
            : userResponse ?? existing?.UserResponse;
        var updatedRecall = new RecallItemAttempt(
            item.Id,
            response,
            true,
            existing?.Rating ?? RecallRating.Unknown,
            DateTimeOffset.UtcNow);
        var updatedAttempt = attempt with
        {
            RecallItems = ReplaceRecallItemAttempt(attempt.RecallItems, updatedRecall)
        };

        await SaveAttemptAsync(updatedAttempt, cancellationToken);
        return updatedAttempt;
    }

    public async Task<Attempt> RateRecallItemAsync(string attemptId, string itemId, RecallRating rating, CancellationToken cancellationToken = default)
    {
        if (rating is RecallRating.Unknown)
        {
            throw new InvalidOperationException("Recall rating must be easy, correct, needsReview, or forgotCompletely.");
        }

        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        var assessment = await GetValidAssessmentAsync(attempt.AssessmentId, cancellationToken);
        if (assessment.AssessmentType is not AssessmentType.RecallDrill and not AssessmentType.Glossary)
        {
            throw new InvalidOperationException("Only recall drill and glossary attempts can rate recall answers.");
        }

        if (attempt.Status is not AttemptStatus.InProgress)
        {
            throw new InvalidOperationException("Can only rate recall answers on an in-progress attempt.");
        }

        EnsureGlossaryStudyComplete(assessment, attempt);
        var item = scoringService.GetRecallItems(assessment).FirstOrDefault(candidate => string.Equals(candidate.Id, itemId, StringComparison.OrdinalIgnoreCase))
            ?? throw new InvalidOperationException($"Recall item '{itemId}' does not exist on this assessment.");
        var existing = attempt.RecallItems.FirstOrDefault(candidate => string.Equals(candidate.ItemId, item.Id, StringComparison.OrdinalIgnoreCase));
        if (existing?.AnswerRevealed != true)
        {
            throw new InvalidOperationException("Reveal the recall answer before rating it.");
        }

        var updatedRecall = existing with
        {
            Rating = rating,
            UpdatedAt = DateTimeOffset.UtcNow
        };
        var updatedRecallItems = ReplaceRecallItemAttempt(attempt.RecallItems, updatedRecall);
        var allRated = attempt.QuestionOrder.All(orderItemId => updatedRecallItems.Any(recall =>
            string.Equals(recall.ItemId, orderItemId, StringComparison.OrdinalIgnoreCase)
            && recall.Rating is not RecallRating.Unknown));
        var updatedAttempt = allRated
            ? attempt with { RecallItems = updatedRecallItems, Status = AttemptStatus.Completed, CompletedAt = DateTimeOffset.UtcNow, PausedAt = null }
            : attempt with { RecallItems = updatedRecallItems };

        await SaveAttemptAsync(updatedAttempt, cancellationToken);
        return updatedAttempt;
    }

    public async Task<Attempt> ResumeAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        if (attempt.Status is not AttemptStatus.InProgress and not AttemptStatus.Paused)
        {
            throw new InvalidOperationException("Only in-progress or paused attempts can be resumed.");
        }

        var updatedAttempt = attempt with
        {
            Status = AttemptStatus.InProgress,
            PausedAt = null
        };
        await SaveAttemptAsync(updatedAttempt, cancellationToken);
        return updatedAttempt;
    }

    public async Task<Attempt> PauseAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        if (attempt.Status is not AttemptStatus.InProgress and not AttemptStatus.Paused)
        {
            throw new InvalidOperationException("Only in-progress or paused attempts can be saved and quit.");
        }

        var updatedAttempt = attempt with
        {
            Status = AttemptStatus.Paused,
            PausedAt = DateTimeOffset.UtcNow
        };
        await SaveAttemptAsync(updatedAttempt, cancellationToken);
        return updatedAttempt;
    }

    public async Task<Attempt> AbandonAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        if (attempt.Status is AttemptStatus.Completed)
        {
            throw new InvalidOperationException("Completed attempts cannot be abandoned.");
        }

        var updatedAttempt = attempt with
        {
            Status = AttemptStatus.Abandoned,
            AbandonedAt = DateTimeOffset.UtcNow,
            PausedAt = null
        };
        await DeleteAsync(attemptId, cancellationToken);
        return updatedAttempt;
    }

    public async Task<AttemptResults> CompleteAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        if (attempt.Status is AttemptStatus.Abandoned)
        {
            throw new InvalidOperationException("Abandoned attempts cannot be completed.");
        }

        var assessment = await GetValidAssessmentAsync(attempt.AssessmentId, cancellationToken);
        if (assessment.AssessmentType is AssessmentType.WorkedExample
            && !attempt.QuestionOrder.All(questionId => attempt.Answers.Any(answer =>
                string.Equals(answer.QuestionId, questionId, StringComparison.OrdinalIgnoreCase)
                && IsResolved(answer))))
        {
            throw new InvalidOperationException("Worked examples can only be completed after every step is correct or resolved.");
        }

        if (assessment.AssessmentType is AssessmentType.RecallDrill
            && !attempt.QuestionOrder.All(itemId => attempt.RecallItems.Any(item =>
                string.Equals(item.ItemId, itemId, StringComparison.OrdinalIgnoreCase)
                && item.Rating is not RecallRating.Unknown)))
        {
            throw new InvalidOperationException("Recall drills can only be completed after every item is rated.");
        }

        if (assessment.AssessmentType is AssessmentType.Glossary)
        {
            EnsureGlossaryStudyComplete(assessment, attempt);
            if (!attempt.QuestionOrder.All(itemId => attempt.RecallItems.Any(item =>
                string.Equals(item.ItemId, itemId, StringComparison.OrdinalIgnoreCase)
                && item.Rating is not RecallRating.Unknown)))
            {
                throw new InvalidOperationException("Glossaries can only be completed after every drill is rated.");
            }
        }

        if (assessment.AssessmentType is AssessmentType.ConceptLesson or AssessmentType.InteractiveExploration)
        {
            var requiredSections = GetLearningSections(assessment).Where(section => section.Required).ToList();
            if (!requiredSections.All(section => attempt.LearningSections.Any(progress =>
                string.Equals(progress.SectionId, section.Id, StringComparison.OrdinalIgnoreCase)
                && progress.Completed)))
            {
                throw new InvalidOperationException("Learning sessions can only be completed after every required section is complete.");
            }
        }

        if (assessment.AssessmentType is AssessmentType.DirectedProject)
        {
            var requiredSteps = assessment.DirectedProject!.Phases.Where(p => p.Required).SelectMany(p => p.Steps).ToList();
            if (!requiredSteps.All(step => attempt.DirectedProjectSteps.Any(progress =>
                string.Equals(progress.StepId, step.Id, StringComparison.OrdinalIgnoreCase)
                && progress.Completed)))
            {
                throw new InvalidOperationException("Directed projects can only be completed after every required step is complete.");
            }
        }

        var completedAttempt = attempt.Status is not AttemptStatus.Completed
            ? attempt with { Status = AttemptStatus.Completed, CompletedAt = DateTimeOffset.UtcNow, PausedAt = null }
            : attempt;

        await SaveAttemptAsync(completedAttempt, cancellationToken);
        return await GetResultsAsync(completedAttempt.Id, cancellationToken);
    }

    public async Task DeleteAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        await gradeLogRepository.RemoveByAttemptIdAsync(attemptId, cancellationToken);
        await attemptSessionStore.DeleteAsync(attemptId, cancellationToken);
        await attemptRepository.DeleteAsync(attemptId, cancellationToken);
        await guidedProjectSessionRepository.DeleteAsync(attemptId, cancellationToken);
    }

    public async Task DeleteManyAsync(IReadOnlyList<string> attemptIds, CancellationToken cancellationToken = default)
    {
        foreach (var attemptId in attemptIds.Where(id => !string.IsNullOrWhiteSpace(id)).Distinct(StringComparer.OrdinalIgnoreCase))
        {
            await DeleteAsync(attemptId, cancellationToken);
        }
    }

    public async Task<AttemptResults> GetResultsAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        var assessment = await GetValidAssessmentAsync(attempt.AssessmentId, cancellationToken);
        return scoringService.BuildResults(assessment, attempt);
    }

    public async Task<Attempt> GetAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        return await GetAttemptAsync(attemptId, cancellationToken);
    }

    public async Task<IReadOnlyList<AttemptResults>> ListResultsAsync(CancellationToken cancellationToken = default)
    {
        var attempts = await ListAllAttemptsAsync(cancellationToken);
        var results = new List<AttemptResults>();

        foreach (var attempt in attempts)
        {
            var assessment = await assessmentRepository.GetByIdAsync(attempt.AssessmentId, cancellationToken);
            if (assessment is not null)
            {
                results.Add(scoringService.BuildResults(assessment, attempt));
            }
        }

        return results;
    }

    private async Task<AssessmentDefinition> GetValidAssessmentAsync(string assessmentId, CancellationToken cancellationToken)
    {
        var assessment = await assessmentRepository.GetByIdAsync(assessmentId, cancellationToken)
            ?? throw new InvalidOperationException($"Assessment '{assessmentId}' was not found.");

        var validation = validator.Validate(assessment);
        if (!validation.IsValid)
        {
            throw new InvalidOperationException($"Assessment '{assessmentId}' is invalid: {string.Join("; ", validation.Issues.Select(issue => issue.Message))}");
        }

        return assessment;
    }

    private static bool IsInstructionalAssessment(AssessmentType type)
    {
        return type is AssessmentType.WorkedExample
            or AssessmentType.GuidedProject
            or AssessmentType.RecallDrill
            or AssessmentType.Glossary
            or AssessmentType.ConceptLesson
            or AssessmentType.InteractiveExploration
            or AssessmentType.DirectedProject;
    }

    private static void EnsureLearningAssessment(AssessmentDefinition assessment)
    {
        if (assessment.AssessmentType is not AssessmentType.ConceptLesson
            and not AssessmentType.InteractiveExploration
            and not AssessmentType.Glossary)
        {
            throw new InvalidOperationException("Only concept lessons, interactive explorations, and glossaries use learning section state.");
        }
    }

    private static void EnsureLearningAttemptInProgress(Attempt attempt)
    {
        if (attempt.Status is not AttemptStatus.InProgress)
        {
            throw new InvalidOperationException("Learning section progress can only be changed on an in-progress attempt.");
        }
    }

    private static IReadOnlyList<LearningSectionInfo> GetLearningSections(AssessmentDefinition assessment)
    {
        return assessment.AssessmentType switch
        {
            AssessmentType.ConceptLesson => assessment.Lesson!.Sections
                .Select(section => new LearningSectionInfo(section.Id, section.Title, section.Required, section.Check))
                .ToList(),
            AssessmentType.InteractiveExploration => assessment.Exploration!.Sections
                .Select(section => new LearningSectionInfo(section.Id, section.Title, section.Required, section.Check))
                .ToList(),
            AssessmentType.Glossary => assessment.Glossary!.Sections
                .Select(section => new LearningSectionInfo(section.Id, section.Title, section.Required, null))
                .ToList(),
            _ => Array.Empty<LearningSectionInfo>()
        };
    }

    private static void EnsureGlossaryStudyComplete(AssessmentDefinition assessment, Attempt attempt)
    {
        if (assessment.AssessmentType is not AssessmentType.Glossary)
        {
            return;
        }

        var incomplete = assessment.Glossary!.Sections
            .Where(section => section.Required)
            .Any(section => !attempt.LearningSections.Any(progress =>
                string.Equals(progress.SectionId, section.Id, StringComparison.OrdinalIgnoreCase)
                && progress.Completed));
        if (incomplete)
        {
            throw new InvalidOperationException("Review every required glossary section before beginning recall.");
        }
    }

    private static void EnsureLearningSectionUnlocked(AssessmentDefinition assessment, Attempt attempt, string sectionId)
    {
        var sections = GetLearningSections(assessment);
        var index = sections.ToList().FindIndex(section => string.Equals(section.Id, sectionId, StringComparison.OrdinalIgnoreCase));
        if (index < 0)
        {
            throw new InvalidOperationException($"Learning section '{sectionId}' does not exist on this assessment.");
        }

        var blocked = sections.Take(index).Where(section => section.Required).Any(section =>
            !attempt.LearningSections.Any(progress =>
                string.Equals(progress.SectionId, section.Id, StringComparison.OrdinalIgnoreCase)
                && progress.Completed));
        if (blocked)
        {
            throw new InvalidOperationException("Complete the preceding required sections first.");
        }
    }

    private static IReadOnlyList<LearningSectionAttempt> ReplaceLearningSection(
        IReadOnlyList<LearningSectionAttempt> existing,
        LearningSectionAttempt updated)
    {
        return existing
            .Where(item => !string.Equals(item.SectionId, updated.SectionId, StringComparison.OrdinalIgnoreCase))
            .Append(updated)
            .ToList();
    }

    private sealed record LearningSectionInfo(string Id, string Title, bool Required, QuestionDefinition? Check);

    private async Task<Attempt> GetAttemptAsync(string attemptId, CancellationToken cancellationToken)
    {
        return await attemptSessionStore.GetByIdAsync(attemptId, cancellationToken)
            ?? await attemptRepository.GetByIdAsync(attemptId, cancellationToken)
            ?? throw new InvalidOperationException($"Attempt '{attemptId}' was not found.");
    }

    private async Task<IReadOnlyList<Attempt>> ListAllAttemptsAsync(CancellationToken cancellationToken)
    {
        var activeAttempts = await attemptSessionStore.ListAsync(cancellationToken);
        var persistedAttempts = await attemptRepository.ListAsync(cancellationToken);

        return activeAttempts
            .Concat(persistedAttempts)
            .GroupBy(attempt => attempt.Id, StringComparer.OrdinalIgnoreCase)
            .Select(group => group.First())
            .OrderByDescending(attempt => attempt.StartedAt)
            .ToList();
    }

    private async Task SaveAttemptAsync(Attempt attempt, CancellationToken cancellationToken)
    {
        if (attempt.Status is AttemptStatus.InProgress)
        {
            await attemptSessionStore.SaveAsync(attempt, cancellationToken);
            return;
        }

        await attemptRepository.SaveAsync(attempt, cancellationToken);
        await attemptSessionStore.DeleteAsync(attempt.Id, cancellationToken);
    }

    private static bool CanUpdateCompletedFreeResponseSelfCheck(
        Attempt attempt,
        QuestionDefinition question,
        SubmittedAnswer submittedAnswer,
        AttemptAnswer? existingAnswer)
    {
        return attempt.Status is AttemptStatus.Completed
            && question.Type is QuestionType.FreeResponse
            && existingAnswer?.Answer.FreeResponseText is not null
            && submittedAnswer.SelfCheckCorrect is not null;
    }

    private static SubmittedAnswer NormalizeSubmittedAnswer(
        QuestionDefinition question,
        SubmittedAnswer submittedAnswer,
        AttemptAnswer? existingAnswer)
    {
        if (question.Type is not QuestionType.FreeResponse
            || submittedAnswer.SelfCheckCorrect is null
            || existingAnswer?.Answer.FreeResponseText is null)
        {
            return submittedAnswer;
        }

        return submittedAnswer with { FreeResponseText = existingAnswer.Answer.FreeResponseText };
    }

    private static string? GetCurrentWorkedExampleStepId(Attempt attempt)
    {
        foreach (var questionId in attempt.QuestionOrder)
        {
            var answer = attempt.Answers.LastOrDefault(candidate => string.Equals(candidate.QuestionId, questionId, StringComparison.OrdinalIgnoreCase));
            if (answer == null || !IsResolved(answer))
            {
                return questionId;
            }
        }

        return attempt.QuestionOrder.LastOrDefault();
    }

    private static bool IsResolved(AttemptAnswer answer)
    {
        return answer.UserOverriddenCorrect == true
            || answer.Evaluation?.IsCorrect == true
            || (answer.Answer.FreeResponseText is not null && answer.Answer.SelfCheckCorrect is not null);
    }

    private static IReadOnlyList<RecallItemAttempt> ReplaceRecallItemAttempt(
        IReadOnlyList<RecallItemAttempt> recallItems,
        RecallItemAttempt updated)
    {
        return recallItems
            .Where(item => !string.Equals(item.ItemId, updated.ItemId, StringComparison.OrdinalIgnoreCase))
            .Append(updated)
            .ToList();
    }

    private static void Shuffle<T>(IList<T> values)
    {
        for (var index = values.Count - 1; index > 0; index--)
        {
            var swapIndex = RandomNumberGenerator.GetInt32(index + 1);
            (values[index], values[swapIndex]) = (values[swapIndex], values[index]);
        }
    }

    public Task<IReadOnlyList<string>> GetCompletedAssessmentIdsAsync(CancellationToken cancellationToken = default)
    {
        return attemptRepository.GetCompletedAssessmentIdsAsync(cancellationToken);
    }
}
