using System.Text;
using System.Text.Json;
using Microsoft.Data.Sqlite;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;
using QuizApp.Core.Services;

namespace QuizApp.Infrastructure.Retention;

public sealed class SqliteAssessmentSearchService
{
    private readonly SqliteRetentionOptions options;
    private readonly IAssessmentRepository assessmentRepository;
    
    public bool IsAvailable { get; private set; }

    public SqliteAssessmentSearchService(SqliteRetentionOptions options, IAssessmentRepository assessmentRepository)
    {
        this.options = options;
        this.assessmentRepository = assessmentRepository;
        CheckAvailability();
    }

    private void CheckAvailability()
    {
        try
        {
            using var connection = new SqliteConnectionFactory(options).CreateConnection();
            connection.Open();
            using var cmd = connection.CreateCommand();
            cmd.CommandText = "SELECT 1 FROM assessment_search_fts LIMIT 1;";
            cmd.ExecuteScalar();
            IsAvailable = true;
        }
        catch
        {
            IsAvailable = false;
        }
    }

    public async Task<IReadOnlyList<AssessmentSearchSuggestion>> GetSuggestionsAsync(
        string? query,
        string? subjectId,
        string? areaId,
        string? topicId,
        int limit = 12,
        CancellationToken cancellationToken = default)
    {
        if (!IsAvailable) return Array.Empty<AssessmentSearchSuggestion>();
        
        var normalizedQuery = SearchNormalizer.Normalize(query);
        if (string.IsNullOrWhiteSpace(normalizedQuery)) return Array.Empty<AssessmentSearchSuggestion>();

        // Limit the Levenshtein to distance 1 for short queries, 2 for longer ones.
        // But for really short (length <= 2), only do prefix matching.
        var maxDistance = normalizedQuery.Length <= 2 ? 0 : (normalizedQuery.Length <= 5 ? 1 : 2);
        
        await using var connection = new SqliteConnectionFactory(options).CreateConnection();
        await connection.OpenAsync(cancellationToken);

        var sql = new StringBuilder("""
            SELECT term, kind, subject_id, MAX(weight) as max_wt, normalized_term
            FROM assessment_search_terms
            WHERE 1=1
            """);

        if (!string.IsNullOrWhiteSpace(subjectId))
        {
            sql.Append(" AND (subject_id = @subjectId COLLATE NOCASE OR subject_id IS NULL)");
        }
        if (!string.IsNullOrWhiteSpace(areaId))
            sql.Append(" AND EXISTS (SELECT 1 FROM assessment_areas aa WHERE aa.assessment_id = source_id AND aa.area_id = @areaId COLLATE NOCASE)");
        if (!string.IsNullOrWhiteSpace(topicId))
            sql.Append(" AND EXISTS (SELECT 1 FROM assessment_subcategories st WHERE st.assessment_id = source_id AND st.subcategory_id = @topicId COLLATE NOCASE)");
        
        // SQLite doesn't natively do fast bounded Levenshtein without custom extensions, 
        // so we load a candidate set. Prefix matches first.
        sql.Append(" AND (normalized_term LIKE @prefix OR normalized_term LIKE @contains)");
        sql.Append(" GROUP BY term, kind, subject_id, normalized_term LIMIT 500");

        await using var cmd = connection.CreateCommand();
        cmd.CommandText = sql.ToString();
        if (!string.IsNullOrWhiteSpace(subjectId))
        {
            cmd.Parameters.AddWithValue("@subjectId", subjectId);
        }
        if (!string.IsNullOrWhiteSpace(areaId)) cmd.Parameters.AddWithValue("@areaId", areaId);
        if (!string.IsNullOrWhiteSpace(topicId)) cmd.Parameters.AddWithValue("@topicId", topicId);
        cmd.Parameters.AddWithValue("@prefix", normalizedQuery + "%");
        cmd.Parameters.AddWithValue("@contains", "%" + normalizedQuery + "%");

        var candidates = new List<(string Term, string Kind, string? Subject, int Weight, string Norm)>();
        await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
        {
            candidates.Add((
                reader.GetString(0),
                reader.GetString(1),
                reader.IsDBNull(2) ? null : reader.GetString(2),
                reader.GetInt32(3),
                reader.GetString(4)
            ));
        }

        var results = new List<AssessmentSearchSuggestion>();
        foreach (var c in candidates)
        {
            // Prefer exact prefix, then bounded fuzzy
            int dist = 0;
            if (c.Norm.StartsWith(normalizedQuery))
            {
                dist = 0; // exact prefix
            }
            else
            {
                dist = SearchNormalizer.BoundedLevenshteinDistance(normalizedQuery, c.Norm, maxDistance);
                if (dist > maxDistance) continue;
            }

            var score = c.Weight - (dist * 20); // Penalty for distance
            if (c.Norm.Length == normalizedQuery.Length) score += 10; // Bonus for exact length match

            results.Add(new AssessmentSearchSuggestion(
                c.Kind,
                c.Term, // Use term as id/label for simple suggestions
                c.Term,
                c.Subject,
                1, // We could count actual assessments, but for suggestions just returning 1 is fine for now
                score
            ));
        }

        return results
            .GroupBy(r => new { r.Kind, r.Label })
            .Select(g => g.OrderByDescending(r => r.Score).First())
            .OrderByDescending(r => r.Score)
            .ThenBy(r => r.Label.Length)
            .Take(limit)
            .ToList();
    }

    public async Task<IReadOnlyList<AssessmentSearchResult>> SearchAsync(
        AssessmentSearchRequest request,
        CancellationToken cancellationToken = default)
    {
        if (!IsAvailable) return Array.Empty<AssessmentSearchResult>();

        var normalizedQuery = SearchNormalizer.Normalize(request.Query);
        var hasQuery = !string.IsNullOrWhiteSpace(normalizedQuery);

        await using var connection = new SqliteConnectionFactory(options).CreateConnection();
        await connection.OpenAsync(cancellationToken);

        var sql = new StringBuilder();
        if (hasQuery)
        {
            sql.Append("""
                SELECT a.definition_json, a.content_hash, bm25(assessment_search_fts) as score,
                       aa.area_id, st.subcategory_id
                FROM assessment_search_fts
                JOIN assessments a ON a.id = assessment_search_fts.assessment_id
                JOIN assessment_areas aa ON aa.assessment_id = a.id
                JOIN assessment_subcategories st ON st.assessment_id = a.id
                WHERE a.is_active = 1
                """);
            
            // FTS5 MATCH syntax: query* OR *query* fallback
            sql.Append(" AND assessment_search_fts MATCH @match");
        }
        else
        {
            sql.Append("""
                SELECT a.definition_json, a.content_hash, 0 as score,
                       aa.area_id, st.subcategory_id
                FROM assessments a
                JOIN assessment_areas aa ON aa.assessment_id = a.id
                JOIN assessment_subcategories st ON st.assessment_id = a.id
                WHERE a.is_active = 1
                """);
        }

        if (!string.IsNullOrWhiteSpace(request.SubjectId)) sql.Append(" AND a.category_id = @subjectId COLLATE NOCASE");
        if (!string.IsNullOrWhiteSpace(request.LearningGoal)) sql.Append(" AND a.learning_goal = @goal COLLATE NOCASE");
        if (!string.IsNullOrWhiteSpace(request.ActivityType)) sql.Append(" AND a.activity_type = @activity COLLATE NOCASE");
        if (!string.IsNullOrWhiteSpace(request.AssessmentType)) sql.Append(" AND a.assessment_type = @type COLLATE NOCASE");
        if (!string.IsNullOrWhiteSpace(request.AreaId)) sql.Append(" AND aa.area_id = @areaId COLLATE NOCASE");
        if (!string.IsNullOrWhiteSpace(request.TopicId)) sql.Append(" AND st.subcategory_id = @topicId COLLATE NOCASE");

        if (hasQuery) sql.Append(" ORDER BY bm25(assessment_search_fts) LIMIT 200"); // Limit for C# reranking
        else sql.Append(" ORDER BY a.title LIMIT @limit"); // No query, just filter

        await using var cmd = connection.CreateCommand();
        cmd.CommandText = sql.ToString();

        if (hasQuery)
        {
            // Basic prefix match tokenization for FTS
            var tokens = normalizedQuery.Split(' ', StringSplitOptions.RemoveEmptyEntries);
            var matchStr = string.Join(" AND ", tokens.Select(t => $"\"{t}\"*"));
            cmd.Parameters.AddWithValue("@match", matchStr);
        }
        else
        {
            cmd.Parameters.AddWithValue("@limit", Math.Min(request.Limit, 100));
        }

        if (!string.IsNullOrWhiteSpace(request.SubjectId)) cmd.Parameters.AddWithValue("@subjectId", request.SubjectId);
        if (!string.IsNullOrWhiteSpace(request.LearningGoal)) cmd.Parameters.AddWithValue("@goal", request.LearningGoal);
        if (!string.IsNullOrWhiteSpace(request.ActivityType)) cmd.Parameters.AddWithValue("@activity", request.ActivityType);
        if (!string.IsNullOrWhiteSpace(request.AssessmentType)) cmd.Parameters.AddWithValue("@type", request.AssessmentType);
        if (!string.IsNullOrWhiteSpace(request.AreaId)) cmd.Parameters.AddWithValue("@areaId", request.AreaId);
        if (!string.IsNullOrWhiteSpace(request.TopicId)) cmd.Parameters.AddWithValue("@topicId", request.TopicId);

        var candidates = new List<(AssessmentDefinition Def, double InitialScore, string AreaId, string TopicId)>();
        
        await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
        {
            var json = reader.GetString(0);
            var score = reader.GetDouble(2);
            var def = JsonSerializer.Deserialize<AssessmentDefinition>(json, new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase, Converters = { new System.Text.Json.Serialization.JsonStringEnumConverter(JsonNamingPolicy.CamelCase) } });
            if (def != null)
            {
                candidates.Add((def, score, reader.GetString(3), reader.GetString(4)));
            }
        }

        // Apply remaining filters in memory
        var filtered = candidates.AsEnumerable();

        // Apply Tag / Skill filters
        if (request.Tags?.Count > 0)
        {
            filtered = filtered.Where(c => request.Tags.All(t => c.Def.Navigation?.Tags?.Contains(t, StringComparer.OrdinalIgnoreCase) == true));
        }
        if (request.Skills?.Count > 0)
        {
            filtered = filtered.Where(c => request.Skills.All(s => c.Def.Skills.Contains(s, StringComparer.OrdinalIgnoreCase)));
        }

        var results = new List<AssessmentSearchResult>();
        foreach (var c in filtered)
        {
            var def = c.Def;
            var nav = NavigationInference.Infer(def);
            decimal score = hasQuery ? RankCandidate(def, nav, normalizedQuery, c.InitialScore) : 0;
            
            results.Add(new AssessmentSearchResult(
                def.Id,
                def.Title,
                def.AssessmentType,
                def.CategoryId,
                def.CategoryId, // We don't have subject title here easily without joining, but UI doesn't strict need it usually.
                [c.AreaId],
                [c.AreaId],
                [c.TopicId],
                [c.TopicId],
                nav.LearningGoal ?? string.Empty,
                nav.ActivityType ?? string.Empty,
                nav.Tags,
                def.Skills,
                GetEffectiveItemCount(def),
                AssessmentItemCounter.Count(def),
                AssessmentItemCounter.EffectiveAttemptCount(def),
                score,
                Array.Empty<string>(), // matched fields
                null
            ));
        }

        return results
            .OrderByDescending(r => r.Score)
            .ThenBy(r => r.Title)
            .Take(request.Limit)
            .ToList();
    }

    private static int GetEffectiveItemCount(AssessmentDefinition definition)
    {
        var authoredCount = AssessmentItemCounter.Count(definition);
        return definition.AssessmentType is AssessmentType.Quiz or AssessmentType.Test
            ? Math.Min(AssessmentItemCounter.EffectiveAttemptCount(definition) ?? authoredCount, authoredCount)
            : authoredCount;
    }

    private decimal RankCandidate(AssessmentDefinition def, NavigationMetadata nav, string query, double bm25Score)
    {
        decimal score = 50; // base score, inverted bm25 maybe? SQLite bm25 returns more negative = better.
        // FTS5 bm25 returns negative values, more negative is more relevant.
        score += (decimal)(-bm25Score * 10); 
        
        var normTitle = SearchNormalizer.Normalize(def.Title);
        if (normTitle == query) score += 1000;
        else if (normTitle.StartsWith(query)) score += 500;
        else if (normTitle.Contains(query)) score += 100;

        if (nav.Tags?.Any(t => SearchNormalizer.Normalize(t) == query) == true) score += 300;
        if (def.Skills.Any(s => SearchNormalizer.Normalize(s) == query)) score += 300;

        return score;
    }
}
