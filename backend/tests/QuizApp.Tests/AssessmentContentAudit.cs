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

namespace QuizApp.Tests;

public sealed class AssessmentContentAudit
{
    private readonly FileStorageOptions options;
    private readonly FileAssessmentRepository assessmentRepo;
    private readonly FileCategoryRepository categoryRepo;
    private readonly FileAreaRepository areaRepo;
    private readonly AssessmentValidator validator;
    private readonly AssessmentTaxonomyValidator taxonomyValidator;

    public AssessmentContentAudit(string basePath)
    {
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
