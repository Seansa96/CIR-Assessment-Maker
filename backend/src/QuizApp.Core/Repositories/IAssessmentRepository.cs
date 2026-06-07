using QuizApp.Core.Domain;

namespace QuizApp.Core.Repositories;

public interface IAssessmentRepository
{
    Task<IReadOnlyList<AssessmentSummary>> ListByCategoryAsync(string categoryId, CancellationToken cancellationToken = default);
    Task<AssessmentDefinition?> GetByIdAsync(string assessmentId, CancellationToken cancellationToken = default);
    Task<AssessmentValidationResult> ValidateFileAsync(string fileName, CancellationToken cancellationToken = default);
}
