using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Microsoft.Data.Sqlite;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Infrastructure.Retention;

/// <summary>
/// Idempotent, hash-based importer that syncs YAML/JSON assessment files into the SQLite catalog.
/// Skips unchanged files, upserts changed/new ones, marks missing ones inactive.
/// </summary>
public sealed class SqliteAssessmentCatalogImporter
{
    private readonly SqliteRetentionOptions retentionOptions;
    private readonly FileStorageOptions storageOptions;
    private readonly IAreaRepository areaRepository;
    private readonly AssessmentValidator validator;

    public bool CatalogInitialized { get; private set; }

    public SqliteAssessmentCatalogImporter(
        SqliteRetentionOptions retentionOptions,
        FileStorageOptions storageOptions,
        IAreaRepository areaRepository,
        AssessmentValidator validator)
    {
        this.retentionOptions = retentionOptions;
        this.storageOptions = storageOptions;
        this.areaRepository = areaRepository;
        this.validator = validator;
    }

    public async Task ImportAsync(CancellationToken cancellationToken = default)
    {
        try
        {
            var factory = new SqliteConnectionFactory(retentionOptions);
            var areas = await areaRepository.ListAsync(cancellationToken);
            var areasBySubcategory = BuildSubcategoryToAreaIndex(areas);
            var areasByCategory = BuildCategoryToAreaIndex(areas);

            var files = EnumerateAssessmentFiles().ToList();
            var seenIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

            await using var connection = factory.CreateConnection();
            await connection.OpenAsync(cancellationToken);

            foreach (var path in files)
            {
                try
                {
                    await ImportFileAsync(connection, path, areasBySubcategory, areasByCategory, seenIds, cancellationToken);
                }
                catch (Exception ex)
                {
                    var existingId = await GetIdByPathAsync(connection, path, cancellationToken);
                    if (existingId is not null) seenIds.Add(existingId);
                    Console.Error.WriteLine($"[CatalogImporter] Skipping invalid assessment file: {path}. {ex.Message}");
                }
            }

            // Mark assessments whose source files no longer exist as inactive
            await MarkMissingInactiveAsync(connection, seenIds, cancellationToken);

            CatalogInitialized = true;
            Console.WriteLine($"[CatalogImporter] Import complete. {files.Count} files processed.");
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"[CatalogImporter] Import failed; falling back to file repository. {ex.Message}");
            CatalogInitialized = false;
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
            var path = Path.Combine(storageOptions.AssessmentsPath, $"{ToSafeFileName(assessment.Id)}.yaml");
            var content = await File.ReadAllTextAsync(path, cancellationToken);
            var areas = await areaRepository.ListAsync(cancellationToken);
            var nav = NavigationInference.Infer(assessment);
            var resolvedAreas = ResolveAreas(
                assessment,
                BuildSubcategoryToAreaIndex(areas),
                BuildCategoryToAreaIndex(areas));

            await using var connection = new SqliteConnectionFactory(retentionOptions).CreateConnection();
            await connection.OpenAsync(cancellationToken);
            await UpsertAssessmentAsync(
                connection,
                assessment,
                nav,
                resolvedAreas,
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
        string path,
        Dictionary<string, List<string>> areasBySubcategory,
        Dictionary<string, List<string>> areasByCategory,
        HashSet<string> seenIds,
        CancellationToken cancellationToken)
    {
        var content = await File.ReadAllTextAsync(path, cancellationToken);
        var hash = ComputeHash(content);
        var existingId = await GetIdByPathAsync(connection, path, cancellationToken);

        // Check if unchanged
        var existingHash = await GetExistingHashAsync(connection, path, cancellationToken);
        if (existingHash == hash)
        {
            if (existingId is not null)
                seenIds.Add(existingId);
            return;
        }

        var dto = FileFormat.ReadFromString<AssessmentFileDto>(content, Path.GetExtension(path));
        if (dto is null || string.IsNullOrWhiteSpace(dto.Id))
        {
            if (existingId is not null) seenIds.Add(existingId);
            Console.Error.WriteLine($"[CatalogImporter] Assessment file has no ID, skipping: {path}");
            return;
        }

        var domain = dto.ToDomain();
        var validation = validator.Validate(domain);
        if (!validation.IsValid)
        {
            if (existingId is not null) seenIds.Add(existingId);
            Console.Error.WriteLine(
                $"[CatalogImporter] Assessment '{domain.Id}' is invalid; keeping the last valid catalog version. "
                + string.Join("; ", validation.Issues.Select(issue => issue.Message)));
            return;
        }

        if (seenIds.Contains(domain.Id))
        {
            Console.Error.WriteLine($"[CatalogImporter] Duplicate assessment ID '{domain.Id}' in '{path}', skipping later file.");
            return;
        }

        var nav = NavigationInference.Infer(domain);

        var resolvedAreas = ResolveAreas(domain, areasBySubcategory, areasByCategory);
        var definitionJson = JsonSerializer.Serialize(domain, JsonOptions);
        var now = DateTimeOffset.UtcNow.ToString("O");

        seenIds.Add(domain.Id);

        await UpsertAssessmentAsync(connection, domain, nav, resolvedAreas, definitionJson, path, hash, now, cancellationToken);
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
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };
}
