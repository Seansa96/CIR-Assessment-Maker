using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public interface IAuthoringWorkspaceService
{
    Task<IReadOnlyList<SourceManifest>> ListSourcesAsync(CancellationToken cancellationToken = default);
    Task<SourceDocument?> GetSourceAsync(string sourceId, CancellationToken cancellationToken = default);
    Task<SourceDocument> ImportSourceAsync(SourceImportRequest request, CancellationToken cancellationToken = default);
    Task<SourceDocument> RetryExtractionAsync(string sourceId, CancellationToken cancellationToken = default);
    Task<SourceDocument> RenderPdfPagesAsync(string sourceId, SourcePageRenderRequest request, CancellationToken cancellationToken = default);
    Task<SourceDocument> UpdatePageTranscriptionAsync(string sourceId, string chunkId, SourceTranscriptionUpdate update, CancellationToken cancellationToken = default);
    Task<(string Path, string ContentType)?> GetPageImageAsync(string sourceId, string chunkId, CancellationToken cancellationToken = default);
    Task<SourceOutline?> GetOutlineAsync(string sourceId, CancellationToken cancellationToken = default);
    Task<SourceOutline> RebuildOutlineAsync(string sourceId, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<SourceSearchResult>> SearchSourcesAsync(string query, int limit, CancellationToken cancellationToken = default);
    Task SaveCurriculumAsync(CurriculumManifest manifest, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<CurriculumManifest>> ListCurriculumsAsync(CancellationToken cancellationToken = default);
    Task SaveContentManifestAsync(ContentManifest manifest, CancellationToken cancellationToken = default);
    Task SaveBlueprintAsync(QuestionBlueprint blueprint, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<QuestionBlueprint>> ListBlueprintsAsync(string? categoryId, CancellationToken cancellationToken = default);
    Task<AuthoringPacket> ExportPacketAsync(string categoryId, string topicId, IReadOnlyList<string> objectiveIds, IReadOnlyList<string> chunkIds, IReadOnlyList<string>? outlineNodeIds = null, AssessmentDifficultyTier targetDifficultyTier = AssessmentDifficultyTier.Unspecified, CancellationToken cancellationToken = default);
    Task<AuthoringDraft> ImportDraftAsync(string packetId, string payloadJson, CancellationToken cancellationToken = default);
    Task<AuthoringDraft> SetDraftStateAsync(string draftId, SourceReviewState state, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<AuthoringDraft>> ListDraftsAsync(CancellationToken cancellationToken = default);
    Task<IReadOnlyList<AuthoringCoverageRow>> GetCoverageAsync(string? categoryId, CancellationToken cancellationToken = default);
}
