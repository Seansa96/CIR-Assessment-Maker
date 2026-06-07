namespace QuizApp.Core.Domain;

public sealed record ValidationIssue(string Code, string Message, string? QuestionId = null);

public sealed record AssessmentValidationResult(IReadOnlyList<ValidationIssue> Issues)
{
    public bool IsValid => Issues.Count == 0;
}
