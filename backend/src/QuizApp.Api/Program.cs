using System.Text.Json;
using System.Text.Json.Serialization;
using QuizApp.Api.Contracts;
using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.CodeRunner;
using QuizApp.Infrastructure.Files;
using QuizApp.Infrastructure.Retention;
using QuizApp.Infrastructure.SymbolicMath;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.ConfigureHttpJsonOptions(options =>
{
    options.SerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
    options.SerializerOptions.Converters.Add(new JsonStringEnumConverter(JsonNamingPolicy.CamelCase));
});

var dataRoot = Path.GetFullPath(Path.Combine(builder.Environment.ContentRootPath, "../../..", "data"));
var configuredSqlitePath = builder.Configuration["Retention:SqlitePath"];
var sqlitePath = string.IsNullOrWhiteSpace(configuredSqlitePath)
    ? Path.Combine(dataRoot, "retention", "quizapp.db")
    : Path.IsPathRooted(configuredSqlitePath)
        ? configuredSqlitePath
        : Path.GetFullPath(Path.Combine(builder.Environment.ContentRootPath, configuredSqlitePath));
builder.Services.AddSingleton<AssessmentValidator>();
builder.Services.AddSingleton<ScoringService>();
builder.Services.AddSingleton<ICodeQuestionScorer, CodeQuestionScorer>();
builder.Services.AddSingleton<ISymbolicExpressionScorer, SymbolicExpressionScorer>();
builder.Services.AddSingleton<ICircuitQuestionScorer, CircuitQuestionScorer>();
builder.Services.AddSingleton<ISymbolicMathEngine, CortexSymbolicMathEngine>();
builder.Services.AddHttpClient<ICodeRunnerClient, PistonCodeRunnerClient>();
builder.Services.AddSingleton<AttemptService>();
builder.Services.AddSingleton<GradeLogService>();
builder.Services.AddSingleton<GradeAnalyticsService>();
builder.Services.AddSingleton<IDockerCommandRunner, QuizApp.Infrastructure.CodeRunner.DockerCommandRunner>();
builder.Services.AddSingleton<IGuidedProjectRunner, LegacyHarnessGuidedProjectRunner>();
builder.Services.AddSingleton<IGuidedProjectRunner, DockerWorkspaceGuidedProjectRunner>();
builder.Services.AddSingleton<GuidedProjectService>();
builder.Services.AddSingleton(new FileStorageOptions { DataRoot = dataRoot });
builder.Services.AddSingleton(new SqliteRetentionOptions { DatabasePath = sqlitePath });
builder.Services.AddSingleton<SqliteRetentionInitializer>();
builder.Services.AddSingleton<SqliteAttemptRepository>();
builder.Services.AddSingleton<SqliteGradeLogRepository>();
builder.Services.AddSingleton<LegacyRetentionMigrationService>();
builder.Services.AddSingleton<ISettingsRepository, FileSettingsRepository>();
builder.Services.AddSingleton<ICategoryRepository, FileCategoryRepository>();
builder.Services.AddSingleton<FileAssessmentRepository>();
builder.Services.AddSingleton<IAssessmentSourceInspector, QuizApp.Infrastructure.Files.AssessmentSourceInspector>();
builder.Services.AddSingleton<IAssessmentTaxonomyValidator, AssessmentTaxonomyValidator>();
builder.Services.AddSingleton<ICatalogTaxonomyValidator, CatalogTaxonomyValidator>();
builder.Services.AddSingleton<SqliteAssessmentCatalogImporter>();
builder.Services.AddSingleton<HybridAssessmentRepository>();
builder.Services.AddSingleton<IAssessmentRepository>(provider => provider.GetRequiredService<HybridAssessmentRepository>());
builder.Services.AddSingleton<IAttemptRepository>(provider => provider.GetRequiredService<SqliteAttemptRepository>());
builder.Services.AddSingleton<IAttemptSessionStore, InMemoryAttemptSessionStore>();
builder.Services.AddSingleton<IGradeLogRepository>(provider => provider.GetRequiredService<SqliteGradeLogRepository>());
builder.Services.AddSingleton<IAreaRepository, FileAreaRepository>();
builder.Services.AddSingleton<IGuidedProjectSessionRepository, FileGuidedProjectSessionRepository>();
builder.Services.AddSingleton<SqliteNavigationCatalogService>();
builder.Services.AddSingleton<INavigationCatalogService>(sp => sp.GetRequiredService<SqliteNavigationCatalogService>());
builder.Services.AddSingleton<NavigationRecommendationService>();
builder.Services.AddSingleton<SqliteAssessmentSearchService>();

builder.Services.AddCors(options =>
{
    options.AddPolicy("LocalFrontend", policy =>
    {
        policy.WithOrigins("http://localhost:4321", "http://127.0.0.1:4321", "http://localhost:3000", "http://127.0.0.1:3000")
            .AllowAnyHeader()
            .AllowAnyMethod();
    });
});

var app = builder.Build();

await app.Services.GetRequiredService<LegacyRetentionMigrationService>().MigrateAsync();
await app.Services.GetRequiredService<SqliteRetentionInitializer>().InitializeAsync();

var importer = app.Services.GetRequiredService<SqliteAssessmentCatalogImporter>();
await importer.ImportAsync();

if (importer.CatalogInitialized)
{
    var options = app.Services.GetRequiredService<SqliteRetentionOptions>();
    await using var conn = new QuizApp.Infrastructure.Retention.SqliteConnectionFactory(options).CreateConnection();
    await conn.OpenAsync();
    await using var cmd = conn.CreateCommand();
    cmd.CommandText = "SELECT severity, COUNT(*) FROM import_diagnostics WHERE run_id = (SELECT id FROM import_runs ORDER BY started_at DESC LIMIT 1) GROUP BY severity;";
    await using var reader = await cmd.ExecuteReaderAsync();
    var counts = new Dictionary<string, int>();
    while (await reader.ReadAsync()) counts[reader.GetString(0)] = reader.GetInt32(1);
    
    var errorCount = counts.GetValueOrDefault("Error", 0);
    var warningCount = counts.GetValueOrDefault("Warning", 0);
    if (errorCount > 0 || warningCount > 0)
    {
        Console.WriteLine($"[CatalogImporter] Startup diagnostic summary: {errorCount} errors, {warningCount} warnings. Check /api/navigation/catalog/diagnostics.");
    }
}

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}


app.UseCors("LocalFrontend");

var api = app.MapGroup("/api");

api.MapGet("/settings", async (ISettingsRepository repository, CancellationToken cancellationToken) =>
{
    return Results.Ok(await repository.GetAsync(cancellationToken));
});

api.MapPut("/settings", async (AppSettings settings, ISettingsRepository repository, CancellationToken cancellationToken) =>
{
    if (settings.DefaultQuizLength is <= 0 or > AssessmentValidator.QuizMaxQuestions)
    {
        return Results.BadRequest(ApiError("INVALID_DEFAULT_QUIZ_LENGTH", "Default quiz length must be between 1 and 50."));
    }

    if (settings.DefaultTestLength is <= 0 or > AssessmentValidator.TestMaxQuestions)
    {
        return Results.BadRequest(ApiError("INVALID_DEFAULT_TEST_LENGTH", "Default test length must be between 1 and 200."));
    }

    if (settings.QuestionTimerSeconds is < 0 || settings.AssessmentTimerSeconds is < 0)
    {
        return Results.BadRequest(ApiError("INVALID_TIMER", "Timers must be null or non-negative seconds."));
    }

    if (!Uri.TryCreate(settings.CodeRunnerBaseUrl, UriKind.Absolute, out _))
    {
        return Results.BadRequest(ApiError("INVALID_CODE_RUNNER_URL", "Code runner base URL must be an absolute URL."));
    }

    if (settings.CodeRunnerCompileTimeoutMs <= 0 || settings.CodeRunnerRunTimeoutMs <= 0)
    {
        return Results.BadRequest(ApiError("INVALID_CODE_RUNNER_TIMEOUT", "Code runner timeouts must be positive."));
    }

    await repository.SaveAsync(settings, cancellationToken);
    return Results.Ok(settings);
});

api.MapGet("/categories", async (ICategoryRepository repository, CancellationToken cancellationToken) =>
{
    return Results.Ok(await repository.ListAsync(cancellationToken));
});

api.MapGet("/assessments", async (string categoryId, IAssessmentRepository repository, CancellationToken cancellationToken) =>
{
    return Results.Ok(await repository.ListByCategoryAsync(categoryId, cancellationToken));
});

api.MapGet("/navigation/catalog", async (SqliteNavigationCatalogService catalogService, CancellationToken cancellationToken) =>
{
    if (!catalogService.IsAvailable)
    {
        return Results.Json(
            ApiError("CATALOG_UNAVAILABLE", "The SQLite assessment catalog is unavailable. Use the classic assessment picker."),
            statusCode: StatusCodes.Status503ServiceUnavailable);
    }

    var catalog = await catalogService.GetCatalogAsync(cancellationToken);
    return Results.Ok(catalog);
});

api.MapGet("/navigation/catalog/diagnostics", async (SqliteRetentionOptions options, CancellationToken cancellationToken) =>
{
    await using var connection = new QuizApp.Infrastructure.Retention.SqliteConnectionFactory(options).CreateConnection();
    await connection.OpenAsync(cancellationToken);

    await using var runCmd = connection.CreateCommand();
    runCmd.CommandText = "SELECT id, started_at, finished_at, status FROM import_runs ORDER BY started_at DESC LIMIT 1;";
    await using var runReader = await runCmd.ExecuteReaderAsync(cancellationToken);
    
    if (!await runReader.ReadAsync(cancellationToken))
        return Results.Ok(new { run = (object?)null, diagnostics = Array.Empty<object>() });

    var runId = runReader.GetString(0);
    var run = new 
    {
        Id = runId,
        StartedAt = runReader.GetString(1),
        FinishedAt = runReader.IsDBNull(2) ? null : runReader.GetString(2),
        Status = runReader.GetString(3)
    };

    var diagnostics = new List<object>();
    await using var diagCmd = connection.CreateCommand();
    diagCmd.CommandText = "SELECT path, assessment_id, severity, code, message, line, column, actual_key, suggested_key FROM import_diagnostics WHERE run_id = @runId;";
    diagCmd.Parameters.AddWithValue("@runId", runId);
    await using var diagReader = await diagCmd.ExecuteReaderAsync(cancellationToken);
    while (await diagReader.ReadAsync(cancellationToken))
    {
        diagnostics.Add(new
        {
            Path = diagReader.IsDBNull(0) ? null : diagReader.GetString(0),
            AssessmentId = diagReader.IsDBNull(1) ? null : diagReader.GetString(1),
            Severity = diagReader.GetString(2),
            Code = diagReader.GetString(3),
            Message = diagReader.GetString(4),
            Line = diagReader.IsDBNull(5) ? (int?)null : diagReader.GetInt32(5),
            Column = diagReader.IsDBNull(6) ? (int?)null : diagReader.GetInt32(6),
            ActualKey = diagReader.IsDBNull(7) ? null : diagReader.GetString(7),
            SuggestedKey = diagReader.IsDBNull(8) ? null : diagReader.GetString(8)
        });
    }

    return Results.Ok(new { run, diagnostics });
});

api.MapGet("/navigation/recommendations", async (NavigationRecommendationService recommendationService, CancellationToken cancellationToken) =>
{
    var recommendations = await recommendationService.GetRecommendationsAsync(cancellationToken);
    return Results.Ok(recommendations);
});

api.MapGet("/search/assessments", async (
    string? q,
    string? subjectId,
    string? areaId,
    string? topicId,
    string? learningGoal,
    string? activityType,
    string? assessmentType,
    string? tag,
    string? skill,
    int? limit,
    SqliteAssessmentSearchService searchService,
    CancellationToken cancellationToken) =>
{
    if (!searchService.IsAvailable)
    {
        return Results.Json(
            ApiError("SEARCH_UNAVAILABLE", "Search is currently unavailable."),
            statusCode: StatusCodes.Status503ServiceUnavailable);
    }

    var tags = string.IsNullOrWhiteSpace(tag) ? null : new[] { tag };
    var skills = string.IsNullOrWhiteSpace(skill) ? null : new[] { skill };
    
    var request = new AssessmentSearchRequest(
        q, subjectId, areaId, topicId, learningGoal, activityType, assessmentType,
        tags, skills, limit ?? 25);

    var results = await searchService.SearchAsync(request, cancellationToken);
    return Results.Ok(results);
});

api.MapGet("/search/suggestions", async (
    string? q,
    string? subjectId,
    string? areaId,
    string? topicId,
    int? limit,
    SqliteAssessmentSearchService searchService,
    CancellationToken cancellationToken) =>
{
    if (!searchService.IsAvailable)
    {
        return Results.Json(
            ApiError("SEARCH_UNAVAILABLE", "Search is currently unavailable."),
            statusCode: StatusCodes.Status503ServiceUnavailable);
    }

    var results = await searchService.GetSuggestionsAsync(q, subjectId, areaId, topicId, limit ?? 12, cancellationToken);
    return Results.Ok(results);
});


api.MapGet("/assessments/{assessmentId}", async (string assessmentId, IAssessmentRepository repository, CancellationToken cancellationToken) =>
{
    var assessment = await repository.GetByIdAsync(assessmentId, cancellationToken);
    return assessment is null
        ? Results.NotFound(ApiError("ASSESSMENT_NOT_FOUND", $"Assessment '{assessmentId}' was not found."))
        : Results.Ok(assessment);
});

api.MapPost("/assessments", async (
    SaveAssessmentRequest request,
    IAssessmentRepository repository,
    AssessmentValidator validator,
    CancellationToken cancellationToken) =>
{
    var assessment = request.ToDomain();
    var validation = validator.Validate(assessment);
    if (!validation.IsValid)
    {
        return Results.BadRequest(new { error = new { code = "ASSESSMENT_INVALID", message = "Assessment validation failed.", details = validation.Issues } });
    }

    await repository.SaveAsync(assessment, cancellationToken);
    return Results.Created($"/api/assessments/{assessment.Id}", assessment);
});

api.MapPut("/assessments/{assessmentId}", async (
    string assessmentId,
    SaveAssessmentRequest request,
    IAssessmentRepository repository,
    AssessmentValidator validator,
    CancellationToken cancellationToken) =>
{
    var assessment = request.ToDomain() with { Id = assessmentId.Trim() };
    var validation = validator.Validate(assessment);
    if (!validation.IsValid)
    {
        return Results.BadRequest(new { error = new { code = "ASSESSMENT_INVALID", message = "Assessment validation failed.", details = validation.Issues } });
    }

    await repository.SaveAsync(assessment, cancellationToken);
    return Results.Ok(assessment);
});

api.MapPost("/assessments/validate", async (ValidateAssessmentFileRequest request, IAssessmentRepository repository, CancellationToken cancellationToken) =>
{
    return Results.Ok(await repository.ValidateFileAsync(request.FileName, cancellationToken));
});

api.MapPost("/attempts", async (StartAttemptRequest request, AttemptService attemptService, CancellationToken cancellationToken) =>
{
    try
    {
        var attempt = await attemptService.StartAsync(request.AssessmentId, request.Mode, cancellationToken);
        return Results.Created($"/api/attempts/{attempt.Id}/results", attempt);
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("ATTEMPT_START_FAILED", ex.Message));
    }
});

api.MapGet("/attempts", async (AttemptService attemptService, CancellationToken cancellationToken) =>
{
    return Results.Ok(await attemptService.ListResultsAsync(cancellationToken));
});

api.MapGet("/attempts/completed-assessments", async (AttemptService attemptService, CancellationToken cancellationToken) =>
{
    return Results.Ok(await attemptService.GetCompletedAssessmentIdsAsync(cancellationToken));
});

api.MapGet("/attempts/{attemptId}/session", async (
    string attemptId,
    AttemptService attemptService,
    IAssessmentRepository assessmentRepository,
    CancellationToken cancellationToken) =>
{
    try
    {
        var results = await attemptService.GetResultsAsync(attemptId, cancellationToken);
        var attempt = await attemptService.GetAsync(attemptId, cancellationToken);
        var assessment = await assessmentRepository.GetByIdAsync(attempt.AssessmentId, cancellationToken);

        return assessment is null
            ? Results.NotFound(ApiError("ASSESSMENT_NOT_FOUND", $"Assessment '{attempt.AssessmentId}' was not found."))
            : Results.Ok(new AttemptSessionResponse(attempt, assessment, results));
    }
    catch (InvalidOperationException ex)
    {
        return Results.NotFound(ApiError("ATTEMPT_NOT_FOUND", ex.Message));
    }
});

api.MapPost("/attempts/{attemptId}/resume", async (
    string attemptId,
    AttemptService attemptService,
    IAssessmentRepository assessmentRepository,
    CancellationToken cancellationToken) =>
{
    try
    {
        var attempt = await attemptService.ResumeAsync(attemptId, cancellationToken);
        var assessment = await assessmentRepository.GetByIdAsync(attempt.AssessmentId, cancellationToken);
        var results = await attemptService.GetResultsAsync(attemptId, cancellationToken);

        return assessment is null
            ? Results.NotFound(ApiError("ASSESSMENT_NOT_FOUND", $"Assessment '{attempt.AssessmentId}' was not found."))
            : Results.Ok(new AttemptSessionResponse(attempt, assessment, results));
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("ATTEMPT_RESUME_FAILED", ex.Message));
    }
});

api.MapPost("/attempts/{attemptId}/pause", async (string attemptId, AttemptService attemptService, CancellationToken cancellationToken) =>
{
    try
    {
        var attempt = await attemptService.PauseAsync(attemptId, cancellationToken);
        var results = await attemptService.GetResultsAsync(attemptId, cancellationToken);
        return Results.Ok(new { attempt, results });
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("ATTEMPT_PAUSE_FAILED", ex.Message));
    }
});

api.MapPost("/attempts/{attemptId}/abandon", async (string attemptId, AttemptService attemptService, CancellationToken cancellationToken) =>
{
    try
    {
        var results = await attemptService.GetResultsAsync(attemptId, cancellationToken);
        var attempt = await attemptService.AbandonAsync(attemptId, cancellationToken);
        return Results.Ok(new { attempt, results = results with { Status = AttemptStatus.Abandoned } });
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("ATTEMPT_ABANDON_FAILED", ex.Message));
    }
});

api.MapDelete("/attempts/{attemptId}", async (string attemptId, AttemptService attemptService, CancellationToken cancellationToken) =>
{
    await attemptService.DeleteAsync(attemptId, cancellationToken);
    return Results.NoContent();
});

api.MapPost("/attempts/bulk-delete", async (BulkDeleteAttemptsRequest request, AttemptService attemptService, CancellationToken cancellationToken) =>
{
    await attemptService.DeleteManyAsync(request.AttemptIds ?? Array.Empty<string>(), cancellationToken);
    return Results.NoContent();
});

api.MapPost("/attempts/{attemptId}/answers", async (string attemptId, SubmitAnswerRequest request, AttemptService attemptService, CancellationToken cancellationToken) =>
{
    try
    {
        return Results.Ok(await attemptService.SubmitAnswerAsync(attemptId, request.ToDomain(), cancellationToken));
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("ANSWER_SUBMIT_FAILED", ex.Message));
    }
});

api.MapPost("/attempts/{attemptId}/answers/{questionId}/override", async (string attemptId, string questionId, AttemptService attemptService, CancellationToken cancellationToken) =>
{
    try
    {
        await attemptService.OverrideAnswerEvaluationAsync(attemptId, questionId, true, cancellationToken);
        var results = await attemptService.GetResultsAsync(attemptId, cancellationToken);
        return Results.Ok(new { results });
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("ANSWER_OVERRIDE_FAILED", ex.Message));
    }
});

api.MapPost("/attempts/{attemptId}/recall/{itemId}/reveal", async (
    string attemptId,
    string itemId,
    RevealRecallItemRequest request,
    AttemptService attemptService,
    CancellationToken cancellationToken) =>
{
    try
    {
        var attempt = await attemptService.RevealRecallItemAsync(attemptId, itemId, request.UserResponse, cancellationToken);
        var results = await attemptService.GetResultsAsync(attemptId, cancellationToken);
        return Results.Ok(new { attempt, results });
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("RECALL_REVEAL_FAILED", ex.Message));
    }
});

api.MapPost("/attempts/{attemptId}/recall/{itemId}/rate", async (
    string attemptId,
    string itemId,
    RateRecallItemRequest request,
    AttemptService attemptService,
    CancellationToken cancellationToken) =>
{
    try
    {
        var attempt = await attemptService.RateRecallItemAsync(attemptId, itemId, request.Rating, cancellationToken);
        var results = await attemptService.GetResultsAsync(attemptId, cancellationToken);
        return Results.Ok(new { attempt, results });
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("RECALL_RATE_FAILED", ex.Message));
    }
});

api.MapPut("/attempts/{attemptId}/learn/sections/{sectionId}/state", async (
    string attemptId,
    string sectionId,
    UpdateLearningSectionStateRequest request,
    AttemptService attemptService,
    CancellationToken cancellationToken) =>
{
    try
    {
        var attempt = await attemptService.UpdateLearningSectionStateAsync(
            attemptId,
            sectionId,
            request.Visited,
            request.InteractionChanged,
            request.ControlValues,
            cancellationToken);
        var results = await attemptService.GetResultsAsync(attemptId, cancellationToken);
        return Results.Ok(new { attempt, results });
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("LEARNING_SECTION_STATE_FAILED", ex.Message));
    }
});

api.MapPost("/attempts/{attemptId}/learn/sections/{sectionId}/complete", async (
    string attemptId,
    string sectionId,
    AttemptService attemptService,
    CancellationToken cancellationToken) =>
{
    try
    {
        var attempt = await attemptService.CompleteLearningSectionAsync(attemptId, sectionId, cancellationToken);
        var results = await attemptService.GetResultsAsync(attemptId, cancellationToken);
        return Results.Ok(new { attempt, results });
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("LEARNING_SECTION_COMPLETE_FAILED", ex.Message));
    }
});

api.MapPut("/attempts/{attemptId}/directed-project/steps/{stepId}/state", async (
    string attemptId,
    string stepId,
    UpdateDirectedProjectStepStateRequest request,
    AttemptService attemptService,
    CancellationToken cancellationToken) =>
{
    try
    {
        var attempt = await attemptService.UpdateDirectedProjectStepStateAsync(
            attemptId,
            stepId,
            request.Visited,
            request.Completed,
            request.CompletedChecklistItemIds ?? Array.Empty<string>(),
            request.Notes,
            cancellationToken);
        var results = await attemptService.GetResultsAsync(attemptId, cancellationToken);
        return Results.Ok(new { attempt, results });
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("DIRECTED_PROJECT_STEP_STATE_FAILED", ex.Message));
    }
});

api.MapPost("/attempts/{attemptId}/directed-project/steps/{stepId}/complete", async (
    string attemptId,
    string stepId,
    AttemptService attemptService,
    CancellationToken cancellationToken) =>
{
    try
    {
        var attempt = await attemptService.CompleteDirectedProjectStepAsync(attemptId, stepId, cancellationToken);
        var results = await attemptService.GetResultsAsync(attemptId, cancellationToken);
        return Results.Ok(new { attempt, results });
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("DIRECTED_PROJECT_STEP_COMPLETE_FAILED", ex.Message));
    }
});

api.MapGet("/attempts/{attemptId}/guided-project", async (
    string attemptId,
    GuidedProjectService guidedProjectService,
    CancellationToken cancellationToken) =>
{
    try
    {
        return Results.Ok(await guidedProjectService.GetSessionAsync(attemptId, cancellationToken));
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("GUIDED_PROJECT_SESSION_FAILED", ex.Message));
    }
});

api.MapPut("/attempts/{attemptId}/guided-project/files", async (
    string attemptId,
    SaveGuidedProjectFilesRequest request,
    GuidedProjectService guidedProjectService,
    CancellationToken cancellationToken) =>
{
    try
    {
        return Results.Ok(await guidedProjectService.SaveFilesAsync(attemptId, request.ToDomain(), cancellationToken));
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("GUIDED_PROJECT_SAVE_FAILED", ex.Message));
    }
});

api.MapPost("/attempts/{attemptId}/guided-project/run", async (
    string attemptId,
    SaveGuidedProjectFilesRequest request,
    GuidedProjectService guidedProjectService,
    CancellationToken cancellationToken) =>
{
    try
    {
        return Results.Ok(await guidedProjectService.RunAsync(attemptId, request.ToDomain(), cancellationToken));
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("GUIDED_PROJECT_RUN_FAILED", ex.Message));
    }
});

api.MapPost("/attempts/{attemptId}/guided-project/complete", async (
    string attemptId,
    GuidedProjectService guidedProjectService,
    CancellationToken cancellationToken) =>
{
    try
    {
        return Results.Ok(new { results = await guidedProjectService.CompleteAsync(attemptId, cancellationToken) });
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("GUIDED_PROJECT_COMPLETE_FAILED", ex.Message));
    }
});

api.MapPost("/attempts/{attemptId}/complete", async (
    string attemptId,
    AttemptService attemptService,
    GradeLogService gradeLogService,
    ISettingsRepository settingsRepository,
    CancellationToken cancellationToken) =>
{
    try
    {
        var results = await attemptService.CompleteAsync(attemptId, cancellationToken);
        var settings = await settingsRepository.GetAsync(cancellationToken);
        GradeLogEntry? committedGrade = null;

        if (results.Mode is AssessmentMode.Scored && settings.CommitScoredAttemptsAutomatically && !results.HasPendingSelfChecks)
        {
            committedGrade = await gradeLogService.CommitAttemptAsync(attemptId, cancellationToken);
        }

        return Results.Ok(new { results, committedGrade });
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("ATTEMPT_COMPLETE_FAILED", ex.Message));
    }
});

api.MapGet("/attempts/{attemptId}/results", async (string attemptId, AttemptService attemptService, CancellationToken cancellationToken) =>
{
    try
    {
        return Results.Ok(await attemptService.GetResultsAsync(attemptId, cancellationToken));
    }
    catch (InvalidOperationException ex)
    {
        return Results.NotFound(ApiError("ATTEMPT_NOT_FOUND", ex.Message));
    }
});

api.MapDelete("/grades/{attemptId}", async (string attemptId, AttemptService attemptService, CancellationToken cancellationToken) =>
{
    await attemptService.DeleteAsync(attemptId, cancellationToken);
    return Results.NoContent();
});

api.MapPost("/grades/commit", async (CommitGradeRequest request, GradeLogService gradeLogService, CancellationToken cancellationToken) =>
{
    try
    {
        return Results.Ok(await gradeLogService.CommitAttemptAsync(request.AttemptId, cancellationToken));
    }
    catch (InvalidOperationException ex)
    {
        return Results.BadRequest(ApiError("GRADE_COMMIT_FAILED", ex.Message));
    }
});

api.MapGet("/grades/summary", async (GradeLogService gradeLogService, CancellationToken cancellationToken) =>
{
    return Results.Ok(await gradeLogService.GetSummaryAsync(cancellationToken));
});

api.MapGet("/analytics/grades", async (
    string? status,
    string? mode,
    string? assessmentType,
    string? categoryId,
    string? subcategoryId,
    string? areaId,
    string? questionType,
    bool? committed,
    DateTimeOffset? from,
    DateTimeOffset? to,
    decimal? minScore,
    decimal? maxScore,
    GradeAnalyticsService analyticsService,
    CancellationToken cancellationToken) =>
{
    var filter = new GradeAnalyticsFilter(
        ParseEnum<AttemptStatus>(status),
        ParseEnum<AssessmentMode>(mode),
        ParseEnum<AssessmentType>(assessmentType),
        categoryId,
        subcategoryId,
        areaId,
        ParseEnum<QuestionType>(questionType),
        committed,
        from,
        to,
        minScore,
        maxScore);

    return Results.Ok(await analyticsService.GetSummaryAsync(filter, cancellationToken));
});

app.Run();

static object ApiError(string code, string message)
{
    return new { error = new { code, message } };
}

static TEnum? ParseEnum<TEnum>(string? value)
    where TEnum : struct
{
    return string.IsNullOrWhiteSpace(value) || !Enum.TryParse<TEnum>(value, true, out var parsed)
        ? null
        : parsed;
}
