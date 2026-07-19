namespace QuizApp.Core.Domain;

public enum SourceReviewState
{
    Draft,
    NeedsReview,
    Approved,
    Quarantined,
    Superseded
}

public sealed record SourceImportRequest(string LocalPath, string? Title, string? LicenseNote);

public sealed record SourceChunk(
    string Id,
    int Ordinal,
    string Kind,
    string Locator,
    string Text,
    int TokenCount,
    decimal? OcrConfidence = null);

public sealed record SourceManifest(
    int SchemaVersion,
    string Id,
    string Title,
    string OriginalFileName,
    string Format,
    string Sha256,
    string LicenseNote,
    string Extractor,
    string ExtractionStatus,
    IReadOnlyList<string> Warnings,
    DateTimeOffset ImportedAt,
    int ChunkCount,
    SourceReviewState ReviewState);

public sealed record SourceDocument(SourceManifest Manifest, IReadOnlyList<SourceChunk> Chunks);

public sealed record SourceSearchResult(
    string SourceId,
    string SourceTitle,
    SourceChunk Chunk,
    string LicenseNote);

public sealed record CurriculumObjective(
    string Id,
    string Title,
    IReadOnlyList<string> PrerequisiteIds,
    IReadOnlyList<string> RequiredActivities,
    IReadOnlyList<string> SourceIds);

public sealed record CurriculumManifest(
    int SchemaVersion,
    string Id,
    string CategoryId,
    string AreaId,
    string Title,
    IReadOnlyList<CurriculumObjective> Objectives,
    SourceReviewState ReviewState);

public sealed record QuestionBlueprint(
    int SchemaVersion,
    string Id,
    string CategoryId,
    string TopicId,
    string ObjectiveId,
    string QuestionType,
    IReadOnlyList<string> SourceChunkIds,
    IReadOnlyList<string> GoverningPrinciples,
    IReadOnlyList<string> MethodSteps,
    IReadOnlyList<string> VariationAxes,
    string CommonTrap,
    string Difficulty,
    int ReasoningDepth,
    bool RequiresDiagram,
    SourceReviewState ReviewState);

public sealed record ContentManifest(
    int SchemaVersion,
    string Id,
    string CategoryId,
    string TopicId,
    string ObjectiveId,
    string ArtifactType,
    IReadOnlyList<string> SourceChunkIds,
    bool RequiresVisual,
    SourceReviewState ReviewState);

public sealed record AuthoringPacket(
    int SchemaVersion,
    string Id,
    string CategoryId,
    string TopicId,
    IReadOnlyList<string> ObjectiveIds,
    IReadOnlyList<SourceManifest> Sources,
    IReadOnlyList<SourceChunk> Chunks,
    IReadOnlyList<string> RequiredArtifacts,
    string OutputContract);

public sealed record AuthoringDraft(
    string Id,
    string PacketId,
    SourceReviewState ReviewState,
    DateTimeOffset ImportedAt,
    string PayloadJson,
    IReadOnlyList<string> Diagnostics);

public sealed record AuthoringCoverageRow(
    string CategoryId,
    string AreaId,
    string ObjectiveId,
    int ApprovedContentCount,
    int ApprovedBlueprintCount,
    bool MeetsContentRequirement,
    bool MeetsPracticeRequirement);
