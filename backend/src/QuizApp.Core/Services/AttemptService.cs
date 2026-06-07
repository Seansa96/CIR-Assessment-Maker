using System.Security.Cryptography;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Core.Services;

public sealed class AttemptService
{
    private readonly IAssessmentRepository assessmentRepository;
    private readonly IAttemptRepository attemptRepository;
    private readonly ISettingsRepository settingsRepository;
    private readonly AssessmentValidator validator;
    private readonly ScoringService scoringService;

    public AttemptService(
        IAssessmentRepository assessmentRepository,
        IAttemptRepository attemptRepository,
        ISettingsRepository settingsRepository,
        AssessmentValidator validator,
        ScoringService scoringService)
    {
        this.assessmentRepository = assessmentRepository;
        this.attemptRepository = attemptRepository;
        this.settingsRepository = settingsRepository;
        this.validator = validator;
        this.scoringService = scoringService;
    }

    public async Task<Attempt> StartAsync(string assessmentId, AssessmentMode? mode, CancellationToken cancellationToken = default)
    {
        var assessment = await GetValidAssessmentAsync(assessmentId, cancellationToken);
        var settings = await settingsRepository.GetAsync(cancellationToken);
        var selectedMode = mode ?? assessment.ModeDefault;
        var questionOrder = assessment.Questions.Select(question => question.Id).ToList();

        if (assessment.RandomizeQuestions && settings.DefaultQuestionOrder is QuestionOrderMode.Randomized)
        {
            Shuffle(questionOrder);
        }

        var attempt = new Attempt(
            Guid.NewGuid().ToString("n"),
            assessment.Id,
            selectedMode,
            questionOrder,
            Array.Empty<AttemptAnswer>(),
            DateTimeOffset.UtcNow,
            null);

        await attemptRepository.SaveAsync(attempt, cancellationToken);
        return attempt;
    }

    public async Task<Attempt> SubmitAnswerAsync(string attemptId, SubmittedAnswer submittedAnswer, CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        if (attempt.CompletedAt is not null)
        {
            throw new InvalidOperationException("Cannot submit answers after an attempt is complete.");
        }

        var assessment = await GetValidAssessmentAsync(attempt.AssessmentId, cancellationToken);
        var question = assessment.Questions.FirstOrDefault(candidate => string.Equals(candidate.Id, submittedAnswer.QuestionId, StringComparison.OrdinalIgnoreCase))
            ?? throw new InvalidOperationException($"Question '{submittedAnswer.QuestionId}' does not exist on this assessment.");

        var evaluation = scoringService.ScoreAnswer(question, submittedAnswer);
        var answers = attempt.Answers
            .Where(answer => !string.Equals(answer.QuestionId, submittedAnswer.QuestionId, StringComparison.OrdinalIgnoreCase))
            .Append(new AttemptAnswer(submittedAnswer.QuestionId, submittedAnswer, evaluation, DateTimeOffset.UtcNow))
            .ToList();

        var updatedAttempt = attempt with { Answers = answers };
        await attemptRepository.SaveAsync(updatedAttempt, cancellationToken);
        return updatedAttempt;
    }

    public async Task<AttemptResults> CompleteAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        var completedAttempt = attempt.CompletedAt is null
            ? attempt with { CompletedAt = DateTimeOffset.UtcNow }
            : attempt;

        await attemptRepository.SaveAsync(completedAttempt, cancellationToken);
        return await GetResultsAsync(completedAttempt.Id, cancellationToken);
    }

    public async Task<AttemptResults> GetResultsAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var attempt = await GetAttemptAsync(attemptId, cancellationToken);
        var assessment = await GetValidAssessmentAsync(attempt.AssessmentId, cancellationToken);
        return scoringService.BuildResults(assessment, attempt);
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

    private static void Shuffle<T>(IList<T> values)
    {
        for (var index = values.Count - 1; index > 0; index--)
        {
            var swapIndex = RandomNumberGenerator.GetInt32(index + 1);
            (values[index], values[swapIndex]) = (values[swapIndex], values[index]);
        }
    }
}
