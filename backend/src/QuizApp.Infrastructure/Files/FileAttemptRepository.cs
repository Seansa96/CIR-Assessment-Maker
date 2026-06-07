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

    public async Task<Attempt?> GetByIdAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var path = GetAttemptPath(attemptId);
        return await FileFormat.ReadAsync<Attempt>(path, cancellationToken);
    }

    public async Task SaveAsync(Attempt attempt, CancellationToken cancellationToken = default)
    {
        await FileFormat.WriteJsonAsync(GetAttemptPath(attempt.Id), attempt, cancellationToken);
    }

    private string GetAttemptPath(string attemptId)
    {
        return Path.Combine(options.AttemptsPath, $"{Path.GetFileName(attemptId)}.json");
    }
}
