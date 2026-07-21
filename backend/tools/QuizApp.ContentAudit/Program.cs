using System.Text.Json;
using System.Text.RegularExpressions;
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
        var questionBankAudit = new QuestionBankAudit();
        var authoringContractAudit = new AssessmentAuthoringContractAudit();

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
        var auditByCategory = categories.ToDictionary(category => category.Id, _ => new CategoryAudit(), StringComparer.OrdinalIgnoreCase);

        var repositoryRoot = Directory.GetParent(Path.GetFullPath(dataRoot))?.FullName;
        var assessmentReferenceRoot = repositoryRoot is null
            ? null
            : Path.Combine(repositoryRoot, "docs", "assessment-reference");
        if (assessmentReferenceRoot is not null && Directory.Exists(assessmentReferenceRoot))
        {
            var bankResult = questionBankAudit.AuditRegistry(assessmentReferenceRoot);
            foreach (var warning in bankResult.Warnings)
            {
                Console.WriteLine($"[WARN] [{warning.Code}] {warning.Path}: {warning.Message}");
            }
            foreach (var error in bankResult.Errors)
            {
                Console.WriteLine($"[ERROR] [{error.Code}] {error.Path}: {error.Message}");
                errors++;
            }
        }

        foreach (var dir in new[] { files.AssessmentsPath, files.SamplesPath })
        {
            if (!Directory.Exists(dir)) continue;

            foreach (var path in Directory.EnumerateFiles(dir, "*.*").Where(p => p.EndsWith(".yaml") || p.EndsWith(".yml") || p.EndsWith(".json")))
            {
                try
                {
                    var content = await File.ReadAllTextAsync(path);
                    if (Path.GetFileName(path).StartsWith("aops-", StringComparison.OrdinalIgnoreCase)
                        && (Path.GetFileName(path).EndsWith("-concept-lesson.yaml", StringComparison.OrdinalIgnoreCase)
                            || Path.GetFileName(path).EndsWith("-worked-example.yaml", StringComparison.OrdinalIgnoreCase)
                            || Path.GetFileName(path).EndsWith("-quiz.yaml", StringComparison.OrdinalIgnoreCase)))
                    {
                        var banned = new[] { "This scenario mirrors", "An original .* problem variant", "The purpose is to test method selection", "This concept lesson introduces" };
                        foreach (var pattern in banned.Where(pattern => Regex.IsMatch(content, pattern, RegexOptions.IgnoreCase)))
                        {
                            Console.WriteLine($"[ERROR] [AOPS_TEMPLATE_PHRASE] {path}: contains banned template phrase '{pattern}'.");
                            errors++;
                        }
                    }
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

                    if (string.Equals(dto.CategoryId, "art-of-problem-solving", StringComparison.OrdinalIgnoreCase))
                    {
                        if (string.Equals(dto.AssessmentType, "quiz", StringComparison.OrdinalIgnoreCase)
                            && (dto.Questions?.Count ?? 0) < 15)
                        {
                            Console.WriteLine($"[ERROR] [AOPS_QUIZ_LENGTH] {path}: AoPS quizzes require at least 15 questions.");
                            errors++;
                        }

                        if (string.Equals(dto.AssessmentType, "workedExample", StringComparison.OrdinalIgnoreCase)
                            && (dto.WorkedExamples?.Count ?? 0) < 3)
                        {
                            Console.WriteLine($"[ERROR] [AOPS_WORKED_PROBLEMS] {path}: AoPS worked examples require three problems.");
                            errors++;
                        }
                    }

                    var domain = dto.ToDomain();
                    var category = categories.FirstOrDefault(item => item.Id.Equals(domain.CategoryId, StringComparison.OrdinalIgnoreCase));
                    foreach (var diagnostic in authoringContractAudit.Evaluate(category, domain, strict: false))
                    {
                        Console.WriteLine($"[WARN] [AUTHORING_{diagnostic.Code}] {path}: {diagnostic.Message}");
                    }
                    if (auditByCategory.TryGetValue(domain.CategoryId, out var categoryAudit))
                    {
                        categoryAudit.Assessments++;
                        var navigation = domain.Navigation;
                        if (domain.Skills.Count == 0) { categoryAudit.MissingSkills++; errors++; Console.WriteLine($"[ERROR] [MISSING_SKILLS] {path}: Assessment needs at least one skill."); }
                        if (navigation is null || string.IsNullOrWhiteSpace(navigation.LearningGoal) || string.IsNullOrWhiteSpace(navigation.ActivityType)) { categoryAudit.MissingNavigation++; errors++; Console.WriteLine($"[ERROR] [MISSING_NAVIGATION] {path}: Assessment needs navigation learningGoal and activityType."); }
                        if (navigation?.Tags.Count is null or 0) { categoryAudit.MissingTags++; errors++; Console.WriteLine($"[ERROR] [MISSING_TAGS] {path}: Assessment needs navigation tags."); }
                        else
                        {
                            if (!navigation.Tags.Contains(domain.CategoryId, StringComparer.OrdinalIgnoreCase)) { categoryAudit.CategoryTagGaps++; errors++; Console.WriteLine($"[ERROR] [CATEGORY_TAG_GAP] {path}: Tags must include '{domain.CategoryId}'."); }
                            if (!navigation.Tags.Contains(domain.TopicId, StringComparer.OrdinalIgnoreCase)) { categoryAudit.TopicTagGaps++; errors++; Console.WriteLine($"[ERROR] [TOPIC_TAG_GAP] {path}: Tags must include the singular topicId '{domain.TopicId}'."); }
                        }
                    }

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

        Console.WriteLine("\nCategory metadata and progression report:");
        foreach (var category in categories.OrderBy(category => category.Id, StringComparer.OrdinalIgnoreCase))
        {
            var audit = auditByCategory[category.Id];
            var missingAreaTopics = category.Subcategories.Count(topic => !areas.Any(area => area.CategoryIds.Contains(category.Id, StringComparer.OrdinalIgnoreCase) && area.SubcategoryIds.Contains(topic.Id, StringComparer.OrdinalIgnoreCase)));
            var ranks = category.Subcategories.Select((topic, index) => (topic.Id, index)).ToDictionary(pair => pair.Id, pair => pair.index, StringComparer.OrdinalIgnoreCase);
            var inversions = areas.Where(area => area.CategoryIds.Contains(category.Id, StringComparer.OrdinalIgnoreCase))
                .Sum(area => area.SubcategoryIds.Where(ranks.ContainsKey).Select(id => ranks[id]).Zip(area.SubcategoryIds.Where(ranks.ContainsKey).Select(id => ranks[id]).Skip(1), (left, right) => left > right ? 1 : 0).Sum());
            Console.WriteLine($"[REPORT] {category.Id}: assessments={audit.Assessments}, missingSkills={audit.MissingSkills}, missingNavigation={audit.MissingNavigation}, missingTags={audit.MissingTags}, categoryTagGaps={audit.CategoryTagGaps}, topicTagGaps={audit.TopicTagGaps}, unmappedTopics={missingAreaTopics}, areaOrderInversions={inversions}, explicitPrerequisiteTopics={category.Subcategories.Count(topic => topic.PrerequisiteIds.Count > 0)}.");
        }

        Console.WriteLine($"Audit complete. {errors} error(s) found.");
        return errors > 0 ? 1 : 0;
    }

    private sealed class CategoryAudit
    {
        public int Assessments { get; set; }
        public int MissingSkills { get; set; }
        public int MissingNavigation { get; set; }
        public int MissingTags { get; set; }
        public int CategoryTagGaps { get; set; }
        public int TopicTagGaps { get; set; }
    }
}
