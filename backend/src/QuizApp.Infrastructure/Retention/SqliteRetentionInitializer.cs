using Microsoft.Data.Sqlite;

namespace QuizApp.Infrastructure.Retention;

public sealed class SqliteRetentionInitializer
{
    private readonly SqliteConnectionFactory connectionFactory;

    public SqliteRetentionInitializer(SqliteRetentionOptions options)
        : this(new SqliteConnectionFactory(options))
    {
    }

    internal SqliteRetentionInitializer(SqliteConnectionFactory connectionFactory)
    {
        this.connectionFactory = connectionFactory;
    }

    public async Task InitializeAsync(CancellationToken cancellationToken = default)
    {
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);

        await ExecuteAsync(connection, """
            CREATE TABLE IF NOT EXISTS retention_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """, cancellationToken);

        await ExecuteAsync(connection, """
            CREATE TABLE IF NOT EXISTS attempts (
                id TEXT PRIMARY KEY,
                assessment_id TEXT NOT NULL,
                mode INTEGER NOT NULL,
                status INTEGER NOT NULL,
                question_order_json TEXT NOT NULL,
                answers_json TEXT NOT NULL,
                recall_items_json TEXT NOT NULL DEFAULT '[]',
                started_at TEXT NOT NULL,
                paused_at TEXT NULL,
                completed_at TEXT NULL,
                abandoned_at TEXT NULL
            );
            """, cancellationToken);

        if (!await ColumnExistsAsync(connection, "attempts", "recall_items_json", cancellationToken))
        {
            await ExecuteAsync(connection, "ALTER TABLE attempts ADD COLUMN recall_items_json TEXT NOT NULL DEFAULT '[]';", cancellationToken);
        }

        await ExecuteAsync(connection, """
            CREATE TABLE IF NOT EXISTS grade_log_entries (
                id TEXT PRIMARY KEY,
                attempt_id TEXT NOT NULL UNIQUE,
                assessment_id TEXT NOT NULL,
                assessment_title TEXT NOT NULL,
                mode INTEGER NOT NULL,
                correct_count INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                percent_score TEXT NOT NULL,
                committed_at TEXT NOT NULL
            );
            """, cancellationToken);

        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_attempts_started_at ON attempts(started_at DESC);", cancellationToken);
        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_grades_committed_at ON grade_log_entries(committed_at DESC);", cancellationToken);
    }

    private static async Task<bool> ColumnExistsAsync(
        SqliteConnection connection,
        string tableName,
        string columnName,
        CancellationToken cancellationToken)
    {
        await using var command = connection.CreateCommand();
        command.CommandText = $"PRAGMA table_info({tableName});";
        await using var reader = await command.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
        {
            if (string.Equals(reader.GetString(1), columnName, StringComparison.OrdinalIgnoreCase))
            {
                return true;
            }
        }

        return false;
    }

    private static async Task ExecuteAsync(SqliteConnection connection, string commandText, CancellationToken cancellationToken)
    {
        await using var command = connection.CreateCommand();
        command.CommandText = commandText;
        await command.ExecuteNonQueryAsync(cancellationToken);
    }
}
