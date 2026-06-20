using Microsoft.Data.Sqlite;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Infrastructure.Retention;

public sealed class SqliteGradeLogRepository : IGradeLogRepository
{
    private readonly SqliteConnectionFactory connectionFactory;
    private readonly SqliteRetentionInitializer initializer;

    public SqliteGradeLogRepository(SqliteRetentionOptions options)
        : this(new SqliteConnectionFactory(options))
    {
    }

    internal SqliteGradeLogRepository(SqliteConnectionFactory connectionFactory)
    {
        this.connectionFactory = connectionFactory;
        initializer = new SqliteRetentionInitializer(connectionFactory);
    }

    public async Task<IReadOnlyList<GradeLogEntry>> ListAsync(CancellationToken cancellationToken = default)
    {
        await initializer.InitializeAsync(cancellationToken);
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = """
            SELECT id, attempt_id, assessment_id, assessment_title, mode, correct_count, total_questions, percent_score, committed_at, earned_points, possible_points
            FROM grade_log_entries
            ORDER BY committed_at DESC;
            """;

        var entries = new List<GradeLogEntry>();
        await using var reader = await command.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
        {
            entries.Add(ReadEntry(reader));
        }

        return entries;
    }

    public async Task AddAsync(GradeLogEntry entry, CancellationToken cancellationToken = default)
    {
        await initializer.InitializeAsync(cancellationToken);
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = """
            INSERT INTO grade_log_entries (
                id, attempt_id, assessment_id, assessment_title, mode, correct_count, total_questions, percent_score, committed_at, earned_points, possible_points
            )
            VALUES (
                $id, $attempt_id, $assessment_id, $assessment_title, $mode, $correct_count, $total_questions, $percent_score, $committed_at, $earned_points, $possible_points
            )
            ON CONFLICT(attempt_id) DO UPDATE SET
                id = excluded.id,
                assessment_id = excluded.assessment_id,
                assessment_title = excluded.assessment_title,
                mode = excluded.mode,
                correct_count = excluded.correct_count,
                total_questions = excluded.total_questions,
                percent_score = excluded.percent_score,
                committed_at = excluded.committed_at,
                earned_points = excluded.earned_points,
                possible_points = excluded.possible_points;
            """;
        command.Parameters.AddWithValue("$id", entry.Id);
        command.Parameters.AddWithValue("$attempt_id", entry.AttemptId);
        command.Parameters.AddWithValue("$assessment_id", entry.AssessmentId);
        command.Parameters.AddWithValue("$assessment_title", entry.AssessmentTitle);
        command.Parameters.AddWithValue("$mode", (int)entry.Mode);
        command.Parameters.AddWithValue("$correct_count", entry.CorrectCount);
        command.Parameters.AddWithValue("$total_questions", entry.TotalQuestions);
        command.Parameters.AddWithValue("$percent_score", entry.PercentScore.ToString(System.Globalization.CultureInfo.InvariantCulture));
        command.Parameters.AddWithValue("$committed_at", entry.CommittedAt.ToString("O"));
        command.Parameters.AddWithValue("$earned_points", entry.EarnedPoints.ToString(System.Globalization.CultureInfo.InvariantCulture));
        command.Parameters.AddWithValue("$possible_points", entry.PossiblePoints.ToString(System.Globalization.CultureInfo.InvariantCulture));
        await command.ExecuteNonQueryAsync(cancellationToken);
    }

    public async Task RemoveByAttemptIdAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        await initializer.InitializeAsync(cancellationToken);
        await using var connection = connectionFactory.CreateConnection();
        await connection.OpenAsync(cancellationToken);
        await using var command = connection.CreateCommand();
        command.CommandText = "DELETE FROM grade_log_entries WHERE attempt_id = $attempt_id;";
        command.Parameters.AddWithValue("$attempt_id", attemptId);
        await command.ExecuteNonQueryAsync(cancellationToken);
    }

    private static GradeLogEntry ReadEntry(SqliteDataReader reader)
    {
        return new GradeLogEntry(
            reader.GetString(0),
            reader.GetString(1),
            reader.GetString(2),
            reader.GetString(3),
            (AssessmentMode)reader.GetInt32(4),
            reader.GetInt32(5),
            reader.GetInt32(6),
            decimal.Parse(reader.GetString(7), System.Globalization.CultureInfo.InvariantCulture),
            DateTimeOffset.Parse(reader.GetString(8)))
        {
            EarnedPoints = decimal.Parse(reader.GetString(9), System.Globalization.CultureInfo.InvariantCulture),
            PossiblePoints = decimal.Parse(reader.GetString(10), System.Globalization.CultureInfo.InvariantCulture)
        };
    }
}
