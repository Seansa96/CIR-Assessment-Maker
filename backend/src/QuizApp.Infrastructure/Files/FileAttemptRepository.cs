using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Infrastructure.Files;

public sealed class FileAttemptRepository : IAttemptRepository
{
    private readonly FileStorageOptions options;

    public FileAttemptRepository(FileStorageOptions options)
    {
        this.options = options;
    }

    public async Task<IReadOnlyList<Attempt>> ListAsync(CancellationToken cancellationToken = default)
    {
        Directory.CreateDirectory(options.AttemptsPath);
        var attempts = new List<Attempt>();

        foreach (var path in Directory.EnumerateFiles(options.AttemptsPath, "*.json"))
        {
            var attempt = await FileFormat.ReadAsync<Attempt>(path, cancellationToken);
            if (attempt is not null)
            {
                attempts.Add(NormalizeAttempt(attempt));
            }
        }

        return attempts.OrderByDescending(attempt => attempt.StartedAt).ToList();
    }

    public async Task<Attempt?> GetByIdAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var path = GetAttemptPath(attemptId);
        var attempt = await FileFormat.ReadAsync<Attempt>(path, cancellationToken);
        return attempt is null ? null : NormalizeAttempt(attempt);
    }

    public async Task SaveAsync(Attempt attempt, CancellationToken cancellationToken = default)
    {
        await FileFormat.WriteJsonAsync(GetAttemptPath(attempt.Id), attempt, cancellationToken);
    }

    public Task DeleteAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var path = GetAttemptPath(attemptId);
        if (File.Exists(path))
        {
            File.Delete(path);
        }

        return Task.CompletedTask;
    }

    public async Task<IReadOnlyList<string>> GetCompletedAssessmentIdsAsync(CancellationToken cancellationToken = default)
    {
        var attempts = await ListAsync(cancellationToken);
        return attempts
            .Where(a => a.Status == AttemptStatus.Completed)
            .Select(a => a.AssessmentId)
            .Distinct()
            .ToList();
    }

    private string GetAttemptPath(string attemptId)
    {
        return Path.Combine(options.AttemptsPath, $"{Path.GetFileName(attemptId)}.json");
    }

    private static Attempt NormalizeAttempt(Attempt attempt)
    {
        if (attempt.Status is not AttemptStatus.Unknown)
        {
            return attempt;
        }

        return attempt with
        {
            Status = attempt.CompletedAt is null ? AttemptStatus.InProgress : AttemptStatus.Completed
        };
    }
}
