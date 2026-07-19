using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public interface IAuthoringWorkspaceService
{
    Task<IReadOnlyList<SourceManifest>> ListSourcesAsync(CancellationToken cancellationToken = default);
    Task<SourceDocument?> GetSourceAsync(string sourceId, CancellationToken cancellationToken = default);
    Task<SourceDocument> ImportSourceAsync(SourceImportRequest request, CancellationToken cancellationToken = default);
    Task<SourceDocument> RetryExtractionAsync(string sourceId, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<SourceSearchResult>> SearchSourcesAsync(string query, int limit, CancellationToken cancellationToken = default);
    Task SaveCurriculumAsync(CurriculumManifest manifest, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<CurriculumManifest>> ListCurriculumsAsync(CancellationToken cancellationToken = default);
    Task SaveContentManifestAsync(ContentManifest manifest, CancellationToken cancellationToken = default);
    Task SaveBlueprintAsync(QuestionBlueprint blueprint, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<QuestionBlueprint>> ListBlueprintsAsync(string? categoryId, CancellationToken cancellationToken = default);
    Task<AuthoringPacket> ExportPacketAsync(string categoryId, string topicId, IReadOnlyList<string> objectiveIds, IReadOnlyList<string> chunkIds, CancellationToken cancellationToken = default);
    Task<AuthoringDraft> ImportDraftAsync(string packetId, string payloadJson, CancellationToken cancellationToken = default);
    Task<AuthoringDraft> SetDraftStateAsync(string draftId, SourceReviewState state, CancellationToken cancellationToken = default);
    Task<IReadOnlyList<AuthoringDraft>> ListDraftsAsync(CancellationToken cancellationToken = default);
    Task<IReadOnlyList<AuthoringCoverageRow>> GetCoverageAsync(string? categoryId, CancellationToken cancellationToken = default);
}
