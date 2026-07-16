using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;
using Xunit;

namespace QuizApp.Tests;

public class TaxonomyValidationTests
{
    [Fact]
    public void AssessmentSourceInspector_IdentifiesLegacyKeys()
    {
        var yaml = """
            id: test-1
            subcategoryId: topic-1
            learningGoal: practice
            activityType: mixedPractice
            tags: [a, b]
            type: numericResponse
            answer:
              expected: 42
            """;

        var inspector = new AssessmentSourceInspector();
        var result = inspector.Inspect(yaml, ".yaml");

        Assert.False(result.IsValid);
        Assert.Contains(result.Diagnostics, d => d.Code == "LEGACY_SUBCATEGORY_ID");
        Assert.Contains(result.Diagnostics, d => d.Code == "MISPLACED_LEARNING_GOAL");
        Assert.Contains(result.Diagnostics, d => d.Code == "MISPLACED_ACTIVITY_TYPE");
        Assert.Contains(result.Diagnostics, d => d.Code == "MISPLACED_NAVIGATION_TAGS");
        Assert.Contains(result.Diagnostics, d => d.Code == "LEGACY_NUMERIC_EXPECTED");
    }

    [Fact]
    public void AssessmentTaxonomyValidator_ValidatesCorrectly()
    {
        var category = new Category(1, "cat-1", "Cat 1", [new SubCategory("topic-1", "Topic 1", "Desc")], "Desc");
        var area = new AreaDefinition("area-1", "Area 1", ["cat-1"], ["topic-1"]);

        var validator = new AssessmentTaxonomyValidator();
        var assessment = new AssessmentDefinition(1, "a-1", "A 1", AssessmentType.Quiz, "cat-1", ["topic-1"], AssessmentMode.Practice, false, null, null, null, []);

        var result = validator.Validate(assessment, [category], [area]);
        Assert.True(result.IsValid);

        // Unknown category
        var badCatAsmt = assessment with { CategoryId = "cat-2" };
        result = validator.Validate(badCatAsmt, [category], [area]);
        Assert.False(result.IsValid);
        Assert.Contains(result.Errors, e => e.Contains("UNKNOWN_CATEGORY_ID"));

        // Unknown subcategory
        var badSubAsmt = assessment with { SubcategoryIds = ["topic-2"] };
        result = validator.Validate(badSubAsmt, [category], [area]);
        Assert.False(result.IsValid);
        Assert.Contains(result.Errors, e => e.Contains("UNKNOWN_SUBCATEGORY_ID"));

        // Not mapped to area
        result = validator.Validate(assessment, [category], []);
        Assert.False(result.IsValid);
        Assert.Contains(result.Errors, e => e.Contains("SUBCATEGORY_NOT_MAPPED_TO_AREA"));
    }

    [Fact]
    public void CatalogTaxonomyValidator_ValidatesCorrectly()
    {
        var category = new Category(1, "cat-1", "Cat 1", [new SubCategory("topic-1", "Topic 1", "Desc")], "Desc");
        var area = new AreaDefinition("area-1", "Area 1", ["cat-1"], ["topic-1"]);

        var validator = new CatalogTaxonomyValidator();
        var result = validator.Validate([category], [area]);
        Assert.True(result.IsValid);

        // Unknown category in area
        var badArea = new AreaDefinition("area-2", "Area 2", ["cat-2"], ["topic-1"]);
        result = validator.Validate([category], [badArea]);
        Assert.False(result.IsValid);
        Assert.Contains(result.Errors, e => e.Contains("AREA_CATEGORY_UNKNOWN"));
    }

    [Fact]
    public void CatalogTaxonomyValidator_Rejects_invalid_prerequisite_graphs()
    {
        var first = new SubCategory("first", "First") { PrerequisiteIds = ["second"] };
        var second = new SubCategory("second", "Second") { PrerequisiteIds = ["first"] };
        var category = new Category(1, "cat-1", "Cat 1", [first, second]);
        var area = new AreaDefinition("area-1", "Area 1", ["cat-1"], ["first", "second"]);
        var validator = new CatalogTaxonomyValidator();

        var result = validator.Validate([category], [area]);

        Assert.False(result.IsValid);
        Assert.Contains(result.Errors, error => error.Contains("PREREQUISITE_CYCLE"));

        var selfReferencing = new SubCategory("only", "Only") { PrerequisiteIds = ["only", "missing"] };
        result = validator.Validate([new Category(1, "cat-2", "Cat 2", [selfReferencing])],
            [new AreaDefinition("area-2", "Area 2", ["cat-2"], ["only"])]);

        Assert.Contains(result.Errors, error => error.Contains("PREREQUISITE_SELF_REFERENCE"));
        Assert.Contains(result.Errors, error => error.Contains("PREREQUISITE_UNKNOWN_OR_CROSS_CATEGORY"));
    }
}
