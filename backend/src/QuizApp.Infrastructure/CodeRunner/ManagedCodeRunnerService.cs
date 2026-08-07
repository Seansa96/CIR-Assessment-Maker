using System.ComponentModel;
using System.Net.Http.Json;
using System.Text.Json;
using Microsoft.Extensions.Logging;
using QuizApp.Core.Services;

namespace QuizApp.Infrastructure.CodeRunner;

/// <summary>Owns the single local Piston sidecar used by ordinary code questions.</summary>
public sealed class ManagedCodeRunnerService : IManagedCodeRunnerService
{
    private const string ManagedLabel = "cir.managed-code-runner";
    private readonly ICodeRunnerDockerClient docker;
    private readonly ManagedCodeRunnerOptions options;
    private readonly ILogger<ManagedCodeRunnerService> logger;
    private readonly SemaphoreSlim gate = new(1, 1);
    private readonly HttpClient httpClient;
    private CodeRunnerStatus status = new("unavailable", Array.Empty<string>(), "Code runner has not been prepared.", DateTimeOffset.UtcNow);
    private bool ownsContainer;

    public ManagedCodeRunnerService(ICodeRunnerDockerClient docker, ManagedCodeRunnerOptions options, ILogger<ManagedCodeRunnerService> logger)
        : this(docker, options, logger, new HttpClient { Timeout = TimeSpan.FromSeconds(5) })
    {
    }

    public ManagedCodeRunnerService(ICodeRunnerDockerClient docker, ManagedCodeRunnerOptions options, ILogger<ManagedCodeRunnerService> logger, HttpClient httpClient)
    {
        this.docker = docker;
        this.options = options;
        this.logger = logger;
        this.httpClient = httpClient;
    }

    public Task<CodeRunnerStatus> GetStatusAsync(CancellationToken cancellationToken = default) => Task.FromResult(status);

    public async Task<CodeRunnerStatus> PrepareAsync(IReadOnlyList<string> languages, CancellationToken cancellationToken = default)
    {
        await gate.WaitAsync(cancellationToken);
        try
        {
            var requested = languages.Select(NormalizeLanguage).Distinct(StringComparer.OrdinalIgnoreCase).ToList();
            SetStatus("starting", Array.Empty<string>(), "Starting the local code runner.");

            if (!await EnsureContainerAsync(cancellationToken)) return status;

            var runtimes = await WaitForRuntimesAsync(cancellationToken);
            if (runtimes is null)
            {
                SetStatus("unavailable", Array.Empty<string>(), "The local code runner did not become reachable in time.", status.Diagnostics);
                logger.LogError("Local code runner did not become reachable. {Diagnostics}", status.Diagnostics);
                return status;
            }

            var available = GetAvailableLanguages(runtimes);
            var missing = requested.Where(language => !available.Contains(language, StringComparer.OrdinalIgnoreCase)).ToList();
            if (missing.Count > 0)
            {
                SetStatus("provisioning", available, $"Installing {string.Join(" and ", missing)} support.");
                if (!await ProvisionAsync(missing, cancellationToken)) return status;

                runtimes = await WaitForRuntimesAsync(cancellationToken);
                available = runtimes is null ? Array.Empty<string>() : GetAvailableLanguages(runtimes);
                missing = requested.Where(language => !available.Contains(language, StringComparer.OrdinalIgnoreCase)).ToList();
                if (missing.Count > 0)
                {
                    await RefreshDiagnosticsAsync(status.Diagnostics?.LastProbeError, cancellationToken);
                    SetStatus("failed", available, $"The local runner is missing required runtime(s): {string.Join(", ", missing)}.", status.Diagnostics);
                    return status;
                }
            }

            await RefreshDiagnosticsAsync(null, cancellationToken);
            SetStatus("ready", available, "Code runner ready.", status.Diagnostics);
            logger.LogInformation("Local code runner is ready with {LanguageCount} language aliases.", available.Count);
            return status;
        }
        catch (Exception ex) when (ex is HttpRequestException or InvalidOperationException or Win32Exception or TaskCanceledException or JsonException)
        {
            await RefreshDiagnosticsAsync(ex.Message, CancellationToken.None);
            SetStatus("failed", Array.Empty<string>(), $"Code runner startup failed: {ex.Message}", status.Diagnostics);
            logger.LogError(ex, "Local code runner startup failed. {Diagnostics}", status.Diagnostics);
            return status;
        }
        finally { gate.Release(); }
    }

    private async Task<bool> EnsureContainerAsync(CancellationToken cancellationToken)
    {
        var existing = await InspectAsync(cancellationToken);
        if (existing is not null)
        {
            var diagnostics = ToDiagnostics(existing, null, null);
            if (!IsManaged(existing))
            {
                SetStatus("failed", Array.Empty<string>(), $"The container '{options.ContainerName}' is not managed by CIR and will not be replaced.", diagnostics);
                logger.LogError("Refusing to modify non-CIR code runner container {ContainerName}. {Diagnostics}", options.ContainerName, diagnostics);
                return false;
            }

            if (IsCompatibleAndRunning(existing))
            {
                ownsContainer = true;
                SetStatus("starting", Array.Empty<string>(), "Reusing the healthy local code runner.", diagnostics);
                return true;
            }

            logger.LogWarning("Replacing unhealthy or mismatched CIR code runner. {Diagnostics}", diagnostics);
            var remove = await docker.RunAsync(new[] { "rm", "-f", options.ContainerName }, cancellationToken);
            if (remove.ExitCode != 0)
            {
                SetStatus("failed", Array.Empty<string>(), $"Could not replace local code runner: {remove.Output}", diagnostics);
                return false;
            }
        }

        var pull = await docker.RunAsync(new[] { "pull", options.Image }, cancellationToken);
        if (pull.ExitCode != 0)
        {
            SetStatus("unavailable", Array.Empty<string>(), $"Docker could not pull the local code-runner image: {pull.Output}");
            return false;
        }

        var volume = await docker.RunAsync(new[] { "volume", "create", options.VolumeName }, cancellationToken);
        if (volume.ExitCode != 0)
        {
            SetStatus("failed", Array.Empty<string>(), $"Docker could not create the local code-runner volume: {volume.Output}");
            return false;
        }

        var create = await docker.RunAsync(new[]
        {
            "run", "-d", "--privileged", "--name", options.ContainerName,
            "--label", $"{ManagedLabel}=true", "-v", $"{options.VolumeName}:/piston",
            "-p", "127.0.0.1:2000:2000", options.Image
        }, cancellationToken);
        if (create.ExitCode != 0)
        {
            SetStatus("failed", Array.Empty<string>(), $"Docker could not create the local code runner: {create.Output}");
            return false;
        }

        ownsContainer = true;
        return true;
    }

    private async Task<IReadOnlyList<PistonRuntime>?> WaitForRuntimesAsync(CancellationToken cancellationToken)
    {
        var attempts = Math.Max(1, (int)Math.Ceiling(options.ReadinessTimeoutSeconds * 1000d / Math.Max(1, options.ProbeRetryMilliseconds)));
        string? lastProbeError = null;
        for (var attempt = 0; attempt < attempts; attempt++)
        {
            try
            {
                var runtimes = await httpClient.GetFromJsonAsync<List<PistonRuntime>>("http://localhost:2000/api/v2/runtimes", cancellationToken);
                if (runtimes is not null) return runtimes;
                lastProbeError = "The runtimes endpoint returned an empty response.";
            }
            catch (Exception ex) when (ex is HttpRequestException or TaskCanceledException or JsonException)
            {
                lastProbeError = ex.Message;
                logger.LogDebug(ex, "Local code runner readiness probe {Attempt}/{Attempts} failed.", attempt + 1, attempts);
            }

            if (attempt + 1 < attempts) await Task.Delay(TimeSpan.FromMilliseconds(Math.Max(1, options.ProbeRetryMilliseconds)), cancellationToken);
        }

        await RefreshDiagnosticsAsync(lastProbeError, cancellationToken);
        return null;
    }

    private async Task<bool> ProvisionAsync(IReadOnlyList<string> languages, CancellationToken cancellationToken)
    {
        IReadOnlyList<PistonPackage> packages;
        try
        {
            packages = await httpClient.GetFromJsonAsync<List<PistonPackage>>("http://localhost:2000/api/v2/packages", cancellationToken) ?? new List<PistonPackage>();
        }
        catch (Exception ex) when (ex is HttpRequestException or TaskCanceledException or JsonException)
        {
            await RefreshDiagnosticsAsync(ex.Message, CancellationToken.None);
            SetStatus("failed", Array.Empty<string>(), $"Could not read the local runtime package catalog: {ex.Message}", status.Diagnostics);
            logger.LogError(ex, "Could not read local code runner package catalog. {Diagnostics}", status.Diagnostics);
            return false;
        }

        foreach (var requestedLanguage in languages)
        {
            var packageLanguage = requestedLanguage == "cpp" ? "gcc" : requestedLanguage;
            var package = packages.Where(package => string.Equals(package.Language, packageLanguage, StringComparison.OrdinalIgnoreCase))
                .OrderByDescending(package => ParseVersion(package.LanguageVersion))
                .FirstOrDefault();
            if (package is null)
            {
                await RefreshDiagnosticsAsync(null, cancellationToken);
                SetStatus("failed", Array.Empty<string>(), $"The local runner package catalog does not provide '{requestedLanguage}' (expected package '{packageLanguage}').", status.Diagnostics);
                return false;
            }

            try
            {
                // Piston's package manager is exposed by its local API. Calling it directly avoids
                // relying on a CLI path inside the API image (the image intentionally does not ship it).
                using var response = await httpClient.PostAsJsonAsync(
                    "http://localhost:2000/api/v2/packages",
                    new { language = package.Language, version = package.LanguageVersion },
                    cancellationToken);
                if (response.IsSuccessStatusCode) continue;

                var output = await response.Content.ReadAsStringAsync(cancellationToken);
                await RefreshDiagnosticsAsync(null, cancellationToken);
                SetStatus("failed", Array.Empty<string>(), $"Runtime provisioning failed for '{requestedLanguage}': HTTP {(int)response.StatusCode} {output}", status.Diagnostics);
                logger.LogError("Local code runner runtime provisioning failed for {Language}: HTTP {StatusCode} {Output}. {Diagnostics}", requestedLanguage, response.StatusCode, output, status.Diagnostics);
                return false;
            }
            catch (Exception ex) when (ex is HttpRequestException or TaskCanceledException or JsonException)
            {
                await RefreshDiagnosticsAsync(ex.Message, CancellationToken.None);
                SetStatus("failed", Array.Empty<string>(), $"Runtime provisioning failed for '{requestedLanguage}': {ex.Message}", status.Diagnostics);
                logger.LogError(ex, "Local code runner runtime provisioning failed for {Language}. {Diagnostics}", requestedLanguage, status.Diagnostics);
                return false;
            }
        }

        return true;
    }

    private async Task<ContainerInspection?> InspectAsync(CancellationToken cancellationToken)
    {
        var result = await docker.RunAsync(new[] { "container", "inspect", "--format", "{{json .}}", options.ContainerName }, cancellationToken);
        if (result.ExitCode != 0) return null;
        try { return JsonSerializer.Deserialize<ContainerInspection>(result.Output, JsonOptions); }
        catch (JsonException ex)
        {
            SetStatus("failed", Array.Empty<string>(), $"Docker returned invalid container inspection data: {ex.Message}");
            logger.LogError(ex, "Docker returned invalid inspection data for {ContainerName}: {Output}", options.ContainerName, result.Output);
            return null;
        }
    }

    private async Task RefreshDiagnosticsAsync(string? lastProbeError, CancellationToken cancellationToken)
    {
        var inspection = await InspectAsync(cancellationToken);
        string? logs = null;
        if (inspection is not null && !string.Equals(inspection.State?.Status, "running", StringComparison.OrdinalIgnoreCase))
        {
            var result = await docker.RunAsync(new[] { "logs", "--tail", Math.Max(1, options.DockerLogTailLines).ToString(), options.ContainerName }, cancellationToken);
            logs = result.Output;
        }
        var diagnostics = inspection is null ? new CodeRunnerDiagnostics(null, null, null, null, options.Image, null, lastProbeError, logs) : ToDiagnostics(inspection, lastProbeError, logs);
        status = status with { Diagnostics = diagnostics, UpdatedAt = DateTimeOffset.UtcNow };
    }

    private bool IsCompatibleAndRunning(ContainerInspection inspection) =>
        string.Equals(inspection.State?.Status, "running", StringComparison.OrdinalIgnoreCase)
        && string.Equals(inspection.Config?.Image, options.Image, StringComparison.Ordinal)
        && inspection.Mounts?.Any(m => string.Equals(m.Type, "volume", StringComparison.OrdinalIgnoreCase)
            && string.Equals(m.Name, options.VolumeName, StringComparison.Ordinal)
            && string.Equals(m.Destination, "/piston", StringComparison.Ordinal)) == true;

    private static bool IsManaged(ContainerInspection inspection) =>
        string.Equals(inspection.Config?.Labels?.GetValueOrDefault(ManagedLabel), "true", StringComparison.OrdinalIgnoreCase);

    private static CodeRunnerDiagnostics ToDiagnostics(ContainerInspection inspection, string? lastProbeError, string? logs) => new(
        inspection.State?.Status, inspection.State?.ExitCode, inspection.State?.StartedAt, inspection.State?.FinishedAt,
        inspection.Config?.Image, inspection.NetworkSettings?.Ports?.GetValueOrDefault("2000/tcp")?.FirstOrDefault()?.HostPort,
        lastProbeError, logs);

    private void SetStatus(string state, IReadOnlyList<string> languages, string message, CodeRunnerDiagnostics? diagnostics = null) =>
        status = new CodeRunnerStatus(state, languages, message, DateTimeOffset.UtcNow, diagnostics ?? status.Diagnostics);

    private static IReadOnlyList<string> GetAvailableLanguages(IEnumerable<PistonRuntime> runtimes) => runtimes
        .SelectMany(runtime => new[] { runtime.Language }.Concat(runtime.Aliases ?? Array.Empty<string>()))
        .Select(NormalizeLanguage).Distinct(StringComparer.OrdinalIgnoreCase).ToList();

    private static string NormalizeLanguage(string language) => language.Equals("c++", StringComparison.OrdinalIgnoreCase) ? "cpp" : language.Trim().ToLowerInvariant();

    private static Version ParseVersion(string version) => Version.TryParse(version, out var parsed) ? parsed : new Version(0, 0);

    public async Task StopAsync(CancellationToken cancellationToken)
    {
        if (ownsContainer) await docker.RunAsync(new[] { "stop", options.ContainerName }, cancellationToken);
    }

    private sealed record PistonRuntime(string Language, IReadOnlyList<string>? Aliases);
    private sealed record PistonPackage(string Language, string LanguageVersion, bool Installed);
    private sealed record ContainerInspection(ContainerState? State, ContainerConfig? Config, IReadOnlyList<ContainerMount>? Mounts, ContainerNetworkSettings? NetworkSettings);
    private sealed record ContainerState(string? Status, int? ExitCode, DateTimeOffset? StartedAt, DateTimeOffset? FinishedAt);
    private sealed record ContainerConfig(string? Image, Dictionary<string, string>? Labels);
    private sealed record ContainerMount(string? Type, string? Name, string? Destination);
    private sealed record ContainerNetworkSettings(Dictionary<string, List<ContainerPortBinding>?>? Ports);
    private sealed record ContainerPortBinding(string? HostIp, string? HostPort);
    private static readonly JsonSerializerOptions JsonOptions = new() { PropertyNameCaseInsensitive = true };
}
