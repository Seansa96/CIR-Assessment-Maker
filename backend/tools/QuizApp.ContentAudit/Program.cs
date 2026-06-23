using System.Text.Json;
using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;
using QuizApp.Infrastructure.Retention;

namespace QuizApp.ContentAudit;

public static class Program
{
    public static async Task<int> Main(string[] args)
    {
        if (args.Length == 0)
        {
            Console.WriteLine("Usage: dotnet run --project backend/tools/QuizApp.ContentAudit -- <data_directory>");
            return 1;
        }

        var dataRoot = args[0];
        var files = new FileStorageOptions { DataRoot = dataRoot };
        var areaRepository = new FileAreaRepository(files);
        var categoryRepository = new FileCategoryRepository(files);
        var validator = new AssessmentValidator();
        var sourceInspector = new AssessmentSourceInspector();
        var taxonomyValidator = new AssessmentTaxonomyValidator();
        var catalogTaxonomyValidator = new CatalogTaxonomyValidator();

        var categories = await categoryRepository.ListAsync();
        var areas = await areaRepository.ListAsync();

        int exitCode = 0;
        int errors = 0;

        var catalogTaxonomyResult = catalogTaxonomyValidator.Validate(categories, areas);
        if (!catalogTaxonomyResult.IsValid)
        {
            foreach (var err in catalogTaxonomyResult.Errors)
            {
                Console.WriteLine($"[ERROR] [TAXONOMY_SCHEMA]: {err}");
                errors++;
            }
        }

        var seenIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        foreach (var dir in new[] { files.AssessmentsPath, files.SamplesPath })
        {
            if (!Directory.Exists(dir)) continue;

            foreach (var path in Directory.EnumerateFiles(dir, "*.*").Where(p => p.EndsWith(".yaml") || p.EndsWith(".yml") || p.EndsWith(".json")))
            {
                try
                {
                    var content = await File.ReadAllTextAsync(path);
                    var inspection = sourceInspector.Inspect(content, Path.GetExtension(path), path);
                    
                    foreach (var diag in inspection.Diagnostics)
                    {
                        var prefix = diag.Severity == DiagnosticSeverity.Error ? "[ERROR]" : "[WARN]";
                        if (diag.Severity == DiagnosticSeverity.Error) errors++;
                        Console.WriteLine($"{prefix} [{diag.Code}] {path}({diag.Line},{diag.Column}): {diag.Message}");
                    }

                    if (!inspection.IsValid) continue;

                    var dto = FileFormat.ReadFromString<AssessmentFileDto>(content, Path.GetExtension(path));
                    if (dto is null || string.IsNullOrWhiteSpace(dto.Id))
                    {
                        Console.WriteLine($"[ERROR] [MISSING_ID] {path}: Assessment has no ID.");
                        errors++;
                        continue;
                    }

                    var domain = dto.ToDomain();

                    var validation = validator.Validate(domain);
                    if (!validation.IsValid)
                    {
                        foreach (var issue in validation.Issues)
                        {
                            Console.WriteLine($"[ERROR] [{issue.Code}] {path}: {issue.Message}");
                            errors++;
                        }
                    }

                    var taxValidation = taxonomyValidator.Validate(domain, categories, areas);
                    if (!taxValidation.IsValid)
                    {
                        foreach (var issue in taxValidation.Errors)
                        {
                            Console.WriteLine($"[ERROR] [TAXONOMY] {path}: {issue}");
                            errors++;
                        }
                    }

                    if (!seenIds.Add(domain.Id))
                    {
                        Console.WriteLine($"[ERROR] [DUPLICATE_ID] {path}: Duplicate ID '{domain.Id}'.");
                        errors++;
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"[ERROR] [EXCEPTION] {path}: {ex.Message}");
                    errors++;
                }
            }
        }

        Console.WriteLine($"Audit complete. {errors} error(s) found.");
        return errors > 0 ? 1 : 0;
    }
}
