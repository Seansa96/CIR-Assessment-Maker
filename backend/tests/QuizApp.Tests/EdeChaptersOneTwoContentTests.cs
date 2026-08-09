using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;
using Xunit;

namespace QuizApp.Tests;

public sealed class EdeChaptersOneThroughFourContentTests
{
    private static readonly string[] AssessmentIds =
    [
        "ede-ch01-introduction-concept-lesson",
        "ede-ch01-introduction-glossary",
        "ede-ch01-introduction-worked-examples",
        "ede-ch01-introduction-recall-drill",
        "ede-ch01-introduction-easy-quiz",
        "ede-ch01-introduction-test",
        "ede-ch02-first-order-equations-concept-lesson",
        "ede-ch02-first-order-equations-glossary",
        "ede-ch02-first-order-equations-worked-examples",
        "ede-ch02-first-order-equations-recall-drill",
        "ede-ch02-first-order-equations-easy-quiz",
        "ede-ch02-first-order-equations-test",
        "ede-ch01-ode-readiness-concept-lesson",
        "ede-ch01-ode-readiness-worked-examples",
        "ede-ch01-modeling-depth-concept-lesson",
        "ede-ch01-modeling-depth-worked-examples",
        "ede-ch01-solution-geometry-concept-lesson",
        "ede-ch01-solution-geometry-worked-examples",
        "ede-ch02-linear-separable-depth-concept-lesson",
        "ede-ch02-linear-separable-depth-worked-examples",
        "ede-ch02-existence-uniqueness-depth-concept-lesson",
        "ede-ch02-existence-uniqueness-depth-worked-examples",
        "ede-ch02-nonlinear-transformations-depth-concept-lesson",
        "ede-ch02-nonlinear-transformations-depth-worked-examples",
        "ede-ch02-exactness-integrating-factors-depth-concept-lesson",
        "ede-ch02-exactness-integrating-factors-depth-worked-examples",
        "ede-ch03-numerical-methods-concept-lesson",
        "ede-ch03-numerical-methods-glossary",
        "ede-ch03-numerical-methods-worked-examples",
        "ede-ch03-numerical-methods-recall-drill",
        "ede-ch03-numerical-methods-easy-quiz",
        "ede-ch03-numerical-methods-test",
        "ede-ch03-error-convergence-depth-concept-lesson",
        "ede-ch03-error-convergence-depth-worked-examples",
        "ede-ch03-two-stage-methods-depth-concept-lesson",
        "ede-ch03-two-stage-methods-depth-worked-examples",
        "ede-ch03-rk4-backward-depth-concept-lesson",
        "ede-ch03-rk4-backward-depth-worked-examples",
        "ede-ch03-semilinear-methods-depth-concept-lesson",
        "ede-ch03-semilinear-methods-depth-worked-examples",
        "ede-ch04-first-order-applications-concept-lesson",
        "ede-ch04-first-order-applications-glossary",
        "ede-ch04-first-order-applications-worked-examples",
        "ede-ch04-first-order-applications-recall-drill",
        "ede-ch04-first-order-applications-easy-quiz",
        "ede-ch04-first-order-applications-test",
        "ede-ch04-growth-input-inference-depth-concept-lesson",
        "ede-ch04-growth-input-inference-depth-worked-examples",
        "ede-ch04-cooling-variable-mixing-depth-concept-lesson",
        "ede-ch04-cooling-variable-mixing-depth-worked-examples",
        "ede-ch04-resistance-escape-mechanics-depth-concept-lesson",
        "ede-ch04-resistance-escape-mechanics-depth-worked-examples",
        "ede-ch04-autonomous-second-order-depth-concept-lesson",
        "ede-ch04-autonomous-second-order-depth-worked-examples",
        "ede-ch04-energy-damping-phase-depth-concept-lesson",
        "ede-ch04-energy-damping-phase-depth-worked-examples",
        "ede-ch04-curve-family-geometry-depth-concept-lesson",
        "ede-ch04-curve-family-geometry-depth-worked-examples"
    ];

    private static readonly Dictionary<string, int> ChapterThreeFourCounts = new()
    {
        ["ede-ch01-ode-readiness-concept-lesson"] = 6,
        ["ede-ch01-ode-readiness-worked-examples"] = 3,
        ["ede-ch01-modeling-depth-concept-lesson"] = 6,
        ["ede-ch01-modeling-depth-worked-examples"] = 3,
        ["ede-ch01-solution-geometry-concept-lesson"] = 6,
        ["ede-ch01-solution-geometry-worked-examples"] = 3,
        ["ede-ch02-linear-separable-depth-concept-lesson"] = 6,
        ["ede-ch02-linear-separable-depth-worked-examples"] = 3,
        ["ede-ch02-existence-uniqueness-depth-concept-lesson"] = 6,
        ["ede-ch02-existence-uniqueness-depth-worked-examples"] = 3,
        ["ede-ch02-nonlinear-transformations-depth-concept-lesson"] = 6,
        ["ede-ch02-nonlinear-transformations-depth-worked-examples"] = 3,
        ["ede-ch02-exactness-integrating-factors-depth-concept-lesson"] = 6,
        ["ede-ch02-exactness-integrating-factors-depth-worked-examples"] = 3,
        ["ede-ch03-numerical-methods-concept-lesson"] = 6,
        ["ede-ch03-numerical-methods-glossary"] = 15,
        ["ede-ch03-numerical-methods-worked-examples"] = 3,
        ["ede-ch03-numerical-methods-recall-drill"] = 12,
        ["ede-ch03-numerical-methods-easy-quiz"] = 10,
        ["ede-ch03-numerical-methods-test"] = 12,
        ["ede-ch03-error-convergence-depth-concept-lesson"] = 6,
        ["ede-ch03-error-convergence-depth-worked-examples"] = 3,
        ["ede-ch03-two-stage-methods-depth-concept-lesson"] = 6,
        ["ede-ch03-two-stage-methods-depth-worked-examples"] = 3,
        ["ede-ch03-rk4-backward-depth-concept-lesson"] = 6,
        ["ede-ch03-rk4-backward-depth-worked-examples"] = 3,
        ["ede-ch03-semilinear-methods-depth-concept-lesson"] = 6,
        ["ede-ch03-semilinear-methods-depth-worked-examples"] = 3,
        ["ede-ch04-first-order-applications-concept-lesson"] = 6,
        ["ede-ch04-first-order-applications-glossary"] = 18,
        ["ede-ch04-first-order-applications-worked-examples"] = 3,
        ["ede-ch04-first-order-applications-recall-drill"] = 12,
        ["ede-ch04-first-order-applications-easy-quiz"] = 10,
        ["ede-ch04-first-order-applications-test"] = 12,
        ["ede-ch04-growth-input-inference-depth-concept-lesson"] = 6,
        ["ede-ch04-growth-input-inference-depth-worked-examples"] = 3,
        ["ede-ch04-cooling-variable-mixing-depth-concept-lesson"] = 6,
        ["ede-ch04-cooling-variable-mixing-depth-worked-examples"] = 3,
        ["ede-ch04-resistance-escape-mechanics-depth-concept-lesson"] = 6,
        ["ede-ch04-resistance-escape-mechanics-depth-worked-examples"] = 3,
        ["ede-ch04-autonomous-second-order-depth-concept-lesson"] = 6,
        ["ede-ch04-autonomous-second-order-depth-worked-examples"] = 3,
        ["ede-ch04-energy-damping-phase-depth-concept-lesson"] = 6,
        ["ede-ch04-energy-damping-phase-depth-worked-examples"] = 3,
        ["ede-ch04-curve-family-geometry-depth-concept-lesson"] = 6,
        ["ede-ch04-curve-family-geometry-depth-worked-examples"] = 3
    };

    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task Refreshed_assessments_deserialize_with_stable_ids()
    {
        var dataRoot = FindDataRoot();
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());
        foreach (var id in AssessmentIds)
        {
            var path = Path.Combine(dataRoot, "assessments", $"{id}.yaml");
            var assessment = await FileFormat.ReadAsync<AssessmentFileDto>(path);
            Assert.NotNull(assessment);
            Assert.Equal(id, assessment.Id);
            Assert.Equal("elementary-differential-equations-bvp", assessment.CategoryId);
            Assert.False(string.IsNullOrWhiteSpace(assessment.TopicId));
            var validation = await repository.ValidateFileAsync($"{id}.yaml");
            Assert.True(validation.IsValid, $"{id}: {string.Join("; ", validation.Issues.Select(issue => issue.Message))}");

            if (ChapterThreeFourCounts.TryGetValue(id, out var expectedCount))
            {
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
    }

    private static string FindDataRoot()
    {
        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current is not null)
        {
            var candidate = Path.Combine(current.FullName, "data");
            if (Directory.Exists(Path.Combine(candidate, "assessments")))
            {
                return candidate;
            }
            current = current.Parent;
        }
        throw new DirectoryNotFoundException("Could not locate data/assessments.");
    }
}
