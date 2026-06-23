using Microsoft.Data.Sqlite;

namespace QuizApp.Infrastructure.Retention;

public sealed class SqliteConnectionFactory
{
    private readonly SqliteRetentionOptions options;

    public SqliteConnectionFactory(SqliteRetentionOptions options)
    {
        this.options = options;
    }

    public SqliteConnection CreateConnection()
    {
        Directory.CreateDirectory(Path.GetDirectoryName(options.DatabasePath)!);
        var builder = new SqliteConnectionStringBuilder
        {
            DataSource = options.DatabasePath,
            ForeignKeys = true
        };

        return new SqliteConnection(builder.ToString());
    }
}
