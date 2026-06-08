using System.Text.Json;
using QuizApp.Core.Domain;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Tests;

public sealed class FileAttemptRepositoryTests
{
    [Fact]
    public async Task GetByIdAsync_infers_status_for_legacy_completed_attempt()
    {
        var dataRoot = CreateDataRoot();
        var attemptId = "legacy-completed";
        var attemptPath = Path.Combine(dataRoot, "attempts", $"{attemptId}.json");
        await File.WriteAllTextAsync(attemptPath, JsonSerializer.Serialize(new
        {
            id = attemptId,
            assessmentId = "area-between-curves-basic",
            mode = AssessmentMode.Practice,
            questionOrder = new[] { "q001" },
            answers = Array.Empty<object>(),
            startedAt = DateTimeOffset.UtcNow,
            completedAt = DateTimeOffset.UtcNow
        }));
        var repository = new FileAttemptRepository(new FileStorageOptions { DataRoot = dataRoot });

        var attempt = await repository.GetByIdAsync(attemptId);

        Assert.NotNull(attempt);
        Assert.Equal(AttemptStatus.Completed, attempt.Status);
    }

    [Fact]
    public async Task GetByIdAsync_infers_status_for_legacy_in_progress_attempt()
    {
        var dataRoot = CreateDataRoot();
        var attemptId = "legacy-in-progress";
        var attemptPath = Path.Combine(dataRoot, "attempts", $"{attemptId}.json");
        await File.WriteAllTextAsync(attemptPath, JsonSerializer.Serialize(new
        {
            id = attemptId,
            assessmentId = "area-between-curves-basic",
            mode = AssessmentMode.Practice,
            questionOrder = new[] { "q001" },
            answers = Array.Empty<object>(),
            startedAt = DateTimeOffset.UtcNow,
            completedAt = (DateTimeOffset?)null
        }));
        var repository = new FileAttemptRepository(new FileStorageOptions { DataRoot = dataRoot });

        var attempt = await repository.GetByIdAsync(attemptId);

        Assert.NotNull(attempt);
        Assert.Equal(AttemptStatus.InProgress, attempt.Status);
    }

    private static string CreateDataRoot()
    {
        var dataRoot = Path.Combine(AppContext.BaseDirectory, "file-attempt-tests", Guid.NewGuid().ToString("n"));
        Directory.CreateDirectory(Path.Combine(dataRoot, "attempts"));
        return dataRoot;
    }
}
