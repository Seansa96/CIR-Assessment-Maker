using System.Diagnostics;
using System.ComponentModel;
using System.Net.Http.Json;
using QuizApp.Core.Services;

namespace QuizApp.Infrastructure.CodeRunner;

/// <summary>Owns the single local Piston sidecar used by ordinary code questions.</summary>
public sealed class ManagedCodeRunnerService : IManagedCodeRunnerService
{
    private const string ContainerName = "cir-code-runner";
    private const string ImageName = "ghcr.io/engineer-man/piston";
    private readonly SemaphoreSlim gate = new(1, 1);
    private readonly HttpClient httpClient = new() { Timeout = TimeSpan.FromSeconds(5) };
    private CodeRunnerStatus status = new("unavailable", Array.Empty<string>(), "Code runner has not been prepared.", DateTimeOffset.UtcNow);
    private bool ownsContainer;

    public Task<CodeRunnerStatus> GetStatusAsync(CancellationToken cancellationToken = default) => Task.FromResult(status);

    public async Task<CodeRunnerStatus> PrepareAsync(IReadOnlyList<string> languages, CancellationToken cancellationToken = default)
    {
        await gate.WaitAsync(cancellationToken);
        try
        {
            var requested = languages.Select(NormalizeLanguage).Distinct(StringComparer.OrdinalIgnoreCase).ToList();
            status = new CodeRunnerStatus("starting", Array.Empty<string>(), "Starting the local code runner.", DateTimeOffset.UtcNow);

            if (!await EnsureContainerAsync(cancellationToken))
            {
                return status;
            }

            var runtimes = await WaitForRuntimesAsync(cancellationToken);
            if (runtimes is null)
            {
                status = new CodeRunnerStatus("unavailable", Array.Empty<string>(), "The local code runner did not become reachable in time.", DateTimeOffset.UtcNow);
                return status;
            }

            var available = GetAvailableLanguages(runtimes);
            var missing = requested.Where(language => !available.Contains(language, StringComparer.OrdinalIgnoreCase)).ToList();
            if (missing.Count > 0)
            {
                status = new CodeRunnerStatus("provisioning", available, $"Installing {string.Join(" and ", missing)} support.", DateTimeOffset.UtcNow);
                if (!await ProvisionAsync(missing, cancellationToken))
                {
                    return status;
                }

                runtimes = await WaitForRuntimesAsync(cancellationToken);
                available = runtimes is null ? Array.Empty<string>() : GetAvailableLanguages(runtimes);
                missing = requested.Where(language => !available.Contains(language, StringComparer.OrdinalIgnoreCase)).ToList();
                if (missing.Count > 0)
                {
                    status = new CodeRunnerStatus("failed", available, $"The local runner is missing required runtime(s): {string.Join(", ", missing)}.", DateTimeOffset.UtcNow);
                    return status;
                }
            }

            status = new CodeRunnerStatus("ready", available, "Code runner ready.", DateTimeOffset.UtcNow);
            return status;
        }
        catch (Exception ex) when (ex is HttpRequestException or InvalidOperationException or Win32Exception or TaskCanceledException)
        {
            status = new CodeRunnerStatus("failed", Array.Empty<string>(), $"Code runner startup failed: {ex.Message}", DateTimeOffset.UtcNow);
            return status;
        }
        finally
        {
            gate.Release();
        }
    }

    private async Task<bool> EnsureContainerAsync(CancellationToken cancellationToken)
    {
        var inspect = await RunDockerAsync(new[] { "container", "inspect", ContainerName }, cancellationToken);
        if (inspect.ExitCode == 0)
        {
            var started = await RunDockerAsync(new[] { "start", ContainerName }, cancellationToken);
            if (started.ExitCode != 0 && !started.Output.Contains("already started", StringComparison.OrdinalIgnoreCase))
            {
                status = new CodeRunnerStatus("failed", Array.Empty<string>(), $"Could not start local code runner: {started.Output}", DateTimeOffset.UtcNow);
                return false;
            }

            ownsContainer = true;
            return true;
        }

        var pull = await RunDockerAsync(new[] { "pull", ImageName }, cancellationToken);
        if (pull.ExitCode != 0)
        {
            status = new CodeRunnerStatus("unavailable", Array.Empty<string>(), $"Docker could not pull the local code-runner image: {pull.Output}", DateTimeOffset.UtcNow);
            return false;
        }

        var create = await RunDockerAsync(new[]
        {
            "run", "-d", "--privileged", "--name", ContainerName,
            "--label", "cir.managed-code-runner=true", "-p", "127.0.0.1:2000:2000", ImageName
        }, cancellationToken);
        if (create.ExitCode != 0)
        {
            status = new CodeRunnerStatus("failed", Array.Empty<string>(), $"Docker could not create the local code runner: {create.Output}", DateTimeOffset.UtcNow);
            return false;
        }

        ownsContainer = true;
        return true;
    }

    private async Task<IReadOnlyList<PistonRuntime>?> WaitForRuntimesAsync(CancellationToken cancellationToken)
    {
        for (var attempt = 0; attempt < 30; attempt++)
        {
            try
            {
                var runtimes = await httpClient.GetFromJsonAsync<List<PistonRuntime>>("http://localhost:2000/api/v2/runtimes", cancellationToken);
                if (runtimes is not null) return runtimes;
            }
            catch (HttpRequestException) { }
            catch (TaskCanceledException) { }

            await Task.Delay(TimeSpan.FromSeconds(1), cancellationToken);
        }

        return null;
    }

    private async Task<bool> ProvisionAsync(IReadOnlyList<string> languages, CancellationToken cancellationToken)
    {
        // The official image includes Piston's package manager beneath /piston. Keep the command
        // explicit so failed provisioning is reported as a runner diagnostic rather than a 500.
        var packageNames = languages.Select(language => language == "cpp" ? "c++" : language);
        var command = string.Join(" && ", packageNames.Select(language => $"node /piston/cli/index.js ppman install {language}"));
        var result = await RunDockerAsync(new[] { "exec", ContainerName, "sh", "-lc", command }, cancellationToken);
        if (result.ExitCode == 0) return true;

        status = new CodeRunnerStatus("failed", Array.Empty<string>(), $"Runtime provisioning failed: {result.Output}", DateTimeOffset.UtcNow);
        return false;
    }

    private static IReadOnlyList<string> GetAvailableLanguages(IEnumerable<PistonRuntime> runtimes)
    {
        return runtimes.SelectMany(runtime => new[] { runtime.Language }.Concat(runtime.Aliases ?? Array.Empty<string>()))
            .Select(NormalizeLanguage)
            .Distinct(StringComparer.OrdinalIgnoreCase)
            .ToList();
    }

    private static string NormalizeLanguage(string language) => language.Equals("c++", StringComparison.OrdinalIgnoreCase) ? "cpp" : language.Trim().ToLowerInvariant();

    private static async Task<DockerResult> RunDockerAsync(IReadOnlyList<string> arguments, CancellationToken cancellationToken)
    {
        var startInfo = new ProcessStartInfo { FileName = "docker", RedirectStandardOutput = true, RedirectStandardError = true, UseShellExecute = false, CreateNoWindow = true };
        foreach (var argument in arguments) startInfo.ArgumentList.Add(argument);
        using var process = new Process { StartInfo = startInfo };
        if (!process.Start()) throw new InvalidOperationException("Docker could not be started.");
        var stdout = await process.StandardOutput.ReadToEndAsync(cancellationToken);
        var stderr = await process.StandardError.ReadToEndAsync(cancellationToken);
        await process.WaitForExitAsync(cancellationToken);
        return new DockerResult(process.ExitCode, string.Concat(stdout, stderr).Trim());
    }

    public async Task StopAsync(CancellationToken cancellationToken)
    {
        if (ownsContainer)
        {
            await RunDockerAsync(new[] { "stop", ContainerName }, cancellationToken);
        }
    }

    private sealed record PistonRuntime(string Language, IReadOnlyList<string>? Aliases);
    private sealed record DockerResult(int ExitCode, string Output);
}
