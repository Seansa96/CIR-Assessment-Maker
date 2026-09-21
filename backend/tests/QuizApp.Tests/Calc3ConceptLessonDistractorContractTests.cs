using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

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
        var lessonIds = Directory.EnumerateFiles(options.AssessmentsPath, "*-concept-lesson-s2c.yaml")
            .Where(path => File.ReadAllText(path).Contains("categoryId: calculus-3", StringComparison.Ordinal))
            .Select(path => Path.GetFileNameWithoutExtension(path)!)
            .Where(id => id != "calc3-readiness-concept-lesson-s2c")
            .ToList();
        var lessons = lessonIds.Select(id => repository.GetByIdAsync(id)).ToList();
        var assessments = await Task.WhenAll(lessons);

        Assert.Equal(27, assessments.Length);
        var audit = new AssessmentAuthoringContractAudit();
        foreach (var assessment in assessments)
        {
            Assert.NotNull(assessment);
            Assert.DoesNotContain(audit.Evaluate(category, assessment!, strict: true), diagnostic => diagnostic.IsBlocking);

            var checks = assessment.Lesson!.Sections.Select(section => section.Check!).ToList();
            Assert.InRange(checks.Count, 7, 8);
            Assert.All(checks, check => Assert.Equal(QuestionType.MultipleChoice, check.Type));
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
    [InlineData("multivariable-chain-rule-worked-example-s2c", 3)]
    [InlineData("directional-derivatives-gradients-worked-example-s2c", 3)]
    [InlineData("level-curves-contour-maps-worked-example-s2c", 3)]
    [Trait("Category", "ContentValidation")]
    public async Task Expanded_calc3_worked_examples_are_multiple_choice_at_every_step(string assessmentId, int expectedExamples)
    {
        var root = FindProjectRoot();
        var options = new FileStorageOptions { DataRoot = Path.Combine(root, "data") };
        var yaml = new DeserializerBuilder().WithNamingConvention(CamelCaseNamingConvention.Instance).IgnoreUnmatchedProperties().Build();
        var assessmentFile = Path.Combine(root, "data", "assessments", assessmentId + ".yaml");
        try { _ = yaml.Deserialize<AssessmentFileDto>(await File.ReadAllTextAsync(assessmentFile)); }
        catch (Exception exception) { Assert.Fail($"Could not deserialize {assessmentFile}: {exception}"); }
        var assessment = await new FileAssessmentRepository(options, new AssessmentValidator()).GetByIdAsync(assessmentId);

        Assert.NotNull(assessment);
        Assert.Equal(expectedExamples, assessment!.WorkedExamples!.Count);
        Assert.All(assessment.WorkedExamples.SelectMany(example => example.Steps), step =>
            Assert.Equal(QuestionType.MultipleChoice, step.Question.Type));
        var category = Assert.Single((await new FileCategoryRepository(options).ListAsync()).Where(item => item.Id == "calculus-3"));
        Assert.DoesNotContain(new AssessmentAuthoringContractAudit().Evaluate(category, assessment, strict: true), diagnostic => diagnostic.IsBlocking);
    }

    [Theory]
    [InlineData("multivariable-chain-rule-concept-lesson-s2c")]
    [InlineData("directional-derivatives-gradients-concept-lesson-s2c")]
    [InlineData("level-curves-contour-maps-concept-lesson-s2c")]
    [Trait("Category", "ContentValidation")]
    public async Task Expanded_calc3_lessons_deserialize_and_pass_the_strict_contract(string assessmentId)
    {
        var root = FindProjectRoot();
        var options = new FileStorageOptions { DataRoot = Path.Combine(root, "data") };
        var yaml = new DeserializerBuilder().WithNamingConvention(CamelCaseNamingConvention.Instance).IgnoreUnmatchedProperties().Build();
        var path = Path.Combine(root, "data", "assessments", assessmentId + ".yaml");
        var dto = yaml.Deserialize<AssessmentFileDto>(await File.ReadAllTextAsync(path));
        var assessment = dto.ToDomain();
        var category = Assert.Single((await new FileCategoryRepository(options).ListAsync()).Where(item => item.Id == "calculus-3"));

        Assert.Equal(8, assessment.Lesson!.Sections.Count);
        Assert.All(assessment.Lesson.Sections, section => Assert.Equal(QuestionType.MultipleChoice, section.Check!.Type));
        Assert.DoesNotContain(new AssessmentAuthoringContractAudit().Evaluate(category, assessment, strict: true), diagnostic => diagnostic.IsBlocking);
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
