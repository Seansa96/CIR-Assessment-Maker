using QuizApp.Core.Domain;

namespace QuizApp.Core.Repositories;

public interface ICategoryRepository
{
    Task<IReadOnlyList<Category>> ListAsync(CancellationToken cancellationToken = default);
}
