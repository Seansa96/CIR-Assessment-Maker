using Microsoft.Data.Sqlite;
using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;
using QuizApp.Infrastructure.Retention;

namespace QuizApp.Tests;

public sealed class SqliteAssessmentCatalogTests
{
    [Fact]
    public async Task SqliteAssessmentCatalog_import_is_idempotent_and_preserves_last_valid_row()
    {
        var fixture = CreateFixture();
        var assessmentPath = Path.Combine(fixture.Files.AssessmentsPath, "sample-quiz.yaml");
        await File.WriteAllTextAsync(assessmentPath, QuizYaml("sample-quiz", "First title", "known-topic"));

        await fixture.Initializer.InitializeAsync();
        await fixture.Importer.ImportAsync();
        await fixture.Importer.ImportAsync();
        Assert.Equal(("First title", 1L), await ReadCatalogRowAsync(fixture.Sqlite.DatabasePath, "sample-quiz"));

        await File.WriteAllTextAsync(assessmentPath, QuizYaml("sample-quiz", "Updated title", "known-topic"));
        await fixture.Importer.ImportAsync();
        Assert.Equal(("Updated title", 1L), await ReadCatalogRowAsync(fixture.Sqlite.DatabasePath, "sample-quiz"));

        await File.WriteAllTextAsync(assessmentPath, "schemaVersion: 1\nid: sample-quiz\ntitle: \"unterminated");
        await fixture.Importer.ImportAsync();
        Assert.Equal(("Updated title", 1L), await ReadCatalogRowAsync(fixture.Sqlite.DatabasePath, "sample-quiz"));

        File.Delete(assessmentPath);
        await fixture.Importer.ImportAsync();
        Assert.Equal(("Updated title", 0L), await ReadCatalogRowAsync(fixture.Sqlite.DatabasePath, "sample-quiz"));
    }

    [Fact]
    public async Task NavigationCatalog_infers_overrides_unmapped_topics_and_refreshes_after_save()
    {
        var fixture = CreateFixture();
        await File.WriteAllTextAsync(
            Path.Combine(fixture.Files.AssessmentsPath, "recall.yaml"),
            RecallYaml("recall-set", "known-topic"));
        await File.WriteAllTextAsync(
            Path.Combine(fixture.Files.AssessmentsPath, "override.yaml"),
            QuizYaml("override-quiz", "Override quiz", "missing-topic", """
navigation:
  learningGoal: evaluate
  activityType: masteryCheck
  tags: [checkpoint]
"""));

        await fixture.Initializer.InitializeAsync();
        await fixture.Importer.ImportAsync();

        var catalogService = new SqliteNavigationCatalogService(
            fixture.Sqlite,
            fixture.Importer,
            new FileCategoryRepository(fixture.Files),
            new FileAreaRepository(fixture.Files));
        var catalog = await catalogService.GetCatalogAsync();

        Assert.Contains(catalog.Assessments, assessment =>
            assessment.Id == "recall-set"
            && assessment.LearningGoal == LearningGoals.Recall
            && assessment.ActivityType == "clozeDrill");
        Assert.Contains(catalog.Assessments, assessment =>
            assessment.Id == "override-quiz"
            && assessment.LearningGoal == LearningGoals.Evaluate
            && assessment.ActivityType == "masteryCheck"
            && assessment.TopicIds.Contains("subject-one--other-unmapped"));

        var fileRepository = new FileAssessmentRepository(fixture.Files, new AssessmentValidator());
        var hybrid = new HybridAssessmentRepository(fixture.Importer, fixture.Sqlite, fileRepository);
        var saved = TestData.Assessment(questions: new[] { TestData.MultipleChoiceQuestion("q001") }) with
        {
            Id = "saved-immediately",
            Title = "Saved Immediately",
            CategoryId = "subject-one",
            SubcategoryIds = new[] { "known-topic" }
        };
        await hybrid.SaveAsync(saved);
        Assert.NotNull(await hybrid.GetByIdAsync(saved.Id));
        Assert.Contains(await hybrid.ListByCategoryAsync("subject-one"), assessment => assessment.Id == saved.Id);

        var unavailableImporter = new SqliteAssessmentCatalogImporter(
            fixture.Sqlite,
            fixture.Files,
            new FileAreaRepository(fixture.Files),
            new AssessmentValidator());
        var fallback = new HybridAssessmentRepository(unavailableImporter, fixture.Sqlite, fileRepository);
        Assert.Contains(await fallback.ListByCategoryAsync("subject-one"), assessment => assessment.Id == saved.Id);
    }

    private static CatalogFixture CreateFixture()
    {
        var root = Path.Combine(AppContext.BaseDirectory, "assessment-catalog-tests", Guid.NewGuid().ToString("n"));
        Directory.CreateDirectory(Path.Combine(root, "assessments"));
        Directory.CreateDirectory(Path.Combine(root, "samples"));
        Directory.CreateDirectory(Path.Combine(root, "categories"));
        Directory.CreateDirectory(Path.Combine(root, "retention"));

        File.WriteAllText(Path.Combine(root, "categories", "subject-one.yaml"), """
schemaVersion: 1
id: subject-one
title: Subject One
subcategories:
  - id: known-topic
    title: Known Topic
""");
        File.WriteAllText(Path.Combine(root, "areas.yaml"), """
schemaVersion: 1
areas:
  - id: core-area
    title: Core Area
    description: Core mapped material.
    categoryIds: [subject-one]
    subcategoryIds: [known-topic]
""");

        var files = new FileStorageOptions { DataRoot = root };
        var sqlite = new SqliteRetentionOptions { DatabasePath = Path.Combine(root, "retention", "catalog.db") };
        var initializer = new SqliteRetentionInitializer(sqlite);
        var importer = new SqliteAssessmentCatalogImporter(
            sqlite,
            files,
            new FileAreaRepository(files),
            new AssessmentValidator());
        return new CatalogFixture(files, sqlite, initializer, importer);
    }

    private static async Task<(string Title, long IsActive)> ReadCatalogRowAsync(string databasePath, string id)
    {
        await using var connection = new SqliteConnection($"Data Source={databasePath}");
        await connection.OpenAsync();
        await using var command = connection.CreateCommand();
        command.CommandText = "SELECT title, is_active FROM assessments WHERE id = $id;";
        command.Parameters.AddWithValue("$id", id);
        await using var reader = await command.ExecuteReaderAsync();
        Assert.True(await reader.ReadAsync());
        return (reader.GetString(0), reader.GetInt64(1));
    }

    private static string QuizYaml(string id, string title, string topic, string navigation = "")
    {
        var navigationBlock = string.IsNullOrWhiteSpace(navigation)
            ? string.Empty
            : navigation.TrimEnd() + Environment.NewLine;
        return $$"""
schemaVersion: 1
id: {{id}}
title: {{title}}
assessmentType: quiz
categoryId: subject-one
subcategoryIds: [{{topic}}]
modeDefault: practice
randomizeQuestions: false
{{navigationBlock}}questions:
  - id: q001
    type: multipleChoice
    prompt: Pick one.
    choices:
      - id: a
        text: Correct
      - id: b
        text: Incorrect
    answer:
      choiceId: a
    explanation: Explanation.
""";
    }

    private static string RecallYaml(string id, string topic)
    {
        return $$"""
schemaVersion: 1
id: {{id}}
title: Recall Set
assessmentType: recallDrill
categoryId: subject-one
subcategoryIds: [{{topic}}]
modeDefault: practice
randomizeQuestions: false
items:
  - id: item-1
    type: cloze
    prompt: Complete this.
    answer:
      expected: answer
    tags: [memory]
""";
    }

    private sealed record CatalogFixture(
        FileStorageOptions Files,
        SqliteRetentionOptions Sqlite,
        SqliteRetentionInitializer Initializer,
        SqliteAssessmentCatalogImporter Importer);
}
