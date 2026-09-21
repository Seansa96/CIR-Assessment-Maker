using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Tests;

public sealed class Calc3ContourMapContentTests
{
    [Theory]
    [InlineData("level-curves-contour-maps-focused-practice-s2c", 10, false)]
    [InlineData("level-curves-contour-maps-formal-test-s2c", 20, true)]
    [Trait("Category", "ContentValidation")]
    public async Task Contour_map_banks_use_unique_original_maps_and_pass_strict_authoring(string id, int count, bool isTest)
    {
        var root = FindProjectRoot();
        var options = new FileStorageOptions { DataRoot = Path.Combine(root, "data") };
        var repository = new FileAssessmentRepository(options, new AssessmentValidator());
        var assessment = await repository.GetByIdAsync(id);
        var category = Assert.Single((await new FileCategoryRepository(options).ListAsync()).Where(item => item.Id == "calculus-3"));

        Assert.NotNull(assessment);
        Assert.Equal(count, assessment!.Questions.Count);
        if (isTest)
        {
            Assert.All(assessment.Questions, question => Assert.Equal(QuestionType.FreeResponse, question.Type));
            Assert.All(assessment.Questions, question => Assert.Empty(question.Choices));
        }
        else
        {
            Assert.All(assessment.Questions, question => Assert.Equal(QuestionType.MultipleChoice, question.Type));
            Assert.All(assessment.Questions, question => Assert.Equal(4, question.Choices.Count));
        }
        Assert.All(assessment.Questions, question => Assert.Contains("Solution:", question.Explanation, StringComparison.Ordinal));
        Assert.All(assessment.Questions, question => Assert.Contains("Why it works:", question.Explanation, StringComparison.Ordinal));
        if (!isTest)
            Assert.All(assessment.Questions, question => Assert.Contains("Why the other choices fail:", question.Explanation, StringComparison.Ordinal));

        var figures = assessment.Questions.Select(question => Assert.Single(question.Media).Src).ToList();
        Assert.Equal(count, figures.Distinct(StringComparer.Ordinal).Count());
        foreach (var figure in figures)
        {
            var path = Path.Combine(root, "data", figure.TrimStart('/').Replace('/', Path.DirectorySeparatorChar));
            Assert.True(File.Exists(path), $"Missing contour map: {figure}");
            Assert.Contains("<svg", await File.ReadAllTextAsync(path), StringComparison.Ordinal);
        }

        if (isTest)
        {
            Assert.All(assessment.Questions, question => Assert.True(question.DifficultyDimensions.Distinct().Count() >= 3));
            Assert.All(assessment.Questions, question => Assert.Contains("calc3-gradient-geometry", question.ExtensionObjectiveIds));
        }
        else
        {
            Assert.All(assessment.Questions, question => Assert.True(question.DifficultyDimensions.Distinct().Count() >= 2));
        }

        var blocking = new AssessmentAuthoringContractAudit().Evaluate(category, assessment, strict: true).Where(item => item.IsBlocking).ToList();
        Assert.True(blocking.Count == 0, $"{id}: {string.Join("; ", blocking.Select(item => item.Code))}");
    }

    private static string FindProjectRoot()
    {
        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current is not null && !Directory.Exists(Path.Combine(current.FullName, "data", "assessments")))
            current = current.Parent;
        return current?.FullName ?? throw new DirectoryNotFoundException("Could not locate the project data directory.");
    }
}
