namespace QuizApp.Infrastructure.Files;

public sealed class FileStorageOptions
{
    public required string DataRoot { get; init; }

    public string SettingsPath => Path.Combine(DataRoot, "settings.yaml");
    public string CategoriesPath => Path.Combine(DataRoot, "categories");
    public string AssessmentsPath => Path.Combine(DataRoot, "assessments");
    public string SamplesPath => Path.Combine(DataRoot, "samples");
    public string AttemptsPath => Path.Combine(DataRoot, "attempts");
    public string GradesPath => Path.Combine(DataRoot, "grades");
}
