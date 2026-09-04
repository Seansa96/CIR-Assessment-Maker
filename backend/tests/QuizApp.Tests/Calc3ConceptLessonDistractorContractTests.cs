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

    [Theory]
    [InlineData("vectors-concept-lesson-s2c")]
    [InlineData("vectors-recall-s2c")]
    [InlineData("vectors-worked-example-s2c")]
    [InlineData("vectors-quiz-s2c")]
    [InlineData("vectors-test-s2c")]
    [InlineData("dot-cross-products-concept-lesson-s2c")]
    [InlineData("dot-cross-products-recall-s2c")]
    [InlineData("dot-cross-products-worked-example-s2c")]
    [InlineData("dot-cross-products-quiz-s2c")]
    [InlineData("dot-cross-products-test-s2c")]
    [InlineData("lines-and-planes-concept-lesson-s2c")]
    [InlineData("lines-and-planes-recall-s2c")]
    [InlineData("lines-and-planes-worked-example-s2c")]
    [InlineData("lines-and-planes-quiz-s2c")]
    [InlineData("lines-and-planes-test-s2c")]
    [InlineData("vector-valued-functions-concept-lesson-s2c")]
    [InlineData("vector-valued-functions-recall-s2c")]
    [InlineData("vector-valued-functions-worked-example-s2c")]
    [InlineData("vector-valued-functions-quiz-s2c")]
    [InlineData("vector-valued-functions-test-s2c")]
    [InlineData("motion-in-space-concept-lesson-s2c")]
    [InlineData("motion-in-space-recall-s2c")]
    [InlineData("motion-in-space-worked-example-s2c")]
    [InlineData("motion-in-space-quiz-s2c")]
    [InlineData("motion-in-space-test-s2c")]
    [Trait("Category", "ContentValidation")]
    public async Task Revised_vector_topic_assessments_pass_the_strict_authoring_contract(string assessmentId)
    {
        var root = FindProjectRoot();
        var options = new FileStorageOptions { DataRoot = Path.Combine(root, "data") };
        var category = Assert.Single((await new FileCategoryRepository(options).ListAsync()).Where(item => item.Id == "calculus-3"));
        var assessment = await new FileAssessmentRepository(options, new AssessmentValidator()).GetByIdAsync(assessmentId);

        Assert.NotNull(assessment);
        var diagnostics = new AssessmentAuthoringContractAudit().Evaluate(category, assessment!, strict: true);
        Assert.DoesNotContain(diagnostics, diagnostic => diagnostic.IsBlocking);
    }

    private static string FindProjectRoot()
    {
        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current is not null && !Directory.Exists(Path.Combine(current.FullName, "data", "assessments")))
            current = current.Parent;
        return current?.FullName ?? throw new DirectoryNotFoundException("Could not locate the project data directory.");
    }
}
