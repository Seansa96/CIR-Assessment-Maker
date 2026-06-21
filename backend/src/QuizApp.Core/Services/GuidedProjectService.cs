using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Core.Services;

public sealed class GuidedProjectService
{
    private readonly AttemptService attemptService;
    private readonly IAssessmentRepository assessmentRepository;
    private readonly IGuidedProjectSessionRepository sessionRepository;
    private readonly ISettingsRepository settingsRepository;
    private readonly IEnumerable<IGuidedProjectRunner> runners;

    public GuidedProjectService(
        AttemptService attemptService,
        IAssessmentRepository assessmentRepository,
        IGuidedProjectSessionRepository sessionRepository,
        ISettingsRepository settingsRepository,
        IEnumerable<IGuidedProjectRunner> runners)
    {
        this.attemptService = attemptService;
        this.assessmentRepository = assessmentRepository;
        this.sessionRepository = sessionRepository;
        this.settingsRepository = settingsRepository;
        this.runners = runners;
    }

    public async Task<GuidedProjectSession> GetSessionAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var attempt = await attemptService.GetAsync(attemptId, cancellationToken);
        var assessment = await GetGuidedProjectAssessmentAsync(attempt.AssessmentId, cancellationToken);

        return await sessionRepository.GetAsync(attemptId, cancellationToken)
            ?? await CreateInitialSessionAsync(attempt, assessment, cancellationToken);
    }

    public async Task<GuidedProjectSession> SaveFilesAsync(
        string attemptId,
        IReadOnlyList<GuidedProjectFileState> files,
        CancellationToken cancellationToken = default)
    {
        var attempt = await attemptService.GetAsync(attemptId, cancellationToken);
        if (attempt.Status is not AttemptStatus.InProgress and not AttemptStatus.Paused)
        {
            throw new InvalidOperationException("Only active or paused guided project sessions can be saved.");
        }

        var assessment = await GetGuidedProjectAssessmentAsync(attempt.AssessmentId, cancellationToken);
        var session = await GetSessionAsync(attemptId, cancellationToken);
        var projectFiles = assessment.GuidedProject!.Files.ToDictionary(file => file.Path, StringComparer.OrdinalIgnoreCase);
        var submittedFiles = files.ToDictionary(file => file.Path, StringComparer.OrdinalIgnoreCase);

        var mergedFiles = session.Files.Select(file =>
        {
            if (!projectFiles.TryGetValue(file.Path, out var definition) || definition.ReadOnly)
            {
                return file;
            }

            return submittedFiles.TryGetValue(file.Path, out var submitted)
                ? file with { Content = submitted.Content }
                : file;
        }).ToList();

        var updated = session with { Files = mergedFiles, UpdatedAt = DateTimeOffset.UtcNow };
        await sessionRepository.SaveAsync(updated, cancellationToken);
        return updated;
    }

    public async Task<GuidedProjectRunResult> RunAsync(
        string attemptId,
        IReadOnlyList<GuidedProjectFileState> files,
        CancellationToken cancellationToken = default)
    {
        var attempt = await attemptService.GetAsync(attemptId, cancellationToken);
        if (attempt.Status is not AttemptStatus.InProgress)
        {
            throw new InvalidOperationException("Only in-progress guided project sessions can be run.");
        }

        var assessment = await GetGuidedProjectAssessmentAsync(attempt.AssessmentId, cancellationToken);
        var project = assessment.GuidedProject!;
        var settings = await settingsRepository.GetAsync(cancellationToken);
        var session = await SaveFilesAsync(attemptId, files, cancellationToken);

        var runnerMode = project.RunnerMode ?? "legacyHarness";
        var runner = runners.FirstOrDefault(r => string.Equals(r.Mode, runnerMode, StringComparison.OrdinalIgnoreCase));
        if (runner is null)
        {
            throw new InvalidOperationException($"No runner found for mode '{runnerMode}'.");
        }

        var request = new GuidedProjectRunRequest(session, assessment, settings);
        var result = await runner.RunAsync(request, cancellationToken);

        await sessionRepository.SaveAsync(result.Session, cancellationToken);
        return result;
    }

    public async Task<AttemptResults> CompleteAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var attempt = await attemptService.GetAsync(attemptId, cancellationToken);
        var assessment = await GetGuidedProjectAssessmentAsync(attempt.AssessmentId, cancellationToken);
        var session = await sessionRepository.GetAsync(attemptId, cancellationToken)
            ?? throw new InvalidOperationException("Run the guided project checks before completing the session.");

        var missingRequiredChecks = assessment.GuidedProject!.RequiredChecks
            .Where(check => !session.CheckResults.Any(result =>
                result.Required
                && string.Equals(result.CheckId, check.Id, StringComparison.OrdinalIgnoreCase)
                && result.Passed))
            .ToList();

        if (missingRequiredChecks.Count > 0)
        {
            throw new InvalidOperationException("All required guided project checks must pass before completion.");
        }

        var results = await attemptService.CompleteAsync(attemptId, cancellationToken);
        await sessionRepository.DeleteAsync(attemptId, cancellationToken);
        return results;
    }

    private async Task<GuidedProjectSession> CreateInitialSessionAsync(
        Attempt attempt,
        AssessmentDefinition assessment,
        CancellationToken cancellationToken)
    {
        var project = assessment.GuidedProject!;
        var session = new GuidedProjectSession(
            attempt.Id,
            assessment.Id,
            project.Files.Select(file => new GuidedProjectFileState(file.Path, file.Content, file.ReadOnly)).ToList(),
            Array.Empty<GuidedProjectCheckResult>(),
            DateTimeOffset.UtcNow);

        await sessionRepository.SaveAsync(session, cancellationToken);
        return session;
    }

    private async Task<AssessmentDefinition> GetGuidedProjectAssessmentAsync(
        string assessmentId,
        CancellationToken cancellationToken)
    {
        var assessment = await assessmentRepository.GetByIdAsync(assessmentId, cancellationToken)
            ?? throw new InvalidOperationException($"Assessment '{assessmentId}' was not found.");

        if (assessment.AssessmentType is not AssessmentType.GuidedProject || assessment.GuidedProject is null)
        {
            throw new InvalidOperationException("This attempt is not a guided project.");
        }

        return assessment;
    }

}
