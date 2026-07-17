using System.Text.Json;
using Microsoft.Data.Sqlite;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Infrastructure.Retention;

/// <summary>
/// Reads assessments from SQLite catalog. Falls back to FileAssessmentRepository when unavailable.
/// SaveAsync writes YAML first then upserts catalog. ValidateFileAsync remains file-backed.
/// </summary>
public sealed class HybridAssessmentRepository : IAssessmentRepository
{
    private readonly SqliteAssessmentCatalogImporter importer;
    private readonly SqliteRetentionOptions retentionOptions;
    private readonly FileAssessmentRepository fileRepo;

    private static readonly JsonSerializerOptions JsonOptions = new(JsonSerializerDefaults.Web)
    {
        Converters = { new System.Text.Json.Serialization.JsonStringEnumConverter(JsonNamingPolicy.CamelCase) }
    };

    public HybridAssessmentRepository(
        SqliteAssessmentCatalogImporter importer,
        SqliteRetentionOptions retentionOptions,
        FileAssessmentRepository fileRepo)
    {
        this.importer = importer;
        this.retentionOptions = retentionOptions;
        this.fileRepo = fileRepo;
    }

    private bool UseSqlite => importer.CatalogInitialized;

    private SqliteConnectionFactory Factory => new SqliteConnectionFactory(retentionOptions);

    public async Task<IReadOnlyList<AssessmentSummary>> ListByCategoryAsync(string categoryId, CancellationToken cancellationToken = default)
    {
        if (!UseSqlite)
            return await fileRepo.ListByCategoryAsync(categoryId, cancellationToken);

        try
        {
            await using var connection = Factory.CreateConnection();
            await connection.OpenAsync(cancellationToken);
            var rows = new List<(string Id, string Goal, string Activity, string Json)>();

            await using (var cmd = connection.CreateCommand())
            {
                cmd.CommandText = """
                    SELECT id, learning_goal, activity_type, definition_json
                    FROM assessments
                    WHERE category_id = @cat AND is_active = 1
                    ORDER BY title;
                    """;
                cmd.Parameters.AddWithValue("@cat", categoryId);
                await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
                while (await reader.ReadAsync(cancellationToken))
                    rows.Add((reader.GetString(0), reader.GetString(1), reader.GetString(2), reader.GetString(3)));
            }

            var assessments = new List<AssessmentSummary>();
            foreach (var row in rows)
            {
                var definition = DeserializeDefinition(row.Json);
                if (definition is null) continue;
                assessments.Add(CreateSummary(
                    definition,
                    await GetSubcategoryIdsAsync(connection, row.Id, cancellationToken),
                    await GetAreaIdsAsync(connection, row.Id, cancellationToken),
                    row.Goal,
                    row.Activity,
                    await GetTagsAsync(connection, row.Id, cancellationToken),
                    await GetSkillsAsync(connection, row.Id, cancellationToken)));
            }

            return assessments;
        }
        catch
        {
            return await fileRepo.ListByCategoryAsync(categoryId, cancellationToken);
        }
    }

    public async Task<AssessmentDefinition?> GetByIdAsync(string assessmentId, CancellationToken cancellationToken = default)
    {
        if (!UseSqlite)
            return await fileRepo.GetByIdAsync(assessmentId, cancellationToken);

        try
        {
            await using var connection = Factory.CreateConnection();
            await connection.OpenAsync(cancellationToken);
            await using var cmd = connection.CreateCommand();
            cmd.CommandText = "SELECT definition_json FROM assessments WHERE id = @id AND is_active = 1 LIMIT 1;";
            cmd.Parameters.AddWithValue("@id", assessmentId);
            var result = await cmd.ExecuteScalarAsync(cancellationToken);
            return result is string json ? DeserializeDefinition(json) : null;
        }
        catch
        {
            return await fileRepo.GetByIdAsync(assessmentId, cancellationToken);
        }
    }

    public async Task SaveAsync(AssessmentDefinition assessment, CancellationToken cancellationToken = default)
    {
        // Always write YAML first
        await fileRepo.SaveAsync(assessment, cancellationToken);

        if (UseSqlite)
            await importer.TryImportAssessmentAsync(assessment, cancellationToken);
    }

    public Task<AssessmentValidationResult> ValidateFileAsync(string fileName, CancellationToken cancellationToken = default)
    {
        return fileRepo.ValidateFileAsync(fileName, cancellationToken);
    }

    private static AssessmentDefinition? DeserializeDefinition(string json)
    {
        try { return JsonSerializer.Deserialize<AssessmentDefinition>(json, JsonOptions); }
        catch { return null; }
    }

    private static async Task<List<string>> GetSubcategoryIdsAsync(SqliteConnection connection, string id, CancellationToken cancellationToken)
    {
        var result = new List<string>();
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT subcategory_id FROM assessment_subcategories WHERE assessment_id = @id;";
        cmd.Parameters.AddWithValue("@id", id);
        await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
            result.Add(reader.GetString(0));
        return result;
    }

    private static async Task<List<string>> GetAreaIdsAsync(SqliteConnection connection, string id, CancellationToken cancellationToken)
    {
        var result = new List<string>();
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT area_id FROM assessment_areas WHERE assessment_id = @id;";
        cmd.Parameters.AddWithValue("@id", id);
        await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
            result.Add(reader.GetString(0));
        return result;
    }

    private static async Task<List<string>> GetTagsAsync(SqliteConnection connection, string id, CancellationToken cancellationToken)
    {
        var result = new List<string>();
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT tag FROM assessment_tags WHERE assessment_id = @id;";
        cmd.Parameters.AddWithValue("@id", id);
        await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
            result.Add(reader.GetString(0));
        return result;
    }

    private static async Task<List<string>> GetSkillsAsync(SqliteConnection connection, string id, CancellationToken cancellationToken)
    {
        var result = new List<string>();
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT skill_id FROM assessment_skills WHERE assessment_id = @id;";
        cmd.Parameters.AddWithValue("@id", id);
        await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
            result.Add(reader.GetString(0));
        return result;
    }

    private static AssessmentSummary CreateSummary(
        AssessmentDefinition assessment,
        List<string> subcatIds,
        List<string> areaIds,
        string learningGoal,
        string activityType,
        List<string> tags,
        List<string> skills)
    {
        var authoredCount = CountItems(assessment);
        var effectiveCount = assessment.AssessmentType is AssessmentType.Quiz or AssessmentType.Test
            ? Math.Min(GetEffectiveAttemptCount(assessment) ?? authoredCount, authoredCount)
            : authoredCount;

        return new AssessmentSummary(
            assessment.Id,
            assessment.Title,
            assessment.AssessmentType,
            assessment.CategoryId,
            assessment.TopicId,
            effectiveCount,
            authoredCount,
            GetEffectiveAttemptCount(assessment))
        {
            AreaId = areaIds.SingleOrDefault(),
            LearningGoal = learningGoal,
            ActivityType = activityType,
            Tags = tags,
            Skills = skills
        };
    }

    private static int? GetEffectiveAttemptCount(AssessmentDefinition assessment)
    {
        if (assessment.AssessmentType is AssessmentType.Quiz or AssessmentType.Test
            && assessment.QuestionSelection?.Mode is QuestionSelectionMode.OrderedVariants)
        {
            return assessment.QuestionSelection.Slots.Count;
        }

        return assessment.AttemptQuestionCount;
    }

    private static int CountItems(AssessmentDefinition assessment) => assessment.AssessmentType switch
    {
        AssessmentType.WorkedExample => assessment.WorkedExamples.Sum(e => e.Steps.Count),
        AssessmentType.GuidedProject => assessment.GuidedProject?.RequiredChecks.Count ?? 0,
        AssessmentType.RecallDrill   => assessment.Items.Count,
        AssessmentType.Glossary      => assessment.Glossary?.Sections
            .SelectMany(section => section.Entries)
            .Sum(entry => entry.Drills.Count) ?? 0,
        AssessmentType.ConceptLesson => assessment.Lesson?.Sections.Count ?? 0,
        AssessmentType.InteractiveExploration => assessment.Exploration?.Sections.Count ?? 0,
        _                            => assessment.Questions.Count
    };
}
