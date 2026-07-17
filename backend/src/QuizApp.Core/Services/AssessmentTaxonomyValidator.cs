using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public class AssessmentTaxonomyValidator : IAssessmentTaxonomyValidator
{
    public AssessmentTaxonomyValidationResult Validate(
        AssessmentDefinition assessment,
        IReadOnlyList<Category> categories,
        IReadOnlyList<AreaDefinition> areas)
    {
        var errors = new List<string>();

        // 1. categoryId must identify exactly one category.
        var category = categories.FirstOrDefault(c => c.Id == assessment.CategoryId);
        if (category == null)
        {
            errors.Add($"UNKNOWN_CATEGORY_ID: Category '{assessment.CategoryId}' not found.");
            return new AssessmentTaxonomyValidationResult { IsValid = false, Errors = errors };
        }

        // 2. Every assessment has exactly one authoritative topic.
        if (string.IsNullOrWhiteSpace(assessment.TopicId))
        {
            errors.Add("MISSING_TOPIC_ID: Exactly one singular topicId must be specified.");
        }
        else
        {
            var topicId = assessment.TopicId;
            // 3. The topic must exist under the selected category.
            if (!category.Subcategories.Any(s => string.Equals(s.Id, topicId, StringComparison.OrdinalIgnoreCase)))
            {
                errors.Add($"UNKNOWN_TOPIC_ID: Topic '{topicId}' is not defined in category '{category.Id}'.");
            }
            else
            {
                // 4. The topic must have exactly one canonical same-category area.
                var mappedAreas = areas.Where(a =>
                    a.CategoryIds.Contains(category.Id, StringComparer.OrdinalIgnoreCase) &&
                    a.SubcategoryIds.Contains(topicId, StringComparer.OrdinalIgnoreCase)).ToList();
                if (mappedAreas.Count == 0)
                    errors.Add($"TOPIC_NOT_MAPPED_TO_AREA: Topic '{topicId}' in category '{category.Id}' is not mapped to an area.");
                else if (mappedAreas.Count > 1)
                    errors.Add($"TOPIC_MAPPED_TO_MULTIPLE_AREAS: Topic '{topicId}' in category '{category.Id}' is mapped to multiple areas: {string.Join(", ", mappedAreas.Select(area => area.Id))}.");
            }
        }

        return new AssessmentTaxonomyValidationResult
        {
            IsValid = errors.Count == 0,
            Errors = errors
        };
    }
}
