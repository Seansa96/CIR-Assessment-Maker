using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public class CatalogTaxonomyValidationResult
{
    public bool IsValid { get; init; }
    public IReadOnlyList<string> Errors { get; init; } = [];
}

public interface ICatalogTaxonomyValidator
{
    CatalogTaxonomyValidationResult Validate(
        IReadOnlyList<Category> categories,
        IReadOnlyList<AreaDefinition> areas);
}

public class CatalogTaxonomyValidator : ICatalogTaxonomyValidator
{
    public CatalogTaxonomyValidationResult Validate(
        IReadOnlyList<Category> categories,
        IReadOnlyList<AreaDefinition> areas)
    {
        var errors = new List<string>();

        // Check unique category IDs
        var categoryIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var category in categories)
        {
            if (!categoryIds.Add(category.Id))
            {
                errors.Add($"CATEGORY_ID_DUPLICATE: Category ID '{category.Id}' is not unique.");
            }

            var subcategoryIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            foreach (var sub in category.Subcategories)
            {
                if (!subcategoryIds.Add(sub.Id))
                {
                    errors.Add($"SUBCATEGORY_ID_DUPLICATE: Topic ID '{sub.Id}' in category '{category.Id}' is not unique within the category.");
                }
            }
        }

        // Check area IDs and mappings
        var areaIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var area in areas)
        {
            if (!areaIds.Add(area.Id))
            {
                errors.Add($"AREA_ID_DUPLICATE: Area ID '{area.Id}' is not unique.");
            }

            // Area category exists
            foreach (var catId in area.CategoryIds)
            {
                if (!categoryIds.Contains(catId))
                {
                    errors.Add($"AREA_CATEGORY_UNKNOWN: Area '{area.Id}' references unknown category '{catId}'.");
                }
            }

            // Area topic exists and belongs to area category
            foreach (var subId in area.SubcategoryIds)
            {
                var foundInAnyCat = false;
                var foundInAreaCat = false;

                foreach (var category in categories)
                {
                    if (category.Subcategories.Any(s => string.Equals(s.Id, subId, StringComparison.OrdinalIgnoreCase)))
                    {
                        foundInAnyCat = true;
                        if (area.CategoryIds.Contains(category.Id, StringComparer.OrdinalIgnoreCase))
                        {
                            foundInAreaCat = true;
                        }
                    }
                }

                if (!foundInAnyCat)
                {
                    errors.Add($"AREA_SUBCATEGORY_UNKNOWN: Area '{area.Id}' references unknown topic '{subId}'.");
                }
                else if (!foundInAreaCat)
                {
                    errors.Add($"AREA_CATEGORY_TOPIC_MISMATCH: Area '{area.Id}' references topic '{subId}' but does not include its category.");
                }
            }
        }

        // Every category topic is mapped to at least one same-category area
        foreach (var category in categories)
        {
            foreach (var sub in category.Subcategories)
            {
                var mappedToArea = areas.Any(a => 
                    a.CategoryIds.Contains(category.Id, StringComparer.OrdinalIgnoreCase) && 
                    a.SubcategoryIds.Contains(sub.Id, StringComparer.OrdinalIgnoreCase));

                if (!mappedToArea)
                {
                    errors.Add($"SUBCATEGORY_NOT_MAPPED_TO_AREA: Topic '{sub.Id}' in category '{category.Id}' is not mapped to any same-category area.");
                }
            }
        }

        return new CatalogTaxonomyValidationResult
        {
            IsValid = errors.Count == 0,
            Errors = errors
        };
    }
}
