using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;
using QuizApp.Core.Services;

namespace QuizApp.Infrastructure.Files;

public sealed class FileAssessmentRepository : IAssessmentRepository
{
    private readonly FileStorageOptions options;
    private readonly AssessmentValidator validator;

    public FileAssessmentRepository(FileStorageOptions options, AssessmentValidator validator)
    {
        this.options = options;
        this.validator = validator;
    }

    public async Task<IReadOnlyList<AssessmentSummary>> ListByCategoryAsync(string categoryId, CancellationToken cancellationToken = default)
    {
        var assessments = await LoadAllAsync(cancellationToken);
        return assessments
            .Where(assessment => string.Equals(assessment.CategoryId, categoryId, StringComparison.OrdinalIgnoreCase))
            .OrderBy(assessment => assessment.Title)
            .Select(CreateSummary)
            .ToList();
    }

    public async Task<AssessmentDefinition?> GetByIdAsync(string assessmentId, CancellationToken cancellationToken = default)
    {
        var path = Path.Combine(options.AssessmentsPath, $"{ToSafeFileName(assessmentId)}.yaml");
        if (File.Exists(path))
        {
            var assessment = await LoadFileAsync(path, cancellationToken);
            if (assessment != null && string.Equals(assessment.Id, assessmentId, StringComparison.OrdinalIgnoreCase))
            {
                return assessment;
            }
        }
        var assessments = await LoadAllAsync(cancellationToken);
        return assessments.FirstOrDefault(assessment => string.Equals(assessment.Id, assessmentId, StringComparison.OrdinalIgnoreCase));
    }

    public async Task SaveAsync(AssessmentDefinition assessment, CancellationToken cancellationToken = default)
    {
        var validation = validator.Validate(assessment);
        if (!validation.IsValid)
        {
            throw new InvalidOperationException($"Assessment '{assessment.Id}' is invalid: {string.Join("; ", validation.Issues.Select(issue => issue.Message))}");
        }

        var category = (await new FileCategoryRepository(options).ListAsync(cancellationToken))
            .FirstOrDefault(item => item.Id.Equals(assessment.CategoryId, StringComparison.OrdinalIgnoreCase));
        // Temporary/test repositories without a configured category catalog retain legacy behavior.
        // Real catalog categories declare a profile and therefore opt into strict save-time enforcement.
        var contract = (category?.AuthoringProfile is AuthoringProfile.Stem or AuthoringProfile.NonStem) || assessment.Authoring is not null
            ? new AssessmentAuthoringContractAudit().Evaluate(category, assessment, strict: true)
            : Array.Empty<AuthoringContractDiagnostic>();
        var blocking = contract.Where(item => item.IsBlocking).ToList();
        if (blocking.Count > 0)
        {
            throw new InvalidOperationException($"Assessment '{assessment.Id}' violates the authoring contract: {string.Join("; ", blocking.Select(item => item.Message))}");
        }

        var path = Path.Combine(options.AssessmentsPath, $"{ToSafeFileName(assessment.Id)}.yaml");
        await FileFormat.WriteYamlAsync(path, assessment.ToDto(), cancellationToken);
    }

    public async Task<AssessmentValidationResult> ValidateFileAsync(string fileName, CancellationToken cancellationToken = default)
    {
        var path = ResolveAssessmentFile(fileName);
        if (path is null)
        {
            return new AssessmentValidationResult(new[] { new ValidationIssue("FILE_NOT_FOUND", $"Assessment file '{fileName}' was not found.") });
        }

        var assessment = await LoadFileAsync(path, cancellationToken);
        if (assessment is null)
        {
            return new AssessmentValidationResult(new[] { new ValidationIssue("FILE_NOT_READABLE", $"Assessment file '{fileName}' could not be read.") });
        }

        return validator.Validate(assessment);
    }

    private async Task<IReadOnlyList<AssessmentDefinition>> LoadAllAsync(CancellationToken cancellationToken)
    {
        Directory.CreateDirectory(options.AssessmentsPath);
        Directory.CreateDirectory(options.SamplesPath);
        var assessments = new List<AssessmentDefinition>();

        foreach (var path in EnumerateAssessmentFiles())
        {
            var assessment = await LoadFileAsync(path, cancellationToken);
            if (assessment is not null)
            {
                assessments.Add(assessment);
            }
        }

        return assessments;
    }

    private async Task<AssessmentDefinition?> LoadFileAsync(string path, CancellationToken cancellationToken)
    {
        var dto = await FileFormat.ReadAsync<AssessmentFileDto>(path, cancellationToken);
        return dto?.ToDomain();
    }

    private string? ResolveAssessmentFile(string fileName)
    {
        var safeFileName = Path.GetFileName(fileName);
        return EnumerateAssessmentFiles()
            .FirstOrDefault(path => string.Equals(Path.GetFileName(path), safeFileName, StringComparison.OrdinalIgnoreCase));
    }

    private IEnumerable<string> EnumerateAssessmentFiles()
    {
        return EnumerateDataFiles(options.AssessmentsPath).Concat(EnumerateDataFiles(options.SamplesPath));
    }

    private static IEnumerable<string> EnumerateDataFiles(string directory)
    {
        if (!Directory.Exists(directory))
        {
            return Array.Empty<string>();
        }

        return Directory.EnumerateFiles(directory, "*.*")
            .Where(path => path.EndsWith(".yaml", StringComparison.OrdinalIgnoreCase)
                || path.EndsWith(".yml", StringComparison.OrdinalIgnoreCase)
                || path.EndsWith(".json", StringComparison.OrdinalIgnoreCase));
    }

    private static string ToSafeFileName(string value)
    {
        var safeCharacters = value
            .Select(character => char.IsLetterOrDigit(character) || character is '-' or '_' ? character : '-')
            .ToArray();

        return new string(safeCharacters).Trim('-').ToLowerInvariant();
    }

    private static AssessmentSummary CreateSummary(AssessmentDefinition assessment)
    {
        var authoredCount = AssessmentItemCounter.Count(assessment);
        var effectiveCount = assessment.AssessmentType is AssessmentType.Quiz or AssessmentType.Test
            ? Math.Min(AssessmentItemCounter.EffectiveAttemptCount(assessment) ?? authoredCount, authoredCount)
            : authoredCount;

        return new AssessmentSummary(
            assessment.Id,
            assessment.Title,
            assessment.AssessmentType,
            assessment.CategoryId,
            assessment.TopicId,
            effectiveCount,
            authoredCount,
            AssessmentItemCounter.EffectiveAttemptCount(assessment))
        {
            LearningGoal = assessment.Navigation?.LearningGoal,
            ActivityType = assessment.Navigation?.ActivityType,
            Tags = assessment.Navigation?.Tags ?? Array.Empty<string>(),
            Skills = assessment.Skills
        };
    }

}
