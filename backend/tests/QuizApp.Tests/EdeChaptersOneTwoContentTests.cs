using QuizApp.Infrastructure.Files;
using Xunit;

namespace QuizApp.Tests;

public sealed class EdeChaptersOneTwoContentTests
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
        "ede-ch02-first-order-equations-test"
    ];

    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task Refreshed_assessments_deserialize_with_stable_ids()
    {
        var dataRoot = FindDataRoot();
        foreach (var id in AssessmentIds)
        {
            var path = Path.Combine(dataRoot, "assessments", $"{id}.yaml");
            var assessment = await FileFormat.ReadAsync<AssessmentFileDto>(path);
            Assert.NotNull(assessment);
            Assert.Equal(id, assessment.Id);
            Assert.Equal("elementary-differential-equations-bvp", assessment.CategoryId);
            Assert.False(string.IsNullOrWhiteSpace(assessment.TopicId));
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
