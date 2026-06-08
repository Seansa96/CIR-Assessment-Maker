using QuizApp.Core.Domain;

namespace QuizApp.Core.Repositories;

public interface IGradeLogRepository
{
    Task<IReadOnlyList<GradeLogEntry>> ListAsync(CancellationToken cancellationToken = default);
    Task AddAsync(GradeLogEntry entry, CancellationToken cancellationToken = default);
    Task RemoveByAttemptIdAsync(string attemptId, CancellationToken cancellationToken = default);
}
