using System.Diagnostics;
using System.Text;
using QuizApp.Core.Services;

namespace QuizApp.Infrastructure.CodeRunner;

public sealed class DockerCommandRunner : IDockerCommandRunner
{
    public async Task<DockerCommandResult> RunAsync(
        string image,
        string command,
        IReadOnlyList<string> arguments,
        IReadOnlyDictionary<string, string>? environment = null,
        IReadOnlyDictionary<string, string>? volumeMounts = null,
        string? workingDirectory = null,
        string? standardInput = null,
        bool privileged = false,
        int timeoutSeconds = 30,
        CancellationToken cancellationToken = default)
    {
        var dockerArgs = new List<string> { "run", "--rm" };

        if (privileged)
        {
            dockerArgs.Add("--privileged");
        }

        if (environment is not null)
        {
            foreach (var kvp in environment)
            {
                dockerArgs.Add("-e");
                dockerArgs.Add($"{kvp.Key}={kvp.Value}");
            }
        }

        if (volumeMounts is not null)
        {
            foreach (var kvp in volumeMounts)
            {
                dockerArgs.Add("-v");
                dockerArgs.Add($"{kvp.Key}:{kvp.Value}");
            }
        }

        if (workingDirectory is not null)
        {
            dockerArgs.Add("-w");
            dockerArgs.Add(workingDirectory);
        }

        if (standardInput is not null)
        {
            dockerArgs.Add("-i");
        }

        dockerArgs.Add(image);
        dockerArgs.Add(command);
        dockerArgs.AddRange(arguments);

        var startInfo = new ProcessStartInfo
        {
            FileName = "docker",
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            RedirectStandardInput = standardInput is not null,
            CreateNoWindow = true
        };

        foreach (var arg in dockerArgs)
        {
            startInfo.ArgumentList.Add(arg);
        }

        using var process = new Process { StartInfo = startInfo };
        
        var stdout = new StringBuilder();
        var stderr = new StringBuilder();

        process.OutputDataReceived += (sender, e) => { if (e.Data is not null) stdout.AppendLine(e.Data); };
        process.ErrorDataReceived += (sender, e) => { if (e.Data is not null) stderr.AppendLine(e.Data); };

        try
        {
            if (!process.Start())
            {
                return new DockerCommandResult(false, -1, string.Empty, "Failed to start docker process.");
            }

            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            if (standardInput is not null)
            {
                await process.StandardInput.WriteAsync(standardInput);
                process.StandardInput.Close();
            }

            using var timeoutCts = new CancellationTokenSource(TimeSpan.FromSeconds(timeoutSeconds));
            using var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken, timeoutCts.Token);

            await process.WaitForExitAsync(linkedCts.Token);

            return new DockerCommandResult(
                process.ExitCode == 0,
                process.ExitCode,
                stdout.ToString(),
                stderr.ToString());
        }
        catch (OperationCanceledException)
        {
            if (!process.HasExited)
            {
                process.Kill();
            }
            return new DockerCommandResult(false, -1, stdout.ToString(), stderr.ToString() + "\nProcess timed out.");
        }
        catch (Exception ex)
        {
            return new DockerCommandResult(false, -1, stdout.ToString(), stderr.ToString() + "\n" + ex.Message);
        }
    }
}
