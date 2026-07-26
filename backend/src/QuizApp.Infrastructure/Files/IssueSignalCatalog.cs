using QuizApp.Core.Domain;

namespace QuizApp.Infrastructure.Files;

/// <summary>Validates assessment signal references against data/issue-signals.yaml.</summary>
public sealed class IssueSignalCatalog
{
    private readonly FileStorageOptions options;

    public IssueSignalCatalog(FileStorageOptions options) => this.options = options;

    public async Task<IReadOnlyList<ValidationIssue>> ValidateAsync(AssessmentDefinition assessment, CancellationToken cancellationToken = default)
    {
        var path = Path.Combine(options.DataRoot, "issue-signals.yaml");
        if (!File.Exists(path)) return Array.Empty<ValidationIssue>();

        var entries = await FileFormat.ReadAsync<List<IssueSignalCatalogEntryFileDto>>(path, cancellationToken)
            ?? new List<IssueSignalCatalogEntryFileDto>();
        var catalog = entries
            .Where(entry => !string.IsNullOrWhiteSpace(entry.Id))
            .ToDictionary(entry => entry.Id!, StringComparer.OrdinalIgnoreCase);
        var issues = new List<ValidationIssue>();

        foreach (var (location, signal) in EnumerateSignals(assessment))
        {
            if (string.IsNullOrWhiteSpace(signal.Id))
            {
                issues.Add(new ValidationIssue("MISSING_ISSUE_SIGNAL_ID", "Issue signals must include an id.", location));
                continue;
            }
            if (!catalog.TryGetValue(signal.Id, out var entry))
            {
                issues.Add(new ValidationIssue("UNKNOWN_ISSUE_SIGNAL", $"Issue signal '{signal.Id}' is not present in data/issue-signals.yaml.", location));
                continue;
            }
            if (!(entry.Domains ?? new List<string>()).Contains(assessment.CategoryId, StringComparer.OrdinalIgnoreCase))
            {
                issues.Add(new ValidationIssue("ISSUE_SIGNAL_DOMAIN_MISMATCH", $"Issue signal '{signal.Id}' does not support category '{assessment.CategoryId}'.", location));
            }
        }

        return issues;
    }

    private static IEnumerable<(string Location, IssueSignal Signal)> EnumerateSignals(AssessmentDefinition assessment)
    {
        foreach (var question in assessment.Questions)
            foreach (var result in EnumerateQuestionSignals(question.Id, question)) yield return result;
        foreach (var example in assessment.WorkedExamples)
            foreach (var step in example.Steps)
                foreach (var result in EnumerateQuestionSignals(step.Id, step.Question)) yield return result;
    }

    private static IEnumerable<(string Location, IssueSignal Signal)> EnumerateQuestionSignals(string questionId, QuestionDefinition question)
    {
        foreach (var signal in question.IssueSignals) yield return (questionId, signal);
        foreach (var choice in question.Choices)
            foreach (var signal in choice.IssueSignals) yield return ($"{questionId}:{choice.Id}", signal);
        foreach (var part in question.Parts)
        {
            foreach (var signal in part.IssueSignals) yield return ($"{questionId}:{part.Id}", signal);
            foreach (var choice in part.Choices)
                foreach (var signal in choice.IssueSignals) yield return ($"{questionId}:{part.Id}:{choice.Id}", signal);
        }
    }
}

public sealed class IssueSignalCatalogEntryFileDto
{
    public string? Id { get; set; }
    public string? Description { get; set; }
    public List<string>? Domains { get; set; }
}
