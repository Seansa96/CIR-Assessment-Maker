namespace QuizApp.Core.Services;

public sealed record CodeRunnerStatus(
    string State,
    IReadOnlyList<string> Languages,
    string? Message,
    DateTimeOffset UpdatedAt,
    CodeRunnerDiagnostics? Diagnostics = null)
{
    public bool IsReady => string.Equals(State, "ready", StringComparison.OrdinalIgnoreCase);
}

public sealed record CodeRunnerDiagnostics(
    string? ContainerState,
    int? ContainerExitCode,
    DateTimeOffset? ContainerStartedAt,
    DateTimeOffset? ContainerFinishedAt,
    string? ContainerImage,
    string? PortBinding,
    string? LastProbeError,
    string? RecentContainerLogs);

public interface IManagedCodeRunnerService
{
    Task<CodeRunnerStatus> GetStatusAsync(CancellationToken cancellationToken = default);
    Task<CodeRunnerStatus> PrepareAsync(IReadOnlyList<string> languages, CancellationToken cancellationToken = default);
}
