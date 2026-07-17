namespace QuizApp.Core.Domain;

public sealed record AreaDefinition(
    string Id,
    string Title,
    IReadOnlyList<string> CategoryIds,
    IReadOnlyList<string> SubcategoryIds,
    string? Description = null,
    int Index = 0);

public sealed record GradeAnalyticsFilter(
    AttemptStatus? Status,
    AssessmentMode? Mode,
    AssessmentType? AssessmentType,
    string? CategoryId,
    string? SubcategoryId,
    string? AreaId,
    QuestionType? QuestionType,
    bool? Committed,
    DateTimeOffset? From,
    DateTimeOffset? To,
    decimal? MinScore,
    decimal? MaxScore);

public sealed record GradeAnalyticsSummary(
    int CommittedEntryCount,
    decimal? OverallCommittedAverage,
    AnalyticsFocus? WeakestCategory,
    AnalyticsFocus? WeakestArea,
    QuestionTypePerformance? WeakestQuestionType,
    IReadOnlyList<CategoryGradeAnalytics> Categories,
    IReadOnlyList<SubcategoryGradeAnalytics> Subcategories,
    IReadOnlyList<AreaGradeAnalytics> Areas,
    IReadOnlyList<QuestionTypePerformance> QuestionTypes,
    IReadOnlyList<RecallRatingAnalytics> RecallRatings,
    IReadOnlyList<RecallTagAnalytics> RecallTags,
    IReadOnlyList<RecallGroupAnalytics> RecallCategories,
    IReadOnlyList<RecallGroupAnalytics> RecallSubcategories,
    IReadOnlyList<WeakFocusSummary> WeakAreas,
    IReadOnlyList<SkillPerformance> WeakestSkills,
    IReadOnlyList<ActionableNextStep> ActionableNextSteps,
    IReadOnlyList<AttemptHistoryRow> Attempts);

public sealed record RecallRatingAnalytics(
    RecallRating Rating,
    int Count);

public sealed record RecallTagAnalytics(
    string Tag,
    int AttemptCount,
    decimal AverageRating,
    int WeakCount)
{
    public string? CategoryId { get; init; }
    public string? TopicId { get; init; }
}

public sealed record RecallGroupAnalytics(
    string Id,
    string Title,
    int AttemptCount,
    decimal AverageRating,
    int WeakCount);

public sealed record AnalyticsFocus(
    string Id,
    string Title,
    int AttemptCount,
    decimal AveragePercent);

public sealed record CategoryGradeAnalytics(
    string CategoryId,
    string CategoryTitle,
    int AttemptCount,
    decimal AveragePercent,
    decimal? LastPercent);

public sealed record SubcategoryGradeAnalytics(
    string SubcategoryId,
    string SubcategoryTitle,
    string CategoryId,
    int AttemptCount,
    decimal AveragePercent,
    decimal? LastPercent);

public sealed record AreaGradeAnalytics(
    string AreaId,
    string AreaTitle,
    int AttemptCount,
    decimal AveragePercent,
    string? WeakestSubcategoryId,
    string? WeakestSubcategoryTitle)
{
    public IReadOnlyList<string> CategoryIds { get; init; } = Array.Empty<string>();
}

public sealed record QuestionTypePerformance(
    QuestionType QuestionType,
    int AnsweredCount,
    int CorrectCount,
    int NeedsReviewCount,
    decimal CorrectPercent);

public sealed record SkillPerformance(
    string SkillId,
    int AnsweredCount,
    int CorrectCount,
    decimal CorrectPercent)
{
    public string? CategoryId { get; init; }
    public string? TopicId { get; init; }
}

public sealed record ActionableNextStep(
    string SkillId,
    string Message,
    string RecommendedAssessmentId,
    string RecommendedAssessmentTitle)
{
    public string? CategoryId { get; init; }
    public string? CategoryTitle { get; init; }
    public IReadOnlyList<string>? AreaIds { get; init; }
    public IReadOnlyList<string>? AreaTitles { get; init; }
    public IReadOnlyList<string>? TopicIds { get; init; }
    public IReadOnlyList<string>? TopicTitles { get; init; }
    public string? Source { get; init; }
    public decimal? EvidencePercent { get; init; }
}

public sealed record WeakFocusSummary(
    string Id,
    string Title,
    string FocusType,
    int AttemptCount,
    decimal AveragePercent,
    string Message);

public sealed record AttemptHistoryRow(
    string AttemptId,
    string AssessmentId,
    string AssessmentTitle,
    AssessmentType AssessmentType,
    AssessmentMode Mode,
    AttemptStatus Status,
    string CategoryId,
    string CategoryTitle,
    IReadOnlyList<string> SubcategoryIds,
    IReadOnlyList<string> SubcategoryTitles,
    IReadOnlyList<string> AreaIds,
    IReadOnlyList<string> AreaTitles,
    IReadOnlyList<QuestionType> QuestionTypes,
    int CorrectCount,
    int TotalQuestions,
    decimal PercentScore,
    int AnsweredCount,
    bool HasPendingSelfChecks,
    bool IsCommitted,
    DateTimeOffset StartedAt,
    DateTimeOffset? CompletedAt,
    DateTimeOffset? LastActivityAt,
    string? LearningGoal = null,
    string? ActivityType = null);
