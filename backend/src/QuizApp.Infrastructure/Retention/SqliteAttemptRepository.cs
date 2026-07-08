using Microsoft.Data.Sqlite;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Infrastructure.Retention;

public sealed class SqliteAttemptRepository : IAttemptRepository
{
    private readonly SqliteConnectionFactory connectionFactory;
    private readonly SqliteRetentionInitializer initializer;

    public SqliteAttemptRepository(SqliteRetentionOptions options)
        : this(new SqliteConnectionFactory(options))
    {
    }

    internal SqliteAttemptRepository(SqliteConnectionFactory connectionFactory)
    {
        this.connectionFactory = connectionFactory;
        initializer = new SqliteRetentionInitializer(connectionFactory);
    }

    public async Task<IReadOnlyList<Attempt>> ListAsync(CancellationToken cancellationToken = default)
    {
        await initializer.InitializeAsync(cancellationToken);
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = """
            SELECT id, assessment_id, mode, status, question_order_json, answers_json, recall_items_json, learning_sections_json, directed_project_steps_json, started_at, paused_at, completed_at, abandoned_at
            FROM attempts
            ORDER BY started_at DESC;
            """;

        var attempts = new List<Attempt>();
        await using var reader = await command.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
        {
            attempts.Add(ReadAttempt(reader));
        }

        return attempts;
    }

    public async Task<Attempt?> GetByIdAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        await initializer.InitializeAsync(cancellationToken);
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = """
            SELECT id, assessment_id, mode, status, question_order_json, answers_json, recall_items_json, learning_sections_json, directed_project_steps_json, started_at, paused_at, completed_at, abandoned_at
            FROM attempts
            WHERE id = $id;
            """;
        command.Parameters.AddWithValue("$id", attemptId);

        await using var reader = await command.ExecuteReaderAsync(cancellationToken);
        return await reader.ReadAsync(cancellationToken) ? ReadAttempt(reader) : null;
    }

    public async Task SaveAsync(Attempt attempt, CancellationToken cancellationToken = default)
    {
        await initializer.InitializeAsync(cancellationToken);
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = """
            INSERT INTO attempts (
                id, assessment_id, mode, status, question_order_json, answers_json, recall_items_json, learning_sections_json, directed_project_steps_json, started_at, paused_at, completed_at, abandoned_at
            )
            VALUES (
                $id, $assessment_id, $mode, $status, $question_order_json, $answers_json, $recall_items_json, $learning_sections_json, $directed_project_steps_json, $started_at, $paused_at, $completed_at, $abandoned_at
            )
            ON CONFLICT(id) DO UPDATE SET
                assessment_id = excluded.assessment_id,
                mode = excluded.mode,
                status = excluded.status,
                question_order_json = excluded.question_order_json,
                answers_json = excluded.answers_json,
                recall_items_json = excluded.recall_items_json,
                learning_sections_json = excluded.learning_sections_json,
                directed_project_steps_json = excluded.directed_project_steps_json,
                started_at = excluded.started_at,
                paused_at = excluded.paused_at,
                completed_at = excluded.completed_at,
                abandoned_at = excluded.abandoned_at;
            """;
        AddAttemptParameters(command, attempt);
        await command.ExecuteNonQueryAsync(cancellationToken);
    }

    public async Task DeleteAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        await initializer.InitializeAsync(cancellationToken);
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = "DELETE FROM attempts WHERE id = $id;";
        command.Parameters.AddWithValue("$id", attemptId);
        await command.ExecuteNonQueryAsync(cancellationToken);
    }

    public async Task<IReadOnlyList<string>> GetCompletedAssessmentIdsAsync(CancellationToken cancellationToken = default)
    {
        await initializer.InitializeAsync(cancellationToken);
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = """
            SELECT DISTINCT assessment_id
            FROM attempts
            WHERE status = $status;
            """;
        command.Parameters.AddWithValue("$status", AttemptStatus.Completed.ToString());

        var ids = new List<string>();
        await using var reader = await command.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
        {
            ids.Add(reader.GetString(0));
        }

        return ids;
    }

    private static void AddAttemptParameters(SqliteCommand command, Attempt attempt)
    {
        command.Parameters.AddWithValue("$id", attempt.Id);
        command.Parameters.AddWithValue("$assessment_id", attempt.AssessmentId);
        command.Parameters.AddWithValue("$mode", (int)attempt.Mode);
        command.Parameters.AddWithValue("$status", (int)attempt.Status);
        command.Parameters.AddWithValue("$question_order_json", RetentionJson.Serialize(attempt.QuestionOrder));
        command.Parameters.AddWithValue("$answers_json", RetentionJson.Serialize(attempt.Answers));
        command.Parameters.AddWithValue("$recall_items_json", RetentionJson.Serialize(attempt.RecallItems));
        command.Parameters.AddWithValue("$learning_sections_json", RetentionJson.Serialize(attempt.LearningSections));
        command.Parameters.AddWithValue("$directed_project_steps_json", RetentionJson.Serialize(attempt.DirectedProjectSteps));
        command.Parameters.AddWithValue("$started_at", FormatDate(attempt.StartedAt));
        command.Parameters.AddWithValue("$paused_at", FormatNullableDate(attempt.PausedAt));
        command.Parameters.AddWithValue("$completed_at", FormatNullableDate(attempt.CompletedAt));
        command.Parameters.AddWithValue("$abandoned_at", FormatNullableDate(attempt.AbandonedAt));
    }

    private static Attempt ReadAttempt(SqliteDataReader reader)
    {
        return new Attempt(
            reader.GetString(0),
            reader.GetString(1),
            (AssessmentMode)reader.GetInt32(2),
            NormalizeStatus((AttemptStatus)reader.GetInt32(3), ReadNullableDate(reader, 10)),
            RetentionJson.Deserialize<IReadOnlyList<string>>(reader.GetString(4)) ?? Array.Empty<string>(),
            RetentionJson.Deserialize<IReadOnlyList<AttemptAnswer>>(reader.GetString(5)) ?? Array.Empty<AttemptAnswer>(),
            DateTimeOffset.Parse(reader.GetString(9)),
            ReadNullableDate(reader, 10),
            ReadNullableDate(reader, 11),
            ReadNullableDate(reader, 12))
        {
            RecallItems = RetentionJson.Deserialize<IReadOnlyList<RecallItemAttempt>>(reader.GetString(6)) ?? Array.Empty<RecallItemAttempt>(),
            LearningSections = RetentionJson.Deserialize<IReadOnlyList<LearningSectionAttempt>>(reader.GetString(7)) ?? Array.Empty<LearningSectionAttempt>(),
            DirectedProjectSteps = RetentionJson.Deserialize<IReadOnlyList<DirectedProjectStepAttempt>>(reader.GetString(8)) ?? Array.Empty<DirectedProjectStepAttempt>()
        };
    }

    private static AttemptStatus NormalizeStatus(AttemptStatus status, DateTimeOffset? completedAt)
    {
        return status is AttemptStatus.Unknown
            ? completedAt is null ? AttemptStatus.InProgress : AttemptStatus.Completed
            : status;
    }

    private static string FormatDate(DateTimeOffset value)
    {
        return value.ToString("O");
    }

    private static object FormatNullableDate(DateTimeOffset? value)
    {
        return value is null ? DBNull.Value : value.Value.ToString("O");
    }

    private static DateTimeOffset? ReadNullableDate(SqliteDataReader reader, int ordinal)
    {
        return reader.IsDBNull(ordinal) ? null : DateTimeOffset.Parse(reader.GetString(ordinal));
    }
}
