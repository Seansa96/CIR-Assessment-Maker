using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Tests;

public sealed class Calc3ConceptLessonDistractorContractTests
{
    private static readonly string[] GenericDistractors =
    [
        "Use a relation from a different representation.",
        "Reverse a sign, direction, or role without justification.",
        "Ignore the stated geometric constraints."
    ];

    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task Calc3_concept_lesson_distractors_are_specific_and_nonrepeating()
    {
        var root = FindProjectRoot();
        var options = new FileStorageOptions { DataRoot = Path.Combine(root, "data") };
        var category = Assert.Single((await new FileCategoryRepository(options).ListAsync()).Where(item => item.Id == "calculus-3"));
        var repository = new FileAssessmentRepository(options, new AssessmentValidator());
        var lessons = (await repository.ListByCategoryAsync("calculus-3"))
            .Where(summary => summary.AssessmentType is AssessmentType.ConceptLesson
                && summary.Id.EndsWith("-concept-lesson-s2c", StringComparison.Ordinal)
                && summary.Id != "calc3-readiness-concept-lesson-s2c")
            .Select(summary => repository.GetByIdAsync(summary.Id))
            .ToList();
        var assessments = await Task.WhenAll(lessons);

        Assert.Equal(26, assessments.Length);
        var audit = new AssessmentAuthoringContractAudit();
        foreach (var assessment in assessments)
        {
            Assert.NotNull(assessment);
            Assert.DoesNotContain(audit.Evaluate(category, assessment!, strict: true), diagnostic => diagnostic.IsBlocking);

            var checks = assessment.Lesson!.Sections.Select(section => section.Check!).ToList();
            Assert.Equal(7, checks.Count);
            Assert.DoesNotContain(checks.SelectMany(check => check.Choices), choice => GenericDistractors.Contains(choice.Text));
            Assert.DoesNotContain(checks, check => check.Explanation!.Contains("Why the other choices fail: Each changes a sign, swaps a role, or applies a different relationship.", StringComparison.Ordinal));

            var repeatedIncorrectChoices = checks
                .SelectMany(check => check.Choices.Where(choice => choice.Id != check.Answer.ChoiceId).Select(choice => choice.Text))
                .GroupBy(text => text, StringComparer.OrdinalIgnoreCase)
                .Where(group => group.Count() > 1)
                .ToList();
            Assert.Empty(repeatedIncorrectChoices);
        }
    }

    private static string FindProjectRoot()
    {
        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current is not null && !Directory.Exists(Path.Combine(current.FullName, "data", "assessments")))
            current = current.Parent;
        return current?.FullName ?? throw new DirectoryNotFoundException("Could not locate the project data directory.");
    }
}
