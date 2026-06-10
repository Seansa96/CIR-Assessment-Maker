using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public interface ISymbolicExpressionScorer
{
    Task<AnswerEvaluation> ScoreAsync(
        QuestionDefinition question,
        SubmittedAnswer submittedAnswer,
        AppSettings settings,
        CancellationToken cancellationToken = default);
}

public interface ISymbolicMathEngine
{
    Task<SymbolicComparisonResult> CompareAsync(
        SymbolicComparisonRequest request,
        CancellationToken cancellationToken = default);
}

public sealed record SymbolicComparisonRequest(
    string SubmittedLatex,
    string ExpectedLatex,
    string EquivalenceMode,
    IReadOnlyList<string> Variables,
    decimal Tolerance);

public sealed record SymbolicComparisonResult(
    bool IsEquivalent,
    bool ParseSucceeded,
    string? NormalizedSubmitted,
    string? NormalizedExpected,
    string? Reason);

public sealed class SymbolicExpressionScorer : ISymbolicExpressionScorer
{
    public const int MaxSubmittedLatexLength = 2000;

    private readonly ISymbolicMathEngine mathEngine;

    public SymbolicExpressionScorer(ISymbolicMathEngine mathEngine)
    {
        this.mathEngine = mathEngine;
    }

    public async Task<AnswerEvaluation> ScoreAsync(
        QuestionDefinition question,
        SubmittedAnswer submittedAnswer,
        AppSettings settings,
        CancellationToken cancellationToken = default)
    {
        var expectedLatex = question.Answer.SymbolicExpectedLatex ?? question.Answer.ExpectedLatex ?? string.Empty;
        var configuredMode = question.Answer.SymbolicEquivalenceMode ?? question.Answer.EquivalenceMode;
        var variables = question.Answer.SymbolicVariables.Count > 0 ? question.Answer.SymbolicVariables : question.Answer.Variables;
        var tolerance = question.Answer.SymbolicTolerance ?? question.Answer.Tolerance ?? 0m;
        var mode = string.IsNullOrWhiteSpace(configuredMode)
            ? "expression"
            : configuredMode;
        var submittedLatex = submittedAnswer.SymbolicLatex?.Trim();

        if (string.IsNullOrWhiteSpace(submittedLatex))
        {
            return Incorrect(question, expectedLatex, mode, "No symbolic answer was submitted.");
        }

        if (submittedLatex.Length > MaxSubmittedLatexLength)
        {
            return Incorrect(question, expectedLatex, mode, $"Symbolic answer is too long. Limit is {MaxSubmittedLatexLength} characters.");
        }

        var comparison = await mathEngine.CompareAsync(
            new SymbolicComparisonRequest(
                submittedLatex,
                expectedLatex,
                mode,
                variables,
                tolerance),
            cancellationToken);

        return new AnswerEvaluation(question.Id, comparison.IsEquivalent, question.Explanation, expectedLatex)
        {
            SymbolicFeedback = new SymbolicFeedback(
                comparison.ParseSucceeded,
                comparison.NormalizedSubmitted,
                comparison.NormalizedExpected,
                mode,
                comparison.Reason)
        };
    }

    private static AnswerEvaluation Incorrect(QuestionDefinition question, string expectedLatex, string mode, string reason)
    {
        return new AnswerEvaluation(question.Id, false, question.Explanation, expectedLatex)
        {
            SymbolicFeedback = new SymbolicFeedback(false, null, expectedLatex, mode, reason)
        };
    }
}
