using QuizApp.Core.Domain;

namespace QuizApp.Core.Repositories;

public interface ICourseRepository
{
    Task<IReadOnlyList<CourseDefinition>> ListDefinitionsAsync(CancellationToken cancellationToken = default);
    Task<CourseDefinition?> GetDefinitionAsync(string courseId, CancellationToken cancellationToken = default);
    Task SaveDefinitionAsync(CourseDefinition definition, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<CourseRun>> ListRunsAsync(CancellationToken cancellationToken = default);
    Task<CourseRun?> GetRunAsync(string runId, CancellationToken cancellationToken = default);
    Task SaveRunAsync(CourseRun run, CancellationToken cancellationToken = default);
}
