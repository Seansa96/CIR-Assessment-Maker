using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public interface ICodeQuestionScorer
{
    Task<AnswerEvaluation> ScoreAsync(
        QuestionDefinition question,
        SubmittedAnswer submittedAnswer,
        AppSettings settings,
        CancellationToken cancellationToken = default);
}

public interface ICodeRunnerClient
{
    Task<CodeRunnerExecutionResult> ExecuteAsync(
        CodeRunnerExecuteRequest request,
        AppSettings settings,
        CancellationToken cancellationToken = default);
}

public sealed record CodeRunnerExecuteRequest(
    string Language,
    string FileName,
    string Content,
    int CompileTimeoutMs,
    int RunTimeoutMs)
{
    public IReadOnlyList<CodeRunnerFile> Files { get; init; } = Array.Empty<CodeRunnerFile>();
}

public sealed record CodeRunnerFile(
    string Name,
    string Content);

public sealed record CodeRunnerExecutionResult(
    bool Succeeded,
    string? Stdout,
    string? Stderr,
    string? Output,
    int? ExitCode,
    string? CompileOutput,
    string? Error)
{
    public static CodeRunnerExecutionResult Success(string stdout)
    {
        return new CodeRunnerExecutionResult(true, stdout, null, stdout, 0, null, null);
    }

    public static CodeRunnerExecutionResult CompileFailure(string compileOutput)
    {
        return new CodeRunnerExecutionResult(false, null, null, null, null, compileOutput, null);
    }
}

public sealed class CodeQuestionScorer : ICodeQuestionScorer
{
    private static readonly HashSet<string> SupportedLanguages = new(StringComparer.OrdinalIgnoreCase)
    {
        "python",
        "cpp"
    };

    private readonly ICodeRunnerClient runnerClient;

    public CodeQuestionScorer(ICodeRunnerClient runnerClient)
    {
        this.runnerClient = runnerClient;
    }

    public async Task<AnswerEvaluation> ScoreAsync(
        QuestionDefinition question,
        SubmittedAnswer submittedAnswer,
        AppSettings settings,
        CancellationToken cancellationToken = default)
    {
        var codeQuestion = question.CodeQuestion
            ?? throw new InvalidOperationException("Code question metadata is missing.");

        if (!SupportedLanguages.Contains(codeQuestion.Language))
        {
            throw new InvalidOperationException($"Language '{codeQuestion.Language}' is not supported for code questions.");
        }

        if (string.IsNullOrWhiteSpace(submittedAnswer.CodeText))
        {
            return BuildEvaluation(question, codeQuestion, Array.Empty<CodeTestResult>(), null, null, "No code was submitted.");
        }

        var testResults = new List<CodeTestResult>();
        string? compileOutput = null;
        string? runOutput = null;
        string? error = null;

        for (var index = 0; index < codeQuestion.Tests.Count; index++)
        {
            var test = codeQuestion.Tests[index];
            var request = BuildRequest(codeQuestion, submittedAnswer.CodeText, test, settings);
            var runnerResult = await runnerClient.ExecuteAsync(request, settings, cancellationToken);

            compileOutput ??= runnerResult.CompileOutput;
            runOutput = Combine(runOutput, runnerResult.Output);
            error ??= runnerResult.Error;

            var actual = runnerResult.Stdout?.Trim();
            var expected = test.Expected.Trim();
            var passed = runnerResult.Succeeded && string.Equals(actual, expected, StringComparison.Ordinal);

            testResults.Add(new CodeTestResult(index + 1, test.Input, expected, actual, passed));
        }

        return BuildEvaluation(question, codeQuestion, testResults, compileOutput, runOutput, error);
    }

    private static AnswerEvaluation BuildEvaluation(
        QuestionDefinition question,
        CodeQuestionDefinition codeQuestion,
        IReadOnlyList<CodeTestResult> testResults,
        string? compileOutput,
        string? runOutput,
        string? error)
    {
        var feedback = new CodeFeedback(testResults, TrimOutput(compileOutput), TrimOutput(runOutput), TrimOutput(error));
        return new AnswerEvaluation(
            question.Id,
            testResults.Count == codeQuestion.Tests.Count && testResults.All(test => test.Passed),
            question.Explanation,
            "All code tests pass")
        {
            CodeFeedback = feedback
        };
    }

    private static CodeRunnerExecuteRequest BuildRequest(
        CodeQuestionDefinition question,
        string codeText,
        CodeQuestionTest test,
        AppSettings settings)
    {
        return question.Language.ToLowerInvariant() switch
        {
            "python" => new CodeRunnerExecuteRequest(
                "python",
                "main.py",
                BuildPythonHarness(codeText, question.FunctionName, test.Input),
                settings.CodeRunnerCompileTimeoutMs,
                settings.CodeRunnerRunTimeoutMs),
            "cpp" => new CodeRunnerExecuteRequest(
                "cpp",
                "main.cpp",
                BuildCppHarness(codeText, question.FunctionName, test.Input),
                settings.CodeRunnerCompileTimeoutMs,
                settings.CodeRunnerRunTimeoutMs),
            _ => throw new InvalidOperationException($"Language '{question.Language}' is not supported for code questions.")
        };
    }

    private static string BuildPythonHarness(string codeText, string functionName, string input)
    {
        return string.Join("\n", new[]
        {
            codeText,
            "",
            "if __name__ == \"__main__\":",
            $"    print({functionName}({input}))"
        });
    }

    private static string BuildCppHarness(string codeText, string functionName, string input)
    {
        return string.Join("\n", new[]
        {
            "#include <bits/stdc++.h>",
            "using namespace std;",
            codeText,
            "int main()",
            "{",
            $"    cout << {functionName}({input});",
            "    return 0;",
            "}"
        });
    }

    private static string? Combine(string? current, string? next)
    {
        if (string.IsNullOrWhiteSpace(next))
        {
            return current;
        }

        return string.IsNullOrWhiteSpace(current) ? next : $"{current}\n{next}";
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
