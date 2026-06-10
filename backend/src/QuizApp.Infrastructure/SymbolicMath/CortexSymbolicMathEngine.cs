using System.Diagnostics;
using System.Text.Json;
using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Infrastructure.SymbolicMath;

public sealed class CortexSymbolicMathEngine : ISymbolicMathEngine
{
    private const int TimeoutMs = 3000;
    private readonly FileStorageOptions storageOptions;

    public CortexSymbolicMathEngine(FileStorageOptions storageOptions)
    {
        this.storageOptions = storageOptions;
    }

    public async Task<SymbolicComparisonResult> CompareAsync(
        SymbolicComparisonRequest request,
        CancellationToken cancellationToken = default)
    {
        var scriptPath = GetScriptPath();
        if (!File.Exists(scriptPath))
        {
            return Failed("Symbolic math adapter script was not found.");
        }

        var startInfo = new ProcessStartInfo
        {
            FileName = "node",
            RedirectStandardInput = true,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
            WorkingDirectory = Path.GetDirectoryName(scriptPath) ?? Environment.CurrentDirectory
        };
        startInfo.ArgumentList.Add(scriptPath);

        using var process = new Process { StartInfo = startInfo };
        using var timeout = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
        timeout.CancelAfter(TimeoutMs);

        try
        {
            process.Start();
            await process.StandardInput.WriteAsync(JsonSerializer.Serialize(request).AsMemory(), timeout.Token);
            process.StandardInput.Close();

            var outputTask = process.StandardOutput.ReadToEndAsync(timeout.Token);
            var errorTask = process.StandardError.ReadToEndAsync(timeout.Token);
            await process.WaitForExitAsync(timeout.Token);

            var output = await outputTask;
            var error = await errorTask;
            if (process.ExitCode != 0)
            {
                return Failed(TrimOutput(string.IsNullOrWhiteSpace(error) ? "Symbolic math adapter failed." : error));
            }

            var response = JsonSerializer.Deserialize<SymbolicEngineResponse>(
                output,
                new JsonSerializerOptions { PropertyNameCaseInsensitive = true });

            return response is null
                ? Failed("Symbolic math adapter returned an empty response.")
                : new SymbolicComparisonResult(
                    response.IsEquivalent,
                    response.ParseSucceeded,
                    response.NormalizedSubmitted,
                    response.NormalizedExpected,
                    response.Reason);
        }
        catch (OperationCanceledException)
        {
            TryKill(process);
            return Failed("Symbolic math comparison timed out.");
        }
        catch (Exception ex) when (ex is InvalidOperationException or IOException or JsonException)
        {
            TryKill(process);
            return Failed("Symbolic math comparison failed.");
        }
    }

    private string GetScriptPath()
    {
        var dataRoot = Path.GetFullPath(storageOptions.DataRoot);
        var repoRoot = Directory.GetParent(dataRoot)?.FullName ?? dataRoot;
        return Path.Combine(repoRoot, "frontend", "scripts", "symbolic-engine.mjs");
    }

    private static SymbolicComparisonResult Failed(string reason)
    {
        return new SymbolicComparisonResult(false, false, null, null, reason);
    }

    private static string TrimOutput(string value)
    {
        return value.Length <= 1000 ? value : string.Concat(value.AsSpan(0, 1000), "...");
    }

    private static void TryKill(Process process)
    {
        try
        {
            if (!process.HasExited)
            {
                process.Kill(entireProcessTree: true);
            }
        }
        catch (InvalidOperationException)
        {
        }
    }

    private sealed record SymbolicEngineResponse(
        bool IsEquivalent,
        bool ParseSucceeded,
        string? NormalizedSubmitted,
        string? NormalizedExpected,
        string? Reason);
}
