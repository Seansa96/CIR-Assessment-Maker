using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Infrastructure.Files;

public sealed class InMemoryAttemptSessionStore : IAttemptSessionStore
{
    private readonly Dictionary<string, Attempt> attempts = new(StringComparer.OrdinalIgnoreCase);
    private readonly object gate = new();

    public Task<IReadOnlyList<Attempt>> ListAsync(CancellationToken cancellationToken = default)
    {
        lock (gate)
        {
            return Task.FromResult<IReadOnlyList<Attempt>>(attempts.Values.OrderByDescending(attempt => attempt.StartedAt).ToList());
        }
    }

    public Task<Attempt?> GetByIdAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        lock (gate)
        {
            attempts.TryGetValue(attemptId, out var attempt);
            return Task.FromResult(attempt);
        }
    }

    public Task SaveAsync(Attempt attempt, CancellationToken cancellationToken = default)
    {
        lock (gate)
        {
            attempts[attempt.Id] = attempt;
        }

        return Task.CompletedTask;
    }

    public Task DeleteAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        lock (gate)
        {
            attempts.Remove(attemptId);
        }

        return Task.CompletedTask;
    }
}
