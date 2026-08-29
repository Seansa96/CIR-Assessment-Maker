using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Infrastructure.Retention;

public sealed class SqliteCourseRepository : ICourseRepository
{
    private readonly SqliteConnectionFactory factory;
    private readonly SqliteRetentionInitializer initializer;
    public SqliteCourseRepository(SqliteRetentionOptions options) : this(new SqliteConnectionFactory(options)) { }
    internal SqliteCourseRepository(SqliteConnectionFactory factory) { this.factory = factory; initializer = new SqliteRetentionInitializer(factory); }

    public Task<IReadOnlyList<CourseDefinition>> ListDefinitionsAsync(CancellationToken ct = default) => ListAsync<CourseDefinition>("course_definitions", "updated_at", ct);
    public async Task<CourseDefinition?> GetDefinitionAsync(string id, CancellationToken ct = default) => await GetAsync<CourseDefinition>("course_definitions", id, ct);
    public Task SaveDefinitionAsync(CourseDefinition definition, CancellationToken ct = default) => SaveAsync("course_definitions", definition.Id, definition.CategoryId, RetentionJson.Serialize(definition), definition.UpdatedAt, ct);
    public Task<IReadOnlyList<CourseRun>> ListRunsAsync(CancellationToken ct = default) => ListAsync<CourseRun>("course_runs", "updated_at", ct);
    public async Task<CourseRun?> GetRunAsync(string id, CancellationToken ct = default) => await GetAsync<CourseRun>("course_runs", id, ct);
    public Task SaveRunAsync(CourseRun run, CancellationToken ct = default) => SaveAsync("course_runs", run.Id, run.CategoryId, RetentionJson.Serialize(run), run.StartedAt, ct);

    private async Task<IReadOnlyList<T>> ListAsync<T>(string table, string orderColumn, CancellationToken ct) {
        await initializer.InitializeAsync(ct); await using var connection = factory.CreateConnection(); await connection.OpenAsync(ct); await using var command = connection.CreateCommand();
        command.CommandText = $"SELECT payload_json FROM {table} ORDER BY {orderColumn} DESC;"; var output = new List<T>(); await using var reader = await command.ExecuteReaderAsync(ct);
        while (await reader.ReadAsync(ct)) { var item = RetentionJson.Deserialize<T>(reader.GetString(0)); if (item is not null) output.Add(item); } return output;
    }
    private async Task<T?> GetAsync<T>(string table, string id, CancellationToken ct) {
        await initializer.InitializeAsync(ct); await using var connection = factory.CreateConnection(); await connection.OpenAsync(ct); await using var command = connection.CreateCommand(); command.CommandText = $"SELECT payload_json FROM {table} WHERE id = $id;"; command.Parameters.AddWithValue("$id", id);
        var value = await command.ExecuteScalarAsync(ct); return value is string json ? RetentionJson.Deserialize<T>(json) : default;
    }
    private async Task SaveAsync(string table, string id, string categoryId, string json, DateTimeOffset timestamp, CancellationToken ct) {
        await initializer.InitializeAsync(ct); await using var connection = factory.CreateConnection(); await connection.OpenAsync(ct); await using var command = connection.CreateCommand();
        command.CommandText = $"INSERT INTO {table} (id, category_id, payload_json, updated_at) VALUES ($id, $category, $payload, $at) ON CONFLICT(id) DO UPDATE SET category_id = excluded.category_id, payload_json = excluded.payload_json, updated_at = excluded.updated_at;";
        command.Parameters.AddWithValue("$id", id); command.Parameters.AddWithValue("$category", categoryId); command.Parameters.AddWithValue("$payload", json); command.Parameters.AddWithValue("$at", timestamp.ToString("O")); await command.ExecuteNonQueryAsync(ct);
    }
}
