using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Infrastructure.Files;

public sealed class FileCategoryRepository : ICategoryRepository
{
    private readonly FileStorageOptions options;

    public FileCategoryRepository(FileStorageOptions options)
    {
        this.options = options;
    }

    public async Task<IReadOnlyList<Category>> ListAsync(CancellationToken cancellationToken = default)
    {
        Directory.CreateDirectory(options.CategoriesPath);
        var categories = new List<Category>();

        foreach (var path in EnumerateDataFiles(options.CategoriesPath))
        {
            var dto = await FileFormat.ReadAsync<CategoryFileDto>(path, cancellationToken);
            if (dto is not null)
            {
                categories.Add(dto.ToDomain());
            }
        }

        return categories.OrderBy(category => category.Title).ToList();
    }

    private static IEnumerable<string> EnumerateDataFiles(string directory)
    {
        return Directory.EnumerateFiles(directory, "*.*")
            .Where(path => path.EndsWith(".yaml", StringComparison.OrdinalIgnoreCase)
                || path.EndsWith(".yml", StringComparison.OrdinalIgnoreCase)
                || path.EndsWith(".json", StringComparison.OrdinalIgnoreCase));
    }
}
