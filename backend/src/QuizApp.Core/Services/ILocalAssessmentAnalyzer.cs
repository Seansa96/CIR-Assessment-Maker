using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public interface ILocalAssessmentAnalyzer
{
    Task<AssessmentDefinition> AnalyzeAsync(AssessmentDefinition assessment, CancellationToken cancellationToken = default);
}
