using QuizApp.Infrastructure.Files;
using Xunit;

namespace QuizApp.Tests;

public sealed class RealAnalysisFoundationsContentTests
{
    private static readonly Dictionary<string, int> ExpectedCounts = new()
    {
        ["real-analysis-fundamentals-concept-lesson"] = 7,
        ["real-analysis-fundamentals-glossary"] = 18,
        ["real-analysis-fundamentals-worked-examples"] = 4,
        ["real-analysis-fundamentals-recall-drill"] = 16,
        ["real-analysis-fundamentals-practice-quiz"] = 14,
        ["real-analysis-fundamentals-formal-test"] = 20
    };

    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task Foundations_assessments_deserialize_with_expected_topic_and_counts()
    {
        var dataRoot = FindDataRoot();
        foreach (var (id, expectedCount) in ExpectedCounts)
        {
            var path = Path.Combine(dataRoot, "assessments", $"{id}.yaml");
            var assessment = await FileFormat.ReadAsync<AssessmentFileDto>(path);

            Assert.NotNull(assessment);
            Assert.Equal(id, assessment.Id);
            Assert.Equal("real-analysis", assessment.CategoryId);
            Assert.Equal("real-analysis-fundamentals", assessment.TopicId);

            var actualCount = assessment.AssessmentType switch
            {
                "conceptLesson" => assessment.Lesson?.Sections?.Count,
                "glossary" => assessment.Glossary?.Sections?.Sum(section => section.Entries?.Count ?? 0),
                "workedExample" => assessment.WorkedExamples?.Count,
                "recallDrill" => assessment.Items?.Count,
                "quiz" or "test" => assessment.Questions?.Count,
                _ => null
            };
            Assert.Equal(expectedCount, actualCount);
        }
    }

    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task Foundations_assessments_have_no_catalog_audit_errors()
    {
        var projectRoot = Directory.GetParent(FindDataRoot())!.FullName;
        var audit = new AssessmentContentAudit(projectRoot);

        var errors = (await audit.ValidateAllAssessmentsAsync())
            .Concat(await audit.ValidateTaxonomyAsync())
            .Concat(await audit.ValidateNavigationMetadataAsync())
            .Where(error => error.Contains("real-analysis-fundamentals", StringComparison.OrdinalIgnoreCase))
            .ToList();

        Assert.True(errors.Count == 0, string.Join(Environment.NewLine, errors));
    }

    private static string FindDataRoot()
    {
        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current is not null)
        {
            var candidate = Path.Combine(current.FullName, "data");
            if (Directory.Exists(Path.Combine(candidate, "assessments"))) return candidate;
            current = current.Parent;
        }
        throw new DirectoryNotFoundException("Could not locate data/assessments.");
    }
}
