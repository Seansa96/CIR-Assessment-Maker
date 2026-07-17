using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;
using QuizApp.Core.Services;

namespace QuizApp.Tests;

public sealed class AssessmentReportServiceTests
{
    [Fact]
    public async Task CreateAsync_uses_server_assessment_title_and_active_attempt_context()
    {
        var assessment = TestData.Assessment() with { Id = "assessment-1", Title = "Server title" };
        var sessions = new InMemoryAttemptSessionStore();
        var attempt = SampleAttempt("attempt-1", assessment.Id);
        await sessions.SaveAsync(attempt);
        var reports = new InMemoryAssessmentReportRepository();
        var service = CreateService(assessment, reports, new InMemoryAttemptRepository(), sessions);

        var created = await service.CreateAsync(
            assessment.Id,
            attempt.Id,
            " q001 ",
            AssessmentReportKind.Improvement,
            "  Add a diagram here.  ");

        Assert.Equal("Server title", created.AssessmentTitle);
        Assert.Equal("q001", created.ContextId);
        Assert.Equal("Add a diagram here.", created.Comment);
        Assert.Equal(AssessmentReportStatus.Open, created.Status);
        Assert.StartsWith("report-", created.Id);
        Assert.Equal(created, Assert.Single(await reports.ListAsync()));
    }

    [Fact]
    public async Task CreateAsync_accepts_persisted_attempt_and_optional_context()
    {
        var assessment = TestData.Assessment() with { Id = "assessment-1" };
        var attempts = new InMemoryAttemptRepository();
        var attempt = SampleAttempt("attempt-1", assessment.Id);
        await attempts.SaveAsync(attempt);
        var service = CreateService(
            assessment,
            new InMemoryAssessmentReportRepository(),
            attempts,
            new InMemoryAttemptSessionStore());

        var created = await service.CreateAsync(
            assessment.Id,
            attempt.Id,
            null,
            AssessmentReportKind.Comment,
            "General assessment note.");

        Assert.Null(created.ContextId);
    }

    [Theory]
    [InlineData("")]
    [InlineData("   ")]
    public async Task CreateAsync_rejects_blank_comments(string comment)
    {
        var (service, assessment, attempt) = await ReadyServiceAsync();

        var exception = await Assert.ThrowsAsync<AssessmentReportException>(() =>
            service.CreateAsync(assessment.Id, attempt.Id, null, AssessmentReportKind.Bug, comment));

        Assert.Equal(AssessmentReportErrorKind.Validation, exception.Kind);
        Assert.Equal("INVALID_REPORT_COMMENT", exception.Code);
    }

    [Fact]
    public async Task CreateAsync_rejects_oversized_comment_and_context()
    {
        var (service, assessment, attempt) = await ReadyServiceAsync();

        var commentException = await Assert.ThrowsAsync<AssessmentReportException>(() =>
            service.CreateAsync(
                assessment.Id,
                attempt.Id,
                null,
                AssessmentReportKind.Bug,
                new string('x', AssessmentReportService.MaxCommentLength + 1)));
        var contextException = await Assert.ThrowsAsync<AssessmentReportException>(() =>
            service.CreateAsync(
                assessment.Id,
                attempt.Id,
                new string('x', AssessmentReportService.MaxContextIdLength + 1),
                AssessmentReportKind.Bug,
                "Valid comment"));

        Assert.Equal("INVALID_REPORT_COMMENT", commentException.Code);
        Assert.Equal("INVALID_REPORT_CONTEXT", contextException.Code);
    }

    [Fact]
    public async Task CreateAsync_rejects_unknown_assessment_attempt_and_mismatch()
    {
        var assessment = TestData.Assessment() with { Id = "assessment-1" };
        var sessions = new InMemoryAttemptSessionStore();
        var mismatch = SampleAttempt("attempt-mismatch", "another-assessment");
        await sessions.SaveAsync(mismatch);
        var service = CreateService(
            assessment,
            new InMemoryAssessmentReportRepository(),
            new InMemoryAttemptRepository(),
            sessions);

        var missingAssessment = await Assert.ThrowsAsync<AssessmentReportException>(() =>
            service.CreateAsync("missing", mismatch.Id, null, AssessmentReportKind.Bug, "Valid comment"));
        var missingAttempt = await Assert.ThrowsAsync<AssessmentReportException>(() =>
            service.CreateAsync(assessment.Id, "missing", null, AssessmentReportKind.Bug, "Valid comment"));
        var mismatchException = await Assert.ThrowsAsync<AssessmentReportException>(() =>
            service.CreateAsync(assessment.Id, mismatch.Id, null, AssessmentReportKind.Bug, "Valid comment"));

        Assert.Equal(AssessmentReportErrorKind.NotFound, missingAssessment.Kind);
        Assert.Equal("ASSESSMENT_NOT_FOUND", missingAssessment.Code);
        Assert.Equal(AssessmentReportErrorKind.NotFound, missingAttempt.Kind);
        Assert.Equal("ATTEMPT_NOT_FOUND", missingAttempt.Code);
        Assert.Equal(AssessmentReportErrorKind.Conflict, mismatchException.Kind);
        Assert.Equal("ATTEMPT_ASSESSMENT_MISMATCH", mismatchException.Code);
    }

    [Fact]
    public async Task SetStatusAsync_resolves_reopens_and_rejects_unknown_report()
    {
        var (service, assessment, attempt) = await ReadyServiceAsync();
        var created = await service.CreateAsync(
            assessment.Id,
            attempt.Id,
            null,
            AssessmentReportKind.Bug,
            "Valid comment");

        var resolved = await service.SetStatusAsync(created.Id, AssessmentReportStatus.Resolved);
        var reopened = await service.SetStatusAsync(created.Id, AssessmentReportStatus.Open);
        var missing = await Assert.ThrowsAsync<AssessmentReportException>(() =>
            service.SetStatusAsync("missing", AssessmentReportStatus.Resolved));

        Assert.NotNull(resolved.ResolvedAt);
        Assert.Null(reopened.ResolvedAt);
        Assert.Equal(AssessmentReportStatus.Open, reopened.Status);
        Assert.Equal("REPORT_NOT_FOUND", missing.Code);
    }

    private static async Task<(AssessmentReportService Service, AssessmentDefinition Assessment, Attempt Attempt)> ReadyServiceAsync()
    {
        var assessment = TestData.Assessment() with { Id = "assessment-1" };
        var sessions = new InMemoryAttemptSessionStore();
        var attempt = SampleAttempt("attempt-1", assessment.Id);
        await sessions.SaveAsync(attempt);
        return (
            CreateService(
                assessment,
                new InMemoryAssessmentReportRepository(),
                new InMemoryAttemptRepository(),
                sessions),
            assessment,
            attempt);
    }

    private static AssessmentReportService CreateService(
        AssessmentDefinition assessment,
        IAssessmentReportRepository reports,
        IAttemptRepository attempts,
        IAttemptSessionStore sessions)
    {
        return new AssessmentReportService(
            reports,
            new MultiAssessmentRepository([assessment]),
            attempts,
            sessions);
    }

    internal static Attempt SampleAttempt(string id, string assessmentId)
    {
        return new Attempt(
            id,
            assessmentId,
            AssessmentMode.Practice,
            AttemptStatus.InProgress,
            ["q001"],
            [],
            DateTimeOffset.UtcNow,
            null,
            null,
            null);
    }
}

public sealed class AssessmentReportAggregationTests
{
    [Fact]
    public async Task Dashboard_groups_orders_filters_and_formats_reports_deterministically()
    {
        var reports = new InMemoryAssessmentReportRepository();
        var now = new DateTimeOffset(2026, 7, 17, 12, 0, 0, TimeSpan.Zero);
        await reports.AddAsync(Entry("r1", "assessment-b", "Beta", AssessmentReportKind.Bug, AssessmentReportStatus.Open, "Wrong | answer", now.AddMinutes(-4)));
        await reports.AddAsync(Entry("r2", "assessment-a", "Alpha", AssessmentReportKind.Improvement, AssessmentReportStatus.Open, "Add\nvisual", now.AddMinutes(-3)));
        await reports.AddAsync(Entry("r3", "assessment-a", "Alpha renamed", AssessmentReportKind.Comment, AssessmentReportStatus.Resolved, "Useful note", now.AddMinutes(-2)));
        await reports.AddAsync(Entry("r4", "assessment-a", "Alpha renamed", AssessmentReportKind.Bug, AssessmentReportStatus.Open, "Latest bug", now.AddMinutes(-1)));
        var service = new AssessmentReportService(
            reports,
            new MultiAssessmentRepository([]),
            new InMemoryAttemptRepository(),
            new InMemoryAttemptSessionStore());

        var dashboard = await service.GetDashboardAsync(new AssessmentReportFilter(null, null, AssessmentReportStatus.Open));
        var markdown = AssessmentReportMarkdownFormatter.Format(dashboard);

        Assert.Equal(["assessment-a", "assessment-b"], dashboard.Assessments.Select(group => group.AssessmentId));
        var alpha = dashboard.Assessments[0];
        Assert.Equal("Alpha renamed", alpha.AssessmentTitle);
        Assert.Equal(3, alpha.TotalCount);
        Assert.Equal(2, alpha.OpenCount);
        Assert.Equal(1, alpha.ResolvedCount);
        Assert.Equal(1, alpha.BugCount);
        Assert.Equal(1, alpha.ImprovementCount);
        Assert.Equal(1, alpha.CommentCount);
        Assert.Equal(["r4", "r2", "r1"], dashboard.Entries.Select(entry => entry.Id));
        Assert.Contains("Wrong \\| answer", markdown);
        Assert.Contains("Add<br>visual", markdown);
        Assert.DoesNotContain("Useful note", markdown);
        Assert.Contains("| Alpha renamed (`assessment-a`) | 2 | 1 | 1 | 1 | 1 | 3 |", markdown);
    }

    private static AssessmentReportEntry Entry(
        string id,
        string assessmentId,
        string title,
        AssessmentReportKind kind,
        AssessmentReportStatus status,
        string comment,
        DateTimeOffset createdAt)
    {
        return new AssessmentReportEntry(
            id,
            assessmentId,
            title,
            $"attempt-{id}",
            "q001",
            kind,
            comment,
            status,
            createdAt,
            status is AssessmentReportStatus.Resolved ? createdAt.AddMinutes(1) : null);
    }
}

internal sealed class InMemoryAssessmentReportRepository : IAssessmentReportRepository
{
    private readonly Dictionary<string, AssessmentReportEntry> entries = new(StringComparer.OrdinalIgnoreCase);

    public Task<IReadOnlyList<AssessmentReportEntry>> ListAsync(CancellationToken cancellationToken = default)
    {
        return Task.FromResult<IReadOnlyList<AssessmentReportEntry>>(entries.Values.ToList());
    }

    public Task<AssessmentReportEntry?> GetByIdAsync(string reportId, CancellationToken cancellationToken = default)
    {
        entries.TryGetValue(reportId, out var entry);
        return Task.FromResult(entry);
    }

    public Task AddAsync(AssessmentReportEntry entry, CancellationToken cancellationToken = default)
    {
        entries.Add(entry.Id, entry);
        return Task.CompletedTask;
    }

    public Task<AssessmentReportEntry?> SetStatusAsync(
        string reportId,
        AssessmentReportStatus status,
        DateTimeOffset? resolvedAt,
        CancellationToken cancellationToken = default)
    {
        if (!entries.TryGetValue(reportId, out var entry))
        {
            return Task.FromResult<AssessmentReportEntry?>(null);
        }

        var updated = entry with { Status = status, ResolvedAt = resolvedAt };
        entries[reportId] = updated;
        return Task.FromResult<AssessmentReportEntry?>(updated);
    }
}
