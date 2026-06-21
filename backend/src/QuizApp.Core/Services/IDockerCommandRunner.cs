namespace QuizApp.Core.Services;

public interface IDockerCommandRunner
{
    Task<DockerCommandResult> RunAsync(
        string image,
        string command,
        IReadOnlyList<string> arguments,
        IReadOnlyDictionary<string, string>? environment = null,
        IReadOnlyDictionary<string, string>? volumeMounts = null,
        string? workingDirectory = null,
        string? standardInput = null,
        bool privileged = false,
        int timeoutSeconds = 30,
        CancellationToken cancellationToken = default);
}

public sealed record DockerCommandResult(
    bool Succeeded,
    int ExitCode,
    string Stdout,
    string Stderr);
