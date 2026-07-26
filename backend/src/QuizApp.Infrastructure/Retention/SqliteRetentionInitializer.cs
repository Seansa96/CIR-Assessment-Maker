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
                learning_sections_json TEXT NOT NULL DEFAULT '[]',
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
        if (!await ColumnExistsAsync(connection, "attempts", "learning_sections_json", cancellationToken))
        {
            await ExecuteAsync(connection, "ALTER TABLE attempts ADD COLUMN learning_sections_json TEXT NOT NULL DEFAULT '[]';", cancellationToken);
        }
        if (!await ColumnExistsAsync(connection, "attempts", "directed_project_steps_json", cancellationToken))
        {
            await ExecuteAsync(connection, "ALTER TABLE attempts ADD COLUMN directed_project_steps_json TEXT NOT NULL DEFAULT '[]';", cancellationToken);
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
                committed_at TEXT NOT NULL,
                earned_points TEXT NOT NULL DEFAULT '0',
                possible_points TEXT NOT NULL DEFAULT '0'
            );
            """, cancellationToken);

        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_attempts_started_at ON attempts(started_at DESC);", cancellationToken);
        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_grades_committed_at ON grade_log_entries(committed_at DESC);", cancellationToken);

        await ExecuteAsync(connection, """
            CREATE TABLE IF NOT EXISTS assessment_reports (
                id TEXT PRIMARY KEY,
                assessment_id TEXT NOT NULL,
                assessment_title TEXT NOT NULL,
                attempt_id TEXT NOT NULL,
                context_id TEXT NULL,
                kind TEXT NOT NULL CHECK (kind IN ('bug', 'improvement', 'comment')),
                comment TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'resolved')),
                created_at TEXT NOT NULL,
                resolved_at TEXT NULL
            );
            """, cancellationToken);
        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_assessment_reports_assessment ON assessment_reports(assessment_id);", cancellationToken);
        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_assessment_reports_status ON assessment_reports(status);", cancellationToken);
        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_assessment_reports_kind ON assessment_reports(kind);", cancellationToken);
        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_assessment_reports_created ON assessment_reports(created_at DESC);", cancellationToken);

        if (!await ColumnExistsAsync(connection, "grade_log_entries", "earned_points", cancellationToken))
        {
            await ExecuteAsync(connection, "ALTER TABLE grade_log_entries ADD COLUMN earned_points TEXT NOT NULL DEFAULT '0';", cancellationToken);
            await ExecuteAsync(connection, "UPDATE grade_log_entries SET earned_points = CAST(correct_count AS TEXT);", cancellationToken);
        }
        if (!await ColumnExistsAsync(connection, "grade_log_entries", "possible_points", cancellationToken))
        {
            await ExecuteAsync(connection, "ALTER TABLE grade_log_entries ADD COLUMN possible_points TEXT NOT NULL DEFAULT '0';", cancellationToken);
            await ExecuteAsync(connection, "UPDATE grade_log_entries SET possible_points = CAST(total_questions AS TEXT);", cancellationToken);
        }

        // Assessment catalog tables
        await ExecuteAsync(connection, """
            CREATE TABLE IF NOT EXISTS assessments (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                assessment_type TEXT NOT NULL,
                category_id TEXT NOT NULL,
                learning_goal TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                definition_json TEXT NOT NULL,
                source_path TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                source_last_write_utc TEXT NULL,
                source_length INTEGER NULL,
                import_status TEXT NOT NULL DEFAULT 'valid',
                last_error TEXT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                imported_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """, cancellationToken);

        if (!await ColumnExistsAsync(connection, "assessments", "source_last_write_utc", cancellationToken))
        {
            await ExecuteAsync(connection, "ALTER TABLE assessments ADD COLUMN source_last_write_utc TEXT NULL;", cancellationToken);
        }
        if (!await ColumnExistsAsync(connection, "assessments", "source_length", cancellationToken))
        {
            await ExecuteAsync(connection, "ALTER TABLE assessments ADD COLUMN source_length INTEGER NULL;", cancellationToken);
        }
        if (!await ColumnExistsAsync(connection, "assessments", "import_status", cancellationToken))
        {
            await ExecuteAsync(connection, "ALTER TABLE assessments ADD COLUMN import_status TEXT NOT NULL DEFAULT 'valid';", cancellationToken);
        }
        if (!await ColumnExistsAsync(connection, "assessments", "last_error", cancellationToken))
        {
            await ExecuteAsync(connection, "ALTER TABLE assessments ADD COLUMN last_error TEXT NULL;", cancellationToken);
        }
        if (!await ColumnExistsAsync(connection, "assessments", "metadata_status", cancellationToken))
        {
            await ExecuteAsync(connection, "ALTER TABLE assessments ADD COLUMN metadata_status INTEGER NOT NULL DEFAULT 0;", cancellationToken);
        }

        await ExecuteAsync(connection, """
            CREATE TABLE IF NOT EXISTS assessment_subcategories (
                assessment_id TEXT NOT NULL,
                subcategory_id TEXT NOT NULL,
                PRIMARY KEY (assessment_id, subcategory_id)
            );
            """, cancellationToken);

        await ExecuteAsync(connection, """
            CREATE TABLE IF NOT EXISTS assessment_areas (
                assessment_id TEXT NOT NULL,
                area_id TEXT NOT NULL,
                PRIMARY KEY (assessment_id, area_id)
            );
            """, cancellationToken);

        await ExecuteAsync(connection, """
            CREATE TABLE IF NOT EXISTS assessment_tags (
                assessment_id TEXT NOT NULL,
                tag TEXT NOT NULL,
                PRIMARY KEY (assessment_id, tag)
            );
            """, cancellationToken);

        await ExecuteAsync(connection, """
            CREATE TABLE IF NOT EXISTS assessment_skills (
                assessment_id TEXT NOT NULL,
                skill_id TEXT NOT NULL,
                PRIMARY KEY (assessment_id, skill_id)
            );
            """, cancellationToken);

        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_assessments_category ON assessments(category_id);", cancellationToken);
        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_assessments_goal ON assessments(learning_goal);", cancellationToken);
        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_assessments_activity ON assessments(activity_type);", cancellationToken);
        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_assessments_active ON assessments(is_active);", cancellationToken);
        // Assessment placement is singular. Collapse legacy relation fan-out so
        // the uniqueness constraints can be added to existing catalogs; the
        // importer then repopulates the authoritative topic/area from YAML.
        await ExecuteAsync(connection, "DELETE FROM assessment_subcategories WHERE rowid NOT IN (SELECT MIN(rowid) FROM assessment_subcategories GROUP BY assessment_id);", cancellationToken);
        await ExecuteAsync(connection, "DELETE FROM assessment_areas WHERE rowid NOT IN (SELECT MIN(rowid) FROM assessment_areas GROUP BY assessment_id);", cancellationToken);
        await ExecuteAsync(connection, "CREATE UNIQUE INDEX IF NOT EXISTS ux_assessment_single_topic ON assessment_subcategories(assessment_id);", cancellationToken);
        await ExecuteAsync(connection, "CREATE UNIQUE INDEX IF NOT EXISTS ux_assessment_single_area ON assessment_areas(assessment_id);", cancellationToken);
        
        await ExecuteAsync(connection, """
            CREATE VIRTUAL TABLE IF NOT EXISTS assessment_search_fts
            USING fts5(
                assessment_id UNINDEXED,
                title,
                normalized_title,
                assessment_type,
                subject_title,
                area_titles,
                topic_titles,
                learning_goal,
                activity_type,
                tags,
                skills,
                prompt_terms,
                tokenize = 'unicode61 remove_diacritics 2'
            );
            """, cancellationToken);

        await ExecuteAsync(connection, """
            CREATE TABLE IF NOT EXISTS assessment_search_terms (
                term TEXT NOT NULL,
                normalized_term TEXT NOT NULL,
                kind TEXT NOT NULL,
                source_id TEXT NOT NULL,
                subject_id TEXT NULL,
                weight INTEGER NOT NULL,
                PRIMARY KEY (normalized_term, kind, source_id)
            );
            """, cancellationToken);

        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_assessment_search_terms_prefix ON assessment_search_terms(normalized_term);", cancellationToken);
        await ExecuteAsync(connection, "CREATE INDEX IF NOT EXISTS idx_assessment_search_terms_subject ON assessment_search_terms(subject_id);", cancellationToken);

        
        await ExecuteAsync(connection, """
            CREATE TABLE IF NOT EXISTS import_runs (
                id TEXT PRIMARY KEY,
                started_at TEXT NOT NULL,
                finished_at TEXT NULL,
                status TEXT NOT NULL
            );
            """, cancellationToken);

        await ExecuteAsync(connection, """
            CREATE TABLE IF NOT EXISTS import_diagnostics (
                id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL,
                path TEXT NULL,
                assessment_id TEXT NULL,
                severity TEXT NOT NULL,
                code TEXT NOT NULL,
                message TEXT NOT NULL,
                line INTEGER NULL,
                column INTEGER NULL,
                actual_key TEXT NULL,
                suggested_key TEXT NULL
            );
            """, cancellationToken);
        
        await RunAttemptCleanupMigrationAsync(connection, cancellationToken);
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

    private async Task RunAttemptCleanupMigrationAsync(SqliteConnection connection, CancellationToken cancellationToken)
    {
        await using var checkCommand = connection.CreateCommand();
        checkCommand.CommandText = "SELECT value FROM retention_metadata WHERE key = 'migration_abandoned_cleanup';";
        var result = await checkCommand.ExecuteScalarAsync(cancellationToken);
        if (result is not null)
        {
            return;
        }

        await ExecuteAsync(connection, "DELETE FROM grade_log_entries WHERE attempt_id IN (SELECT id FROM attempts WHERE status = 4);", cancellationToken);
        await ExecuteAsync(connection, "DELETE FROM attempts WHERE status = 4;", cancellationToken);

        await using var updateCommand = connection.CreateCommand();
        updateCommand.CommandText = "INSERT INTO retention_metadata (key, value, updated_at) VALUES ('migration_abandoned_cleanup', 'completed', $updated_at);";
        updateCommand.Parameters.AddWithValue("$updated_at", DateTimeOffset.UtcNow.ToString("O"));
        await updateCommand.ExecuteNonQueryAsync(cancellationToken);
    }
}
