using QuizApp.Core.Domain;

namespace QuizApp.Core.Repositories;

public interface IAssessmentReportRepository
{
    Task<IReadOnlyList<AssessmentReportEntry>> ListAsync(CancellationToken cancellationToken = default);
    Task<AssessmentReportEntry?> GetByIdAsync(string reportId, CancellationToken cancellationToken = default);
    Task AddAsync(AssessmentReportEntry entry, CancellationToken cancellationToken = default);
    Task<AssessmentReportEntry?> SetStatusAsync(
        string reportId,
        AssessmentReportStatus status,
        DateTimeOffset? resolvedAt,
        CancellationToken cancellationToken = default);
}
