using QuizApp.Core.Domain;

namespace QuizApp.Core.Repositories;

public interface IGuidedProjectSessionRepository
{
    Task<GuidedProjectSession?> GetAsync(string attemptId, CancellationToken cancellationToken = default);
    Task SaveAsync(GuidedProjectSession session, CancellationToken cancellationToken = default);
    Task DeleteAsync(string attemptId, CancellationToken cancellationToken = default);
}
