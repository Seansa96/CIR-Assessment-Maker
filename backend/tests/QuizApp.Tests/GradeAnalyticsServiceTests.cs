using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;
using QuizApp.Core.Services;

namespace QuizApp.Tests;

public sealed class GradeAnalyticsServiceTests
{
    [Fact]
    public async Task GetSummaryAsync_computes_category_subcategory_and_area_averages_from_committed_grades()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.MultipleChoiceQuestion("q001"),
            TestData.MultipleChoiceQuestion("q002")
        });
        var attempts = new InMemoryAttemptRepository();
        var sessions = new InMemoryAttemptSessionStore();
        var grades = new InMemoryGradeLogRepository();
        var attempt = new Attempt(
            "attempt-1",
            assessment.Id,
            AssessmentMode.Scored,
            AttemptStatus.Completed,
            new[] { "q001", "q002" },
            new[]
            {
                CorrectAnswer("q001"),
                WrongAnswer("q002")
            },
            DateTimeOffset.UtcNow.AddDays(-1),
            null,
            DateTimeOffset.UtcNow,
            null);
        await attempts.SaveAsync(attempt);
        await grades.AddAsync(new GradeLogEntry("grade-1", attempt.Id, assessment.Id, assessment.Title, attempt.Mode, 1, 2, 50m, DateTimeOffset.UtcNow));
        var service = CreateService(new[] { assessment }, attempts, sessions, grades);

        var summary = await service.GetSummaryAsync(EmptyFilter());

        Assert.Equal(1, summary.CommittedEntryCount);
        Assert.Equal(50m, summary.OverallCommittedAverage);
        Assert.Contains(summary.Categories, category => category.CategoryId == "calculus-2" && category.AveragePercent == 50m);
        Assert.Contains(summary.Subcategories, subcategory => subcategory.SubcategoryId == "area-between-curves" && subcategory.AveragePercent == 50m);
        Assert.Contains(summary.Areas, area => area.AreaId == "integration" && area.AveragePercent == 50m);
        Assert.Contains(summary.WeakAreas, weak => weak.Id == "integration");
    }

    [Fact]
    public async Task GetSummaryAsync_includes_active_sessions_in_attempt_history()
    {
        var assessment = TestData.Assessment();
        var attempts = new InMemoryAttemptRepository();
        var sessions = new InMemoryAttemptSessionStore();
        await sessions.SaveAsync(new Attempt(
            "active-1",
            assessment.Id,
            AssessmentMode.Practice,
            AttemptStatus.InProgress,
            new[] { "q001" },
            Array.Empty<AttemptAnswer>(),
            DateTimeOffset.UtcNow,
            null,
            null,
            null));
        var service = CreateService(new[] { assessment }, attempts, sessions, new InMemoryGradeLogRepository());

        var summary = await service.GetSummaryAsync(EmptyFilter());

        Assert.Contains(summary.Attempts, row => row.AttemptId == "active-1" && row.Status == AttemptStatus.InProgress);
    }

    [Fact]
    public async Task GetSummaryAsync_computes_question_type_performance_from_completed_attempts()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.MultipleChoiceQuestion("q001"),
            TestData.SelectAllQuestion("q002")
        });
        var attempts = new InMemoryAttemptRepository();
        await attempts.SaveAsync(new Attempt(
            "attempt-1",
            assessment.Id,
            AssessmentMode.Practice,
            AttemptStatus.Completed,
            new[] { "q001", "q002" },
            new[]
            {
                CorrectAnswer("q001"),
                new AttemptAnswer(
                    "q002",
                    new SubmittedAnswer("q002", null, new[] { "a" }, null, null, null),
                    new AnswerEvaluation("q002", false, null, "a, b, c"),
                    DateTimeOffset.UtcNow)
            },
            DateTimeOffset.UtcNow.AddMinutes(-5),
            null,
            DateTimeOffset.UtcNow,
            null));
        var service = CreateService(new[] { assessment }, attempts, new InMemoryAttemptSessionStore(), new InMemoryGradeLogRepository());

        var summary = await service.GetSummaryAsync(EmptyFilter());

        Assert.Contains(summary.QuestionTypes, type => type.QuestionType == QuestionType.MultipleChoice && type.CorrectPercent == 100m);
        Assert.Contains(summary.QuestionTypes, type => type.QuestionType == QuestionType.SelectAll && type.CorrectPercent == 0m);
    }

    private static GradeAnalyticsService CreateService(
        IReadOnlyList<AssessmentDefinition> assessments,
        InMemoryAttemptRepository attempts,
        InMemoryAttemptSessionStore sessions,
        InMemoryGradeLogRepository grades)
    {
        return new GradeAnalyticsService(
            grades,
            attempts,
            sessions,
            new MultiAssessmentRepository(assessments),
            new AnalyticsCategoryRepository(),
            new AnalyticsAreaRepository(),
            new ScoringService(null!, null!, null!));
    }

    private static GradeAnalyticsFilter EmptyFilter()
    {
        return new GradeAnalyticsFilter(null, null, null, null, null, null, null, null, null, null, null, null);
    }

    private static AttemptAnswer CorrectAnswer(string questionId)
    {
        return new AttemptAnswer(
            questionId,
            new SubmittedAnswer(questionId, "a", Array.Empty<string>(), null, null, null),
            new AnswerEvaluation(questionId, true, null, "a"),
            DateTimeOffset.UtcNow);
    }

    private static AttemptAnswer WrongAnswer(string questionId)
    {
        return new AttemptAnswer(
            questionId,
            new SubmittedAnswer(questionId, "b", Array.Empty<string>(), null, null, null),
            new AnswerEvaluation(questionId, false, null, "a"),
            DateTimeOffset.UtcNow);
    }
}

internal sealed class MultiAssessmentRepository : IAssessmentRepository
{
    private readonly IReadOnlyList<AssessmentDefinition> assessments;

    public MultiAssessmentRepository(IReadOnlyList<AssessmentDefinition> assessments)
    {
        this.assessments = assessments;
    }

    public Task<IReadOnlyList<AssessmentSummary>> ListByCategoryAsync(string categoryId, CancellationToken cancellationToken = default)
    {
        return Task.FromResult<IReadOnlyList<AssessmentSummary>>(assessments
            .Where(assessment => string.Equals(assessment.CategoryId, categoryId, StringComparison.OrdinalIgnoreCase))
            .Select(assessment => new AssessmentSummary(assessment.Id, assessment.Title, assessment.AssessmentType, assessment.CategoryId, assessment.SubcategoryIds, assessment.Questions.Count))
            .ToList());
    }

    public Task<AssessmentDefinition?> GetByIdAsync(string assessmentId, CancellationToken cancellationToken = default)
    {
        return Task.FromResult(assessments.FirstOrDefault(assessment => string.Equals(assessment.Id, assessmentId, StringComparison.OrdinalIgnoreCase)));
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

internal sealed class AnalyticsCategoryRepository : ICategoryRepository
{
    public Task<IReadOnlyList<Category>> ListAsync(CancellationToken cancellationToken = default)
    {
        IReadOnlyList<Category> categories = new[]
        {
            new Category(1, "calculus-2", "Calculus II", new[] { new SubCategory("area-between-curves", "Area Between Curves") })
        };
        return Task.FromResult(categories);
    }
}

internal sealed class AnalyticsAreaRepository : IAreaRepository
{
    public Task<IReadOnlyList<AreaDefinition>> ListAsync(CancellationToken cancellationToken = default)
    {
        IReadOnlyList<AreaDefinition> areas = new[]
        {
            new AreaDefinition("integration", "Integration", new[] { "calculus-2" }, new[] { "area-between-curves" })
        };
        return Task.FromResult(areas);
    }
}
