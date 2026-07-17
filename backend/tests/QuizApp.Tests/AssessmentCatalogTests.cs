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
        var firstImport = await fixture.Importer.ImportAsync();
        Assert.Equal(1, firstImport.Imported);

        var secondImport = await fixture.Importer.ImportAsync();
        Assert.Equal(1, secondImport.SkippedUnchanged);
        Assert.Equal(("First title", 1L), await ReadCatalogRowAsync(fixture.Sqlite.DatabasePath, "sample-quiz"));

        await File.WriteAllTextAsync(assessmentPath, QuizYaml("sample-quiz", "Updated title", "known-topic"));
        File.SetLastWriteTimeUtc(assessmentPath, DateTime.UtcNow.AddMinutes(1));
        var changedImport = await fixture.Importer.ImportAsync();
        Assert.Equal(1, changedImport.Imported);
        Assert.Equal(("Updated title", 1L), await ReadCatalogRowAsync(fixture.Sqlite.DatabasePath, "sample-quiz"));

        await File.WriteAllTextAsync(assessmentPath, "schemaVersion: 1\nid: sample-quiz\ntitle: \"unterminated");
        File.SetLastWriteTimeUtc(assessmentPath, DateTime.UtcNow.AddMinutes(2));
        var invalidImport = await fixture.Importer.ImportAsync();
        Assert.Equal(1, invalidImport.Invalid);
        Assert.Equal(("Updated title", 1L), await ReadCatalogRowAsync(fixture.Sqlite.DatabasePath, "sample-quiz"));
        Assert.Equal("invalid", await ReadImportStatusAsync(fixture.Sqlite.DatabasePath, "sample-quiz"));

        File.Delete(assessmentPath);
        var missingImport = await fixture.Importer.ImportAsync();
        Assert.Equal(1, missingImport.MissingInactive);
        Assert.Equal(("Updated title", 0L), await ReadCatalogRowAsync(fixture.Sqlite.DatabasePath, "sample-quiz"));
    }

    [Fact]
    public async Task SqliteAssessmentCatalog_reindexes_unchanged_files_when_taxonomy_changes()
    {
        var fixture = CreateFixture();
        var assessmentPath = Path.Combine(fixture.Files.AssessmentsPath, "sample-quiz.yaml");
        await File.WriteAllTextAsync(assessmentPath, QuizYaml("sample-quiz", "First title", "known-topic"));

        await fixture.Initializer.InitializeAsync();
        await fixture.Importer.ImportAsync();

        File.WriteAllText(Path.Combine(fixture.Files.DataRoot, "areas.yaml"), """
schemaVersion: 1
areas:
  - id: renamed-core-area
    title: Renamed Core Area
    description: Core mapped material.
    categoryIds: [subject-one]
    subcategoryIds: [known-topic]
  - id: other-area
    title: Other Area
    categoryIds: [subject-one]
    subcategoryIds: [other-topic]
""");

        var summary = await fixture.Importer.ImportAsync();

        Assert.Equal(1, summary.Reindexed);
        Assert.Equal("renamed-core-area", await ReadAreaIdAsync(fixture.Sqlite.DatabasePath, "sample-quiz"));
    }

    [Fact]
    public async Task Catalog_persistence_rejects_second_topic_or_area_for_an_assessment()
    {
        var fixture = CreateFixture();
        await File.WriteAllTextAsync(
            Path.Combine(fixture.Files.AssessmentsPath, "sample-quiz.yaml"),
            QuizYaml("sample-quiz", "First title", "known-topic"));
        await fixture.Initializer.InitializeAsync();
        Assert.Equal(1, (await fixture.Importer.ImportAsync()).Imported);

        await using var connection = new SqliteConnection($"Data Source={fixture.Sqlite.DatabasePath}");
        await connection.OpenAsync();
        Assert.Equal(1L, await CountRelationsAsync(connection, "assessment_subcategories", "sample-quiz"));
        Assert.Equal(1L, await CountRelationsAsync(connection, "assessment_areas", "sample-quiz"));

        await Assert.ThrowsAsync<SqliteException>(() => InsertRelationAsync(
            connection, "assessment_subcategories", "subcategory_id", "sample-quiz", "another-topic"));
        await Assert.ThrowsAsync<SqliteException>(() => InsertRelationAsync(
            connection, "assessment_areas", "area_id", "sample-quiz", "another-area"));
    }

    [Fact]
    public async Task NavigationCatalog_infers_metadata_preserves_single_topic_and_refreshes_after_save()
    {
        var fixture = CreateFixture();
        await File.WriteAllTextAsync(
            Path.Combine(fixture.Files.AssessmentsPath, "recall.yaml"),
            RecallYaml("recall-set", "known-topic"));
        await File.WriteAllTextAsync(
            Path.Combine(fixture.Files.AssessmentsPath, "override.yaml"),
            QuizYaml("override-quiz", "Override quiz", "known-topic", """
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
            && assessment.TopicIds.SequenceEqual(["known-topic"])
            && assessment.AreaIds.SequenceEqual(["core-area"]));
        Assert.DoesNotContain(catalog.Topics, topic => topic.Id.EndsWith("--other-unmapped", StringComparison.OrdinalIgnoreCase));

        var fileRepository = new FileAssessmentRepository(fixture.Files, new AssessmentValidator());
        var hybrid = new HybridAssessmentRepository(fixture.Importer, fixture.Sqlite, fileRepository);
        var saved = TestData.Assessment(questions: new[] { TestData.MultipleChoiceQuestion("q001") }) with
        {
            Id = "saved-immediately",
            Title = "Saved Immediately",
            CategoryId = "subject-one",
            TopicId = "known-topic",
            Skills = ["other-topic"],
            Navigation = new NavigationMetadata("practice", "focusedPractice", ["subject-one", "known-topic", "other-topic", "other-area"])
        };
        await hybrid.SaveAsync(saved);
        Assert.NotNull(await hybrid.GetByIdAsync(saved.Id));
        Assert.Contains(await hybrid.ListByCategoryAsync("subject-one"), assessment => assessment.Id == saved.Id);
        var refreshed = await catalogService.GetCatalogAsync();
        var savedSummary = Assert.Single(refreshed.Assessments, assessment => assessment.Id == saved.Id);
        Assert.Equal(["known-topic"], savedSummary.TopicIds);
        Assert.Equal(["core-area"], savedSummary.AreaIds);

        var unavailableImporter = new SqliteAssessmentCatalogImporter(
            fixture.Sqlite,
            fixture.Files,
            new FileAreaRepository(fixture.Files),
            new FileCategoryRepository(fixture.Files),
            new AssessmentValidator(),
            new AssessmentSourceInspector(),
            new AssessmentTaxonomyValidator(),
            new CatalogTaxonomyValidator());
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
  - id: other-topic
    title: Other Topic
""");
        File.WriteAllText(Path.Combine(root, "areas.yaml"), """
schemaVersion: 1
areas:
  - id: core-area
    title: Core Area
    description: Core mapped material.
    categoryIds: [subject-one]
    subcategoryIds: [known-topic]
  - id: other-area
    title: Other Area
    categoryIds: [subject-one]
    subcategoryIds: [other-topic]
""");

        var files = new FileStorageOptions { DataRoot = root };
        var sqlite = new SqliteRetentionOptions { DatabasePath = Path.Combine(root, "retention", "catalog.db") };
        var initializer = new SqliteRetentionInitializer(sqlite);
        var importer = new SqliteAssessmentCatalogImporter(
            sqlite,
            files,
            new FileAreaRepository(files),
            new FileCategoryRepository(files),
            new AssessmentValidator(),
            new AssessmentSourceInspector(),
            new AssessmentTaxonomyValidator(),
            new CatalogTaxonomyValidator());
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

    private static async Task<string> ReadImportStatusAsync(string databasePath, string id)
    {
        await using var connection = new SqliteConnection($"Data Source={databasePath}");
        await connection.OpenAsync();
        await using var command = connection.CreateCommand();
        command.CommandText = "SELECT import_status FROM assessments WHERE id = $id;";
        command.Parameters.AddWithValue("$id", id);
        var result = await command.ExecuteScalarAsync();
        return Assert.IsType<string>(result);
    }

    private static async Task<string> ReadAreaIdAsync(string databasePath, string id)
    {
        await using var connection = new SqliteConnection($"Data Source={databasePath}");
        await connection.OpenAsync();
        await using var command = connection.CreateCommand();
        command.CommandText = "SELECT area_id FROM assessment_areas WHERE assessment_id = $id;";
        command.Parameters.AddWithValue("$id", id);
        var result = await command.ExecuteScalarAsync();
        return Assert.IsType<string>(result);
    }

    private static async Task<long> CountRelationsAsync(SqliteConnection connection, string table, string assessmentId)
    {
        await using var command = connection.CreateCommand();
        command.CommandText = $"SELECT COUNT(*) FROM {table} WHERE assessment_id = $id;";
        command.Parameters.AddWithValue("$id", assessmentId);
        return (long)(await command.ExecuteScalarAsync() ?? 0L);
    }

    private static async Task InsertRelationAsync(SqliteConnection connection, string table, string column, string assessmentId, string value)
    {
        await using var command = connection.CreateCommand();
        command.CommandText = $"INSERT INTO {table} (assessment_id, {column}) VALUES ($id, $value);";
        command.Parameters.AddWithValue("$id", assessmentId);
        command.Parameters.AddWithValue("$value", value);
        await command.ExecuteNonQueryAsync();
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
topicId: {{topic}}
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
topicId: {{topic}}
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
