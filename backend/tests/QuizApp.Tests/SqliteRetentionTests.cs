using System.Text.Json;
using QuizApp.Core.Domain;
using QuizApp.Infrastructure.Files;
using QuizApp.Infrastructure.Retention;

namespace QuizApp.Tests;

public sealed class SqliteRetentionTests
{
    [Fact]
    public async Task Attempt_repository_round_trips_attempt_payloads()
    {
        var options = CreateOptions();
        var repository = new SqliteAttemptRepository(options);
        var attempt = SampleAttempt("attempt-1", AttemptStatus.Completed);

        await repository.SaveAsync(attempt);

        var roundTripped = await repository.GetByIdAsync(attempt.Id);

        Assert.NotNull(roundTripped);
        Assert.Equal(attempt.Id, roundTripped.Id);
        Assert.Equal(attempt.AssessmentId, roundTripped.AssessmentId);
        Assert.Equal(attempt.Mode, roundTripped.Mode);
        Assert.Equal(attempt.Status, roundTripped.Status);
        Assert.Equal(attempt.QuestionOrder, roundTripped.QuestionOrder);
        Assert.Equal(3, roundTripped.Answers.Count);
        Assert.Equal("return n * n", roundTripped.Answers[1].Answer.CodeText);
        Assert.NotNull(roundTripped.Answers[1].Evaluation?.CodeFeedback);
        Assert.Equal("\\frac{x^3}{3}+C", roundTripped.Answers[2].Answer.SymbolicLatex);
        Assert.NotNull(roundTripped.Answers[2].Evaluation?.SymbolicFeedback);
    }

    [Fact]
    public async Task InteractiveExploration_progress_round_trips_through_sqlite()
    {
        var repository = new SqliteAttemptRepository(CreateOptions());
        var attempt = SampleAttempt("exploration-attempt", AttemptStatus.Paused) with
        {
            LearningSections = new[]
            {
                new LearningSectionAttempt(
                    "parameter-effect",
                    true,
                    true,
                    false,
                    new Dictionary<string, JsonElement> { ["n"] = JsonSerializer.SerializeToElement(6) },
                    DateTimeOffset.UtcNow)
            }
        };

        await repository.SaveAsync(attempt);
        var roundTripped = await repository.GetByIdAsync(attempt.Id);

        var progress = Assert.Single(roundTripped!.LearningSections);
        Assert.True(progress.Visited);
        Assert.True(progress.InteractionChanged);
        Assert.Equal(6, progress.ControlValues["n"].GetInt32());
    }

    [Fact]
    public async Task Grade_repository_upserts_by_attempt_id_and_removes_by_attempt_id()
    {
        var options = CreateOptions();
        var attempts = new SqliteAttemptRepository(options);
        var grades = new SqliteGradeLogRepository(options);
        var attempt = SampleAttempt("attempt-1", AttemptStatus.Completed);
        await attempts.SaveAsync(attempt);

        await grades.AddAsync(new GradeLogEntry("grade-1", attempt.Id, attempt.AssessmentId, "Original", AssessmentMode.Practice, 1, 2, 50m, DateTimeOffset.UtcNow.AddMinutes(-5)));
        await grades.AddAsync(new GradeLogEntry("grade-2", attempt.Id, attempt.AssessmentId, "Updated", AssessmentMode.Practice, 2, 2, 100m, DateTimeOffset.UtcNow));

        var entries = await grades.ListAsync();
        Assert.Single(entries);
        Assert.Equal("grade-2", entries[0].Id);
        Assert.Equal(100m, entries[0].PercentScore);

        await grades.RemoveByAttemptIdAsync(attempt.Id);

        Assert.Empty(await grades.ListAsync());
    }

    [Fact]
    public async Task Legacy_migration_imports_attempts_and_grades_once()
    {
        var dataRoot = CreateDataRoot();
        var sqliteOptions = CreateOptions();
        var fileOptions = new FileStorageOptions { DataRoot = dataRoot };
        var attempt = SampleAttempt("legacy-attempt", AttemptStatus.Completed);
        var grade = new GradeLogEntry("legacy-grade", attempt.Id, attempt.AssessmentId, "Legacy Assessment", AssessmentMode.Practice, 2, 3, 66.67m, DateTimeOffset.UtcNow);
        await File.WriteAllTextAsync(Path.Combine(dataRoot, "attempts", $"{attempt.Id}.json"), JsonSerializer.Serialize(attempt, JsonOptions));
        await File.WriteAllTextAsync(Path.Combine(dataRoot, "grades", "grade-log.json"), JsonSerializer.Serialize(new[] { grade }, JsonOptions));
        var initializer = new SqliteRetentionInitializer(sqliteOptions);
        var attempts = new SqliteAttemptRepository(sqliteOptions);
        var grades = new SqliteGradeLogRepository(sqliteOptions);
        var migration = new LegacyRetentionMigrationService(fileOptions, sqliteOptions, initializer, attempts, grades);

        await migration.MigrateAsync();
        await migration.MigrateAsync();

        Assert.NotNull(await attempts.GetByIdAsync(attempt.Id));
        Assert.Single(await attempts.ListAsync());
        var entries = await grades.ListAsync();
        Assert.Single(entries);
        Assert.Equal(grade.AttemptId, entries[0].AttemptId);
    }

    [Fact]
    public async Task Legacy_migration_handles_missing_legacy_folders()
    {
        var dataRoot = CreateDataRoot(createAttempts: false, createGrades: false);
        var sqliteOptions = CreateOptions();
        var fileOptions = new FileStorageOptions { DataRoot = dataRoot };
        var initializer = new SqliteRetentionInitializer(sqliteOptions);
        var attempts = new SqliteAttemptRepository(sqliteOptions);
        var grades = new SqliteGradeLogRepository(sqliteOptions);
        var migration = new LegacyRetentionMigrationService(fileOptions, sqliteOptions, initializer, attempts, grades);

        await migration.MigrateAsync();

        Assert.Empty(await attempts.ListAsync());
        Assert.Empty(await grades.ListAsync());
    }

    private static SqliteRetentionOptions CreateOptions()
    {
        var path = Path.Combine(AppContext.BaseDirectory, "sqlite-retention-tests", Guid.NewGuid().ToString("n"), "quizapp.db");
        return new SqliteRetentionOptions { DatabasePath = path };
    }

    private static string CreateDataRoot(bool createAttempts = true, bool createGrades = true)
    {
        var dataRoot = Path.Combine(AppContext.BaseDirectory, "sqlite-retention-legacy-tests", Guid.NewGuid().ToString("n"));
        if (createAttempts)
        {
            Directory.CreateDirectory(Path.Combine(dataRoot, "attempts"));
        }

        if (createGrades)
        {
            Directory.CreateDirectory(Path.Combine(dataRoot, "grades"));
        }

        return dataRoot;
    }

    private static Attempt SampleAttempt(string id, AttemptStatus status)
    {
        var startedAt = DateTimeOffset.UtcNow.AddMinutes(-30);
        DateTimeOffset? completedAt = status is AttemptStatus.Completed ? DateTimeOffset.UtcNow : null;
        DateTimeOffset? pausedAt = status is AttemptStatus.Paused ? DateTimeOffset.UtcNow : null;
        DateTimeOffset? abandonedAt = status is AttemptStatus.Abandoned ? DateTimeOffset.UtcNow : null;
        return new Attempt(
            id,
            "assessment-1",
            AssessmentMode.Practice,
            status,
            new[] { "q001", "q002", "q003" },
            new[]
            {
                new AttemptAnswer(
                    "q001",
                    new SubmittedAnswer("q001", "a", Array.Empty<string>(), null, null, null),
                    new AnswerEvaluation("q001", true, "Correct.", "a"),
                    startedAt.AddMinutes(1)),
                new AttemptAnswer(
                    "q002",
                    new SubmittedAnswer("q002", null, Array.Empty<string>(), null, null, null)
                    {
                        CodeText = "return n * n"
                    },
                    new AnswerEvaluation("q002", true, "All tests pass.", "All tests pass")
                    {
                        CodeFeedback = new CodeFeedback(
                            new[] { new CodeTestResult(1, "3", "9", "9", true) },
                            null,
                            "ok",
                            null)
                    },
                    startedAt.AddMinutes(2)),
                new AttemptAnswer(
                    "q003",
                    new SubmittedAnswer("q003", null, Array.Empty<string>(), null, null, null)
                    {
                        SymbolicLatex = "\\frac{x^3}{3}+C"
                    },
                    new AnswerEvaluation("q003", true, "Equivalent.", "x^3/3+C")
                    {
                        SymbolicFeedback = new SymbolicFeedback(true, "x^3/3+C", "x^3/3+C", "derivative", "Equivalent derivatives")
                    },
                    startedAt.AddMinutes(3))
            },
            startedAt,
            pausedAt,
            completedAt,
            abandonedAt);
    }

    private static readonly JsonSerializerOptions JsonOptions = new(JsonSerializerDefaults.Web)
    {
        WriteIndented = true,
        PropertyNameCaseInsensitive = true
    };
}
