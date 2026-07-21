using System.Collections.Concurrent;
using System.Threading.Channels;
using QuizApp.Core.Domain;
using QuizApp.Core.Services;

namespace QuizApp.Api;

public sealed record AuthoringImportJob(string Id, string Title, string State, string Stage, int? ProgressPercent, string? SourceId, string? Error, DateTimeOffset CreatedAt, DateTimeOffset? CompletedAt);

public sealed class AuthoringImportJobQueue
{
    private readonly ConcurrentDictionary<string, AuthoringImportJob> jobs = new(StringComparer.OrdinalIgnoreCase);
    private readonly Channel<(string JobId, SourceImportRequest Request)> queue = Channel.CreateUnbounded<(string, SourceImportRequest)>();

    public AuthoringImportJob Enqueue(SourceImportRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.LocalPath) || !File.Exists(request.LocalPath)) throw new InvalidOperationException("The selected local source file was not found.");
        var job = new AuthoringImportJob($"import-{Guid.NewGuid():N}", string.IsNullOrWhiteSpace(request.Title) ? Path.GetFileNameWithoutExtension(request.LocalPath) : request.Title.Trim(), "queued", "Waiting to import", 0, null, null, DateTimeOffset.UtcNow, null);
        jobs[job.Id] = job;
        queue.Writer.TryWrite((job.Id, request));
        return job;
    }
    public AuthoringImportJob? Get(string id) => jobs.TryGetValue(id, out var job) ? job : null;
    internal IAsyncEnumerable<(string JobId, SourceImportRequest Request)> ReadAllAsync(CancellationToken ct) => queue.Reader.ReadAllAsync(ct);
    internal void SetRunning(string id) => Update(id, job => job with { State = "running", Stage = "Extracting and indexing source", ProgressPercent = 10 });
    internal void SetCompleted(string id, SourceDocument source) => Update(id, job => job with { State = "completed", Stage = $"Imported {source.Manifest.ChunkCount} searchable chunks", ProgressPercent = 100, SourceId = source.Manifest.Id, CompletedAt = DateTimeOffset.UtcNow });
    internal void SetFailed(string id, Exception ex) => Update(id, job => job with { State = "failed", Stage = "Import failed", Error = ex.Message, CompletedAt = DateTimeOffset.UtcNow });
    private void Update(string id, Func<AuthoringImportJob, AuthoringImportJob> update) { if (jobs.TryGetValue(id, out var job)) jobs[id] = update(job); }
}

public sealed class AuthoringImportWorker(AuthoringImportJobQueue queue, IAuthoringWorkspaceService workspace, ILogger<AuthoringImportWorker> logger) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await foreach (var item in queue.ReadAllAsync(stoppingToken))
        {
            try { queue.SetRunning(item.JobId); queue.SetCompleted(item.JobId, await workspace.ImportSourceAsync(item.Request, stoppingToken)); }
            catch (Exception ex) { logger.LogWarning(ex, "Authoring import {JobId} failed", item.JobId); queue.SetFailed(item.JobId, ex); }
        }
    }
}
