using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public interface INavigationCatalogService
{
    Task<NavigationCatalog> GetCatalogAsync(CancellationToken cancellationToken = default);
}
