namespace QuizApp.Infrastructure.Retention;

public sealed class SqliteRetentionOptions
{
    public required string DatabasePath { get; init; }
}
