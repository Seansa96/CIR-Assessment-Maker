namespace QuizApp.Core.Domain;

public enum DiagnosticSeverity
{
    Warning,
    Error
}

public class AssessmentSourceDiagnostic
{
    public DiagnosticSeverity Severity { get; init; }
    public required string Code { get; init; }
    public required string Message { get; init; }
    public string? Path { get; init; }
    public int? Line { get; init; }
    public int? Column { get; init; }
    public string? ActualKey { get; init; }
    public string? SuggestedKey { get; init; }
}

public class AssessmentSourceInspection
{
    public bool IsValid { get; init; }
    public IReadOnlyList<AssessmentSourceDiagnostic> Diagnostics { get; init; } = [];
}
