using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Microsoft.Data.Sqlite;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Infrastructure.Retention;

public sealed class SqliteAssessmentCatalogImporter
{
    private const string PipelineVersion = "v3"; // Phase 7: Add pipeline version invalidation

    private readonly SqliteRetentionOptions retentionOptions;
    private readonly FileStorageOptions storageOptions;
    private readonly IAreaRepository areaRepository;
    private readonly ICategoryRepository categoryRepository;
    private readonly AssessmentValidator validator;
    private readonly IAssessmentSourceInspector sourceInspector;
    private readonly IAssessmentTaxonomyValidator taxonomyValidator;
    private readonly ICatalogTaxonomyValidator catalogTaxonomyValidator;

    public bool CatalogInitialized { get; private set; }

    public SqliteAssessmentCatalogImporter(
        SqliteRetentionOptions retentionOptions,
        FileStorageOptions storageOptions,
        IAreaRepository areaRepository,
        ICategoryRepository categoryRepository,
        AssessmentValidator validator,
        IAssessmentSourceInspector sourceInspector,
        IAssessmentTaxonomyValidator taxonomyValidator,
        ICatalogTaxonomyValidator catalogTaxonomyValidator)
    {
        this.retentionOptions = retentionOptions;
        this.storageOptions = storageOptions;
        this.areaRepository = areaRepository;
        this.categoryRepository = categoryRepository;
        this.validator = validator;
        this.sourceInspector = sourceInspector;
        this.taxonomyValidator = taxonomyValidator;
        this.catalogTaxonomyValidator = catalogTaxonomyValidator;
    }

    public async Task ImportAsync(CancellationToken cancellationToken = default)
    {
        var runId = Guid.NewGuid().ToString("N");
        var factory = new SqliteConnectionFactory(retentionOptions);

        try
        {
            await using var connection = factory.CreateConnection();
            await connection.OpenAsync(cancellationToken);

            // 1. Record Import Run start
            await RecordImportRunStartAsync(connection, runId, cancellationToken);

            var categories = await categoryRepository.ListAsync(cancellationToken);
            var areas = await areaRepository.ListAsync(cancellationToken);
            
            // Validate taxonomy sources globally
            var catalogTaxonomyResult = catalogTaxonomyValidator.Validate(categories, areas);
            if (!catalogTaxonomyResult.IsValid)
            {
                foreach (var err in catalogTaxonomyResult.Errors)
                {
                    await InsertDiagnosticAsync(connection, runId, null, null, "Error", "TAXONOMY_SCHEMA", err, null, null, null, null, cancellationToken);
                }
            }

            var areasBySubcategory = BuildSubcategoryToAreaIndex(areas);
            var areasByCategory = BuildCategoryToAreaIndex(areas);

            var files = EnumerateAssessmentFiles().ToList();
            var seenIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

            var globalHash = await ComputeGlobalConfigHashAsync(cancellationToken);
            var storedGlobalHash = await GetMetadataAsync(connection, "global_config_hash", cancellationToken);
            var forceFullReimport = globalHash != storedGlobalHash;

            foreach (var path in files)
            {
                try
                {
                    await ImportFileAsync(connection, runId, path, categories, areas, areasBySubcategory, areasByCategory, seenIds, forceFullReimport, cancellationToken);
                }
                catch (Exception ex)
                {
                    var existingId = await GetIdByPathAsync(connection, path, cancellationToken);
                    if (existingId is not null) seenIds.Add(existingId);
                    await InsertDiagnosticAsync(connection, runId, path, existingId, "Error", "UNHANDLED_EXCEPTION", ex.Message, null, null, null, null, cancellationToken);
                    Console.Error.WriteLine($"[CatalogImporter] Skipping invalid assessment file: {path}. {ex.Message}");
                }
            }

            if (forceFullReimport)
            {
                await SetMetadataAsync(connection, "global_config_hash", globalHash, cancellationToken);
            }

            // Mark assessments whose source files no longer exist as inactive
            await MarkMissingInactiveAsync(connection, seenIds, cancellationToken);

            // Mark Import Run finished
            await RecordImportRunEndAsync(connection, runId, "Success", cancellationToken);

            CatalogInitialized = true;
            Console.WriteLine($"[CatalogImporter] Import complete. {files.Count} files processed. Run: {runId}");
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"[CatalogImporter] Import failed; falling back to file repository. {ex.Message}");
            CatalogInitialized = false;

            // Try to record failure
            try
            {
                await using var connection = factory.CreateConnection();
                await connection.OpenAsync(cancellationToken);
                await RecordImportRunEndAsync(connection, runId, "Failed", cancellationToken);
            }
            catch { }
        }
    }

    public async Task<bool> TryImportAssessmentAsync(
        AssessmentDefinition assessment,
        CancellationToken cancellationToken = default)
    {
        if (!CatalogInitialized || !validator.Validate(assessment).IsValid)
        {
            return false;
        }

        try
        {
            var categories = await categoryRepository.ListAsync(cancellationToken);
            var areas = await areaRepository.ListAsync(cancellationToken);

            var taxonomyResult = taxonomyValidator.Validate(assessment, categories, areas);
            if (!taxonomyResult.IsValid) return false;

            var path = Path.Combine(storageOptions.AssessmentsPath, $"{ToSafeFileName(assessment.Id)}.yaml");
            var content = await File.ReadAllTextAsync(path, cancellationToken);
            var nav = NavigationInference.Infer(assessment);
            var resolvedAreas = ResolveAreas(
                assessment,
                BuildSubcategoryToAreaIndex(areas),
                BuildCategoryToAreaIndex(areas));
            var subjectTitle = categories.FirstOrDefault(c => c.Id == assessment.CategoryId)?.Title ?? string.Empty;
            var areaTitles = areas.Where(a => resolvedAreas.Contains(a.Id)).Select(a => a.Title).ToList();
            var topicTitles = categories.SelectMany(c => c.Subcategories).Where(s => assessment.SubcategoryIds.Contains(s.Id)).Select(s => s.Title).ToList();

            await using var connection = new SqliteConnectionFactory(retentionOptions).CreateConnection();
            await connection.OpenAsync(cancellationToken);
            await UpsertAssessmentAsync(
                connection,
                assessment,
                nav,
                resolvedAreas,
                subjectTitle,
                areaTitles,
                topicTitles,
                JsonSerializer.Serialize(assessment, JsonOptions),
                path,
                ComputeHash(content),
                DateTimeOffset.UtcNow.ToString("O"),
                cancellationToken);
            return true;
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"[CatalogImporter] Could not refresh assessment '{assessment.Id}'. {ex.Message}");
            return false;
        }
    }

    private async Task ImportFileAsync(
        SqliteConnection connection,
        string runId,
        string path,
        IReadOnlyList<Category> categories,
        IReadOnlyList<AreaDefinition> areas,
        Dictionary<string, List<string>> areasBySubcategory,
        Dictionary<string, List<string>> areasByCategory,
        HashSet<string> seenIds,
        bool forceFullReimport,
        CancellationToken cancellationToken)
    {
        var content = await File.ReadAllTextAsync(path, cancellationToken);
        var hash = ComputeHash(content);
        var existingId = await GetIdByPathAsync(connection, path, cancellationToken);

        // Preflight Source Inspection
        var inspection = sourceInspector.Inspect(content, Path.GetExtension(path), path);
        foreach (var diag in inspection.Diagnostics)
        {
            await InsertDiagnosticAsync(connection, runId, path, existingId, diag.Severity.ToString(), diag.Code, diag.Message, diag.Line, diag.Column, diag.ActualKey, diag.SuggestedKey, cancellationToken);
        }

        if (!inspection.IsValid)
        {
            if (existingId is not null) seenIds.Add(existingId);
            return;
        }

        // Check if unchanged
        var existingHash = await GetExistingHashAsync(connection, path, cancellationToken);
        if (!forceFullReimport && existingHash == hash)
        {
            if (existingId is not null)
                seenIds.Add(existingId);
            return;
        }

        var dto = FileFormat.ReadFromString<AssessmentFileDto>(content, Path.GetExtension(path));
        if (dto is null || string.IsNullOrWhiteSpace(dto.Id))
        {
            if (existingId is not null) seenIds.Add(existingId);
            await InsertDiagnosticAsync(connection, runId, path, existingId, "Error", "MISSING_ID", "Assessment file has no ID", null, null, null, null, cancellationToken);
            Console.Error.WriteLine($"[CatalogImporter] Assessment file has no ID, skipping: {path}");
            return;
        }

        var domain = dto.ToDomain();
        
        // 1. Domain Validation
        var validation = validator.Validate(domain);
        if (!validation.IsValid)
        {
            if (existingId is not null) seenIds.Add(existingId);
            foreach (var issue in validation.Issues)
            {
                await InsertDiagnosticAsync(connection, runId, path, domain.Id, "Error", issue.Code, issue.Message, null, null, null, null, cancellationToken);
            }
            return;
        }

        // 2. Taxonomy Validation
        var taxonomyValidation = taxonomyValidator.Validate(domain, categories, areas);
        if (!taxonomyValidation.IsValid)
        {
            if (existingId is not null) seenIds.Add(existingId);
            foreach (var err in taxonomyValidation.Errors)
            {
                var code = err.Split(':')[0];
                var msg = err.Contains(':') ? err.Substring(err.IndexOf(':') + 1).Trim() : err;
                // Log as warning since we still import it (system infers unmapped topics)
                await InsertDiagnosticAsync(connection, runId, path, domain.Id, "Warning", code, msg, null, null, null, null, cancellationToken);
            }
            // Do not return here! We want to import unmapped taxonomy files so the system can infer an 'unmapped' topic.
        }

        if (seenIds.Contains(domain.Id))
        {
            await InsertDiagnosticAsync(connection, runId, path, domain.Id, "Error", "DUPLICATE_ID", $"Duplicate assessment ID '{domain.Id}' in '{path}'", null, null, null, null, cancellationToken);
            return;
        }

        var nav = NavigationInference.Infer(domain);

        var resolvedAreas = ResolveAreas(domain, areasBySubcategory, areasByCategory);
        var subjectTitle = categories.FirstOrDefault(c => c.Id == domain.CategoryId)?.Title ?? string.Empty;
        var areaTitles = areas.Where(a => resolvedAreas.Contains(a.Id)).Select(a => a.Title).ToList();
        var topicTitles = categories.SelectMany(c => c.Subcategories).Where(s => domain.SubcategoryIds.Contains(s.Id)).Select(s => s.Title).ToList();
        
        var definitionJson = JsonSerializer.Serialize(domain, JsonOptions);
        var now = DateTimeOffset.UtcNow.ToString("O");

        seenIds.Add(domain.Id);

        await UpsertAssessmentAsync(connection, domain, nav, resolvedAreas, subjectTitle, areaTitles, topicTitles, definitionJson, path, hash, now, cancellationToken);
    }

    private static List<string> ResolveAreas(
        AssessmentDefinition domain,
        Dictionary<string, List<string>> areasBySubcategory,
        Dictionary<string, List<string>> areasByCategory)
    {
        var areaIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        // Primary: resolve through subcategories
        foreach (var subId in domain.SubcategoryIds)
        {
            if (areasBySubcategory.TryGetValue(subId, out var matchedAreas))
                foreach (var a in matchedAreas) areaIds.Add(a);
        }

        // Fallback: category-level area membership (only when area has no subcategories or no subcategory matched)
        if (areaIds.Count == 0 && areasByCategory.TryGetValue(domain.CategoryId, out var catAreas))
            foreach (var a in catAreas) areaIds.Add(a);

        // If still none, add to synthetic unmapped area
        if (areaIds.Count == 0)
            areaIds.Add("other-unmapped");

        return areaIds.ToList();
    }

    private static async Task UpsertAssessmentAsync(
        SqliteConnection connection,
        AssessmentDefinition domain,
        NavigationMetadata nav,
        List<string> areaIds,
        string subjectTitle,
        List<string> areaTitles,
        List<string> topicTitles,
        string definitionJson,
        string path,
        string hash,
        string now,
        CancellationToken cancellationToken)
    {
        await using var tx = connection.BeginTransaction();

        // Check if already in DB to preserve imported_at
        var importedAt = await GetImportedAtAsync(connection, domain.Id, cancellationToken) ?? now;

        await using var upsertCmd = connection.CreateCommand();
        upsertCmd.Transaction = tx;
        upsertCmd.CommandText = """
            INSERT INTO assessments (id, title, assessment_type, category_id, learning_goal, activity_type,
                definition_json, source_path, content_hash, is_active, imported_at, updated_at)
            VALUES (@id, @title, @type, @cat, @goal, @activity, @json, @path, @hash, 1, @importedAt, @now)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                assessment_type = excluded.assessment_type,
                category_id = excluded.category_id,
                learning_goal = excluded.learning_goal,
                activity_type = excluded.activity_type,
                definition_json = excluded.definition_json,
                source_path = excluded.source_path,
                content_hash = excluded.content_hash,
                is_active = 1,
                updated_at = excluded.updated_at;
            """;
        upsertCmd.Parameters.AddWithValue("@id", domain.Id);
        upsertCmd.Parameters.AddWithValue("@title", domain.Title);
        upsertCmd.Parameters.AddWithValue("@type", domain.AssessmentType.ToString());
        upsertCmd.Parameters.AddWithValue("@cat", domain.CategoryId);
        upsertCmd.Parameters.AddWithValue("@goal", nav.LearningGoal ?? string.Empty);
        upsertCmd.Parameters.AddWithValue("@activity", nav.ActivityType ?? string.Empty);
        upsertCmd.Parameters.AddWithValue("@json", definitionJson);
        upsertCmd.Parameters.AddWithValue("@path", path);
        upsertCmd.Parameters.AddWithValue("@hash", hash);
        upsertCmd.Parameters.AddWithValue("@importedAt", importedAt);
        upsertCmd.Parameters.AddWithValue("@now", now);
        await upsertCmd.ExecuteNonQueryAsync(cancellationToken);

        // Replace subcategory rows
        await DeleteAndInsertRelationsAsync(connection, tx, domain.Id, "assessment_subcategories", "subcategory_id",
            domain.SubcategoryIds, cancellationToken);

        // Replace area rows
        await DeleteAndInsertRelationsAsync(connection, tx, domain.Id, "assessment_areas", "area_id",
            areaIds, cancellationToken);

        // Replace tag rows
        await DeleteAndInsertRelationsAsync(connection, tx, domain.Id, "assessment_tags", "tag",
            nav.Tags, cancellationToken);

        // Replace skill rows
        await DeleteAndInsertRelationsAsync(connection, tx, domain.Id, "assessment_skills", "skill_id",
            domain.Skills, cancellationToken);

        // Update Search FTS
        await using var delFtsCmd = connection.CreateCommand();
        delFtsCmd.Transaction = tx;
        delFtsCmd.CommandText = "DELETE FROM assessment_search_fts WHERE assessment_id = @id;";
        delFtsCmd.Parameters.AddWithValue("@id", domain.Id);
        await delFtsCmd.ExecuteNonQueryAsync(cancellationToken);

        await using var insFtsCmd = connection.CreateCommand();
        insFtsCmd.Transaction = tx;
        insFtsCmd.CommandText = """
            INSERT INTO assessment_search_fts(
                assessment_id, title, normalized_title, assessment_type, subject_title,
                area_titles, topic_titles, learning_goal, activity_type, tags, skills, prompt_terms
            ) VALUES (
                @id, @title, @normalizedTitle, @type, @subjectTitle,
                @areaTitles, @topicTitles, @goal, @activity, @tags, @skills, @promptTerms
            );
            """;
        insFtsCmd.Parameters.AddWithValue("@id", domain.Id);
        insFtsCmd.Parameters.AddWithValue("@title", domain.Title);
        insFtsCmd.Parameters.AddWithValue("@normalizedTitle", SearchNormalizer.Normalize(domain.Title));
        insFtsCmd.Parameters.AddWithValue("@type", domain.AssessmentType.ToString());
        insFtsCmd.Parameters.AddWithValue("@subjectTitle", SearchNormalizer.Normalize(subjectTitle));
        insFtsCmd.Parameters.AddWithValue("@areaTitles", SearchNormalizer.Normalize(string.Join(" ", areaTitles)));
        insFtsCmd.Parameters.AddWithValue("@topicTitles", SearchNormalizer.Normalize(string.Join(" ", topicTitles)));
        insFtsCmd.Parameters.AddWithValue("@goal", nav.LearningGoal ?? string.Empty);
        insFtsCmd.Parameters.AddWithValue("@activity", nav.ActivityType ?? string.Empty);
        insFtsCmd.Parameters.AddWithValue("@tags", SearchNormalizer.Normalize(string.Join(" ", nav.Tags)));
        insFtsCmd.Parameters.AddWithValue("@skills", SearchNormalizer.Normalize(string.Join(" ", domain.Skills)));
        insFtsCmd.Parameters.AddWithValue("@promptTerms", ""); // omitted for v1
        await insFtsCmd.ExecuteNonQueryAsync(cancellationToken);

        // Update Search Terms
        await using var delTermsCmd = connection.CreateCommand();
        delTermsCmd.Transaction = tx;
        delTermsCmd.CommandText = "DELETE FROM assessment_search_terms WHERE source_id = @id;";
        delTermsCmd.Parameters.AddWithValue("@id", domain.Id);
        await delTermsCmd.ExecuteNonQueryAsync(cancellationToken);

        // Term Population
        var termsToInsert = new Dictionary<(string Term, string Kind), int>(); // Term/Kind -> Weight
        void AddTerm(string term, string kind, int weight)
        {
            if (string.IsNullOrWhiteSpace(term)) return;
            var norm = SearchNormalizer.Normalize(term);
            if (string.IsNullOrWhiteSpace(norm)) return;
            
            // Allow duplicate term insertions to just take max weight (handled in SQL)
            if (!termsToInsert.ContainsKey((term, kind)))
                termsToInsert[(term, kind)] = weight;
            else
                termsToInsert[(term, kind)] = Math.Max(termsToInsert[(term, kind)], weight);
        }

        AddTerm(domain.Title, "assessment", 100);
        foreach (var t in topicTitles) AddTerm(t, "topic", 80);
        foreach (var a in areaTitles) AddTerm(a, "area", 60);
        foreach (var t in nav.Tags) AddTerm(t, "tag", 70);
        foreach (var s in domain.Skills) AddTerm(s, "skill", 75);

        foreach (var kvp in termsToInsert)
        {
            await using var insTermCmd = connection.CreateCommand();
            insTermCmd.Transaction = tx;
            insTermCmd.CommandText = """
                INSERT OR REPLACE INTO assessment_search_terms (term, normalized_term, kind, source_id, subject_id, weight)
                VALUES (@term, @norm, @kind, @source, @subject, @weight);
                """;
            insTermCmd.Parameters.AddWithValue("@term", kvp.Key.Term);
            insTermCmd.Parameters.AddWithValue("@norm", SearchNormalizer.Normalize(kvp.Key.Term));
            insTermCmd.Parameters.AddWithValue("@kind", kvp.Key.Kind);
            insTermCmd.Parameters.AddWithValue("@source", domain.Id);
            insTermCmd.Parameters.AddWithValue("@subject", domain.CategoryId);
            insTermCmd.Parameters.AddWithValue("@weight", kvp.Value);
            await insTermCmd.ExecuteNonQueryAsync(cancellationToken);
        }

        await tx.CommitAsync(cancellationToken);
    }

    private static async Task DeleteAndInsertRelationsAsync(
        SqliteConnection connection,
        SqliteTransaction tx,
        string assessmentId,
        string table,
        string column,
        IEnumerable<string> values,
        CancellationToken cancellationToken)
    {
        await using var delCmd = connection.CreateCommand();
        delCmd.Transaction = tx;
        delCmd.CommandText = $"DELETE FROM {table} WHERE assessment_id = @id;";
        delCmd.Parameters.AddWithValue("@id", assessmentId);
        await delCmd.ExecuteNonQueryAsync(cancellationToken);

        foreach (var val in values)
        {
            await using var insCmd = connection.CreateCommand();
            insCmd.Transaction = tx;
            insCmd.CommandText = $"INSERT OR IGNORE INTO {table} (assessment_id, {column}) VALUES (@id, @val);";
            insCmd.Parameters.AddWithValue("@id", assessmentId);
            insCmd.Parameters.AddWithValue("@val", val);
            await insCmd.ExecuteNonQueryAsync(cancellationToken);
        }
    }

    private static async Task MarkMissingInactiveAsync(
        SqliteConnection connection,
        HashSet<string> seenIds,
        CancellationToken cancellationToken)
    {
        // Get all active IDs from DB
        var dbIds = new List<string>();
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT id FROM assessments WHERE is_active = 1;";
        await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
        while (await reader.ReadAsync(cancellationToken))
            dbIds.Add(reader.GetString(0));

        foreach (var id in dbIds.Where(id => !seenIds.Contains(id)))
        {
            await using var updateCmd = connection.CreateCommand();
            updateCmd.CommandText = "UPDATE assessments SET is_active = 0, updated_at = @now WHERE id = @id;";
            updateCmd.Parameters.AddWithValue("@now", DateTimeOffset.UtcNow.ToString("O"));
            updateCmd.Parameters.AddWithValue("@id", id);
            await updateCmd.ExecuteNonQueryAsync(cancellationToken);
            
            // Remove from FTS and Terms if inactive
            await using var delFtsCmd = connection.CreateCommand();
            delFtsCmd.CommandText = "DELETE FROM assessment_search_fts WHERE assessment_id = @id;";
            delFtsCmd.Parameters.AddWithValue("@id", id);
            await delFtsCmd.ExecuteNonQueryAsync(cancellationToken);

            await using var delTermsCmd = connection.CreateCommand();
            delTermsCmd.CommandText = "DELETE FROM assessment_search_terms WHERE source_id = @id;";
            delTermsCmd.Parameters.AddWithValue("@id", id);
            await delTermsCmd.ExecuteNonQueryAsync(cancellationToken);
        }
    }

    private static async Task<string?> GetExistingHashAsync(SqliteConnection connection, string path, CancellationToken cancellationToken)
    {
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT content_hash FROM assessments WHERE source_path = @path LIMIT 1;";
        cmd.Parameters.AddWithValue("@path", path);
        var result = await cmd.ExecuteScalarAsync(cancellationToken);
        return result as string;
    }

    private static async Task<string?> GetIdByPathAsync(SqliteConnection connection, string path, CancellationToken cancellationToken)
    {
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT id FROM assessments WHERE source_path = @path LIMIT 1;";
        cmd.Parameters.AddWithValue("@path", path);
        var result = await cmd.ExecuteScalarAsync(cancellationToken);
        return result as string;
    }

    private static async Task<string?> GetImportedAtAsync(SqliteConnection connection, string id, CancellationToken cancellationToken)
    {
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT imported_at FROM assessments WHERE id = @id LIMIT 1;";
        cmd.Parameters.AddWithValue("@id", id);
        var result = await cmd.ExecuteScalarAsync(cancellationToken);
        return result as string;
    }

    private static async Task<string?> GetMetadataAsync(SqliteConnection connection, string key, CancellationToken cancellationToken)
    {
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "SELECT value FROM retention_metadata WHERE key = @key LIMIT 1;";
        cmd.Parameters.AddWithValue("@key", key);
        var result = await cmd.ExecuteScalarAsync(cancellationToken);
        return result as string;
    }

    private static async Task SetMetadataAsync(SqliteConnection connection, string key, string value, CancellationToken cancellationToken)
    {
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = """
            INSERT INTO retention_metadata (key, value, updated_at) 
            VALUES (@key, @value, @now)
            ON CONFLICT(key) DO UPDATE SET 
                value = excluded.value, 
                updated_at = excluded.updated_at;
            """;
        cmd.Parameters.AddWithValue("@key", key);
        cmd.Parameters.AddWithValue("@value", value);
        cmd.Parameters.AddWithValue("@now", DateTimeOffset.UtcNow.ToString("O"));
        await cmd.ExecuteNonQueryAsync(cancellationToken);
    }

    private async Task<string> ComputeGlobalConfigHashAsync(CancellationToken cancellationToken)
    {
        var sb = new StringBuilder();
        sb.Append(PipelineVersion);
        
        var areasPath = Path.Combine(storageOptions.DataRoot, "areas.yaml");
        if (File.Exists(areasPath))
        {
            sb.Append(await File.ReadAllTextAsync(areasPath, cancellationToken));
        }

        if (Directory.Exists(storageOptions.CategoriesPath))
        {
            foreach (var file in Directory.EnumerateFiles(storageOptions.CategoriesPath, "*.yaml").OrderBy(f => f))
            {
                sb.Append(await File.ReadAllTextAsync(file, cancellationToken));
            }
        }

        return ComputeHash(sb.ToString());
    }

    private IEnumerable<string> EnumerateAssessmentFiles()
    {
        return EnumerateDir(storageOptions.AssessmentsPath)
            .Concat(EnumerateDir(storageOptions.SamplesPath))
            .OrderBy(p => p, StringComparer.OrdinalIgnoreCase);
    }

    private static IEnumerable<string> EnumerateDir(string dir)
    {
        if (!Directory.Exists(dir)) return Array.Empty<string>();
        return Directory.EnumerateFiles(dir, "*.*")
            .Where(p => p.EndsWith(".yaml", StringComparison.OrdinalIgnoreCase)
                     || p.EndsWith(".yml", StringComparison.OrdinalIgnoreCase)
                     || p.EndsWith(".json", StringComparison.OrdinalIgnoreCase));
    }

    private static Dictionary<string, List<string>> BuildSubcategoryToAreaIndex(IReadOnlyList<AreaDefinition> areas)
    {
        var index = new Dictionary<string, List<string>>(StringComparer.OrdinalIgnoreCase);
        foreach (var area in areas)
            foreach (var sub in area.SubcategoryIds)
            {
                if (!index.TryGetValue(sub, out var list))
                    index[sub] = list = new List<string>();
                list.Add(area.Id);
            }
        return index;
    }

    private static Dictionary<string, List<string>> BuildCategoryToAreaIndex(IReadOnlyList<AreaDefinition> areas)
    {
        var index = new Dictionary<string, List<string>>(StringComparer.OrdinalIgnoreCase);
        foreach (var area in areas.Where(candidate => candidate.SubcategoryIds.Count == 0))
            foreach (var cat in area.CategoryIds)
            {
                if (!index.TryGetValue(cat, out var list))
                    index[cat] = list = new List<string>();
                list.Add(area.Id);
            }
        return index;
    }

    private static string ComputeHash(string content)
    {
        var bytes = SHA256.HashData(Encoding.UTF8.GetBytes(content));
        return Convert.ToHexString(bytes);
    }

    private static string ToSafeFileName(string value)
    {
        var safeCharacters = value
            .Select(character => char.IsLetterOrDigit(character) || character is '-' or '_' ? character : '-')
            .ToArray();
        return new string(safeCharacters).Trim('-').ToLowerInvariant();
    }

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        Converters = { new System.Text.Json.Serialization.JsonStringEnumConverter(JsonNamingPolicy.CamelCase) }
    };

    private static async Task RecordImportRunStartAsync(SqliteConnection connection, string runId, CancellationToken cancellationToken)
    {
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "INSERT INTO import_runs (id, started_at, status) VALUES (@id, @now, 'Running');";
        cmd.Parameters.AddWithValue("@id", runId);
        cmd.Parameters.AddWithValue("@now", DateTimeOffset.UtcNow.ToString("O"));
        await cmd.ExecuteNonQueryAsync(cancellationToken);
    }

    private static async Task RecordImportRunEndAsync(SqliteConnection connection, string runId, string status, CancellationToken cancellationToken)
    {
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = "UPDATE import_runs SET finished_at = @now, status = @status WHERE id = @id;";
        cmd.Parameters.AddWithValue("@id", runId);
        cmd.Parameters.AddWithValue("@now", DateTimeOffset.UtcNow.ToString("O"));
        cmd.Parameters.AddWithValue("@status", status);
        await cmd.ExecuteNonQueryAsync(cancellationToken);
    }

    private static async Task InsertDiagnosticAsync(SqliteConnection connection, string runId, string? path, string? assessmentId, string severity, string code, string message, int? line, int? column, string? actualKey, string? suggestedKey, CancellationToken cancellationToken)
    {
        await using var cmd = connection.CreateCommand();
        cmd.CommandText = """
            INSERT INTO import_diagnostics (id, run_id, path, assessment_id, severity, code, message, line, column, actual_key, suggested_key)
            VALUES (@id, @runId, @path, @assessmentId, @severity, @code, @message, @line, @column, @actualKey, @suggestedKey);
            """;
        cmd.Parameters.AddWithValue("@id", Guid.NewGuid().ToString("N"));
        cmd.Parameters.AddWithValue("@runId", runId);
        cmd.Parameters.AddWithValue("@path", path ?? (object)DBNull.Value);
        cmd.Parameters.AddWithValue("@assessmentId", assessmentId ?? (object)DBNull.Value);
        cmd.Parameters.AddWithValue("@severity", severity);
        cmd.Parameters.AddWithValue("@code", code);
        cmd.Parameters.AddWithValue("@message", message);
        cmd.Parameters.AddWithValue("@line", line ?? (object)DBNull.Value);
        cmd.Parameters.AddWithValue("@column", column ?? (object)DBNull.Value);
        cmd.Parameters.AddWithValue("@actualKey", actualKey ?? (object)DBNull.Value);
        cmd.Parameters.AddWithValue("@suggestedKey", suggestedKey ?? (object)DBNull.Value);
        await cmd.ExecuteNonQueryAsync(cancellationToken);
    }
}
