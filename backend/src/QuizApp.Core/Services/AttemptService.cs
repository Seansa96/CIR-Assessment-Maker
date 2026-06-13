using System.Security.Cryptography;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Core.Services;

public sealed class AttemptService
{
    private readonly IAssessmentRepository assessmentRepository;
    private readonly IAttemptRepository attemptRepository;
    private readonly IGradeLogRepository gradeLogRepository;
    private readonly ISettingsRepository settingsRepository;
    private readonly AssessmentValidator validator;
    private readonly ScoringService scoringService;
    private readonly ICodeQuestionScorer codeQuestionScorer;
    private readonly ISymbolicExpressionScorer symbolicExpressionScorer;

    public AttemptService(
        IAssessmentRepository assessmentRepository,
        IAttemptRepository attemptRepository,
        IGradeLogRepository gradeLogRepository,
        ISettingsRepository settingsRepository,
        AssessmentValidator validator,
        ScoringService scoringService,
        ICodeQuestionScorer codeQuestionScorer,
        ISymbolicExpressionScorer symbolicExpressionScorer)
    {
        this.assessmentRepository = assessmentRepository;
        this.attemptRepository = attemptRepository;
        this.gradeLogRepository = gradeLogRepository;
        this.settingsRepository = settingsRepository;
        this.validator = validator;
        this.scoringService = scoringService;
        this.codeQuestionScorer = codeQuestionScorer;
        this.symbolicExpressionScorer = symbolicExpressionScorer;
    }

    public async Task<Attempt> StartAsync(string assessmentId, AssessmentMode? mode, CancellationToken cancellationToken = default)
    {
        var assessment = await GetValidAssessmentAsync(assessmentId, cancellationToken);
        var settings = await settingsRepository.GetAsync(cancellationToken);
        var selectedMode = assessment.AssessmentType is AssessmentType.WorkedExample
            ? AssessmentMode.Practice
            : mode ?? assessment.ModeDefault;
        var questionOrder = scoringService.GetAttemptQuestions(assessment).Select(question => question.Id).ToList();

        if (assessment.AssessmentType is not AssessmentType.WorkedExample
            && assessment.RandomizeQuestions
            && settings.DefaultQuestionOrder is QuestionOrderMode.Randomized)
        {
            Shuffle(questionOrder);
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

        await attemptRepository.SaveAsync(attempt, cancellationToken);
        return attempt;
    }

    public async Task<Attempt> SubmitAnswerAsync(string attemptId, SubmittedAnswer submittedAnswer, CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        if (attempt.Status is not AttemptStatus.InProgress)
        {
            throw new InvalidOperationException("Can only submit answers to an in-progress attempt.");
        }

        var assessment = await GetValidAssessmentAsync(attempt.AssessmentId, cancellationToken);
        var questions = scoringService.GetAttemptQuestions(assessment);
        var question = questions.FirstOrDefault(candidate => string.Equals(candidate.Id, submittedAnswer.QuestionId, StringComparison.OrdinalIgnoreCase))
            ?? throw new InvalidOperationException($"Question '{submittedAnswer.QuestionId}' does not exist on this assessment.");

        if (assessment.AssessmentType is AssessmentType.WorkedExample)
        {
            var currentStepId = GetCurrentWorkedExampleStepId(attempt);
            if (!string.Equals(currentStepId, submittedAnswer.QuestionId, StringComparison.OrdinalIgnoreCase))
            {
                throw new InvalidOperationException("Worked example steps must be completed in order.");
            }
        }

        var settings = await settingsRepository.GetAsync(cancellationToken);
        var evaluation = question.Type switch
        {
            QuestionType.Code => await codeQuestionScorer.ScoreAsync(question, submittedAnswer, settings, cancellationToken),
            QuestionType.SymbolicResponse => await symbolicExpressionScorer.ScoreAsync(question, submittedAnswer, settings, cancellationToken),
            _ => scoringService.ScoreAnswer(question, submittedAnswer)
        };
        var answers = attempt.Answers
            .Where(answer => !string.Equals(answer.QuestionId, submittedAnswer.QuestionId, StringComparison.OrdinalIgnoreCase))
            .Append(new AttemptAnswer(submittedAnswer.QuestionId, submittedAnswer, evaluation, DateTimeOffset.UtcNow))
            .ToList();

        var shouldCompleteWorkedExample = assessment.AssessmentType is AssessmentType.WorkedExample
            && evaluation.IsCorrect
            && attempt.QuestionOrder.All(questionId => answers.Any(answer =>
                string.Equals(answer.QuestionId, questionId, StringComparison.OrdinalIgnoreCase)
                && answer.Evaluation?.IsCorrect == true));
        var updatedAttempt = shouldCompleteWorkedExample
            ? attempt with { Answers = answers, Status = AttemptStatus.Completed, CompletedAt = DateTimeOffset.UtcNow, PausedAt = null }
            : attempt with { Answers = answers };
        await attemptRepository.SaveAsync(updatedAttempt, cancellationToken);
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
        await attemptRepository.SaveAsync(updatedAttempt, cancellationToken);
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
        await attemptRepository.SaveAsync(updatedAttempt, cancellationToken);
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
        await attemptRepository.SaveAsync(updatedAttempt, cancellationToken);
        await gradeLogRepository.RemoveByAttemptIdAsync(attemptId, cancellationToken);
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
                && answer.Evaluation?.IsCorrect == true)))
        {
            throw new InvalidOperationException("Worked examples can only be completed after every step is correct.");
        }

        var completedAttempt = attempt.Status is not AttemptStatus.Completed
            ? attempt with { Status = AttemptStatus.Completed, CompletedAt = DateTimeOffset.UtcNow, PausedAt = null }
            : attempt;

        await attemptRepository.SaveAsync(completedAttempt, cancellationToken);
        return await GetResultsAsync(completedAttempt.Id, cancellationToken);
    }

    public async Task DeleteAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        await gradeLogRepository.RemoveByAttemptIdAsync(attemptId, cancellationToken);
        await attemptRepository.DeleteAsync(attemptId, cancellationToken);
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
        var attempts = await attemptRepository.ListAsync(cancellationToken);
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

    private async Task<Attempt> GetAttemptAsync(string attemptId, CancellationToken cancellationToken)
    {
        return await attemptRepository.GetByIdAsync(attemptId, cancellationToken)
            ?? throw new InvalidOperationException($"Attempt '{attemptId}' was not found.");
    }

    private static string? GetCurrentWorkedExampleStepId(Attempt attempt)
    {
        foreach (var questionId in attempt.QuestionOrder)
        {
            var answer = attempt.Answers.LastOrDefault(candidate => string.Equals(candidate.QuestionId, questionId, StringComparison.OrdinalIgnoreCase));
            if (answer?.Evaluation?.IsCorrect != true)
            {
                return questionId;
            }
        }

        return attempt.QuestionOrder.LastOrDefault();
    }

    private static void Shuffle<T>(IList<T> values)
    {
        for (var index = values.Count - 1; index > 0; index--)
        {
            var swapIndex = RandomNumberGenerator.GetInt32(index + 1);
            (values[index], values[swapIndex]) = (values[swapIndex], values[index]);
        }
    }
}
