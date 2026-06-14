using System.Net.Http.Json;
using QuizApp.Core.Domain;
using QuizApp.Core.Services;

namespace QuizApp.Infrastructure.CodeRunner;

public sealed class PistonCodeRunnerClient : ICodeRunnerClient
{
    private readonly HttpClient httpClient;

    public PistonCodeRunnerClient(HttpClient httpClient)
    {
        this.httpClient = httpClient;
    }

    public async Task<CodeRunnerExecutionResult> ExecuteAsync(
        CodeRunnerExecuteRequest request,
        AppSettings settings,
        CancellationToken cancellationToken = default)
    {
        if (!Uri.TryCreate(settings.CodeRunnerBaseUrl.TrimEnd('/') + "/", UriKind.Absolute, out var baseUri))
        {
            throw new InvalidOperationException("Code runner base URL is invalid.");
        }

        var runtime = await ResolveRuntimeAsync(baseUri, request.Language, cancellationToken);
        var files = request.Files.Count > 0
            ? request.Files.Select(file => new { name = file.Name, content = file.Content }).ToArray()
            : new[] { new { name = request.FileName, content = request.Content } };

        var payload = new
        {
            language = runtime.Language,
            version = runtime.Version,
            files,
            stdin = "",
            args = Array.Empty<string>(),
            compile_timeout = request.CompileTimeoutMs,
            run_timeout = request.RunTimeoutMs,
            compile_memory_limit = -1,
            run_memory_limit = -1
        };

        using var response = await httpClient.PostAsJsonAsync(new Uri(baseUri, "execute"), payload, cancellationToken);
        if (!response.IsSuccessStatusCode)
        {
            var error = await response.Content.ReadFromJsonAsync<PistonErrorResponse>(cancellationToken);
            throw new InvalidOperationException(error?.Message ?? "Code runner execution failed.");
        }

        var result = await response.Content.ReadFromJsonAsync<PistonExecuteResponse>(cancellationToken)
            ?? throw new InvalidOperationException("Code runner returned an empty response.");

        var compileOutput = result.Compile?.Output;
        var runOutput = result.Run?.Output;
        var succeeded = (result.Compile is null || result.Compile.Code == 0) && result.Run?.Code == 0;

        return new CodeRunnerExecutionResult(
            succeeded,
            result.Run?.Stdout,
            result.Run?.Stderr,
            runOutput,
            result.Run?.Code,
            compileOutput,
            null);
    }

    private async Task<PistonRuntime> ResolveRuntimeAsync(Uri baseUri, string language, CancellationToken cancellationToken)
    {
        var runtimes = await httpClient.GetFromJsonAsync<List<PistonRuntime>>(new Uri(baseUri, "runtimes"), cancellationToken)
            ?? throw new InvalidOperationException("Code runner returned no runtimes.");

        var normalizedLanguage = NormalizeLanguage(language);
        return runtimes.FirstOrDefault(runtime =>
            string.Equals(runtime.Language, normalizedLanguage, StringComparison.OrdinalIgnoreCase)
            || (runtime.Aliases ?? Array.Empty<string>()).Any(alias => string.Equals(alias, normalizedLanguage, StringComparison.OrdinalIgnoreCase)))
            ?? throw new InvalidOperationException($"Code runner does not provide a runtime for '{language}'.");
    }

    private static string NormalizeLanguage(string language)
    {
        return language.Equals("cpp", StringComparison.OrdinalIgnoreCase) ? "cpp" : language;
    }

    private sealed record PistonRuntime(string Language, string Version, IReadOnlyList<string>? Aliases);

    private sealed record PistonExecuteResponse(
        string Language,
        string Version,
        PistonStageResult? Run,
        PistonStageResult? Compile);

    private sealed record PistonStageResult(
        string? Stdout,
        string? Stderr,
        string? Output,
        int? Code,
        string? Signal);

    private sealed record PistonErrorResponse(string? Message);
}
