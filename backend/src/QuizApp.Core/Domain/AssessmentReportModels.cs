namespace QuizApp.Core.Domain;

public enum AssessmentReportKind
{
    Bug,
    Improvement,
    Comment
}

public enum AssessmentReportStatus
{
    Open,
    Resolved
}

public sealed record AssessmentReportEntry(
    string Id,
    string AssessmentId,
    string AssessmentTitle,
    string AttemptId,
    string? ContextId,
    AssessmentReportKind Kind,
    string Comment,
    AssessmentReportStatus Status,
    DateTimeOffset CreatedAt,
    DateTimeOffset? ResolvedAt);

public sealed record AssessmentReportFilter(
    string? AssessmentId,
    AssessmentReportKind? Kind,
    AssessmentReportStatus? Status);

public sealed record AssessmentReportGroup(
    string AssessmentId,
    string AssessmentTitle,
    int TotalCount,
    int OpenCount,
    int ResolvedCount,
    int BugCount,
    int ImprovementCount,
    int CommentCount,
    DateTimeOffset LatestReportedAt);

public sealed record AssessmentReportDashboard(
    IReadOnlyList<AssessmentReportEntry> Entries,
    IReadOnlyList<AssessmentReportGroup> Assessments);

public enum AssessmentReportErrorKind
{
    Validation,
    NotFound,
    Conflict
}

public sealed class AssessmentReportException : Exception
{
    public AssessmentReportException(AssessmentReportErrorKind kind, string code, string message)
        : base(message)
    {
        Kind = kind;
        Code = code;
    }

    public AssessmentReportErrorKind Kind { get; }

    public string Code { get; }
}
