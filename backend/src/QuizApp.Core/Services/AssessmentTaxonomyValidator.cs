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

        // 2. At least one subcategoryIds value is required for active authored assessments.
        if (assessment.SubcategoryIds == null || assessment.SubcategoryIds.Count == 0)
        {
            errors.Add("MISSING_SUBCATEGORY_IDS: At least one topic (subcategoryId) must be specified.");
        }

        if (assessment.SubcategoryIds != null)
        {
            foreach (var topicId in assessment.SubcategoryIds)
            {
                // 3. Every topic must exist under the selected category.
                if (!category.Subcategories.Any(s => s.Id == topicId))
                {
                    errors.Add($"UNKNOWN_SUBCATEGORY_ID: Topic '{topicId}' is not defined in category '{category.Id}'.");
                    continue; // Skip area check if it's not even in the category
                }

                // 4. Every topic must belong to at least one area that also contains the category.
                var mappedToArea = areas.Any(a => 
                    a.CategoryIds.Contains(category.Id) && 
                    a.SubcategoryIds.Contains(topicId));

                if (!mappedToArea)
                {
                    errors.Add($"SUBCATEGORY_NOT_MAPPED_TO_AREA: Topic '{topicId}' in category '{category.Id}' is not mapped to any area.");
                }
            }
        }

        return new AssessmentTaxonomyValidationResult
        {
            IsValid = errors.Count == 0,
            Errors = errors
        };
    }
}
