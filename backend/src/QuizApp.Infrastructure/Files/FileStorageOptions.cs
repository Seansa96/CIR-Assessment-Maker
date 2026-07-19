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
    public string ProjectSessionsPath => Path.Combine(DataRoot, "project-sessions");
    /// <summary>Private, gitignored source files and verbatim extraction artifacts.</summary>
    public string SourceLibraryPath => Path.Combine(DataRoot, "source-library");
    public string AssessmentReferencePath => Path.GetFullPath(Path.Combine(DataRoot, "..", "docs", "assessment-reference"));
}
