using Microsoft.Data.Sqlite;
using QuizApp.Core.Repositories;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Retention;

namespace QuizApp.Api.Services;

public class PassiveAnalyzerBackgroundService : BackgroundService
{
    private readonly IServiceProvider serviceProvider;
    private readonly ILogger<PassiveAnalyzerBackgroundService> logger;
    private readonly TimeSpan checkInterval = TimeSpan.FromMinutes(15);

    public PassiveAnalyzerBackgroundService(
        IServiceProvider serviceProvider,
        ILogger<PassiveAnalyzerBackgroundService> logger)
    {
        this.serviceProvider = serviceProvider;
        this.logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        logger.LogInformation("Passive Analyzer Background Service is starting.");

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await ProcessPendingAssessmentsAsync(stoppingToken);
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "An error occurred while processing passive assessment analysis.");
            }

            await Task.Delay(checkInterval, stoppingToken);
        }
    }

    private async Task ProcessPendingAssessmentsAsync(CancellationToken cancellationToken)
    {
        using var scope = serviceProvider.CreateScope();
        var retentionOptions = scope.ServiceProvider.GetRequiredService<SqliteRetentionOptions>();
        var repository = scope.ServiceProvider.GetRequiredService<IAssessmentRepository>();
        var analyzer = scope.ServiceProvider.GetRequiredService<ILocalAssessmentAnalyzer>();

        var factory = new SqliteConnectionFactory(retentionOptions);
        
        var pendingIds = new List<string>();
        
        try
        {
            await using var connection = factory.CreateConnection();
            await connection.OpenAsync(cancellationToken);
            await using var cmd = connection.CreateCommand();
            cmd.CommandText = "SELECT id FROM assessments WHERE metadata_status = 0 AND is_active = 1;";
            await using var reader = await cmd.ExecuteReaderAsync(cancellationToken);
            while (await reader.ReadAsync(cancellationToken))
            {
                pendingIds.Add(reader.GetString(0));
            }
        }
        catch (Exception ex)
        {
            logger.LogWarning(ex, "Could not query pending assessments from catalog.");
            return;
        }

        if (pendingIds.Count > 0)
        {
            logger.LogInformation("Found {Count} assessments requiring metadata analysis.", pendingIds.Count);
        }

        foreach (var id in pendingIds)
        {
            cancellationToken.ThrowIfCancellationRequested();

            try
            {
                var assessment = await repository.GetByIdAsync(id, cancellationToken);
                if (assessment == null) continue;

                var analyzed = await analyzer.AnalyzeAsync(assessment, cancellationToken);
                
                // Save back to repository (which writes to YAML and updates SQLite)
                await repository.SaveAsync(analyzed, cancellationToken);
                
                logger.LogInformation("Successfully analyzed and saved assessment: {Id}", id);
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Error analyzing assessment {Id}", id);
            }
        }
    }
}
