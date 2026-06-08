using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;
using QuizApp.Core.Services;

namespace QuizApp.Tests;

public sealed class AttemptFlowTests
{
    [Fact]
    public async Task StartAsync_saves_the_question_order_on_the_attempt()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.MultipleChoiceQuestion("q001"),
            TestData.MultipleChoiceQuestion("q002"),
            TestData.MultipleChoiceQuestion("q003")
        });
        var attempts = new InMemoryAttemptRepository();
        var service = CreateAttemptService(assessment, attempts);

        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);
        var savedAttempt = await attempts.GetByIdAsync(attempt.Id);

        Assert.NotNull(savedAttempt);
        Assert.Equal(attempt.QuestionOrder, savedAttempt.QuestionOrder);
        Assert.Equal(assessment.Questions.Count, savedAttempt.QuestionOrder.Count);
    }

    [Fact]
    public async Task Free_response_self_check_scores_and_shows_feedback_in_practice_mode()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.FreeResponseQuestion("q001") });
        var service = CreateAttemptService(assessment);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(
            attempt.Id,
            new SubmittedAnswer("q001", null, Array.Empty<string>(), "It sums upper minus lower.", true, null));

        var results = await service.GetResultsAsync(attempt.Id);

        Assert.False(results.IsComplete);
        Assert.Equal(1, results.CorrectCount);
        Assert.True(results.Questions.Single().IsCorrect);
        Assert.NotNull(results.Questions.Single().Explanation);
    }

    [Fact]
    public async Task Grade_log_commit_records_completed_attempt_once()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.MultipleChoiceQuestion("q001") });
        var attemptService = CreateAttemptService(assessment);
        var gradeRepository = new InMemoryGradeLogRepository();
        var gradeService = new GradeLogService(gradeRepository, attemptService);
        var attempt = await attemptService.StartAsync(assessment.Id, AssessmentMode.Scored);

        await attemptService.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("q001", "a", Array.Empty<string>(), null, null, null));
        await attemptService.CompleteAsync(attempt.Id);

        var firstCommit = await gradeService.CommitAttemptAsync(attempt.Id);
        var secondCommit = await gradeService.CommitAttemptAsync(attempt.Id);
        var summary = await gradeService.GetSummaryAsync();

        Assert.Equal(firstCommit.Id, secondCommit.Id);
        Assert.Equal(1, summary.EntryCount);
        Assert.Equal(100m, summary.AveragePercentScore);
    }

    [Fact]
    public async Task ListResultsAsync_returns_saved_attempt_results()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.MultipleChoiceQuestion("q001") });
        var attempts = new InMemoryAttemptRepository();
        var service = CreateAttemptService(assessment, attempts);
        var attempt = await service.StartAsync(assessment.Id, AssessmentMode.Practice);

        await service.SubmitAnswerAsync(attempt.Id, new SubmittedAnswer("q001", "a", Array.Empty<string>(), null, null, null));

        var results = await service.ListResultsAsync();

        Assert.Contains(results, result => result.AttemptId == attempt.Id && result.PercentScore == 100m);
    }

    private static AttemptService CreateAttemptService(AssessmentDefinition assessment, InMemoryAttemptRepository? attempts = null)
    {
        return new AttemptService(
            new InMemoryAssessmentRepository(assessment),
            attempts ?? new InMemoryAttemptRepository(),
            new InMemorySettingsRepository(),
            new AssessmentValidator(),
            new ScoringService());
    }
}

internal static class TestData
{
    public static AssessmentDefinition Assessment(
        AssessmentType type = AssessmentType.Quiz,
        IReadOnlyList<QuestionDefinition>? questions = null)
    {
        return new AssessmentDefinition(
            1,
            "area-between-curves-basic",
            "Area Between Curves Basic Quiz",
            type,
            "calculus-2",
            new[] { "area-between-curves" },
            AssessmentMode.Practice,
            true,
            null,
            null,
            questions ?? new[] { MultipleChoiceQuestion("q001") });
    }

    public static QuestionDefinition MultipleChoiceQuestion(string id)
    {
        return new QuestionDefinition(
            id,
            QuestionType.MultipleChoice,
            "What does the area between two curves represent?",
            new[]
            {
                new ChoiceOption("a", "The accumulated vertical difference between two functions over an interval", Array.Empty<MediaAsset>()),
                new ChoiceOption("b", "The slope of the upper function", Array.Empty<MediaAsset>())
            },
            new AnswerDefinition("a", Array.Empty<string>(), null, null, null, null, Array.Empty<MediaAsset>()),
            "Area between curves measures accumulated difference.",
            Array.Empty<MediaAsset>());
    }

    public static QuestionDefinition SelectAllQuestion(string id)
    {
        return new QuestionDefinition(
            id,
            QuestionType.SelectAll,
            "Which are valid setup steps?",
            new[]
            {
                new ChoiceOption("a", "Identify the upper function", Array.Empty<MediaAsset>()),
                new ChoiceOption("b", "Identify the lower function", Array.Empty<MediaAsset>()),
                new ChoiceOption("c", "Subtract lower from upper", Array.Empty<MediaAsset>())
            },
            new AnswerDefinition(null, new[] { "a", "b", "c" }, null, null, null, null, Array.Empty<MediaAsset>()),
            "Area between curves requires upper minus lower.",
            Array.Empty<MediaAsset>());
    }

    public static QuestionDefinition FreeResponseQuestion(string id)
    {
        return new QuestionDefinition(
            id,
            QuestionType.FreeResponse,
            "Explain what the integral represents.",
            Array.Empty<ChoiceOption>(),
            new AnswerDefinition(null, Array.Empty<string>(), "The accumulated difference between upper and lower functions.", "selfCheck", null, null, Array.Empty<MediaAsset>()),
            "The integral sums vertical differences over the interval.",
            Array.Empty<MediaAsset>());
    }

    public static QuestionDefinition NumericResponseQuestion(string id)
    {
        return new QuestionDefinition(
            id,
            QuestionType.NumericResponse,
            "Compute the volume to the nearest hundredth.",
            Array.Empty<ChoiceOption>(),
            new AnswerDefinition(null, Array.Empty<string>(), null, null, 8.38m, 0.01m, Array.Empty<MediaAsset>()),
            "The exact value is 8 pi over 3.",
            new[] { new MediaAsset("image", "/samples/volume-washer.svg", "Washer cross section diagram", null) });
    }
}

internal sealed class InMemorySettingsRepository : ISettingsRepository
{
    public Task<AppSettings> GetAsync(CancellationToken cancellationToken = default)
    {
        return Task.FromResult(new AppSettings(1, AssessmentMode.Practice, QuestionOrderMode.Randomized, 15, 25, null, null, false));
    }

    public Task SaveAsync(AppSettings settings, CancellationToken cancellationToken = default)
    {
        return Task.CompletedTask;
    }
}

internal sealed class InMemoryAssessmentRepository : IAssessmentRepository
{
    private readonly AssessmentDefinition assessment;

    public InMemoryAssessmentRepository(AssessmentDefinition assessment)
    {
        this.assessment = assessment;
    }

    public Task<IReadOnlyList<AssessmentSummary>> ListByCategoryAsync(string categoryId, CancellationToken cancellationToken = default)
    {
        IReadOnlyList<AssessmentSummary> summaries = new[]
        {
            new AssessmentSummary(assessment.Id, assessment.Title, assessment.AssessmentType, assessment.CategoryId, assessment.SubcategoryIds, assessment.Questions.Count)
        };

        return Task.FromResult(summaries);
    }

    public Task<AssessmentDefinition?> GetByIdAsync(string assessmentId, CancellationToken cancellationToken = default)
    {
        return Task.FromResult<AssessmentDefinition?>(assessment);
    }

    public Task SaveAsync(AssessmentDefinition assessment, CancellationToken cancellationToken = default)
    {
        return Task.CompletedTask;
    }

    public Task<AssessmentValidationResult> ValidateFileAsync(string fileName, CancellationToken cancellationToken = default)
    {
        return Task.FromResult(new AssessmentValidationResult(Array.Empty<ValidationIssue>()));
    }
}

internal sealed class InMemoryAttemptRepository : IAttemptRepository
{
    private readonly Dictionary<string, Attempt> attempts = new(StringComparer.OrdinalIgnoreCase);

    public Task<IReadOnlyList<Attempt>> ListAsync(CancellationToken cancellationToken = default)
    {
        return Task.FromResult<IReadOnlyList<Attempt>>(attempts.Values.OrderByDescending(attempt => attempt.StartedAt).ToList());
    }

    public Task<Attempt?> GetByIdAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        attempts.TryGetValue(attemptId, out var attempt);
        return Task.FromResult(attempt);
    }

    public Task SaveAsync(Attempt attempt, CancellationToken cancellationToken = default)
    {
        attempts[attempt.Id] = attempt;
        return Task.CompletedTask;
    }
}

internal sealed class InMemoryGradeLogRepository : IGradeLogRepository
{
    private readonly List<GradeLogEntry> entries = new();

    public Task<IReadOnlyList<GradeLogEntry>> ListAsync(CancellationToken cancellationToken = default)
    {
        return Task.FromResult<IReadOnlyList<GradeLogEntry>>(entries.ToList());
    }

    public Task AddAsync(GradeLogEntry entry, CancellationToken cancellationToken = default)
    {
        entries.Add(entry);
        return Task.CompletedTask;
    }
}
