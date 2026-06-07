using QuizApp.Core.Domain;

namespace QuizApp.Core.Repositories;

public interface IAttemptRepository
{
    Task<Attempt?> GetByIdAsync(string attemptId, CancellationToken cancellationToken = default);
    Task SaveAsync(Attempt attempt, CancellationToken cancellationToken = default);
}
