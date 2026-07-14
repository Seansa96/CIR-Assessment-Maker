using Xunit;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;
using QuizApp.Infrastructure.Retention;
using Microsoft.Data.Sqlite;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace QuizApp.Tests;

public class AssessmentSearchTests
{
    [Fact]
    public void SearchNormalizer_Handles_Punctuation_And_MathTerms()
    {
        var input = "This is a u-sub (integration) problem with dy/dx! And A-B_C.";
        var expected = "this is a u sub integration problem with dy dx and a b c";
        
        var actual = SearchNormalizer.Normalize(input);
        
        Assert.Equal(expected, actual);
    }

    [Theory]
    [InlineData("work", "work", 0, 0)]
    [InlineData("work", "word", 1, 1)]
    [InlineData("wor", "word", 1, 1)]
    [InlineData("work", "working", 3, 3)]
    [InlineData("work", "working", 2, 3)] // Max distance 2, should return 3
    public void SearchNormalizer_BoundedLevenshtein_ReturnsExpected(string s, string t, int maxDistance, int expectedDistance)
    {
        var distance = SearchNormalizer.BoundedLevenshteinDistance(s, t, maxDistance);
        Assert.Equal(expectedDistance, distance);
    }

    [Fact]
    public async Task SearchService_Applies_Exact_Filters_Case_Insensitively()
    {
        var options = CreateSearchDatabase();
        var service = new SqliteAssessmentSearchService(options, new StubAssessmentRepository());

        var results = await service.SearchAsync(new AssessmentSearchRequest(
            "ATWOOD",
            "PHYSICS-1",
            null,
            "PHYSICS-WORK-ENERGY",
            "LEARN",
            "GUIDEDWORKEDEXAMPLE",
            "WORKEDEXAMPLE",
            null,
            new[] { "ATWOOD-MACHINE" },
            10));

        Assert.Single(results);
        Assert.Equal("physics-work-energy-atwood-worked-example", results[0].Id);

        var suggestions = await service.GetSuggestionsAsync("ATW", "PHYSICS-1", null, null);
        Assert.Contains(suggestions, suggestion => suggestion.Label == "Atwood Machine");
    }

    private static SqliteRetentionOptions CreateSearchDatabase()
    {
        var root = Path.Combine(AppContext.BaseDirectory, "assessment-search-tests", Guid.NewGuid().ToString("n"));
        Directory.CreateDirectory(root);
        var options = new SqliteRetentionOptions { DatabasePath = Path.Combine(root, "search.db") };
        new SqliteRetentionInitializer(options).InitializeAsync().GetAwaiter().GetResult();

        var definition = TestData.Assessment(AssessmentType.WorkedExample, Array.Empty<QuestionDefinition>()) with
        {
            Id = "physics-work-energy-atwood-worked-example",
            Title = "Atwood Machine using Energy Methods",
            CategoryId = "physics-1",
            SubcategoryIds = new[] { "physics-work-energy" },
            Navigation = new NavigationMetadata("learn", "guidedWorkedExample", new[] { "atwood-machine" }),
            Skills = new[] { "physics-work-energy", "atwood-machine" }
        };

        var jsonOptions = new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
            Converters = { new JsonStringEnumConverter(JsonNamingPolicy.CamelCase) }
        };

        using var connection = new SqliteConnection($"Data Source={options.DatabasePath}");
        connection.Open();

        using (var command = connection.CreateCommand())
        {
            command.CommandText = """
                INSERT INTO assessments (
                    id, title, assessment_type, category_id, learning_goal, activity_type,
                    definition_json, source_path, content_hash, is_active, imported_at, updated_at)
                VALUES (
                    @id, @title, @type, @category, @goal, @activity,
                    @json, @source, @hash, 1, @now, @now);
                """;
            command.Parameters.AddWithValue("@id", definition.Id);
            command.Parameters.AddWithValue("@title", definition.Title);
            command.Parameters.AddWithValue("@type", "workedExample");
            command.Parameters.AddWithValue("@category", "physics-1");
            command.Parameters.AddWithValue("@goal", "learn");
            command.Parameters.AddWithValue("@activity", "guidedWorkedExample");
            command.Parameters.AddWithValue("@json", JsonSerializer.Serialize(definition, jsonOptions));
            command.Parameters.AddWithValue("@source", "physics-work-energy-atwood-worked-example.yaml");
            command.Parameters.AddWithValue("@hash", "hash");
            command.Parameters.AddWithValue("@now", DateTimeOffset.UtcNow.ToString("O"));
            command.ExecuteNonQuery();
        }

        using (var command = connection.CreateCommand())
        {
            command.CommandText = "INSERT INTO assessment_subcategories (assessment_id, subcategory_id) VALUES (@id, @topic);";
            command.Parameters.AddWithValue("@id", definition.Id);
            command.Parameters.AddWithValue("@topic", "physics-work-energy");
            command.ExecuteNonQuery();
        }

        using (var command = connection.CreateCommand())
        {
            command.CommandText = "INSERT INTO assessment_skills (assessment_id, skill_id) VALUES (@id, @skill);";
            command.Parameters.AddWithValue("@id", definition.Id);
            command.Parameters.AddWithValue("@skill", "atwood-machine");
            command.ExecuteNonQuery();
        }

        using (var command = connection.CreateCommand())
        {
            command.CommandText = """
                INSERT INTO assessment_search_fts (
                    assessment_id, title, normalized_title, assessment_type, subject_title,
                    area_titles, topic_titles, learning_goal, activity_type, tags, skills, prompt_terms)
                VALUES (
                    @id, @title, @normalizedTitle, @type, @subject,
                    @area, @topic, @goal, @activity, @tags, @skills, @prompt);
                """;
            command.Parameters.AddWithValue("@id", definition.Id);
            command.Parameters.AddWithValue("@title", definition.Title);
            command.Parameters.AddWithValue("@normalizedTitle", "atwood machine using energy methods");
            command.Parameters.AddWithValue("@type", "workedExample");
            command.Parameters.AddWithValue("@subject", "physics 1");
            command.Parameters.AddWithValue("@area", "physics energy momentum");
            command.Parameters.AddWithValue("@topic", "physics work energy");
            command.Parameters.AddWithValue("@goal", "learn");
            command.Parameters.AddWithValue("@activity", "guided worked example");
            command.Parameters.AddWithValue("@tags", "atwood machine");
            command.Parameters.AddWithValue("@skills", "atwood machine physics work energy");
            command.Parameters.AddWithValue("@prompt", "atwood machine energy methods");
            command.ExecuteNonQuery();
        }

        using (var command = connection.CreateCommand())
        {
            command.CommandText = """
                INSERT INTO assessment_search_terms (term, normalized_term, kind, source_id, subject_id, weight)
                VALUES (@term, @normalized, @kind, @source, @subject, @weight);
                """;
            command.Parameters.AddWithValue("@term", "Atwood Machine");
            command.Parameters.AddWithValue("@normalized", "atwood machine");
            command.Parameters.AddWithValue("@kind", "skill");
            command.Parameters.AddWithValue("@source", definition.Id);
            command.Parameters.AddWithValue("@subject", "physics-1");
            command.Parameters.AddWithValue("@weight", 100);
            command.ExecuteNonQuery();
        }

        return options;
    }

    private sealed class StubAssessmentRepository : IAssessmentRepository
    {
        public Task<IReadOnlyList<AssessmentSummary>> ListByCategoryAsync(string categoryId, CancellationToken cancellationToken = default) =>
            Task.FromResult<IReadOnlyList<AssessmentSummary>>(Array.Empty<AssessmentSummary>());

        public Task<AssessmentDefinition?> GetByIdAsync(string assessmentId, CancellationToken cancellationToken = default) =>
            Task.FromResult<AssessmentDefinition?>(null);

        public Task SaveAsync(AssessmentDefinition assessment, CancellationToken cancellationToken = default) =>
            Task.CompletedTask;

        public Task<AssessmentValidationResult> ValidateFileAsync(string fileName, CancellationToken cancellationToken = default) =>
            Task.FromResult(new AssessmentValidationResult(Array.Empty<ValidationIssue>()));
    }
}
