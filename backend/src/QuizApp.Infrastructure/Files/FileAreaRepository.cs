using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Infrastructure.Files;

public sealed class FileAreaRepository : IAreaRepository
{
    private readonly FileStorageOptions options;

    public FileAreaRepository(FileStorageOptions options)
    {
        this.options = options;
    }

    public async Task<IReadOnlyList<AreaDefinition>> ListAsync(CancellationToken cancellationToken = default)
    {
        var path = Path.Combine(options.DataRoot, "areas.yaml");
        if (!File.Exists(path))
        {
            return Array.Empty<AreaDefinition>();
        }

        var dto = await FileFormat.ReadAsync<AreaFileDto>(path, cancellationToken);
        if (dto?.Areas is null)
        {
            return Array.Empty<AreaDefinition>();
        }

        return dto.Areas
            .Where(area => !string.IsNullOrWhiteSpace(area.Id))
            .Select(area => new AreaDefinition(
                area.Id!.Trim(),
                string.IsNullOrWhiteSpace(area.Title) ? area.Id!.Trim() : area.Title!.Trim(),
                area.CategoryIds?.ToList() ?? new List<string>(),
                area.SubcategoryIds?.ToList() ?? new List<string>(),
                area.Description))
            .OrderBy(area => area.Title)
            .ToList();
    }
}

internal sealed class AreaFileDto
{
    public int SchemaVersion { get; set; }
    public List<AreaItemFileDto>? Areas { get; set; }
}

internal sealed class AreaItemFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public string? Description { get; set; }
    public List<string>? CategoryIds { get; set; }
    public List<string>? SubcategoryIds { get; set; }
}
