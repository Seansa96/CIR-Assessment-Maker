using System.Text.RegularExpressions;
using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Tests;

public sealed class PhysicsTwoAuthoringContractTests
{
    [Fact]
    [Trait("Category", "ContentValidation")]
    public async Task Physics_two_category_assets_meet_the_strict_authoring_contract_and_inventory()
    {
        var root = FindProjectRoot();
        var options = new FileStorageOptions { DataRoot = Path.Combine(root, "data") };
        var categories = await new FileCategoryRepository(options).ListAsync();
        var category = Assert.Single(categories.Where(item => item.Id == "physics-2"));
        var repository = new FileAssessmentRepository(options, new AssessmentValidator());
        var assessments = (await repository.ListByCategoryAsync("physics-2")).ToList();

        Assert.Equal(135, assessments.Count);

        var audit = new AssessmentAuthoringContractAudit();
        foreach (var summary in assessments)
        {
            var assessment = await repository.GetByIdAsync(summary.Id);
            Assert.NotNull(assessment);

            var blocking = audit.Evaluate(category, assessment!, strict: true)
                .Where(diagnostic => diagnostic.IsBlocking)
                .ToList();
            Assert.True(blocking.Count == 0, $"{summary.Id}: {string.Join("; ", blocking.Select(item => item.Code))}");

            var path = Path.Combine(options.AssessmentsPath, $"{summary.Id}.yaml");
            Assert.True(File.Exists(path), $"Expected stable assessment file '{path}'.");
            var raw = await File.ReadAllTextAsync(path);
            foreach (var requiredField in new[] { "modeDefault", "randomizeQuestions", "skills", "navigation", "learningGoal", "activityType", "authoring" })
            {
                Assert.Matches(new Regex($"(?m)^\\s*{requiredField}:"), raw);
            }
        }

        for (var chapter = 1; chapter <= 16; chapter++)
        {
            var prefix = $"physics2-ch{chapter:00}-";
            var chapterAssets = assessments.Where(item => item.Id.StartsWith(prefix, StringComparison.Ordinal)).ToList();
            var glossary = Assert.Single(chapterAssets.Where(item => item.AssessmentType == AssessmentType.Glossary));
            var recall = Assert.Single(chapterAssets.Where(item => item.AssessmentType == AssessmentType.RecallDrill));
            var quiz = Assert.Single(chapterAssets.Where(item => item.AssessmentType == AssessmentType.Quiz));
            var test = Assert.Single(chapterAssets.Where(item => item.AssessmentType == AssessmentType.Test));

            var glossaryDefinition = await repository.GetByIdAsync(glossary.Id);
            var recallDefinition = await repository.GetByIdAsync(recall.Id);
            var quizDefinition = await repository.GetByIdAsync(quiz.Id);
            var testDefinition = await repository.GetByIdAsync(test.Id);
            Assert.NotNull(glossaryDefinition);
            Assert.NotNull(recallDefinition);
            Assert.NotNull(quizDefinition);
            Assert.NotNull(testDefinition);

            Assert.InRange(glossaryDefinition!.Glossary!.Sections.Sum(section => section.Entries.Count), 14, 20);
            Assert.Equal(12, recallDefinition!.Items.Count);
            Assert.Equal(10, quizDefinition!.Questions.Count);
            Assert.Equal(10, quizDefinition.AttemptQuestionCount);
            Assert.Equal(12, testDefinition!.Questions.Count);
            Assert.Equal(12, testDefinition.AttemptQuestionCount);
            Assert.Equal("glossary", glossaryDefinition!.Navigation.ActivityType);
            Assert.Equal("mixedRecallSet", recallDefinition!.Navigation.ActivityType);
            Assert.Equal("focusedPractice", quizDefinition!.Navigation.ActivityType);
            Assert.Equal("formalTest", testDefinition!.Navigation.ActivityType);
        }
    }

    private static string FindProjectRoot()
    {
        var current = new DirectoryInfo(AppContext.BaseDirectory);
        while (current is not null && !Directory.Exists(Path.Combine(current.FullName, "data", "assessments")))
        {
            current = current.Parent;
        }

        return current?.FullName ?? throw new DirectoryNotFoundException("Could not locate the project data directory.");
    }
}
