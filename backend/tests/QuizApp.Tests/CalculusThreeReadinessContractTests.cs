using System.Text.RegularExpressions;
using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Tests;

public sealed class CalculusThreeReadinessContractTests
{
    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task Calculus_three_readiness_assets_meet_the_strict_authoring_contract()
    {
        var root = FindProjectRoot();
        var options = new FileStorageOptions { DataRoot = Path.Combine(root, "data") };
        var category = Assert.Single((await new FileCategoryRepository(options).ListAsync()).Where(item => item.Id == "calculus-3"));
        var repository = new FileAssessmentRepository(options, new AssessmentValidator());
        var ids = new[]
        {
            "calc3-readiness-concept-lesson-s2c",
            "calc3-readiness-mastery-check-s2c",
            "calc3-readiness-recall-s2c",
        };

        var audit = new AssessmentAuthoringContractAudit();
        foreach (var id in ids)
        {
            var assessment = await repository.GetByIdAsync(id);
            Assert.NotNull(assessment);
            var blocking = audit.Evaluate(category, assessment!, strict: true).Where(diagnostic => diagnostic.IsBlocking).ToList();
            Assert.True(blocking.Count == 0, $"{id}: {string.Join("; ", blocking.Select(item => item.Code))}");

            var raw = await File.ReadAllTextAsync(Path.Combine(options.AssessmentsPath, $"{id}.yaml"));
            foreach (var field in new[] { "modeDefault", "randomizeQuestions", "skills", "navigation", "learningGoal", "activityType", "authoring", "visualRequirement" })
                Assert.Matches(new Regex($"(?m)^\\s*{field}:"), raw);
            Assert.Contains("calculus-3", raw, StringComparison.Ordinal);
        }

        var lesson = await repository.GetByIdAsync(ids[0]);
        var mastery = await repository.GetByIdAsync(ids[1]);
        var recall = await repository.GetByIdAsync(ids[2]);
        Assert.Equal(8, lesson!.Lesson!.Sections.Count);
        Assert.All(lesson.Lesson.Sections, section => Assert.NotNull(section.Check));
        Assert.Equal(18, mastery!.Questions.Count);
        Assert.Equal(12, recall!.Items.Count);
    }

    private static string FindProjectRoot()
    {
        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current is not null && !Directory.Exists(Path.Combine(current.FullName, "data", "assessments")))
            current = current.Parent;
        return current?.FullName ?? throw new DirectoryNotFoundException("Could not locate the project data directory.");
    }
}
