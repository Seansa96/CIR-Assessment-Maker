using QuizApp.Core.Domain;

namespace QuizApp.Core.Repositories;

public interface IAttemptSessionStore
{
    Task<IReadOnlyList<Attempt>> ListAsync(CancellationToken cancellationToken = default);
    Task<Attempt?> GetByIdAsync(string attemptId, CancellationToken cancellationToken = default);
    Task SaveAsync(Attempt attempt, CancellationToken cancellationToken = default);
    Task DeleteAsync(string attemptId, CancellationToken cancellationToken = default);
}
