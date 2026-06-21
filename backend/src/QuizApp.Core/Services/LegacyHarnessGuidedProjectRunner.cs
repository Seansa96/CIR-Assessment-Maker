using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public sealed class LegacyHarnessGuidedProjectRunner : IGuidedProjectRunner
{
    private readonly ICodeRunnerClient _runnerClient;

    public string Mode => "legacyHarness";

    public LegacyHarnessGuidedProjectRunner(ICodeRunnerClient runnerClient)
    {
        _runnerClient = runnerClient;
    }

    public async Task<GuidedProjectRunResult> RunAsync(
        GuidedProjectRunRequest request,
        CancellationToken cancellationToken)
    {
        var project = request.Assessment.GuidedProject!;
        var session = request.Session;
        var settings = request.Settings;

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

        var allRequiredPassed = project.RequiredChecks.All(check => checkResults.Any(result =>
            result.Required
            && string.Equals(result.CheckId, check.Id, StringComparison.OrdinalIgnoreCase)
            && result.Passed));

        return new GuidedProjectRunResult(updated, allRequiredPassed);
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
            var testCode = check.TestCode ?? string.Empty;
            var expectedContains = check.ExpectedOutputContains ?? Array.Empty<string>();

            var request = BuildRequest(project, files, testCode, settings);
            var result = await _runnerClient.ExecuteAsync(request, settings, cancellationToken);
            var output = (result.Stdout ?? string.Empty).Trim();
            var passed = result.Succeeded
                && expectedContains.All(expected => output.Contains(expected, StringComparison.Ordinal));

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
        string testCode,
        AppSettings settings)
    {
        if (!string.Equals(project.Language, "cpp", StringComparison.OrdinalIgnoreCase))
        {
            throw new InvalidOperationException("Guided project execution currently supports C++ projects.");
        }

        return new CodeRunnerExecuteRequest(
            "cpp",
            "main.cpp",
            BuildCppTestHarness(files, testCode),
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
