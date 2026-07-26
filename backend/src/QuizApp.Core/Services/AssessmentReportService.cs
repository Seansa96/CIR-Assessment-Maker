using System.Text;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Core.Services;

public sealed class AssessmentReportService
{
    public const int MaxCommentLength = 1000;
    public const int MaxContextIdLength = 200;

    private readonly IAssessmentReportRepository reportRepository;
    private readonly IAssessmentRepository assessmentRepository;
    private readonly IAttemptRepository attemptRepository;
    private readonly IAttemptSessionStore attemptSessionStore;

    public AssessmentReportService(
        IAssessmentReportRepository reportRepository,
        IAssessmentRepository assessmentRepository,
        IAttemptRepository attemptRepository,
        IAttemptSessionStore attemptSessionStore)
    {
        this.reportRepository = reportRepository;
        this.assessmentRepository = assessmentRepository;
        this.attemptRepository = attemptRepository;
        this.attemptSessionStore = attemptSessionStore;
    }

    public async Task<AssessmentReportEntry> CreateAsync(
        string assessmentId,
        string attemptId,
        string? contextId,
        AssessmentReportKind kind,
        string comment,
        CancellationToken cancellationToken = default)
    {
        assessmentId = Required(assessmentId, "assessment ID", "INVALID_ASSESSMENT_ID");
        attemptId = Required(attemptId, "attempt ID", "INVALID_ATTEMPT_ID");
        comment = Required(comment, "comment", "INVALID_REPORT_COMMENT");
        contextId = string.IsNullOrWhiteSpace(contextId) ? null : contextId.Trim();

        if (comment.Length > MaxCommentLength)
        {
            throw Validation(
                "INVALID_REPORT_COMMENT",
                $"Report comments must be between 1 and {MaxCommentLength} characters.");
        }

        if (contextId?.Length > MaxContextIdLength)
        {
            throw Validation(
                "INVALID_REPORT_CONTEXT",
                $"Report context IDs cannot exceed {MaxContextIdLength} characters.");
        }

        if (!Enum.IsDefined(kind))
        {
            throw Validation("INVALID_REPORT_KIND", "Report kind must be bug, improvement, or comment.");
        }

        var assessment = await assessmentRepository.GetByIdAsync(assessmentId, cancellationToken)
            ?? throw NotFound("ASSESSMENT_NOT_FOUND", $"Assessment '{assessmentId}' was not found.");
        var attempt = await attemptSessionStore.GetByIdAsync(attemptId, cancellationToken)
            ?? await attemptRepository.GetByIdAsync(attemptId, cancellationToken)
            ?? throw NotFound("ATTEMPT_NOT_FOUND", $"Attempt '{attemptId}' was not found.");

        if (!string.Equals(attempt.AssessmentId, assessment.Id, StringComparison.OrdinalIgnoreCase))
        {
            throw new AssessmentReportException(
                AssessmentReportErrorKind.Conflict,
                "ATTEMPT_ASSESSMENT_MISMATCH",
                $"Attempt '{attemptId}' belongs to assessment '{attempt.AssessmentId}', not '{assessment.Id}'.");
        }

        var createdAt = DateTimeOffset.UtcNow;
        var entry = new AssessmentReportEntry(
            $"report-{Guid.NewGuid():N}",
            assessment.Id,
            assessment.Title,
            attempt.Id,
            contextId,
            kind,
            comment,
            AssessmentReportStatus.Open,
            createdAt,
            null);
        await reportRepository.AddAsync(entry, cancellationToken);
        return entry;
    }

    public async Task<AssessmentReportDashboard> GetDashboardAsync(
        AssessmentReportFilter filter,
        CancellationToken cancellationToken = default)
    {
        var allEntries = await reportRepository.ListAsync(cancellationToken);
        var entries = allEntries
            .Where(entry => string.IsNullOrWhiteSpace(filter.AssessmentId)
                || string.Equals(entry.AssessmentId, filter.AssessmentId.Trim(), StringComparison.OrdinalIgnoreCase))
            .Where(entry => filter.Kind is null || entry.Kind == filter.Kind)
            .Where(entry => filter.Status is null || entry.Status == filter.Status)
            .OrderBy(entry => entry.Status is AssessmentReportStatus.Open ? 0 : 1)
            .ThenByDescending(entry => entry.CreatedAt)
            .ThenBy(entry => entry.Id, StringComparer.Ordinal)
            .ToList();

        var groups = entries
            .GroupBy(entry => entry.AssessmentId, StringComparer.OrdinalIgnoreCase)
            .Select(group =>
            {
                var latest = group.OrderByDescending(entry => entry.CreatedAt).ThenBy(entry => entry.Id, StringComparer.Ordinal).First();
                return new AssessmentReportGroup(
                    group.Key,
                    latest.AssessmentTitle,
                    group.Count(),
                    group.Count(entry => entry.Status is AssessmentReportStatus.Open),
                    group.Count(entry => entry.Status is AssessmentReportStatus.Resolved),
                    group.Count(entry => entry.Kind is AssessmentReportKind.Bug),
                    group.Count(entry => entry.Kind is AssessmentReportKind.Improvement),
                    group.Count(entry => entry.Kind is AssessmentReportKind.Comment),
                    group.Max(entry => entry.CreatedAt));
            })
            .OrderByDescending(group => group.OpenCount)
            .ThenByDescending(group => group.LatestReportedAt)
            .ThenBy(group => group.AssessmentTitle, StringComparer.OrdinalIgnoreCase)
            .ThenBy(group => group.AssessmentId, StringComparer.OrdinalIgnoreCase)
            .ToList();

        return new AssessmentReportDashboard(entries, groups);
    }

    public async Task<AssessmentReportEntry> SetStatusAsync(
        string reportId,
        AssessmentReportStatus status,
        CancellationToken cancellationToken = default)
    {
        reportId = Required(reportId, "report ID", "INVALID_REPORT_ID");
        if (!Enum.IsDefined(status))
        {
            throw Validation("INVALID_REPORT_STATUS", "Report status must be open or resolved.");
        }

        DateTimeOffset? resolvedAt = status is AssessmentReportStatus.Resolved ? DateTimeOffset.UtcNow : null;
        return await reportRepository.SetStatusAsync(reportId, status, resolvedAt, cancellationToken)
            ?? throw NotFound("REPORT_NOT_FOUND", $"Assessment report '{reportId}' was not found.");
    }

    public async Task<string> FormatMarkdownAsync(
        AssessmentReportFilter filter,
        CancellationToken cancellationToken = default)
    {
        var dashboard = await GetDashboardAsync(filter, cancellationToken);
        return AssessmentReportMarkdownFormatter.Format(dashboard);
    }

    private static string Required(string? value, string fieldName, string code)
    {
        var normalized = value?.Trim();
        if (string.IsNullOrEmpty(normalized))
        {
            throw Validation(code, $"A {fieldName} is required.");
        }

        return normalized;
    }

    private static AssessmentReportException Validation(string code, string message)
        => new(AssessmentReportErrorKind.Validation, code, message);

    private static AssessmentReportException NotFound(string code, string message)
        => new(AssessmentReportErrorKind.NotFound, code, message);
}

public static class AssessmentReportMarkdownFormatter
{
    public static string Format(AssessmentReportDashboard dashboard)
    {
        var builder = new StringBuilder();
        builder.AppendLine("# Assessment Report Summary");
        builder.AppendLine();
        builder.AppendLine("| Assessment | Open | Resolved | Bugs | Improvements | Comments | Total |");
        builder.AppendLine("|---|---:|---:|---:|---:|---:|---:|");
        foreach (var group in dashboard.Assessments)
        {
            builder.Append("| ")
                .Append(Escape(group.AssessmentTitle))
                .Append(" (`").Append(EscapeCode(group.AssessmentId)).Append("`) | ")
                .Append(group.OpenCount).Append(" | ")
                .Append(group.ResolvedCount).Append(" | ")
                .Append(group.BugCount).Append(" | ")
                .Append(group.ImprovementCount).Append(" | ")
                .Append(group.CommentCount).Append(" | ")
                .Append(group.TotalCount).AppendLine(" |");
        }

        builder.AppendLine();
        builder.AppendLine("# Assessment Reports");
        builder.AppendLine();
        builder.AppendLine("| Status | Kind | Assessment | Context | Comment | Attempt | Created (UTC) |");
        builder.AppendLine("|---|---|---|---|---|---|---|");
        foreach (var entry in dashboard.Entries)
        {
            builder.Append("| ").Append(entry.Status.ToString().ToLowerInvariant())
                .Append(" | ").Append(entry.Kind.ToString().ToLowerInvariant())
                .Append(" | ").Append(Escape(entry.AssessmentTitle))
                .Append(" (`").Append(EscapeCode(entry.AssessmentId)).Append("`)")
                .Append(" | ").Append(Escape(entry.ContextId ?? "—"))
                .Append(" | ").Append(Escape(entry.Comment))
                .Append(" | `").Append(EscapeCode(entry.AttemptId)).Append('`')
                .Append(" | ").Append(entry.CreatedAt.UtcDateTime.ToString("yyyy-MM-dd HH:mm:ss"))
                .AppendLine(" |");
        }

        return builder.ToString();
    }

    private static string Escape(string value)
        => value.Replace("\\", "\\\\", StringComparison.Ordinal)
            .Replace("|", "\\|", StringComparison.Ordinal)
            .Replace("\r\n", "<br>", StringComparison.Ordinal)
            .Replace("\n", "<br>", StringComparison.Ordinal)
            .Replace("\r", "<br>", StringComparison.Ordinal);

    private static string EscapeCode(string value)
        => value.Replace("`", "\\`", StringComparison.Ordinal);
}
