using Microsoft.Data.Sqlite;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Infrastructure.Retention;

public sealed class SqliteAssessmentReportRepository : IAssessmentReportRepository
{
    private readonly SqliteConnectionFactory connectionFactory;
    private readonly SqliteRetentionInitializer initializer;

    public SqliteAssessmentReportRepository(SqliteRetentionOptions options)
        : this(new SqliteConnectionFactory(options))
    {
    }

    internal SqliteAssessmentReportRepository(SqliteConnectionFactory connectionFactory)
    {
        this.connectionFactory = connectionFactory;
        initializer = new SqliteRetentionInitializer(connectionFactory);
    }

    public async Task<IReadOnlyList<AssessmentReportEntry>> ListAsync(CancellationToken cancellationToken = default)
    {
        await initializer.InitializeAsync(cancellationToken);
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = """
            SELECT id, assessment_id, assessment_title, attempt_id, context_id, kind, comment, status, created_at, resolved_at
            FROM assessment_reports
            ORDER BY
                CASE status WHEN 'open' THEN 0 ELSE 1 END,
                created_at DESC,
                id ASC;
            """;

        var entries = new List<AssessmentReportEntry>();
        await using var reader = await command.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
        {
            entries.Add(ReadEntry(reader));
        }

        return entries;
    }

    public async Task<AssessmentReportEntry?> GetByIdAsync(
        string reportId,
        CancellationToken cancellationToken = default)
    {
        await initializer.InitializeAsync(cancellationToken);
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = """
            SELECT id, assessment_id, assessment_title, attempt_id, context_id, kind, comment, status, created_at, resolved_at
            FROM assessment_reports
            WHERE id = $id;
            """;
        command.Parameters.AddWithValue("$id", reportId);
        await using var reader = await command.ExecuteReaderAsync(cancellationToken);
        return await reader.ReadAsync(cancellationToken) ? ReadEntry(reader) : null;
    }

    public async Task AddAsync(AssessmentReportEntry entry, CancellationToken cancellationToken = default)
    {
        await initializer.InitializeAsync(cancellationToken);
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = """
            INSERT INTO assessment_reports (
                id, assessment_id, assessment_title, attempt_id, context_id, kind, comment, status, created_at, resolved_at
            )
            VALUES (
                $id, $assessment_id, $assessment_title, $attempt_id, $context_id, $kind, $comment, $status, $created_at, $resolved_at
            );
            """;
        Bind(command, entry);
        await command.ExecuteNonQueryAsync(cancellationToken);
    }

    public async Task<AssessmentReportEntry?> SetStatusAsync(
        string reportId,
        AssessmentReportStatus status,
        DateTimeOffset? resolvedAt,
        CancellationToken cancellationToken = default)
    {
        await initializer.InitializeAsync(cancellationToken);
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = """
            UPDATE assessment_reports
            SET status = $status, resolved_at = $resolved_at
            WHERE id = $id;
            """;
        command.Parameters.AddWithValue("$id", reportId);
        command.Parameters.AddWithValue("$status", ToStorage(status));
        command.Parameters.AddWithValue("$resolved_at", resolvedAt is null ? DBNull.Value : resolvedAt.Value.ToString("O"));
        var changed = await command.ExecuteNonQueryAsync(cancellationToken);
        if (changed == 0)
        {
            return null;
        }

        await using var readCommand = connection.CreateCommand();
        readCommand.CommandText = """
            SELECT id, assessment_id, assessment_title, attempt_id, context_id, kind, comment, status, created_at, resolved_at
            FROM assessment_reports
            WHERE id = $id;
            """;
        readCommand.Parameters.AddWithValue("$id", reportId);
        await using var reader = await readCommand.ExecuteReaderAsync(cancellationToken);
        return await reader.ReadAsync(cancellationToken) ? ReadEntry(reader) : null;
    }

    private static void Bind(SqliteCommand command, AssessmentReportEntry entry)
    {
        command.Parameters.AddWithValue("$id", entry.Id);
        command.Parameters.AddWithValue("$assessment_id", entry.AssessmentId);
        command.Parameters.AddWithValue("$assessment_title", entry.AssessmentTitle);
        command.Parameters.AddWithValue("$attempt_id", entry.AttemptId);
        command.Parameters.AddWithValue("$context_id", entry.ContextId is null ? DBNull.Value : entry.ContextId);
        command.Parameters.AddWithValue("$kind", ToStorage(entry.Kind));
        command.Parameters.AddWithValue("$comment", entry.Comment);
        command.Parameters.AddWithValue("$status", ToStorage(entry.Status));
        command.Parameters.AddWithValue("$created_at", entry.CreatedAt.ToString("O"));
        command.Parameters.AddWithValue("$resolved_at", entry.ResolvedAt is null ? DBNull.Value : entry.ResolvedAt.Value.ToString("O"));
    }

    private static AssessmentReportEntry ReadEntry(SqliteDataReader reader)
    {
        return new AssessmentReportEntry(
            reader.GetString(0),
            reader.GetString(1),
            reader.GetString(2),
            reader.GetString(3),
            reader.IsDBNull(4) ? null : reader.GetString(4),
            ParseKind(reader.GetString(5)),
            reader.GetString(6),
            ParseStatus(reader.GetString(7)),
            DateTimeOffset.Parse(reader.GetString(8)),
            reader.IsDBNull(9) ? null : DateTimeOffset.Parse(reader.GetString(9)));
    }

    private static string ToStorage(AssessmentReportKind kind) => kind switch
    {
        AssessmentReportKind.Bug => "bug",
        AssessmentReportKind.Improvement => "improvement",
        AssessmentReportKind.Comment => "comment",
        _ => throw new ArgumentOutOfRangeException(nameof(kind), kind, null)
    };

    private static string ToStorage(AssessmentReportStatus status) => status switch
    {
        AssessmentReportStatus.Open => "open",
        AssessmentReportStatus.Resolved => "resolved",
        _ => throw new ArgumentOutOfRangeException(nameof(status), status, null)
    };

    private static AssessmentReportKind ParseKind(string value) => value switch
    {
        "bug" => AssessmentReportKind.Bug,
        "improvement" => AssessmentReportKind.Improvement,
        "comment" => AssessmentReportKind.Comment,
        _ => throw new InvalidOperationException($"Unknown assessment report kind '{value}'.")
    };

    private static AssessmentReportStatus ParseStatus(string value) => value switch
    {
        "open" => AssessmentReportStatus.Open,
        "resolved" => AssessmentReportStatus.Resolved,
        _ => throw new InvalidOperationException($"Unknown assessment report status '{value}'.")
    };
}
