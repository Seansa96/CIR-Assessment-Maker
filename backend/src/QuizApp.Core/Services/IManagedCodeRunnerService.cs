namespace QuizApp.Core.Services;

public sealed record CodeRunnerStatus(
    string State,
    IReadOnlyList<string> Languages,
    string? Message,
    DateTimeOffset UpdatedAt)
{
    public bool IsReady => string.Equals(State, "ready", StringComparison.OrdinalIgnoreCase);
}

public interface IManagedCodeRunnerService
{
    Task<CodeRunnerStatus> GetStatusAsync(CancellationToken cancellationToken = default);
    Task<CodeRunnerStatus> PrepareAsync(IReadOnlyList<string> languages, CancellationToken cancellationToken = default);
}
