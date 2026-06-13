using Microsoft.Data.Sqlite;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Infrastructure.Retention;

public sealed class LegacyRetentionMigrationService
{
    private const string MigrationKey = "legacy_retention_import_v1";
    private const string MigrationComplete = "complete";

    private readonly FileStorageOptions fileOptions;
    private readonly SqliteRetentionInitializer initializer;
    private readonly SqliteConnectionFactory connectionFactory;
    private readonly SqliteAttemptRepository attemptRepository;
    private readonly SqliteGradeLogRepository gradeLogRepository;

    public LegacyRetentionMigrationService(
        FileStorageOptions fileOptions,
        SqliteRetentionOptions sqliteOptions,
        SqliteRetentionInitializer initializer,
        SqliteAttemptRepository attemptRepository,
        SqliteGradeLogRepository gradeLogRepository)
    {
        this.fileOptions = fileOptions;
        this.initializer = initializer;
        connectionFactory = new SqliteConnectionFactory(sqliteOptions);
        this.attemptRepository = attemptRepository;
        this.gradeLogRepository = gradeLogRepository;
    }

    public async Task MigrateAsync(CancellationToken cancellationToken = default)
    {
        await initializer.InitializeAsync(cancellationToken);
        if (await IsMigrationCompleteAsync(cancellationToken))
        {
            return;
        }

        var legacyAttempts = new FileAttemptRepository(fileOptions);
        foreach (var attempt in await legacyAttempts.ListAsync(cancellationToken))
        {
            await attemptRepository.SaveAsync(attempt, cancellationToken);
        }

        var legacyGrades = new FileGradeLogRepository(fileOptions);
        foreach (var entry in await legacyGrades.ListAsync(cancellationToken))
        {
            await gradeLogRepository.AddAsync(entry, cancellationToken);
        }

        await MarkMigrationCompleteAsync(cancellationToken);
    }

    private async Task<bool> IsMigrationCompleteAsync(CancellationToken cancellationToken)
    {
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = "SELECT value FROM retention_metadata WHERE key = $key;";
        command.Parameters.AddWithValue("$key", MigrationKey);

        var value = await command.ExecuteScalarAsync(cancellationToken);
        return string.Equals(value as string, MigrationComplete, StringComparison.OrdinalIgnoreCase);
    }

    private async Task MarkMigrationCompleteAsync(CancellationToken cancellationToken)
    {
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = """
            INSERT INTO retention_metadata (key, value, updated_at)
            VALUES ($key, $value, $updated_at)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at;
            """;
        command.Parameters.AddWithValue("$key", MigrationKey);
        command.Parameters.AddWithValue("$value", MigrationComplete);
        command.Parameters.AddWithValue("$updated_at", DateTimeOffset.UtcNow.ToString("O"));
        await command.ExecuteNonQueryAsync(cancellationToken);
    }
}
