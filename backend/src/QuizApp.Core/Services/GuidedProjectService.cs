using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Core.Services;

public sealed class GuidedProjectService
{
    private readonly AttemptService attemptService;
    private readonly IAssessmentRepository assessmentRepository;
    private readonly IGuidedProjectSessionRepository sessionRepository;
    private readonly ISettingsRepository settingsRepository;
    private readonly ICodeRunnerClient runnerClient;

    public GuidedProjectService(
        AttemptService attemptService,
        IAssessmentRepository assessmentRepository,
        IGuidedProjectSessionRepository sessionRepository,
        ISettingsRepository settingsRepository,
        ICodeRunnerClient runnerClient)
    {
        this.attemptService = attemptService;
        this.assessmentRepository = assessmentRepository;
        this.sessionRepository = sessionRepository;
        this.settingsRepository = settingsRepository;
        this.runnerClient = runnerClient;
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

        var checkResults = new List<GuidedProjectCheckResult>();
        foreach (var check in project.RequiredChecks)
        {
            checkResults.Add(await RunCheckAsync(project, session.Files, check, required: true, settings, cancellationToken));
        }

        foreach (var check in project.BonusChecks)
        {
            checkResults.Add(await RunCheckAsync(project, session.Files, check, required: false, settings, cancellationToken));
        }

        var updated = session with
        {
            CheckResults = checkResults,
            UpdatedAt = DateTimeOffset.UtcNow
        };
        await sessionRepository.SaveAsync(updated, cancellationToken);

        return new GuidedProjectRunResult(
            updated,
            project.RequiredChecks.All(check => checkResults.Any(result =>
                result.Required
                && string.Equals(result.CheckId, check.Id, StringComparison.OrdinalIgnoreCase)
                && result.Passed)));
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

    private async Task<GuidedProjectCheckResult> RunCheckAsync(
        GuidedProjectDefinition project,
        IReadOnlyList<GuidedProjectFileState> files,
        GuidedProjectCheckDefinition check,
        bool required,
        AppSettings settings,
        CancellationToken cancellationToken)
    {
        try
        {
            var request = BuildRequest(project, files, check, settings);
            var result = await runnerClient.ExecuteAsync(request, settings, cancellationToken);
            var output = (result.Stdout ?? string.Empty).Trim();
            var passed = result.Succeeded
                && check.ExpectedOutputContains.All(expected => output.Contains(expected, StringComparison.Ordinal));

            return new GuidedProjectCheckResult(
                check.Id,
                check.Title,
                required,
                passed,
                TrimOutput(result.Output ?? result.Stdout ?? result.Stderr),
                TrimOutput(result.CompileOutput),
                TrimOutput(result.Error),
                DateTimeOffset.UtcNow);
        }
        catch (Exception ex) when (ex is InvalidOperationException or HttpRequestException or TaskCanceledException)
        {
            return new GuidedProjectCheckResult(
                check.Id,
                check.Title,
                required,
                false,
                null,
                null,
                TrimOutput(ex.Message),
                DateTimeOffset.UtcNow);
        }
    }

    private static CodeRunnerExecuteRequest BuildRequest(
        GuidedProjectDefinition project,
        IReadOnlyList<GuidedProjectFileState> files,
        GuidedProjectCheckDefinition check,
        AppSettings settings)
    {
        if (!string.Equals(project.Language, "cpp", StringComparison.OrdinalIgnoreCase))
        {
            throw new InvalidOperationException("Guided project execution currently supports C++ projects.");
        }

        return new CodeRunnerExecuteRequest(
            "cpp",
            "main.cpp",
            BuildCppTestHarness(files, check.TestCode),
            settings.CodeRunnerCompileTimeoutMs,
            settings.CodeRunnerRunTimeoutMs);
    }

    private static string BuildCppTestHarness(IReadOnlyList<GuidedProjectFileState> files, string testCode)
    {
        var sourceFiles = files
            .Where(file => IsCppSourceLike(file.Path))
            .Select(file => string.Join("\n", new[]
            {
                $"// ----- {file.Path} -----",
                StripProjectLocalDirectives(file.Content)
            }));

        return string.Join("\n", new[]
        {
            "#include <bits/stdc++.h>",
            "using namespace std;"
        }.Concat(sourceFiles).Concat(new[]
        {
            "",
            "// ----- hidden check -----",
            testCode
        }));
    }

    private static bool IsCppSourceLike(string path)
    {
        return path.EndsWith(".h", StringComparison.OrdinalIgnoreCase)
            || path.EndsWith(".hpp", StringComparison.OrdinalIgnoreCase)
            || path.EndsWith(".hh", StringComparison.OrdinalIgnoreCase)
            || path.EndsWith(".cpp", StringComparison.OrdinalIgnoreCase)
            || path.EndsWith(".cc", StringComparison.OrdinalIgnoreCase)
            || path.EndsWith(".cxx", StringComparison.OrdinalIgnoreCase);
    }

    private static string StripProjectLocalDirectives(string content)
    {
        var lines = content.Replace("\r\n", "\n").Replace('\r', '\n').Split('\n');
        return string.Join("\n", lines.Where(line =>
        {
            var trimmed = line.TrimStart();
            return !trimmed.Equals("#pragma once", StringComparison.Ordinal)
                && !trimmed.StartsWith("#include \"", StringComparison.Ordinal);
        }));
    }

    private static string? TrimOutput(string? value)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            return null;
        }

        return value.Length <= 4000 ? value.Trim() : value[..4000].Trim();
    }
}
