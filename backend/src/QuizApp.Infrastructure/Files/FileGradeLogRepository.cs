using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Infrastructure.Files;

public sealed class FileGradeLogRepository : IGradeLogRepository
{
    private readonly FileStorageOptions options;

    public FileGradeLogRepository(FileStorageOptions options)
    {
        this.options = options;
    }

    public async Task<IReadOnlyList<GradeLogEntry>> ListAsync(CancellationToken cancellationToken = default)
    {
        var entries = await FileFormat.ReadAsync<List<GradeLogEntry>>(GetLogPath(), cancellationToken);
        return entries ?? new List<GradeLogEntry>();
    }

    public async Task AddAsync(GradeLogEntry entry, CancellationToken cancellationToken = default)
    {
        var entries = (await ListAsync(cancellationToken)).ToList();
        entries.Add(entry);
        await FileFormat.WriteJsonAsync(GetLogPath(), entries, cancellationToken);
    }

    private string GetLogPath()
    {
        return Path.Combine(options.GradesPath, "grade-log.json");
    }
}
