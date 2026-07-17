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

                foreach (var prerequisiteId in sub.PrerequisiteIds)
                {
                    if (string.Equals(prerequisiteId, sub.Id, StringComparison.OrdinalIgnoreCase))
                    {
                        errors.Add($"PREREQUISITE_SELF_REFERENCE: Topic '{sub.Id}' in category '{category.Id}' cannot require itself.");
                    }
                    else if (!category.Subcategories.Any(candidate => string.Equals(candidate.Id, prerequisiteId, StringComparison.OrdinalIgnoreCase)))
                    {
                        errors.Add($"PREREQUISITE_UNKNOWN_OR_CROSS_CATEGORY: Topic '{sub.Id}' in category '{category.Id}' references unknown or cross-category prerequisite '{prerequisiteId}'.");
                    }
                }
            }

            var visitState = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase);
            bool Visit(SubCategory topic)
            {
                if (visitState.TryGetValue(topic.Id, out var state))
                    return state != 1;

                visitState[topic.Id] = 1;
                foreach (var prerequisiteId in topic.PrerequisiteIds)
                {
                    var prerequisite = category.Subcategories.FirstOrDefault(candidate => string.Equals(candidate.Id, prerequisiteId, StringComparison.OrdinalIgnoreCase));
                    if (prerequisite is not null && !Visit(prerequisite))
                        return false;
                }

                visitState[topic.Id] = 2;
                return true;
            }

            foreach (var topic in category.Subcategories)
            {
                if (!Visit(topic))
                {
                    errors.Add($"PREREQUISITE_CYCLE: Category '{category.Id}' contains a prerequisite cycle involving '{topic.Id}'.");
                    break;
                }
            }

            var reachable = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            var remaining = category.Subcategories.ToList();
            bool madeProgress;
            do
            {
                madeProgress = false;
                foreach (var topic in remaining.Where(topic => topic.PrerequisiteIds.All(reachable.Contains)).ToList())
                {
                    reachable.Add(topic.Id);
                    remaining.Remove(topic);
                    madeProgress = true;
                }
            }
            while (madeProgress);
            foreach (var topic in category.Subcategories.Where(topic => !reachable.Contains(topic.Id)))
            {
                errors.Add($"PREREQUISITE_UNREACHABLE: Topic '{topic.Id}' in category '{category.Id}' has no valid route from a curriculum entry point.");
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

        // Every category topic is mapped to exactly one canonical same-category area.
        foreach (var category in categories)
        {
            foreach (var sub in category.Subcategories)
            {
                var mappedAreas = areas.Where(a => 
                    a.CategoryIds.Contains(category.Id, StringComparer.OrdinalIgnoreCase) && 
                    a.SubcategoryIds.Contains(sub.Id, StringComparer.OrdinalIgnoreCase)).ToList();

                if (mappedAreas.Count == 0)
                {
                    errors.Add($"SUBCATEGORY_NOT_MAPPED_TO_AREA: Topic '{sub.Id}' in category '{category.Id}' is not mapped to any same-category area.");
                }
                else if (mappedAreas.Count > 1)
                {
                    errors.Add($"TOPIC_MAPPED_TO_MULTIPLE_AREAS: Topic '{sub.Id}' in category '{category.Id}' is mapped to multiple canonical areas: {string.Join(", ", mappedAreas.Select(area => area.Id))}.");
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
