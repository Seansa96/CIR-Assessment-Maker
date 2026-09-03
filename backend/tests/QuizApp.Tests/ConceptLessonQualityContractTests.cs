using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Tests;

public sealed class ConceptLessonQualityContractTests
{
    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task Every_concept_lesson_has_specific_nonrepeating_instruction_and_choices()
    {
        var root = FindProjectRoot();
        var options = new FileStorageOptions { DataRoot = Path.Combine(root, "data") };
        var categories = await new FileCategoryRepository(options).ListAsync();
        var repository = new FileAssessmentRepository(options, new AssessmentValidator());
        var audit = new AssessmentAuthoringContractAudit();
        var guardrailCodes = new HashSet<string>(StringComparer.Ordinal)
        {
            "DUPLICATE_CONCEPT_SECTION_CONTENT", "DUPLICATE_CONCEPT_CHECK_PROMPT",
            "DUPLICATE_CONCEPT_CHECK_EXPLANATION", "REPEATED_CONCEPT_LESSON_CHOICE",
            "REPEATED_MULTIPLE_CHOICE_DISTRACTOR", "GENERIC_MULTIPLE_CHOICE_DISTRACTOR",
            "GENERIC_DISTRACTOR_FEEDBACK"
        };

        foreach (var category in categories)
        {
            var lessons = (await repository.ListByCategoryAsync(category.Id))
                .Where(summary => summary.AssessmentType is AssessmentType.ConceptLesson);
            foreach (var summary in lessons)
            {
                var lesson = await repository.GetByIdAsync(summary.Id);
                Assert.NotNull(lesson);
                if (lesson!.Authoring is null) continue; // Legacy content is not promoted to the new authoring contract.
                var blocking = audit.Evaluate(category, lesson!, strict: true)
                    .Where(diagnostic => diagnostic.IsBlocking && guardrailCodes.Contains(diagnostic.Code))
                    .ToList();
                Assert.True(blocking.Count == 0, $"{summary.Id}: {string.Join(", ", blocking.Select(item => item.Code))}");
            }
        }
    }

    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task Chapter_five_lessons_keep_the_required_calculation_models()
    {
        var root = FindProjectRoot();
        var repository = new FileAssessmentRepository(new FileStorageOptions { DataRoot = Path.Combine(root, "data") }, new AssessmentValidator());
        var required = new Dictionary<string, string>
        {
            ["physics2-ch05-coulombs-law-concept-lesson"] = "F = k q_1 q_2/r^2",
            ["physics2-ch05-electric-fields-points-concept-lesson"] = "E = k q/r^2 and F = q_0 E",
            ["physics2-ch05-continuous-charge-concept-lesson"] = "dE = k dq/r^2"
        };

        foreach (var (id, model) in required)
        {
            var lesson = await repository.GetByIdAsync(id);
            Assert.NotNull(lesson);
            Assert.Equal(7, lesson!.Lesson!.Sections.Count);
            Assert.Contains(lesson.Lesson.Sections, section => section.Content.Contains(model, StringComparison.Ordinal));
        }
    }

    private static string FindProjectRoot()
    {
        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current is not null && !Directory.Exists(Path.Combine(current.FullName, "data", "assessments"))) current = current.Parent;
        return current?.FullName ?? throw new DirectoryNotFoundException("Could not locate the project data directory.");
    }
}
