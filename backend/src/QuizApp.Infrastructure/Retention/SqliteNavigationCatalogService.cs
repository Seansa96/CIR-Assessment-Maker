using Microsoft.Data.Sqlite;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;
using QuizApp.Core.Services;

namespace QuizApp.Infrastructure.Retention;

public sealed class SqliteNavigationCatalogService : INavigationCatalogService
{
    private readonly SqliteRetentionOptions retentionOptions;
    private readonly SqliteAssessmentCatalogImporter importer;
    private readonly ICategoryRepository categoryRepository;
    private readonly IAreaRepository areaRepository;

    public SqliteNavigationCatalogService(
        SqliteRetentionOptions retentionOptions,
        SqliteAssessmentCatalogImporter importer,
        ICategoryRepository categoryRepository,
        IAreaRepository areaRepository)
    {
        this.retentionOptions = retentionOptions;
        this.importer = importer;
        this.categoryRepository = categoryRepository;
        this.areaRepository = areaRepository;
    }

    private SqliteConnectionFactory Factory => new SqliteConnectionFactory(retentionOptions);
    public bool IsAvailable => importer.CatalogInitialized;

    public async Task<NavigationCatalog> GetCatalogAsync(CancellationToken cancellationToken = default)
    {
        var categories = await categoryRepository.ListAsync(cancellationToken);
        var areas = await areaRepository.ListAsync(cancellationToken);

        // Build subjects
        var subjects = categories
            .Select(c => new NavigationSubject(c.Id, c.Title, c.Description))
            .ToList();

        var topics = categories
            .SelectMany(c => c.Subcategories.Select((s, index) => new NavigationTopic(s.Id, s.Title, c.Id, s.Description, s.PrerequisiteIds, index)))
            .ToList();
        var knownTopics = topics.ToDictionary(topic => topic.Id, StringComparer.OrdinalIgnoreCase);

        var assessmentSummaries = importer.CatalogInitialized
            ? await GetAssessmentSummariesAsync(cancellationToken)
            : new List<NavigationAssessmentSummary>();
        var normalizedAssessments = new List<NavigationAssessmentSummary>();
        var syntheticTopicIds = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        foreach (var assessment in assessmentSummaries)
        {
            var topicId = assessment.TopicId;
            if (!knownTopics.TryGetValue(topicId, out var topic)
                || !string.Equals(topic.SubjectId, assessment.SubjectId, StringComparison.OrdinalIgnoreCase))
            {
                var syntheticId = $"{assessment.SubjectId}--other-unmapped";
                syntheticTopicIds[assessment.SubjectId] = syntheticId;
                topicId = syntheticId;
            }
            normalizedAssessments.Add(assessment with { TopicId = topicId });
        }
        topics.AddRange(syntheticTopicIds.Select(pair =>
            new NavigationTopic(pair.Value, "Other / Unmapped", pair.Key, "Assessments whose topic ID is not yet mapped to this subject.")));

        // Build navigation areas
        var navAreas = areas
            .Select(a => new NavigationArea(
                a.Id,
                a.Title,
                a.CategoryIds.ToList(),
                a.SubcategoryIds.Where(knownTopics.ContainsKey).ToList(),
                a.Description,
                a.Index))
            .ToList();
        navAreas = navAreas.Select(area =>
        {
            var syntheticTopics = normalizedAssessments
                .Where(assessment => string.Equals(assessment.AreaId, area.Id, StringComparison.OrdinalIgnoreCase))
                .Select(assessment => assessment.TopicId)
                .Where(topicId => topicId.EndsWith("--other-unmapped", StringComparison.OrdinalIgnoreCase));
            return area with
            {
                TopicIds = area.TopicIds.Concat(syntheticTopics).Distinct(StringComparer.OrdinalIgnoreCase).ToList()
            };
        }).ToList();

        // Add synthetic Other/Unmapped if any assessments reference it
        if (importer.CatalogInitialized && await HasUnmappedAsync(cancellationToken))
        {
            if (!navAreas.Any(a => a.Id == "other-unmapped"))
            {
                var unmappedAssessments = normalizedAssessments
                    .Where(assessment => string.Equals(assessment.AreaId, "other-unmapped", StringComparison.OrdinalIgnoreCase))
                    .ToList();
                navAreas.Add(new NavigationArea("other-unmapped", "Other / Unmapped",
                    unmappedAssessments.Select(assessment => assessment.SubjectId).Distinct(StringComparer.OrdinalIgnoreCase).ToList(),
                    unmappedAssessments.Select(assessment => assessment.TopicId).Distinct(StringComparer.OrdinalIgnoreCase).ToList(),
                    "Assessments not yet assigned to an area."));
            }
        }

        // Build goals
        var goals = LearningGoals.All
            .Select(g => new NavigationGoal(g.Id, g.Label, g.ActivityTypes))
            .ToList();

        return new NavigationCatalog(subjects, navAreas, topics, goals, normalizedAssessments);
    }

    private async Task<List<NavigationAssessmentSummary>> GetAssessmentSummariesAsync(CancellationToken cancellationToken)
    {
        await using var connection = Factory.CreateConnection();
        await connection.OpenAsync(cancellationToken);

        var rows = new List<(string Id, string Title, string TypeStr, string CatId, string Goal, string Activity, int AuthoredCount, int? AttemptCount)>();

        await using var cmd = connection.CreateCommand();
        cmd.CommandText = """
            SELECT a.id, a.title, a.assessment_type, a.category_id, a.learning_goal, a.activity_type,
                   a.definition_json,
                   EXISTS(SELECT 1 FROM attempts att WHERE att.assessment_id = a.id AND att.status = 3) AS has_completed_attempt
            FROM assessments a
            WHERE a.is_active = 1
            ORDER BY a.title;
            """;

        await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
        var tempRows = new List<(string id, string title, string typeStr, string catId, string goal, string activity, string json, bool hasCompleted)>();
        while (await reader.ReadAsync(cancellationToken))
        {
            tempRows.Add((
                reader.GetString(0),
                reader.GetString(1),
                reader.GetString(2),
                reader.GetString(3),
                reader.GetString(4),
                reader.GetString(5),
                reader.GetString(6),
                reader.GetBoolean(7)));
        }

        var result = new List<NavigationAssessmentSummary>();
        foreach (var row in tempRows)
        {
            var areaIds = await GetListAsync(connection, "assessment_areas", "area_id", row.id, cancellationToken);
            var subcatIds = await GetListAsync(connection, "assessment_subcategories", "subcategory_id", row.id, cancellationToken);
            var tags = await GetListAsync(connection, "assessment_tags", "tag", row.id, cancellationToken);
            var skills = await GetListAsync(connection, "assessment_skills", "skill_id", row.id, cancellationToken);

            // Parse authored/attempt count from definition_json briefly
            var (authored, attemptCount) = ParseCounts(row.json, row.typeStr);

            if (!Enum.TryParse<AssessmentType>(row.typeStr, true, out var assessmentType))
                assessmentType = AssessmentType.Unknown;

            result.Add(new NavigationAssessmentSummary(
                row.id,
                row.title,
                assessmentType,
                row.catId,
                areaIds.Single(),
                subcatIds.Single(),
                row.goal,
                row.activity,
                tags,
                QuestionCount: attemptCount.HasValue ? Math.Min(attemptCount.Value, authored) : authored,
                AuthoredQuestionCount: authored,
                AttemptQuestionCount: attemptCount,
                HasCompletedAttempt: row.hasCompleted,
                Skills: skills));
        }

        return result;
    }

    private static (int Authored, int? AttemptCount) ParseCounts(string json, string typeStr)
    {
        try
        {
            using var doc = System.Text.Json.JsonDocument.Parse(json);
            var root = doc.RootElement;
            int? attempt = root.TryGetProperty("attemptQuestionCount", out var aqc) && aqc.ValueKind != System.Text.Json.JsonValueKind.Null
                ? aqc.GetInt32() : null;
            if (root.TryGetProperty("questionSelection", out var selection)
                && IsOrderedVariantSelection(selection)
                && selection.TryGetProperty("slots", out var slots)
                && slots.ValueKind is System.Text.Json.JsonValueKind.Array)
            {
                attempt = slots.GetArrayLength();
            }

            int authored = typeStr.ToLowerInvariant() switch
            {
                "recalldrill" => root.TryGetProperty("items", out var items) ? items.GetArrayLength() : 0,
                "workedexample" => root.TryGetProperty("workedExamples", out var we)
                    ? we.EnumerateArray().Sum(e => e.TryGetProperty("steps", out var steps) ? steps.GetArrayLength() : 0) : 0,
                "guidedproject" => root.TryGetProperty("guidedProject", out var gp)
                    && gp.TryGetProperty("requiredChecks", out var rc) ? rc.GetArrayLength() : 0,
                "conceptlesson" => root.TryGetProperty("lesson", out var lesson)
                    && lesson.TryGetProperty("sections", out var lessonSections) ? lessonSections.GetArrayLength() : 0,
                "interactiveexploration" => root.TryGetProperty("exploration", out var exploration)
                    && exploration.TryGetProperty("sections", out var explorationSections) ? explorationSections.GetArrayLength() : 0,
                _ => root.TryGetProperty("questions", out var qs) ? qs.GetArrayLength() : 0
            };

            return (authored, attempt);
        }
        catch { return (0, null); }
    }

    private static bool IsOrderedVariantSelection(System.Text.Json.JsonElement selection)
    {
        if (!selection.TryGetProperty("mode", out var mode) || mode.ValueKind is System.Text.Json.JsonValueKind.Null)
        {
            return true;
        }

        var value = mode.GetString()?.Trim().ToLowerInvariant();
        return string.IsNullOrWhiteSpace(value) || value is "orderedvariant" or "orderedvariants";
    }

    private static async Task<List<string>> GetListAsync(SqliteConnection connection, string table, string column, string id, CancellationToken cancellationToken)
    {
        var result = new List<string>();
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = $"SELECT {column} FROM {table} WHERE assessment_id = @id;";
        cmd.Parameters.AddWithValue("@id", id);
        await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
            result.Add(reader.GetString(0));
        return result;
    }

    private async Task<bool> HasUnmappedAsync(CancellationToken cancellationToken)
    {
        await using var connection = Factory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT COUNT(*) FROM assessment_areas WHERE area_id = 'other-unmapped';";
        var result = await cmd.ExecuteScalarAsync(cancellationToken);
        return result is long n && n > 0;
    }
}
