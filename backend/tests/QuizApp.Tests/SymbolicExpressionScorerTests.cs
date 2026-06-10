using QuizApp.Core.Domain;
using QuizApp.Core.Services;

namespace QuizApp.Tests;

public sealed class SymbolicExpressionScorerTests
{
    [Fact]
    public async Task ScoreAsync_marks_equivalent_expression_correct()
    {
        var scorer = new SymbolicExpressionScorer(new FakeSymbolicMathEngine(true, "Expressions simplified to the same value."));
        var question = TestData.SymbolicResponseQuestion("q001");
        var submitted = new SubmittedAnswer("q001", null, Array.Empty<string>(), null, null, null)
        {
            SymbolicLatex = "x^2+2x+1"
        };

        var result = await scorer.ScoreAsync(question, submitted, TestSettings());

        Assert.True(result.IsCorrect);
        Assert.Equal("(x+1)^2", result.ExpectedAnswer);
        Assert.Equal("Expressions simplified to the same value.", result.SymbolicFeedback?.Reason);
    }

    [Fact]
    public async Task ScoreAsync_marks_derivative_equivalent_antiderivative_correct()
    {
        var scorer = new SymbolicExpressionScorer(new FakeSymbolicMathEngine(true, "Expressions matched across derivatives."));
        var question = TestData.SymbolicResponseQuestion("q001", "derivative") with
        {
            Answer = TestData.SymbolicResponseQuestion("q001", "derivative").Answer with
            {
                SymbolicExpectedLatex = "\\frac{x^3}{3}+C"
            }
        };
        var submitted = new SubmittedAnswer("q001", null, Array.Empty<string>(), null, null, null)
        {
            SymbolicLatex = "\\frac{x^3}{3}+7"
        };

        var result = await scorer.ScoreAsync(question, submitted, TestSettings());

        Assert.True(result.IsCorrect);
        Assert.Equal("derivative", result.SymbolicFeedback?.EquivalenceMode);
    }

    [Fact]
    public async Task ScoreAsync_returns_parse_feedback_for_malformed_latex()
    {
        var scorer = new SymbolicExpressionScorer(new FakeSymbolicMathEngine(false, "Submitted answer could not be parsed.", parseSucceeded: false));
        var question = TestData.SymbolicResponseQuestion("q001");
        var submitted = new SubmittedAnswer("q001", null, Array.Empty<string>(), null, null, null)
        {
            SymbolicLatex = "\\notacommand{x}"
        };

        var result = await scorer.ScoreAsync(question, submitted, TestSettings());

        Assert.False(result.IsCorrect);
        Assert.False(result.SymbolicFeedback?.ParseSucceeded);
        Assert.Equal("Submitted answer could not be parsed.", result.SymbolicFeedback?.Reason);
    }

    [Fact]
    public async Task ScoreAsync_rejects_empty_submission_before_calling_engine()
    {
        var engine = new FakeSymbolicMathEngine(true, "Should not be called.");
        var scorer = new SymbolicExpressionScorer(engine);
        var question = TestData.SymbolicResponseQuestion("q001");
        var submitted = new SubmittedAnswer("q001", null, Array.Empty<string>(), null, null, null);

        var result = await scorer.ScoreAsync(question, submitted, TestSettings());

        Assert.False(result.IsCorrect);
        Assert.Equal(0, engine.CallCount);
        Assert.Equal("No symbolic answer was submitted.", result.SymbolicFeedback?.Reason);
    }

    [Fact]
    public async Task ScoreAsync_returns_engine_failure_as_incorrect_feedback()
    {
        var scorer = new SymbolicExpressionScorer(new FakeSymbolicMathEngine(false, "Symbolic math comparison timed out.", parseSucceeded: false));
        var question = TestData.SymbolicResponseQuestion("q001");
        var submitted = new SubmittedAnswer("q001", null, Array.Empty<string>(), null, null, null)
        {
            SymbolicLatex = "x^2"
        };

        var result = await scorer.ScoreAsync(question, submitted, TestSettings());

        Assert.False(result.IsCorrect);
        Assert.Equal("Symbolic math comparison timed out.", result.SymbolicFeedback?.Reason);
    }

    private static AppSettings TestSettings()
    {
        return new AppSettings(1, AssessmentMode.Practice, QuestionOrderMode.Randomized, 15, 25, null, null, false);
    }

    private sealed class FakeSymbolicMathEngine : ISymbolicMathEngine
    {
        private readonly bool isEquivalent;
        private readonly string reason;
        private readonly bool parseSucceeded;

        public FakeSymbolicMathEngine(bool isEquivalent, string reason, bool parseSucceeded = true)
        {
            this.isEquivalent = isEquivalent;
            this.reason = reason;
            this.parseSucceeded = parseSucceeded;
        }

        public int CallCount { get; private set; }

        public Task<SymbolicComparisonResult> CompareAsync(
            SymbolicComparisonRequest request,
            CancellationToken cancellationToken = default)
        {
            CallCount++;
            return Task.FromResult(new SymbolicComparisonResult(
                isEquivalent,
                parseSucceeded,
                request.SubmittedLatex,
                request.ExpectedLatex,
                reason));
        }
    }
}
