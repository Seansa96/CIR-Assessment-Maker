using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;
using YamlDotNet.RepresentationModel;

namespace QuizApp.Tests;

public sealed class AssessmentContentAudit
{
    private readonly string basePath;
    private readonly FileStorageOptions options;
    private readonly FileAssessmentRepository assessmentRepo;
    private readonly FileCategoryRepository categoryRepo;
    private readonly FileAreaRepository areaRepo;
    private readonly AssessmentValidator validator;
    private readonly AssessmentTaxonomyValidator taxonomyValidator;

    public AssessmentContentAudit(string basePath)
    {
        this.basePath = basePath;
        options = new FileStorageOptions 
        { 
            DataRoot = Path.Combine(basePath, "data")
        };

        validator = new AssessmentValidator();
        taxonomyValidator = new AssessmentTaxonomyValidator();
        assessmentRepo = new FileAssessmentRepository(options, validator);
        categoryRepo = new FileCategoryRepository(options);
        areaRepo = new FileAreaRepository(options);
    }

    public async Task<List<string>> ValidateAssessmentGeneratorsUseSingularTopicAsync(CancellationToken cancellationToken = default)
    {
        var errors = new List<string>();
        var scripts = Path.Combine(basePath, "scripts");
        if (!Directory.Exists(scripts)) return errors;
        foreach (var path in Directory.EnumerateFiles(scripts, "*.py"))
        {
            if (Path.GetFileName(path) is "add_areas.py" or "update_areas_file.py") continue;
            var content = await File.ReadAllTextAsync(path, cancellationToken);
            if (content.Contains("subcategoryIds", StringComparison.Ordinal))
                errors.Add($"{Path.GetFileName(path)} [LEGACY_GENERATOR_CLASSIFICATION]: Assessment generators must emit singular topicId.");
        }
        return errors;
    }

    public IEnumerable<string> EnumerateAssessmentFiles()
    {
        if (!Directory.Exists(options.AssessmentsPath)) return Enumerable.Empty<string>();
        return Directory.EnumerateFiles(options.AssessmentsPath, "*.yaml", SearchOption.AllDirectories);
    }

    public async Task<List<string>> ValidateAllAssessmentsAsync(CancellationToken cancellationToken = default)
    {
        var errors = new List<string>();
        var files = EnumerateAssessmentFiles();

        foreach (var file in files)
        {
            var fileName = Path.GetFileName(file);
            try
            {
                var result = await assessmentRepo.ValidateFileAsync(fileName, cancellationToken);
                if (!result.IsValid)
                {
                    foreach (var issue in result.Issues)
                    {
                        errors.Add($"{fileName} [{issue.Code}]: {issue.Message}");
                    }
                }
            }
            catch (Exception ex)
            {
                errors.Add($"{fileName} [PARSE_ERROR]: {ex.Message}");
            }
        }
        return errors;
    }

    public async Task<List<string>> CheckForDuplicateIdsAsync(CancellationToken cancellationToken = default)
    {
        var errors = new List<string>();
        var files = EnumerateAssessmentFiles();
        var idToFile = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);

        foreach (var file in files)
        {
            var fileName = Path.GetFileName(file);
            var idLine = (await File.ReadAllLinesAsync(file, cancellationToken))
                .FirstOrDefault(line => line.StartsWith("id:"));
                
            if (idLine != null)
            {
                var id = idLine.Substring(3).Trim();
                if (idToFile.TryGetValue(id, out var existingFile))
                {
                    errors.Add($"DUPLICATE_ID: '{id}' found in both {existingFile} and {fileName}");
                }
                else
                {
                    idToFile[id] = fileName;
                }
            }
        }
        return errors;
    }

    public async Task<List<string>> ValidateTaxonomyAsync(CancellationToken cancellationToken = default)
    {
        var errors = new List<string>();
        var categories = await categoryRepo.ListAsync(cancellationToken);
        var areas = await areaRepo.ListAsync(cancellationToken);
        
        foreach (var file in EnumerateAssessmentFiles())
        {
            try
            {
                var dto = await FileFormat.ReadAsync<QuizApp.Infrastructure.Files.AssessmentFileDto>(file, cancellationToken);
                var assessment = dto?.ToDomain();
                if (assessment != null)
                {
                    var result = taxonomyValidator.Validate(assessment, categories, areas);
                    if (!result.IsValid)
                    {
                        foreach (var err in result.Errors)
                        {
                            errors.Add($"{Path.GetFileName(file)} [{err}]");
                        }
                    }
                }
            }
            catch
            {
                // Ignore parsing errors here
            }
        }
        return errors;
    }

    public async Task<List<string>> ValidateSingleTopicContractAsync(CancellationToken cancellationToken = default)
    {
        var errors = new List<string>();
        foreach (var file in EnumerateAssessmentFiles())
        {
            try
            {
                var yaml = new YamlStream();
                using var reader = new StringReader(await File.ReadAllTextAsync(file, cancellationToken));
                yaml.Load(reader);
                if (yaml.Documents.Single().RootNode is not YamlMappingNode root)
                {
                    errors.Add($"{Path.GetFileName(file)} [INVALID_ROOT]: Assessment root must be a mapping.");
                    continue;
                }

                var keys = root.Children.Keys.OfType<YamlScalarNode>().Select(key => key.Value).ToList();
                if (keys.Contains("subcategoryId") || keys.Contains("subcategoryIds"))
                    errors.Add($"{Path.GetFileName(file)} [LEGACY_TOPIC_CLASSIFICATION]: Use only singular topicId.");
                if (!root.Children.TryGetValue(new YamlScalarNode("topicId"), out var topicNode)
                    || topicNode is not YamlScalarNode topicScalar
                    || string.IsNullOrWhiteSpace(topicScalar.Value))
                    errors.Add($"{Path.GetFileName(file)} [MISSING_TOPIC_ID]: Exactly one non-empty scalar topicId is required.");
            }
            catch (Exception ex)
            {
                errors.Add($"{Path.GetFileName(file)} [PARSE_ERROR]: {ex.Message}");
            }
        }
        return errors;
    }

    public async Task<List<string>> ValidateCatalogTaxonomyAsync(CancellationToken cancellationToken = default)
    {
        var result = new CatalogTaxonomyValidator().Validate(
            await categoryRepo.ListAsync(cancellationToken),
            await areaRepo.ListAsync(cancellationToken));
        return result.Errors.ToList();
    }

    public async Task<List<string>> ValidateNavigationMetadataAsync(CancellationToken cancellationToken = default)
    {
        var errors = new List<string>();
        var inspector = new AssessmentSourceInspector();
        
        foreach (var file in EnumerateAssessmentFiles())
        {
            var content = await File.ReadAllTextAsync(file, cancellationToken);
            var result = inspector.Inspect(content, file);
            if (!result.IsValid)
            {
                foreach (var diag in result.Diagnostics)
                {
                    errors.Add($"{Path.GetFileName(file)} [{diag.Code}]: {diag.Message}");
                }
            }
        }
        return errors;
    }

    public async Task<List<string>> CheckForDoubleQuotedLatexBackslashesAsync(CancellationToken cancellationToken = default)
    {
        var errors = new List<string>();
        var badRegex = new Regex(@"\""[^\""]*\\[^\""ntr\\][^\""]*\""");
        
        foreach (var file in EnumerateAssessmentFiles())
        {
            var lines = await File.ReadAllLinesAsync(file, cancellationToken);
            for (int i = 0; i < lines.Length; i++)
            {
                var line = lines[i];
                if (badRegex.IsMatch(line) && (line.Contains("\\frac") || line.Contains("\\sqrt") || line.Contains("\\text") || line.Contains("\\cdot")))
                {
                    if (line.Contains("\""))
                    {
                        errors.Add($"{Path.GetFileName(file)}: Line {i + 1} contains LaTeX in a double-quoted string.");
                    }
                }
            }
        }
        return errors;
    }
}
