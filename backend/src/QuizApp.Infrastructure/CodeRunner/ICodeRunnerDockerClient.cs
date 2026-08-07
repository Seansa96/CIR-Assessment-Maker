using System.Diagnostics;

namespace QuizApp.Infrastructure.CodeRunner;

public sealed record CodeRunnerDockerResult(int ExitCode, string Output);

public interface ICodeRunnerDockerClient
{
    Task<CodeRunnerDockerResult> RunAsync(IReadOnlyList<string> arguments, CancellationToken cancellationToken = default);
}

public sealed class CodeRunnerDockerClient : ICodeRunnerDockerClient
{
    public async Task<CodeRunnerDockerResult> RunAsync(IReadOnlyList<string> arguments, CancellationToken cancellationToken = default)
    {
        var startInfo = new ProcessStartInfo { FileName = "docker", RedirectStandardOutput = true, RedirectStandardError = true, UseShellExecute = false, CreateNoWindow = true };
        foreach (var argument in arguments) startInfo.ArgumentList.Add(argument);
        using var process = new Process { StartInfo = startInfo };
        if (!process.Start()) throw new InvalidOperationException("Docker could not be started.");
        var stdout = await process.StandardOutput.ReadToEndAsync(cancellationToken);
        var stderr = await process.StandardError.ReadToEndAsync(cancellationToken);
        await process.WaitForExitAsync(cancellationToken);
        return new CodeRunnerDockerResult(process.ExitCode, string.Concat(stdout, stderr).Trim());
    }
}
