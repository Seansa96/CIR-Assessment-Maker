using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Infrastructure.Files;

public sealed class FileSettingsRepository : ISettingsRepository
{
    private readonly FileStorageOptions options;

    public FileSettingsRepository(FileStorageOptions options)
    {
        this.options = options;
    }

    public async Task<AppSettings> GetAsync(CancellationToken cancellationToken = default)
    {
        var dto = await FileFormat.ReadAsync<SettingsFileDto>(options.SettingsPath, cancellationToken);
        if (dto is null)
        {
            return DefaultSettings();
        }

        return dto.ToDomain();
    }

    public async Task SaveAsync(AppSettings settings, CancellationToken cancellationToken = default)
    {
        await FileFormat.WriteYamlAsync(options.SettingsPath, settings.ToDto(), cancellationToken);
    }

    private static AppSettings DefaultSettings()
    {
        return new AppSettings(1, AssessmentMode.Practice, QuestionOrderMode.Randomized, 15, 25, null, null, false);
    }
}
