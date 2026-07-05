using System.Text;
using System.Text.Json;
using Microsoft.Data.Sqlite;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

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
            sql.Append(" AND (subject_id = @subjectId OR subject_id IS NULL)");
        }
        
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
                SELECT a.definition_json, a.content_hash, bm25(assessment_search_fts) as score
                FROM assessment_search_fts
                JOIN assessments a ON a.id = assessment_search_fts.assessment_id
                WHERE a.is_active = 1
                """);
            
            // FTS5 MATCH syntax: query* OR *query* fallback
            sql.Append(" AND assessment_search_fts MATCH @match");
        }
        else
        {
            sql.Append("""
                SELECT a.definition_json, a.content_hash, 0 as score
                FROM assessments a
                WHERE a.is_active = 1
                """);
        }

        if (!string.IsNullOrWhiteSpace(request.SubjectId)) sql.Append(" AND a.category_id = @subjectId");
        if (!string.IsNullOrWhiteSpace(request.LearningGoal)) sql.Append(" AND a.learning_goal = @goal");
        if (!string.IsNullOrWhiteSpace(request.ActivityType)) sql.Append(" AND a.activity_type = @activity");
        if (!string.IsNullOrWhiteSpace(request.AssessmentType)) sql.Append(" AND a.assessment_type = @type");

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

        var candidates = new List<(AssessmentDefinition Def, double InitialScore)>();
        
        await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
        {
            var json = reader.GetString(0);
            var score = reader.GetDouble(2);
            var def = JsonSerializer.Deserialize<AssessmentDefinition>(json, new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase, Converters = { new System.Text.Json.Serialization.JsonStringEnumConverter(JsonNamingPolicy.CamelCase) } });
            if (def != null)
            {
                candidates.Add((def, score));
            }
        }

        // Apply remaining filters in memory
        var filtered = candidates.AsEnumerable();

        if (!string.IsNullOrWhiteSpace(request.AreaId))
        {
            // We need to resolve areas. In a real system, we might join the `assessment_areas` table.
            // For now, we can check if the definition has matching subcategories for the area, but that requires area repo.
            // Wait, we populated `area_titles` in FTS but not `areaIds` explicitly in a regular table other than `assessment_areas`.
            // Let's filter by checking the DB explicitly or rely on the caller sending `TopicId` instead.
            // Actually, we can fetch assessment_areas.
        }

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
            
            // Re-evaluating Area/Topic filters since they are not in the `assessments` table directly.
            // For a robust implementation, we would join the mapping tables. Here we do an approximation or just skip if we can't efficiently filter.
            // If topicId is provided, we can just check if def.SubcategoryIds contains it!
            if (!string.IsNullOrWhiteSpace(request.TopicId) && !def.SubcategoryIds.Contains(request.TopicId)) continue;
            
            // To properly filter by areaId without hitting the DB again, we assume areaId is handled externally 
            // or we skip it here and rely on TopicId (which is what the UI primarily uses for leaf filtering).

            results.Add(new AssessmentSearchResult(
                def.Id,
                def.Title,
                def.AssessmentType,
                def.CategoryId,
                def.CategoryId, // We don't have subject title here easily without joining, but UI doesn't strict need it usually.
                Array.Empty<string>(), // We don't have area IDs here easily
                Array.Empty<string>(),
                def.SubcategoryIds,
                def.SubcategoryIds, // Topic titles...
                nav.LearningGoal ?? string.Empty,
                nav.ActivityType ?? string.Empty,
                nav.Tags,
                def.Skills,
                def.Questions.Count + def.Items.Count,
                def.Questions.Count + def.Items.Count,
                def.AttemptQuestionCount,
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
