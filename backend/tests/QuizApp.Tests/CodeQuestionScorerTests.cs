using QuizApp.Core.Domain;
using QuizApp.Core.Services;

namespace QuizApp.Tests;

public sealed class CodeQuestionScorerTests
{
    [Fact]
    public async Task ScoreAsync_marks_python_submission_correct_when_all_tests_pass()
    {
        var runner = new FakeCodeRunnerClient(_ => CodeRunnerExecutionResult.Success("9\n"));
        var scorer = new CodeQuestionScorer(runner);
        var question = TestData.CodeQuestion("q001", "python");
        var submitted = new SubmittedAnswer("q001", null, Array.Empty<string>(), null, null, null)
        {
            CodeText = "def square(n):\n    return n * n"
        };

        var result = await scorer.ScoreAsync(question, submitted, TestSettings());

        Assert.True(result.IsCorrect);
        Assert.All(result.CodeFeedback!.Tests, test => Assert.True(test.Passed));
    }

    [Fact]
    public async Task ScoreAsync_reports_failed_test_when_actual_output_differs()
    {
        var runner = new FakeCodeRunnerClient(_ => CodeRunnerExecutionResult.Success("8\n"));
        var scorer = new CodeQuestionScorer(runner);
        var question = TestData.CodeQuestion("q001", "cpp");
        var submitted = new SubmittedAnswer("q001", null, Array.Empty<string>(), null, null, null)
        {
            CodeText = "int square(int n) { return n + n; }"
        };

        var result = await scorer.ScoreAsync(question, submitted, TestSettings());

        Assert.False(result.IsCorrect);
        var test = Assert.Single(result.CodeFeedback!.Tests);
        Assert.Equal("9", test.Expected);
        Assert.Equal("8", test.Actual);
    }

    [Fact]
    public async Task ScoreAsync_reports_compile_error_without_passing_tests()
    {
        var runner = new FakeCodeRunnerClient(_ => CodeRunnerExecutionResult.CompileFailure("compile failed"));
        var scorer = new CodeQuestionScorer(runner);
        var question = TestData.CodeQuestion("q001", "cpp");
        var submitted = new SubmittedAnswer("q001", null, Array.Empty<string>(), null, null, null)
        {
            CodeText = "int square(int n) { return n * ; }"
        };

        var result = await scorer.ScoreAsync(question, submitted, TestSettings());

        Assert.False(result.IsCorrect);
        Assert.Equal("compile failed", result.CodeFeedback!.CompileOutput);
        Assert.All(result.CodeFeedback.Tests, test => Assert.False(test.Passed));
    }

    [Fact]
    public async Task ScoreAsync_uses_language_specific_harness()
    {
        CodeRunnerExecuteRequest? captured = null;
        var runner = new FakeCodeRunnerClient(request =>
        {
            captured = request;
            return CodeRunnerExecutionResult.Success("9\n");
        });
        var scorer = new CodeQuestionScorer(runner);
        var question = TestData.CodeQuestion("q001", "cpp");
        var submitted = new SubmittedAnswer("q001", null, Array.Empty<string>(), null, null, null)
        {
            CodeText = "int square(int n) { return n * n; }"
        };

        await scorer.ScoreAsync(question, submitted, TestSettings());

        Assert.NotNull(captured);
        Assert.Equal("cpp", captured.Language);
        Assert.Equal("main.cpp", captured.FileName);
        Assert.Contains("square(3)", captured.Content);
    }

    private static AppSettings TestSettings()
    {
        return new AppSettings(1, AssessmentMode.Practice, QuestionOrderMode.Randomized, 15, 25, null, null, false);
    }

    private sealed class FakeCodeRunnerClient : ICodeRunnerClient
    {
        private readonly Func<CodeRunnerExecuteRequest, CodeRunnerExecutionResult> execute;

        public FakeCodeRunnerClient(Func<CodeRunnerExecuteRequest, CodeRunnerExecutionResult> execute)
        {
            this.execute = execute;
        }

        public Task<CodeRunnerExecutionResult> ExecuteAsync(CodeRunnerExecuteRequest request, AppSettings settings, CancellationToken cancellationToken = default)
        {
            return Task.FromResult(execute(request));
        }
    }
}
