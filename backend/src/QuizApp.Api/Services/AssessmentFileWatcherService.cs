using System.Collections.Concurrent;
using System.IO;
using Microsoft.AspNetCore.SignalR;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using QuizApp.Api.Hubs;
using QuizApp.Infrastructure.Files;
using QuizApp.Infrastructure.Retention;

namespace QuizApp.Api.Services;

public sealed class AssessmentFileWatcherService : BackgroundService
{
    private readonly FileStorageOptions storageOptions;
    private readonly SqliteAssessmentCatalogImporter importer;
    private readonly IHubContext<DiagnosticHub> diagnosticHub;
    private readonly ILogger<AssessmentFileWatcherService> logger;
    private FileSystemWatcher? watcher;
    private readonly ConcurrentDictionary<string, CancellationTokenSource> debouncers = new(StringComparer.OrdinalIgnoreCase);

    public AssessmentFileWatcherService(
        FileStorageOptions storageOptions,
        SqliteAssessmentCatalogImporter importer,
        IHubContext<DiagnosticHub> diagnosticHub,
        ILogger<AssessmentFileWatcherService> logger)
    {
        this.storageOptions = storageOptions;
        this.importer = importer;
        this.diagnosticHub = diagnosticHub;
        this.logger = logger;
    }

    protected override Task ExecuteAsync(CancellationToken stoppingToken)
    {
        if (!Directory.Exists(storageOptions.AssessmentsPath))
        {
            logger.LogWarning("Assessments directory does not exist, file watcher will not start.");
            return Task.CompletedTask;
        }

        watcher = new FileSystemWatcher(storageOptions.AssessmentsPath, "*.yaml")
        {
            NotifyFilter = NotifyFilters.LastWrite | NotifyFilters.FileName | NotifyFilters.DirectoryName | NotifyFilters.CreationTime,
            IncludeSubdirectories = true,
            EnableRaisingEvents = true
        };

        watcher.Changed += OnFileChanged;
        watcher.Created += OnFileChanged;
        watcher.Renamed += OnFileChanged;
        watcher.Deleted += OnFileDeleted;

        logger.LogInformation("Started watching for assessment file changes in {Path}", storageOptions.AssessmentsPath);

        return Task.CompletedTask;
    }

    private void OnFileChanged(object sender, FileSystemEventArgs e)
    {
        if (e.ChangeType == WatcherChangeTypes.Deleted) return; // Handled by OnFileDeleted
        DebounceAndProcess(e.FullPath, e.ChangeType);
    }

    private void OnFileDeleted(object sender, FileSystemEventArgs e)
    {
        DebounceAndProcess(e.FullPath, WatcherChangeTypes.Deleted);
    }

    private void DebounceAndProcess(string fullPath, WatcherChangeTypes changeType)
    {
        // Cancel existing timer for this file
        if (debouncers.TryGetValue(fullPath, out var existingCts))
        {
            existingCts.Cancel();
            existingCts.Dispose();
        }

        var cts = new CancellationTokenSource();
        debouncers[fullPath] = cts;

        _ = Task.Run(async () =>
        {
            try
            {
                await Task.Delay(300, cts.Token); // 300ms debounce

                debouncers.TryRemove(fullPath, out _);

                if (changeType == WatcherChangeTypes.Deleted)
                {
                    logger.LogInformation("File deleted: {Path}, removing from catalog...", fullPath);
                    var removed = await importer.RemoveHotReloadedFileAsync(fullPath, CancellationToken.None);
                    if (removed)
                    {
                        await diagnosticHub.Clients.All.SendAsync("AssessmentDeleted", fullPath);
                    }
                }
                else
                {
                    logger.LogInformation("File changed: {Path}, attempting hot reload...", fullPath);
                    var result = await importer.TryHotReloadFileAsync(fullPath, CancellationToken.None);
                    
                    if (result.Success)
                    {
                        await diagnosticHub.Clients.All.SendAsync("AssessmentUpdated", new { AssessmentId = result.AssessmentId, Path = fullPath });
                    }
                    else
                    {
                        await diagnosticHub.Clients.All.SendAsync("AssessmentError", new { AssessmentId = result.AssessmentId, Path = fullPath, Error = result.ErrorMessage });
                        logger.LogWarning("Hot reload failed for {Path}: {Error}", fullPath, result.ErrorMessage);
                    }
                }
            }
            catch (TaskCanceledException)
            {
                // Expected when debouncing
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Error processing file change for {Path}", fullPath);
            }
        }, cts.Token);
    }

    public override void Dispose()
    {
        watcher?.Dispose();
        foreach (var cts in debouncers.Values)
        {
            cts.Cancel();
            cts.Dispose();
        }
        base.Dispose();
    }
}
