using System.Text.Json;
using System.Text.Json.Serialization;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Infrastructure.Files;

public sealed class FileGuidedProjectSessionRepository : IGuidedProjectSessionRepository
{
    private static readonly JsonSerializerOptions JsonOptions = new(JsonSerializerDefaults.Web)
    {
        WriteIndented = true,
        Converters = { new JsonStringEnumConverter(JsonNamingPolicy.CamelCase) }
    };

    private readonly FileStorageOptions options;

    public FileGuidedProjectSessionRepository(FileStorageOptions options)
    {
        this.options = options;
    }

    public async Task<GuidedProjectSession?> GetAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var path = GetSessionPath(attemptId);
        if (!File.Exists(path))
        {
            return null;
        }

        await using var stream = File.OpenRead(path);
        return await JsonSerializer.DeserializeAsync<GuidedProjectSession>(stream, JsonOptions, cancellationToken);
    }

    public async Task SaveAsync(GuidedProjectSession session, CancellationToken cancellationToken = default)
    {
        Directory.CreateDirectory(options.ProjectSessionsPath);
        var path = GetSessionPath(session.AttemptId);
        await using var stream = File.Create(path);
        await JsonSerializer.SerializeAsync(stream, session, JsonOptions, cancellationToken);
    }

    public Task DeleteAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var path = GetSessionPath(attemptId);
        if (File.Exists(path))
        {
            File.Delete(path);
        }

        return Task.CompletedTask;
    }

    private string GetSessionPath(string attemptId)
    {
        var safeAttemptId = string.Concat(attemptId.Where(character => char.IsLetterOrDigit(character) || character is '-' or '_'));
        return Path.Combine(options.ProjectSessionsPath, $"{safeAttemptId}.json");
    }
}
