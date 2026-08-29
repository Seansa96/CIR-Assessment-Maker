namespace QuizApp.Core.Domain;

/// <summary>Local, learner-facing course configuration. This is intentionally distinct from source authoring curriculum manifests.</summary>
public sealed record CourseDefinition(
    string Id,
    string Title,
    string CategoryId,
    int DefaultGradedAttemptCap,
    int DefaultGraceDays,
    IReadOnlyList<CourseWeek> Weeks,
    DateTimeOffset UpdatedAt)
{
    public int SchemaVersion { get; init; } = 1;
    public string? OwnerNote { get; init; }
}

public sealed record CourseWeek(string Id, string Title, int Order, DateOnly? DueDate, IReadOnlyList<CourseRequirementGroup> Groups);

public sealed record CourseRequirementGroup(
    string Id,
    string TargetType,
    string TargetId,
    string? LearningGoal = null,
    DateOnly? DueDate = null,
    int? GraceDays = null,
    int? GradedAttemptCap = null,
    IReadOnlyList<string>? ReviewAssessmentIds = null)
{
    public IReadOnlyList<string> ReviewLinks => ReviewAssessmentIds ?? Array.Empty<string>();
}

public sealed record CourseRequirement(
    string Id,
    string AssessmentId,
    string AssessmentTitle,
    string LearningGoal,
    string WeekId,
    string GroupId,
    DateOnly? DueDate,
    int GraceDays,
    int GradedAttemptCap,
    IReadOnlyList<string> ReviewAssessmentIds)
{
    public bool IsGraded => LearningGoal is LearningGoals.Practice or LearningGoals.Apply or LearningGoals.Evaluate;
}

public sealed record CourseGradeRecord(string AttemptId, decimal PercentScore, DateTimeOffset CompletedAt);

public sealed record CourseRequirementProgress(
    string RequirementId,
    IReadOnlyList<CourseGradeRecord> GradeRecords,
    bool Completed,
    DateTimeOffset? CompletedAt)
{
    public decimal? BestPercent => GradeRecords.Count == 0 ? null : GradeRecords.Max(record => record.PercentScore);
}

public sealed record CourseAuditEvent(DateTimeOffset At, string Action, string Detail);

public sealed record CourseRun(
    string Id,
    string CourseId,
    string CourseTitle,
    string CategoryId,
    DateOnly StartDate,
    DateTimeOffset StartedAt,
    IReadOnlyList<CourseWeek> Weeks,
    IReadOnlyList<CourseRequirement> Requirements,
    IReadOnlyList<CourseRequirementProgress> Progress,
    IReadOnlyList<CourseAuditEvent> Audit,
    bool Archived = false);

public sealed record CourseRunView(CourseRun Run, IReadOnlyList<CourseRequirementStatus> Requirements, IReadOnlyList<ActionableNextStep> ReviewRecommendations);

public sealed record CourseRequirementStatus(
    CourseRequirement Requirement,
    CourseRequirementProgress Progress,
    bool IsLocked,
    int AttemptsRemaining,
    DateOnly? LockDate);
