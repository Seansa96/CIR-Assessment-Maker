using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public class AssessmentTaxonomyValidationResult
{
    public bool IsValid { get; init; }
    public IReadOnlyList<string> Errors { get; init; } = [];
}

public interface IAssessmentTaxonomyValidator
{
    AssessmentTaxonomyValidationResult Validate(
        AssessmentDefinition assessment,
        IReadOnlyList<Category> categories,
        IReadOnlyList<AreaDefinition> areas);
}
