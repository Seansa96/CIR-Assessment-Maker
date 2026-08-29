using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Core.Services;

public sealed class CourseService
{
    private readonly ICourseRepository courses;
    private readonly IAssessmentRepository assessments;
    private readonly GradeAnalyticsService analytics;
    public CourseService(ICourseRepository courses, IAssessmentRepository assessments, GradeAnalyticsService analytics) { this.courses = courses; this.assessments = assessments; this.analytics = analytics; }

    public Task<IReadOnlyList<CourseDefinition>> ListDefinitionsAsync(CancellationToken ct = default) => courses.ListDefinitionsAsync(ct);
    public Task<IReadOnlyList<CourseRun>> ListRunsAsync(CancellationToken ct = default) => courses.ListRunsAsync(ct);

    public async Task<CourseDefinition> SaveDefinitionAsync(CourseDefinition definition, bool applyToActiveRuns, CancellationToken ct = default)
    {
        ValidateDefinition(definition);
        var saved = definition with { UpdatedAt = DateTimeOffset.UtcNow, SchemaVersion = 1 };
        await courses.SaveDefinitionAsync(saved, ct);
        if (applyToActiveRuns)
        {
            foreach (var run in (await courses.ListRunsAsync(ct)).Where(run => !run.Archived && string.Equals(run.CourseId, saved.Id, StringComparison.OrdinalIgnoreCase)))
            {
                var requirements = await ResolveRequirementsAsync(saved, ct);
                await courses.SaveRunAsync(run with { Weeks = saved.Weeks, Requirements = requirements, Audit = run.Audit.Append(new CourseAuditEvent(DateTimeOffset.UtcNow, "template-applied", "Owner applied the latest course template to this active run.")).ToList() }, ct);
            }
        }
        return saved;
    }

    public async Task<CourseRun> StartRunAsync(string courseId, DateOnly? startDate, CancellationToken ct = default)
    {
        var course = await courses.GetDefinitionAsync(courseId, ct) ?? throw new InvalidOperationException("Course was not found.");
        var requirements = await ResolveRequirementsAsync(course, ct);
        var now = DateTimeOffset.UtcNow;
        var run = new CourseRun(Guid.NewGuid().ToString("n"), course.Id, course.Title, course.CategoryId, startDate ?? DateOnly.FromDateTime(now.UtcDateTime), now, course.Weeks, requirements,
            requirements.Select(requirement => new CourseRequirementProgress(requirement.Id, Array.Empty<CourseGradeRecord>(), false, null)).ToList(), [new CourseAuditEvent(now, "started", "Course run started from a template snapshot.")]);
        await courses.SaveRunAsync(run, ct); return run;
    }

    public async Task<CourseRun> ResetRunAsync(string runId, CancellationToken ct = default)
    {
        var existing = await RequireRunAsync(runId, ct);
        if (!existing.Archived) await courses.SaveRunAsync(existing with { Archived = true, Audit = existing.Audit.Append(new CourseAuditEvent(DateTimeOffset.UtcNow, "archived", "Owner reset the course; attempt history remains global.")).ToList() }, ct);
        var now = DateTimeOffset.UtcNow;
        var replacement = existing with { Id = Guid.NewGuid().ToString("n"), StartDate = DateOnly.FromDateTime(now.UtcDateTime), StartedAt = now, Archived = false,
            Progress = existing.Requirements.Select(requirement => new CourseRequirementProgress(requirement.Id, Array.Empty<CourseGradeRecord>(), false, null)).ToList(), Audit = [new CourseAuditEvent(now, "reset", $"Reset from course run {existing.Id}.")] };
        await courses.SaveRunAsync(replacement, ct); return replacement;
    }

    public async Task<CourseRunView> GetRunViewAsync(string runId, CancellationToken ct = default)
    {
        var run = await RequireRunAsync(runId, ct);
        var today = DateOnly.FromDateTime(DateTime.UtcNow);
        var statuses = run.Requirements.Select(requirement => {
            var progress = run.Progress.FirstOrDefault(item => item.RequirementId == requirement.Id) ?? new CourseRequirementProgress(requirement.Id, Array.Empty<CourseGradeRecord>(), false, null);
            var lockDate = requirement.DueDate?.AddDays(requirement.GraceDays);
            var locked = requirement.IsGraded && (progress.GradeRecords.Count >= requirement.GradedAttemptCap || (lockDate is not null && today > lockDate));
            return new CourseRequirementStatus(requirement, progress, locked, Math.Max(0, requirement.GradedAttemptCap - progress.GradeRecords.Count), lockDate);
        }).ToList();
        var summary = await analytics.GetSummaryAsync(new GradeAnalyticsFilter(null, null, null, run.CategoryId, null, null, null, null, null, null, null, null), ct);
        return new CourseRunView(run, statuses, summary.ActionableNextSteps);
    }

    public async Task<AssessmentMode> PrepareAttemptAsync(string runId, string assessmentId, AssessmentMode? requestedMode, CancellationToken ct = default)
    {
        var view = await GetRunViewAsync(runId, ct);
        if (view.Run.Archived) throw new InvalidOperationException("Archived course runs cannot start attempts.");
        var status = view.Requirements.FirstOrDefault(item => string.Equals(item.Requirement.AssessmentId, assessmentId, StringComparison.OrdinalIgnoreCase))
            ?? throw new InvalidOperationException("This assessment is not scheduled in the selected course run.");
        return status.Requirement.IsGraded && !status.IsLocked ? AssessmentMode.Scored : AssessmentMode.Practice;
    }

    public async Task RecordCompletionAsync(string runId, Attempt attempt, AttemptResults results, CancellationToken ct = default)
    {
        var run = await RequireRunAsync(runId, ct);
        if (run.Archived) return;
        var requirement = run.Requirements.FirstOrDefault(item => string.Equals(item.AssessmentId, attempt.AssessmentId, StringComparison.OrdinalIgnoreCase));
        if (requirement is null) return;
        var progress = run.Progress.First(item => item.RequirementId == requirement.Id);
        var lockDate = requirement.DueDate?.AddDays(requirement.GraceDays);
        var today = DateOnly.FromDateTime(DateTime.UtcNow);
        var alreadyRecorded = progress.GradeRecords.Any(record => string.Equals(record.AttemptId, attempt.Id, StringComparison.OrdinalIgnoreCase));
        var canGrade = !alreadyRecorded && requirement.IsGraded && attempt.Mode is AssessmentMode.Scored && progress.GradeRecords.Count < requirement.GradedAttemptCap && (lockDate is null || today <= lockDate);
        var records = canGrade ? progress.GradeRecords.Append(new CourseGradeRecord(attempt.Id, results.PercentScore, DateTimeOffset.UtcNow)).ToList() : progress.GradeRecords;
        var updated = progress with { GradeRecords = records, Completed = true, CompletedAt = progress.CompletedAt ?? DateTimeOffset.UtcNow };
        await courses.SaveRunAsync(run with { Progress = run.Progress.Where(item => item.RequirementId != updated.RequirementId).Append(updated).ToList(), Audit = run.Audit.Append(new CourseAuditEvent(DateTimeOffset.UtcNow, canGrade ? "grade-recorded" : "completed", requirement.AssessmentId)).ToList() }, ct);
    }

    private async Task<IReadOnlyList<CourseRequirement>> ResolveRequirementsAsync(CourseDefinition course, CancellationToken ct)
    {
        var catalog = await assessments.ListByCategoryAsync(course.CategoryId, ct); var result = new List<CourseRequirement>();
        foreach (var week in course.Weeks.OrderBy(week => week.Order)) foreach (var group in week.Groups)
        {
            var matches = catalog.Where(item => Matches(group, item)).ToList();
            if (matches.Count == 0) throw new InvalidOperationException($"Course group '{group.Id}' does not resolve to any assessments in category '{course.CategoryId}'.");
            foreach (var item in matches.Where(item => result.All(existing => !string.Equals(existing.AssessmentId, item.Id, StringComparison.OrdinalIgnoreCase))))
            {
                var goal = item.LearningGoal ?? NavigationInference.Infer(await assessments.GetByIdAsync(item.Id, ct) ?? throw new InvalidOperationException("Assessment disappeared during course resolution.")).LearningGoal ?? LearningGoals.Practice;
                result.Add(new CourseRequirement($"{week.Id}:{group.Id}:{item.Id}", item.Id, item.Title, goal, week.Id, group.Id, group.DueDate ?? week.DueDate, group.GraceDays ?? course.DefaultGraceDays, group.GradedAttemptCap ?? course.DefaultGradedAttemptCap, group.ReviewLinks));
            }
        }
        return result;
    }
    private static bool Matches(CourseRequirementGroup group, AssessmentSummary item) => group.TargetType.ToLowerInvariant() switch {
        "assessment" => string.Equals(item.Id, group.TargetId, StringComparison.OrdinalIgnoreCase), "topic" => string.Equals(item.TopicId, group.TargetId, StringComparison.OrdinalIgnoreCase),
        "area" => string.Equals(item.AreaId, group.TargetId, StringComparison.OrdinalIgnoreCase), "category" => true, _ => false
    } && (string.IsNullOrWhiteSpace(group.LearningGoal) || string.Equals(item.LearningGoal, group.LearningGoal, StringComparison.OrdinalIgnoreCase));
    private async Task<CourseRun> RequireRunAsync(string id, CancellationToken ct) => await courses.GetRunAsync(id, ct) ?? throw new InvalidOperationException("Course run was not found.");
    private static void ValidateDefinition(CourseDefinition definition) { if (string.IsNullOrWhiteSpace(definition.Id) || string.IsNullOrWhiteSpace(definition.CategoryId) || definition.DefaultGradedAttemptCap < 1 || definition.DefaultGraceDays < 0) throw new InvalidOperationException("Course requires an ID, category, positive attempt cap, and non-negative grace days."); }
}
