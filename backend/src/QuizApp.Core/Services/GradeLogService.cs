using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Core.Services;

public sealed class GradeLogService
{
    private readonly IGradeLogRepository gradeLogRepository;
    private readonly AttemptService attemptService;

    public GradeLogService(IGradeLogRepository gradeLogRepository, AttemptService attemptService)
    {
        this.gradeLogRepository = gradeLogRepository;
        this.attemptService = attemptService;
    }

    public async Task<GradeLogEntry> CommitAttemptAsync(string attemptId, CancellationToken cancellationToken = default)
    {
        var results = await attemptService.GetResultsAsync(attemptId, cancellationToken);
        if (!results.IsComplete)
        {
            throw new InvalidOperationException("Only completed attempts can be committed to the grade log.");
        }

        if (results.AssessmentType is AssessmentType.WorkedExample
            or AssessmentType.GuidedProject
            or AssessmentType.ConceptLesson
            or AssessmentType.InteractiveExploration
            or AssessmentType.DirectedProject)
        {
            throw new InvalidOperationException("Instructional sessions cannot be committed to the grade log.");
        }

        if (results.HasPendingSelfChecks)
        {
            throw new InvalidOperationException("Resolve all free response self-checks before committing this attempt to the grade log.");
        }

        if (results.AssessmentType is AssessmentType.RecallDrill && results.RecallSummary?.ItemsReviewed < results.TotalQuestions)
        {
            throw new InvalidOperationException("Resolve all recall ratings before committing this attempt to the grade log.");
        }

        var existingEntries = await gradeLogRepository.ListAsync(cancellationToken);
        var existingEntry = existingEntries.FirstOrDefault(entry => string.Equals(entry.AttemptId, attemptId, StringComparison.OrdinalIgnoreCase));
        if (existingEntry is not null)
        {
            return existingEntry;
        }

        var entry = new GradeLogEntry(
            Guid.NewGuid().ToString("n"),
            results.AttemptId,
            results.AssessmentId,
            results.AssessmentTitle,
            results.Mode,
            results.CorrectCount,
            results.TotalQuestions,
            results.PercentScore,
            DateTimeOffset.UtcNow)
        {
            EarnedPoints = results.EarnedPoints,
            PossiblePoints = results.PossiblePoints
        };

        await gradeLogRepository.AddAsync(entry, cancellationToken);
        return entry;
    }

    public async Task<GradeLogSummary> GetSummaryAsync(CancellationToken cancellationToken = default)
    {
        var entries = await gradeLogRepository.ListAsync(cancellationToken);
        var average = entries.Count == 0
            ? (decimal?)null
            : Math.Round(entries.Average(entry => entry.PercentScore), 2);

        return new GradeLogSummary(entries.Count, average, entries.OrderByDescending(entry => entry.CommittedAt).ToList());
    }
}
