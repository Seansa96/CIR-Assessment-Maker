using QuizApp.Core.Domain;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Tests;

public sealed class PhysicsTwoWorkedExampleContractTests
{
    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task Electric_charges_and_fields_worked_examples_are_auto_checkable_and_distinct()
    {
        var root = FindProjectRoot();
        var repository = new FileAssessmentRepository(new FileStorageOptions { DataRoot = Path.Combine(root, "data") }, new QuizApp.Core.Services.AssessmentValidator());
        var required = new[]
        {
            "physics2-ch05-coulombs-law-worked-example",
            "physics2-ch05-dipole-worked-example",
            "physics2-ch05-ring-worked-example"
        };
        foreach (var id in required)
        {
            var assessment = await repository.GetByIdAsync(id);
            Assert.NotNull(assessment);
            Assert.Equal(2, assessment!.WorkedExamples.Count);
            Assert.All(assessment.WorkedExamples, example => Assert.InRange(example.Steps.Count, 3, 6));
            Assert.DoesNotContain(assessment.WorkedExamples.SelectMany(example => example.Steps), step => step.Question.Type is QuestionType.FreeResponse);
            Assert.All(assessment.WorkedExamples.SelectMany(example => example.Steps), step => Assert.Contains(step.Question.Type, new[] { QuestionType.MultipleChoice, QuestionType.NumericResponse, QuestionType.SymbolicResponse }));
        }
    }

    private static string FindProjectRoot()
    {
        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current is not null && !Directory.Exists(Path.Combine(current.FullName, "data", "assessments"))) current = current.Parent;
        return current?.FullName ?? throw new DirectoryNotFoundException();
    }
}
