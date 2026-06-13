using QuizApp.Core.Domain;

namespace QuizApp.Core.Repositories;

public interface IAreaRepository
{
    Task<IReadOnlyList<AreaDefinition>> ListAsync(CancellationToken cancellationToken = default);
}
