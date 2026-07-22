using System.Diagnostics;
using System.IO.Compression;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Text.RegularExpressions;
using System.Xml.Linq;
using Microsoft.Data.Sqlite;
using QuizApp.Core.Domain;
using QuizApp.Core.Services;

namespace QuizApp.Infrastructure.Files;

/// <summary>
/// Local-first source library. Raw source text never leaves SourceLibraryPath;
/// only IDs and source locations are permitted in tracked manifests.
/// </summary>
public sealed class FileAuthoringWorkspaceService : IAuthoringWorkspaceService
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        WriteIndented = true,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        Converters = { new JsonStringEnumConverter(JsonNamingPolicy.CamelCase) }
    };
    private static readonly Regex Words = new(@"[\p{L}\p{N}_-]+", RegexOptions.Compiled);
    private static readonly Regex PdfLiteral = new(@"\((?<text>(?:\\.|[^\\)])*)\)", RegexOptions.Compiled);
    private readonly FileStorageOptions options;
    private readonly SemaphoreSlim gate = new(1, 1);

    public FileAuthoringWorkspaceService(FileStorageOptions options) => this.options = options;

    private string SourcesPath => Path.Combine(options.SourceLibraryPath, "sources");
    private string DraftsPath => Path.Combine(options.SourceLibraryPath, "drafts");
    private string CurriculumPath => Path.Combine(options.AssessmentReferencePath, "curriculum-manifests");
    private string ContentPath => Path.Combine(options.AssessmentReferencePath, "content-manifests");
    private string BlueprintPath => Path.Combine(options.AssessmentReferencePath, "question-blueprints");
    private string OutlinePath(string sourceId) => Path.Combine(SourcePath(sourceId), "outline.json");

    public async Task<IReadOnlyList<SourceManifest>> ListSourcesAsync(CancellationToken cancellationToken = default)
    {
        if (!Directory.Exists(SourcesPath)) return [];
        var manifests = new List<SourceManifest>();
        foreach (var file in Directory.EnumerateFiles(SourcesPath, "manifest.json", SearchOption.AllDirectories))
        {
            var manifest = await ReadAsync<SourceManifest>(file, cancellationToken);
            if (manifest is not null) manifests.Add(manifest);
        }
        return manifests.OrderByDescending(item => item.ImportedAt).ToList();
    }

    public async Task<SourceDocument?> GetSourceAsync(string sourceId, CancellationToken cancellationToken = default)
    {
        var path = SourcePath(sourceId);
        var manifest = await ReadAsync<SourceManifest>(Path.Combine(path, "manifest.json"), cancellationToken);
        if (manifest is null) return null;
        return new SourceDocument(manifest, await ReadAsync<List<SourceChunk>>(Path.Combine(path, "chunks.json"), cancellationToken) ?? []);
    }

    public async Task<SourceDocument> ImportSourceAsync(SourceImportRequest request, CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(request.LocalPath) || !File.Exists(request.LocalPath))
            throw new InvalidOperationException("The selected local source file was not found.");
        var fullPath = Path.GetFullPath(request.LocalPath);
        var format = Path.GetExtension(fullPath).TrimStart('.').ToLowerInvariant();
        if (format is not ("pdf" or "epub" or "docx" or "md" or "markdown" or "txt" or "png" or "jpg" or "jpeg" or "webp"))
            throw new InvalidOperationException("Supported formats are PDF, EPUB, DOCX, Markdown/text, PNG, JPG/JPEG, and WebP.");

        var sha = await HashAsync(fullPath, cancellationToken);
        var existing = (await ListSourcesAsync(cancellationToken)).FirstOrDefault(item => item.Sha256 == sha);
        if (existing is not null) return (await GetSourceAsync(existing.Id, cancellationToken))!;

        var id = $"src-{DateTimeOffset.UtcNow:yyyyMMddHHmmss}-{sha[..10]}";
        await gate.WaitAsync(cancellationToken);
        try
        {
            var destination = SourcePath(id);
            Directory.CreateDirectory(destination);
            var originalName = Path.GetFileName(fullPath);
            await using (var input = File.OpenRead(fullPath))
            await using (var output = File.Create(Path.Combine(destination, $"original.{format}")))
                await input.CopyToAsync(output, cancellationToken);

            var extraction = await ExtractAsync(Path.Combine(destination, $"original.{format}"), format, cancellationToken);
            var chunks = Chunk(id, extraction.Text, extraction.Confidence);
            var manifest = new SourceManifest(1, id, request.Title?.Trim() is { Length: > 0 } title ? title : Path.GetFileNameWithoutExtension(originalName), originalName, format, sha,
                string.IsNullOrWhiteSpace(request.LicenseNote) ? "Reuse terms not recorded; review before external distribution." : request.LicenseNote.Trim(),
                extraction.Extractor, extraction.Success ? "completed" : "needs-attention", extraction.Warnings, DateTimeOffset.UtcNow, chunks.Count, SourceReviewState.Draft);
            await WriteAsync(Path.Combine(destination, "manifest.json"), manifest, cancellationToken);
            await WriteAsync(Path.Combine(destination, "chunks.json"), chunks, cancellationToken);
            await IndexSourceAsync(manifest, cancellationToken);
            await WriteAsync(OutlinePath(id), BuildOutline(id, chunks), cancellationToken);
            return new SourceDocument(manifest, chunks);
        }
        finally { gate.Release(); }
    }

    public async Task<SourceDocument> RetryExtractionAsync(string sourceId, CancellationToken cancellationToken = default)
    {
        var current = await GetSourceAsync(sourceId, cancellationToken) ?? throw new InvalidOperationException("Source was not found.");
        var original = Directory.EnumerateFiles(SourcePath(sourceId), "original.*").SingleOrDefault() ?? throw new InvalidOperationException("Original source file is missing.");
        var extraction = await ExtractAsync(original, current.Manifest.Format, cancellationToken);
        var chunks = Chunk(sourceId, extraction.Text, extraction.Confidence);
        var manifest = current.Manifest with { Extractor = extraction.Extractor, ExtractionStatus = extraction.Success ? "completed" : "needs-attention", Warnings = extraction.Warnings, ChunkCount = chunks.Count };
        await WriteAsync(Path.Combine(SourcePath(sourceId), "manifest.json"), manifest, cancellationToken);
        await WriteAsync(Path.Combine(SourcePath(sourceId), "chunks.json"), chunks, cancellationToken);
        await IndexSourceAsync(manifest, cancellationToken);
        await WriteAsync(OutlinePath(sourceId), BuildOutline(sourceId, chunks), cancellationToken);
        return new SourceDocument(manifest, chunks);
    }

    public Task<SourceOutline?> GetOutlineAsync(string sourceId, CancellationToken cancellationToken = default)
        => ReadAsync<SourceOutline>(OutlinePath(sourceId), cancellationToken);

    public async Task<SourceOutline> RebuildOutlineAsync(string sourceId, CancellationToken cancellationToken = default)
    {
        var source = await GetSourceAsync(sourceId, cancellationToken) ?? throw new InvalidOperationException("Source was not found.");
        var outline = BuildOutline(sourceId, source.Chunks);
        await WriteAsync(OutlinePath(sourceId), outline, cancellationToken);
        return outline;
    }

    public async Task<IReadOnlyList<SourceSearchResult>> SearchSourcesAsync(string query, int limit, CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(query)) return [];
        var needle = query.Trim();
        var results = new List<SourceSearchResult>();
        foreach (var source in await ListSourcesAsync(cancellationToken))
        {
            var document = await GetSourceAsync(source.Id, cancellationToken);
            if (document is null) continue;
            results.AddRange(document.Chunks.Where(chunk => chunk.Text.Contains(needle, StringComparison.OrdinalIgnoreCase))
                .Select(chunk => new SourceSearchResult(source.Id, source.Title, chunk, source.LicenseNote)));
        }
        return results.Take(Math.Clamp(limit, 1, 100)).ToList();
    }

    public async Task SaveCurriculumAsync(CurriculumManifest manifest, CancellationToken cancellationToken = default)
    {
        RequireStableId(manifest.Id); RequireStableId(manifest.CategoryId); RequireStableId(manifest.AreaId);
        if (manifest.Objectives.Count == 0 || manifest.Objectives.Any(item => string.IsNullOrWhiteSpace(item.Id) || string.IsNullOrWhiteSpace(item.Title))) throw new InvalidOperationException("A curriculum needs at least one complete objective.");
        if (manifest.Objectives.Select(item => item.Id).Distinct(StringComparer.OrdinalIgnoreCase).Count() != manifest.Objectives.Count) throw new InvalidOperationException("Curriculum objective IDs must be unique.");
        await WriteTrackedAsync(Path.Combine(CurriculumPath, $"{manifest.Id}.json"), manifest, cancellationToken);
    }
    public async Task<IReadOnlyList<CurriculumManifest>> ListCurriculumsAsync(CancellationToken cancellationToken = default)
        => await ReadDirectoryAsync<CurriculumManifest>(CurriculumPath, cancellationToken);

    public async Task SaveContentManifestAsync(ContentManifest manifest, CancellationToken cancellationToken = default)
    {
        RequireStableId(manifest.Id); ValidateSourceFree(manifest.SourceChunkIds, manifest.CategoryId, manifest.TopicId, manifest.ObjectiveId);
        if (manifest.RequiresVisual && manifest.ArtifactType is not ("conceptLesson" or "workedExample")) throw new InvalidOperationException("Only instructional artifacts may require a visual brief.");
        await ValidateSourceReferencesAsync(manifest.SourceChunkIds, cancellationToken);
        await WriteTrackedAsync(Path.Combine(ContentPath, $"{manifest.Id}.json"), manifest, cancellationToken);
    }
    public async Task SaveBlueprintAsync(QuestionBlueprint blueprint, CancellationToken cancellationToken = default)
    {
        RequireStableId(blueprint.Id); ValidateSourceFree(blueprint.SourceChunkIds, blueprint.CategoryId, blueprint.TopicId, blueprint.ObjectiveId);
        if (blueprint.GoverningPrinciples.Count == 0 || blueprint.MethodSteps.Count < 2 || blueprint.VariationAxes.Count < 2) throw new InvalidOperationException("Blueprints need principles, at least two method steps, and two meaningful variation axes.");
        if (blueprint.ExplanationOutline.Count < 2) throw new InvalidOperationException("Blueprints need an explanation outline with Solution and Why it works components.");
        if (blueprint.QuestionType is "multipleChoice" or "selectAll" && blueprint.DistractorRationale.Count == 0) throw new InvalidOperationException("Multiple-choice blueprints need distractor rationale.");
        var tier = ParseDifficultyTier(blueprint.Difficulty);
        var minimum = AssessmentAuthoringContractAudit.MinimumDifficultyDimensions(tier);
        if (minimum > 0)
        {
            if (blueprint.DifficultyDimensions.Count == 0 || blueprint.DifficultyDimensions.Any(dimension => dimension is DifficultyDimension.Unknown)) throw new InvalidOperationException("Blueprints for scored tiers need controlled difficulty dimensions.");
            if (blueprint.DifficultyDimensions.Distinct().Count() != blueprint.DifficultyDimensions.Count) throw new InvalidOperationException("A difficulty dimension may be counted only once per blueprint.");
            if (blueprint.DifficultyDimensions.Count < minimum) throw new InvalidOperationException($"{tier} blueprints need at least {minimum} distinct difficulty dimensions.");
            if (string.IsNullOrWhiteSpace(blueprint.DifficultyEvidence)) throw new InvalidOperationException("Blueprints need difficulty evidence for every declared difficulty dimension.");
            if (tier is AssessmentDifficultyTier.Hard && blueprint.PrerequisiteObjectiveIds.Count == 0 && blueprint.ExtensionObjectiveIds.Count == 0) throw new InvalidOperationException("Hard blueprints need a prerequisite or extension objective.");
            if (tier is AssessmentDifficultyTier.Olympiad && blueprint.ExtensionObjectiveIds.Count == 0) throw new InvalidOperationException("Olympiad blueprints need an extension objective.");
            if (tier is AssessmentDifficultyTier.Olympiad && (blueprint.OlympiadPrerequisites.Count == 0 || blueprint.FurtherStudy.Count == 0)) throw new InvalidOperationException("Olympiad blueprints need prerequisite and further-study guidance.");
        }
        if (blueprint.RequiresDiagram && blueprint.QuestionType is not ("numericResponse" or "symbolicResponse" or "multipleChoice" or "selectAll")) throw new InvalidOperationException("Diagram-backed blueprints must use a supported graded question type.");
        await ValidateSourceReferencesAsync(blueprint.SourceChunkIds, cancellationToken);
        await WriteTrackedAsync(Path.Combine(BlueprintPath, $"{blueprint.Id}.json"), blueprint, cancellationToken);
    }
    public async Task<IReadOnlyList<QuestionBlueprint>> ListBlueprintsAsync(string? categoryId, CancellationToken cancellationToken = default)
        => (await ReadDirectoryAsync<QuestionBlueprint>(BlueprintPath, cancellationToken)).Where(item => string.IsNullOrWhiteSpace(categoryId) || item.CategoryId.Equals(categoryId, StringComparison.OrdinalIgnoreCase)).ToList();

    public async Task<AuthoringPacket> ExportPacketAsync(string categoryId, string topicId, IReadOnlyList<string> objectiveIds, IReadOnlyList<string> chunkIds, IReadOnlyList<string>? outlineNodeIds = null, AssessmentDifficultyTier targetDifficultyTier = AssessmentDifficultyTier.Unspecified, CancellationToken cancellationToken = default)
    {
        if (objectiveIds.Count == 0 || (chunkIds.Count == 0 && (outlineNodeIds?.Count ?? 0) == 0)) throw new InvalidOperationException("Select at least one objective and source chunk or outline node.");
        var documents = new List<SourceDocument>();
        foreach (var source in await ListSourcesAsync(cancellationToken)) { var doc = await GetSourceAsync(source.Id, cancellationToken); if (doc is not null) documents.Add(doc); }
        var selectedChunkIds = new HashSet<string>(chunkIds, StringComparer.OrdinalIgnoreCase);
        foreach (var nodeId in outlineNodeIds ?? [])
        {
            var sourceId = nodeId.Split(':', 2)[0]; var outline = await GetOutlineAsync(sourceId, cancellationToken);
            var node = outline is null ? null : FindNode(outline.Root, nodeId);
            if (node is null) throw new InvalidOperationException($"Outline node was not found: {nodeId}.");
            foreach (var id in node.ChunkIds) selectedChunkIds.Add(id);
        }
        var chunks = documents.SelectMany(document => document.Chunks).Where(chunk => selectedChunkIds.Contains(chunk.Id)).OrderBy(chunk => chunk.Id, StringComparer.OrdinalIgnoreCase).ToList();
        if (chunks.Count != selectedChunkIds.Count) throw new InvalidOperationException("One or more selected source chunks no longer exist.");
        var sourceIds = chunks.Select(chunk => chunk.Id.Split(":", 2)[0]).Distinct(StringComparer.OrdinalIgnoreCase).ToHashSet(StringComparer.OrdinalIgnoreCase);
        var sources = documents.Where(document => sourceIds.Contains(document.Manifest.Id)).Select(document => document.Manifest).ToList();
        var category = (await new FileCategoryRepository(options).ListAsync(cancellationToken)).FirstOrDefault(item => item.Id.Equals(categoryId, StringComparison.OrdinalIgnoreCase));
        var profile = category?.AuthoringProfile is AuthoringProfile.Stem ? "stem" : "nonStem";
        var requirements = profile == "stem"
            ? new[] { "minimum seven active concept-lesson sections", "contextual original visual aids", "worked examples use symbolic/free response primarily", "easy and hard quizzes use ten attempt items; tests use twenty" }
            : new[] { "minimum seven active concept-lesson sections", "code or interface evidence when relevant", "worked examples use free response/code primarily", "easy and hard quizzes use ten attempt items; tests use twenty" };
        var minimumDifficultyDimensions = AssessmentAuthoringContractAudit.MinimumDifficultyDimensions(targetDifficultyTier);
        var tierRequirements = minimumDifficultyDimensions == 0 ? Array.Empty<string>() : new[] { $"every scored item must declare at least {minimumDifficultyDimensions} distinct difficulty dimensions", "every explanation includes Solution and Why it works", targetDifficultyTier is AssessmentDifficultyTier.Hard ? "each item names a prerequisite or extension objective" : targetDifficultyTier is AssessmentDifficultyTier.Olympiad ? "each item names an extension objective, prerequisites, and further-study guidance" : "difficulty evidence must explain each dimension" };
        return new AuthoringPacket(1, $"packet-{Guid.NewGuid():N}", categoryId, topicId, objectiveIds, sources, chunks,
            ["original source-grounded prose", "visual brief for each lesson/worked example", "complete answer and structured Solution/Why it works data", "multiple-choice distractor feedback", "question blueprints rather than parameter substitutions"],
            "Return JSON with contentManifests and questionBlueprints. Each artifact must cite sourceChunkIds and begin in needsReview state. Do not quote source text verbatim except short mathematical notation.")
        { AuthoringProfile = profile, ContractRequirements = requirements.Concat(tierRequirements).ToList(), TargetDifficultyTier = targetDifficultyTier, MinimumDifficultyDimensions = minimumDifficultyDimensions, RequiresTransferObjective = targetDifficultyTier is AssessmentDifficultyTier.Hard or AssessmentDifficultyTier.Olympiad, AllowedSubjectDifficultyTags = profile == "stem" ? ["methodBranch", "representation", "model", "constraint", "prerequisiteTransfer"] : Array.Empty<string>() };
    }

    public async Task<AuthoringDraft> ImportDraftAsync(string packetId, string payloadJson, CancellationToken cancellationToken = default)
    {
        if (string.IsNullOrWhiteSpace(packetId) || string.IsNullOrWhiteSpace(payloadJson)) throw new InvalidOperationException("Packet ID and draft JSON are required.");
        using var json = JsonDocument.Parse(payloadJson);
        if (json.RootElement.ValueKind != JsonValueKind.Object) throw new InvalidOperationException("Draft must be a JSON object.");
        var diagnostics = ValidateDraft(json.RootElement);
        var draft = new AuthoringDraft($"draft-{Guid.NewGuid():N}", packetId, SourceReviewState.NeedsReview, DateTimeOffset.UtcNow, payloadJson, diagnostics);
        Directory.CreateDirectory(DraftsPath); await WriteAsync(Path.Combine(DraftsPath, $"{draft.Id}.json"), draft, cancellationToken); return draft;
    }
    public async Task<AuthoringDraft> SetDraftStateAsync(string draftId, SourceReviewState state, CancellationToken cancellationToken = default)
    {
        var path = Path.Combine(DraftsPath, $"{draftId}.json"); var current = await ReadAsync<AuthoringDraft>(path, cancellationToken) ?? throw new InvalidOperationException("Draft was not found.");
        if (state == SourceReviewState.Approved && current.Diagnostics.Count > 0) throw new InvalidOperationException("Draft diagnostics must be resolved before approval.");
        if (state == SourceReviewState.Approved) await PublishDraftPayloadAsync(current.PayloadJson, cancellationToken);
        var updated = current with { ReviewState = state }; await WriteAsync(path, updated, cancellationToken); return updated;
    }
    public Task<IReadOnlyList<AuthoringDraft>> ListDraftsAsync(CancellationToken cancellationToken = default) => ReadDirectoryAsync<AuthoringDraft>(DraftsPath, cancellationToken);

    public async Task<IReadOnlyList<AuthoringCoverageRow>> GetCoverageAsync(string? categoryId, CancellationToken cancellationToken = default)
    {
        var curriculums = (await ListCurriculumsAsync(cancellationToken)).Where(item => string.IsNullOrWhiteSpace(categoryId) || item.CategoryId.Equals(categoryId, StringComparison.OrdinalIgnoreCase));
        var content = await ReadDirectoryAsync<ContentManifest>(ContentPath, cancellationToken); var blueprints = await ListBlueprintsAsync(categoryId, cancellationToken);
        return curriculums.SelectMany(curriculum => curriculum.Objectives.Select(objective =>
        {
            var approvedContent = content.Count(item => item.CategoryId == curriculum.CategoryId && item.ObjectiveId == objective.Id && item.ReviewState == SourceReviewState.Approved);
            var approvedBlueprints = blueprints.Count(item => item.CategoryId == curriculum.CategoryId && item.ObjectiveId == objective.Id && item.ReviewState == SourceReviewState.Approved);
            return new AuthoringCoverageRow(curriculum.CategoryId, curriculum.AreaId, objective.Id, approvedContent, approvedBlueprints, approvedContent > 0, approvedBlueprints >= 2);
        })).ToList();
    }

    private async Task<(string Text, string Extractor, bool Success, IReadOnlyList<string> Warnings, decimal? Confidence)> ExtractAsync(string path, string format, CancellationToken cancellationToken)
    {
        try
        {
            return format switch
            {
                "txt" or "md" or "markdown" => (await File.ReadAllTextAsync(path, cancellationToken), "native-text-v1", true, [], null),
                "docx" => (ExtractDocx(path), "docx-xml-v1", true, [], null),
                "epub" => (ExtractEpub(path), "epub-xhtml-v1", true, [], null),
                "pdf" => await ExtractPdfAsync(path, cancellationToken),
                _ => await ExtractImageAsync(path, cancellationToken)
            };
        }
        catch (Exception ex) { return (string.Empty, $"{format}-extractor", false, [$"Extraction failed: {ex.Message}"], null); }
    }
    private static string ExtractDocx(string path)
    {
        using var zip = ZipFile.OpenRead(path); var entry = zip.GetEntry("word/document.xml") ?? throw new InvalidOperationException("DOCX document.xml is missing.");
        using var stream = entry.Open(); var doc = XDocument.Load(stream); return string.Join("\n", doc.Descendants().Where(node => node.Name.LocalName == "p").Select(node => string.Concat(node.Descendants().Where(child => child.Name.LocalName == "t").Select(child => child.Value))));
    }
    private static string ExtractEpub(string path)
    {
        using var zip = ZipFile.OpenRead(path); var texts = new List<string>();
        foreach (var entry in zip.Entries.Where(item => item.FullName.EndsWith(".xhtml", StringComparison.OrdinalIgnoreCase) || item.FullName.EndsWith(".html", StringComparison.OrdinalIgnoreCase)))
        using (var reader = new StreamReader(entry.Open())) texts.Add(Regex.Replace(System.Net.WebUtility.HtmlDecode(Regex.Replace(reader.ReadToEnd(), "<[^>]+>", " ")), @"\s+", " "));
        return string.Join("\n\n", texts);
    }
    private static async Task<(string Text, string Extractor, bool Success, IReadOnlyList<string> Warnings, decimal? Confidence)> ExtractPdfAsync(string path, CancellationToken cancellationToken)
    {
        const string program = "from pypdf import PdfReader; import sys; reader=PdfReader(sys.argv[1]); text='\\n\\n'.join('# PAGE {}\\n{}'.format(i+1, page.extract_text() or '') for i,page in enumerate(reader.pages)); sys.stdout.buffer.write(text.encode('utf-8'))";
        try
        {
            var start = new ProcessStartInfo("python") { RedirectStandardOutput = true, RedirectStandardError = true, StandardOutputEncoding = Encoding.UTF8, UseShellExecute = false, CreateNoWindow = true };
            start.ArgumentList.Add("-c"); start.ArgumentList.Add(program); start.ArgumentList.Add(path);
            using var process = Process.Start(start) ?? throw new InvalidOperationException("Python could not start.");
            var text = await process.StandardOutput.ReadToEndAsync(cancellationToken); var error = await process.StandardError.ReadToEndAsync(cancellationToken); await process.WaitForExitAsync(cancellationToken);
            if (process.ExitCode == 0 && !string.IsNullOrWhiteSpace(text)) return (text, "pypdf-v1", true, ["PDF text is extracted page-by-page. Inspect equations and diagrams before approval."], null);
            throw new InvalidOperationException(string.IsNullOrWhiteSpace(error) ? "pypdf returned no usable text." : error);
        }
        catch (Exception ex)
        {
            var raw = Encoding.Latin1.GetString(await File.ReadAllBytesAsync(path, cancellationToken));
            var text = string.Join(" ", PdfLiteral.Matches(raw).Select(match => match.Groups["text"].Value
                .Replace("\\n", " ", StringComparison.Ordinal)
                .Replace("\\(", "(", StringComparison.Ordinal)
                .Replace("\\)", ")", StringComparison.Ordinal)
                .Replace("\\\\", "\\", StringComparison.Ordinal)));
            return string.IsNullOrWhiteSpace(text)
                ? (string.Empty, "pdf-fallback-v1", false, [$"No usable PDF text was found. pypdf diagnostic: {ex.Message}"], null)
                : (text, "pdf-literal-fallback-v1", true, [$"Used a low-fidelity PDF fallback after pypdf failed: {ex.Message}"], null);
        }
    }
    private static async Task<(string Text, string Extractor, bool Success, IReadOnlyList<string> Warnings, decimal? Confidence)> ExtractImageAsync(string path, CancellationToken cancellationToken)
    {
        try
        {
            using var process = Process.Start(new ProcessStartInfo("tesseract", $"\"{path}\" stdout --psm 3") { RedirectStandardOutput = true, RedirectStandardError = true, UseShellExecute = false, CreateNoWindow = true });
            if (process is null) throw new InvalidOperationException("Tesseract could not start."); var text = await process.StandardOutput.ReadToEndAsync(cancellationToken); var error = await process.StandardError.ReadToEndAsync(cancellationToken); await process.WaitForExitAsync(cancellationToken);
            return process.ExitCode == 0 ? (text, "tesseract-ocr", true, ["OCR output should be reviewed against the image."], 0.75m) : (string.Empty, "tesseract-ocr", false, [$"OCR failed: {error}"], null);
        }
        catch { return (string.Empty, "tesseract-ocr", false, ["Image OCR requires the local Tesseract executable. Install it and retry extraction."], null); }
    }
    private static List<SourceChunk> Chunk(string sourceId, string text, decimal? confidence)
    {
        var blocks = Regex.Split(text.Replace("\r\n", "\n"), @"\n\s*\n|(?=^#{1,6}\s)", RegexOptions.Multiline).Select(item => item.Trim()).Where(item => item.Length > 0);
        var result = new List<SourceChunk>(); int ordinal = 0;
        foreach (var block in blocks)
        {
            foreach (var segment in Split(block, 1800))
            {
                ordinal++; var kind = segment.StartsWith('#') ? "heading" : segment.Contains("?") ? "exercise-or-check" : "paragraph";
                result.Add(new SourceChunk($"{sourceId}:chunk-{ordinal:0000}", ordinal, kind, $"chunk {ordinal}", segment, Words.Matches(segment).Count, confidence));
            }
        }
        return result;
    }
    private static SourceOutline BuildOutline(string sourceId, IReadOnlyList<SourceChunk> chunks)
    {
        var chapterPattern = new Regex(@"(?:CHAP\s*TER|CHAPTER)\s+(?<number>\d+)\s+(?<title>[^\n]{3,100})", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        var sectionPattern = new Regex(@"^(?<number>\d+\.\d+)\s+(?<title>[^\n]{3,120})", RegexOptions.Multiline | RegexOptions.Compiled);
        var pagePattern = new Regex(@"#\s*PAGE\s+(?<page>\d+)", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        var candidates = chunks.Select(chunk => new { Chunk = chunk, Match = chapterPattern.Match(chunk.Text), Page = PageOf(chunk, pagePattern) }).Where(item => item.Match.Success).ToList();
        var bodyChapters = candidates.GroupBy(item => item.Match.Groups["number"].Value).Select(group => group.OrderBy(item => item.Chunk.Ordinal).Last()).OrderBy(item => item.Chunk.Ordinal).ToList();
        var warnings = candidates.Count > bodyChapters.Count ? ["Duplicate chapter headings were found; later body occurrences were selected over table-of-contents entries."] : Array.Empty<string>();
        var children = new List<SourceOutlineNode>();
        for (var index = 0; index < bodyChapters.Count; index++)
        {
            var start = bodyChapters[index].Chunk.Ordinal; var end = index + 1 < bodyChapters.Count ? bodyChapters[index + 1].Chunk.Ordinal - 1 : chunks.Count;
            var range = chunks.Where(item => item.Ordinal >= start && item.Ordinal <= end).ToList();
            var chapterNumber = bodyChapters[index].Match.Groups["number"].Value;
            var sections = sectionPattern.Matches(string.Join("\n", range.Select(item => item.Text))).Cast<Match>().ToList();
            var nodeWarnings = new List<string>(); if (range.Count == 0) nodeWarnings.Add("No contiguous chunks were detected for this chapter.");
            var reviewStart = range.FindIndex(item => Regex.IsMatch(item.Text, @"Chapter Review|Conceptual Questions|^Problems\b|Additional Problems|Challenge Problems", RegexOptions.IgnoreCase | RegexOptions.Multiline));
            var nested = new List<SourceOutlineNode>();
            foreach (var section in sections.Take(30)) nested.Add(new SourceOutlineNode($"{sourceId}:section-{section.Groups["number"].Value.Replace('.', '-')}", "section", $"{section.Groups["number"].Value} {section.Groups["title"].Value.Trim()}", PageOf(range.First(), pagePattern), PageOf(range.Last(), pagePattern), start, end, range.Select(item => item.Id).ToList(), [], 0.65m, ["Section range is inferred from heading text; inspect before narrow packet use."]));
            if (reviewStart >= 0)
            {
                var review = range.Skip(reviewStart).ToList();
                nested.Add(new SourceOutlineNode($"{sourceId}:chapter-{chapterNumber}:review", "review", "Chapter review and exercises", PageOf(review.First(), pagePattern), PageOf(review.Last(), pagePattern), review.First().Ordinal, review.Last().Ordinal, review.Select(item => item.Id).ToList(), [], 0.85m, []));
            }
            children.Add(new SourceOutlineNode($"{sourceId}:chapter-{chapterNumber}", "chapter", $"Chapter {chapterNumber}: {bodyChapters[index].Match.Groups["title"].Value.Trim()}", PageOf(range.First(), pagePattern), PageOf(range.Last(), pagePattern), start, end, range.Select(item => item.Id).ToList(), nested, nodeWarnings.Count == 0 ? 0.9m : 0.5m, nodeWarnings));
        }
        var root = new SourceOutlineNode($"{sourceId}:book", "book", "Source outline", PageOf(chunks.FirstOrDefault(), pagePattern), PageOf(chunks.LastOrDefault(), pagePattern), 1, chunks.Count, chunks.Select(item => item.Id).ToList(), children, children.Count > 0 ? 0.85m : 0.3m, children.Count > 0 ? warnings : ["No chapter headings were detected. Search and manual chunk selection remain available."]);
        return new SourceOutline(1, sourceId, root, DateTimeOffset.UtcNow, warnings);
    }
    private static int PageOf(SourceChunk? chunk, Regex pagePattern) => chunk is null ? 0 : int.TryParse(pagePattern.Match(chunk.Text).Groups["page"].Value, out var page) ? page : 0;
    private static SourceOutlineNode? FindNode(SourceOutlineNode node, string id) => node.Id.Equals(id, StringComparison.OrdinalIgnoreCase) ? node : node.Children.Select(child => FindNode(child, id)).FirstOrDefault(found => found is not null);
    private static IEnumerable<string> Split(string value, int maximum) { for (var index = 0; index < value.Length; index += maximum) yield return value[index..Math.Min(value.Length, index + maximum)]; }
    private async Task IndexSourceAsync(SourceManifest manifest, CancellationToken cancellationToken)
    {
        Directory.CreateDirectory(options.SourceLibraryPath);
        await using var connection = new SqliteConnection($"Data Source={Path.Combine(options.SourceLibraryPath, "corpus.db")};Pooling=False");
        await connection.OpenAsync(cancellationToken);
        await using (var create = connection.CreateCommand())
        {
            create.CommandText = "CREATE TABLE IF NOT EXISTS source_index (id TEXT PRIMARY KEY, title TEXT NOT NULL, format TEXT NOT NULL, sha256 TEXT NOT NULL, extraction_status TEXT NOT NULL, review_state TEXT NOT NULL, chunk_count INTEGER NOT NULL, imported_at TEXT NOT NULL);";
            await create.ExecuteNonQueryAsync(cancellationToken);
        }
        await using var command = connection.CreateCommand();
        command.CommandText = "INSERT INTO source_index (id, title, format, sha256, extraction_status, review_state, chunk_count, imported_at) VALUES (@id, @title, @format, @sha, @status, @review, @count, @at) ON CONFLICT(id) DO UPDATE SET title = excluded.title, extraction_status = excluded.extraction_status, review_state = excluded.review_state, chunk_count = excluded.chunk_count;";
        command.Parameters.AddWithValue("@id", manifest.Id); command.Parameters.AddWithValue("@title", manifest.Title); command.Parameters.AddWithValue("@format", manifest.Format); command.Parameters.AddWithValue("@sha", manifest.Sha256);
        command.Parameters.AddWithValue("@status", manifest.ExtractionStatus); command.Parameters.AddWithValue("@review", manifest.ReviewState.ToString()); command.Parameters.AddWithValue("@count", manifest.ChunkCount); command.Parameters.AddWithValue("@at", manifest.ImportedAt.ToString("O"));
        await command.ExecuteNonQueryAsync(cancellationToken);
    }
    private static async Task<string> HashAsync(string path, CancellationToken cancellationToken) { await using var stream = File.OpenRead(path); return Convert.ToHexString(await SHA256.HashDataAsync(stream, cancellationToken)).ToLowerInvariant(); }
    private string SourcePath(string sourceId) { RequireStableId(sourceId); return Path.Combine(SourcesPath, sourceId); }
    private static AssessmentDifficultyTier ParseDifficultyTier(string value) => value.Trim().ToLowerInvariant() switch
    {
        "easy" => AssessmentDifficultyTier.Easy,
        "hard" => AssessmentDifficultyTier.Hard,
        "olympiad" => AssessmentDifficultyTier.Olympiad,
        _ => AssessmentDifficultyTier.Unspecified
    };
    private static void RequireStableId(string id) { if (!Regex.IsMatch(id ?? string.Empty, "^[a-z0-9][a-z0-9-]*$")) throw new InvalidOperationException("IDs must be lowercase hyphenated values."); }
    private static void ValidateSourceFree(IReadOnlyList<string> sourceChunkIds, params string[] ids) { foreach (var id in ids) RequireStableId(id); if (sourceChunkIds.Count == 0 || sourceChunkIds.Any(id => !Regex.IsMatch(id, "^src-[a-z0-9-]+:chunk-[0-9]+$"))) throw new InvalidOperationException("Manifests must link source chunk IDs and must not embed source text."); }
    private async Task ValidateSourceReferencesAsync(IReadOnlyList<string> chunkIds, CancellationToken cancellationToken)
    {
        var valid = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var source in await ListSourcesAsync(cancellationToken))
        {
            var document = await GetSourceAsync(source.Id, cancellationToken);
            if (document is not null) valid.UnionWith(document.Chunks.Select(chunk => chunk.Id));
        }
        var missing = chunkIds.Where(id => !valid.Contains(id)).ToList();
        if (missing.Count > 0) throw new InvalidOperationException($"Manifest references missing private source chunks: {string.Join(", ", missing)}.");
    }
    private static List<string> ValidateDraft(JsonElement root)
    {
        var diagnostics = new List<string>();
        if (!root.TryGetProperty("contentManifests", out var content) && !root.TryGetProperty("questionBlueprints", out _)) diagnostics.Add("Draft contains neither contentManifests nor questionBlueprints.");
        if (root.TryGetProperty("contentManifests", out content) && content.ValueKind != JsonValueKind.Array) diagnostics.Add("contentManifests must be an array.");
        if (root.TryGetProperty("questionBlueprints", out var blueprints) && blueprints.ValueKind != JsonValueKind.Array) diagnostics.Add("questionBlueprints must be an array.");
        try
        {
            if (content.ValueKind == JsonValueKind.Array) foreach (var entry in content.EnumerateArray()) _ = entry.Deserialize<ContentManifest>(JsonOptions) ?? throw new JsonException("Invalid content manifest.");
            if (blueprints.ValueKind == JsonValueKind.Array) foreach (var entry in blueprints.EnumerateArray()) _ = entry.Deserialize<QuestionBlueprint>(JsonOptions) ?? throw new JsonException("Invalid question blueprint.");
        }
        catch (JsonException ex) { diagnostics.Add($"Draft schema error: {ex.Message}"); }
        return diagnostics;
    }
    private async Task PublishDraftPayloadAsync(string payloadJson, CancellationToken cancellationToken)
    {
        using var document = JsonDocument.Parse(payloadJson);
        if (document.RootElement.TryGetProperty("contentManifests", out var content) && content.ValueKind == JsonValueKind.Array)
            foreach (var entry in content.EnumerateArray())
                await SaveContentManifestAsync((entry.Deserialize<ContentManifest>(JsonOptions) ?? throw new InvalidOperationException("Invalid content manifest.")) with { ReviewState = SourceReviewState.Approved }, cancellationToken);
        if (document.RootElement.TryGetProperty("questionBlueprints", out var blueprints) && blueprints.ValueKind == JsonValueKind.Array)
            foreach (var entry in blueprints.EnumerateArray())
                await SaveBlueprintAsync((entry.Deserialize<QuestionBlueprint>(JsonOptions) ?? throw new InvalidOperationException("Invalid question blueprint.")) with { ReviewState = SourceReviewState.Approved }, cancellationToken);
    }
    private static async Task<T?> ReadAsync<T>(string path, CancellationToken ct)
    {
        if (!File.Exists(path)) return default;
        await using var stream = File.OpenRead(path);
        return await JsonSerializer.DeserializeAsync<T>(stream, JsonOptions, ct);
    }
    private static async Task WriteAsync<T>(string path, T value, CancellationToken ct) { Directory.CreateDirectory(Path.GetDirectoryName(path)!); await using var stream = File.Create(path); await JsonSerializer.SerializeAsync(stream, value, JsonOptions, ct); }
    private static async Task<IReadOnlyList<T>> ReadDirectoryAsync<T>(string path, CancellationToken ct) { if (!Directory.Exists(path)) return []; var output = new List<T>(); foreach (var file in Directory.EnumerateFiles(path, "*.json")) { var item = await ReadAsync<T>(file, ct); if (item is not null) output.Add(item); } return output; }
    private static Task WriteTrackedAsync<T>(string path, T value, CancellationToken ct) => WriteAsync(path, value, ct);
}
