using QuizApp.Core.Domain;
using QuizApp.Core.Repositories;

namespace QuizApp.Core.Services;

public sealed class NavigationRecommendationService
{
    private readonly IAssessmentRepository assessmentRepository;
    private readonly IAttemptRepository attemptRepository;
    private readonly IAttemptSessionStore attemptSessionStore;
    private readonly IGradeLogRepository gradeLogRepository;
    private readonly INavigationCatalogService catalogService;
    private readonly ScoringService scoringService;

    public NavigationRecommendationService(
        IAssessmentRepository assessmentRepository,
        IAttemptRepository attemptRepository,
        IAttemptSessionStore attemptSessionStore,
        IGradeLogRepository gradeLogRepository,
        INavigationCatalogService catalogService,
        ScoringService scoringService)
    {
        this.assessmentRepository = assessmentRepository;
        this.attemptRepository = attemptRepository;
        this.attemptSessionStore = attemptSessionStore;
        this.gradeLogRepository = gradeLogRepository;
        this.catalogService = catalogService;
        this.scoringService = scoringService;
    }

    public async Task<IReadOnlyList<NavigationRecommendation>> GetRecommendationsAsync(CancellationToken cancellationToken = default)
    {
        var catalog = await catalogService.GetCatalogAsync(cancellationToken);
        var activeAttempts = await attemptSessionStore.ListAsync(cancellationToken);
        var persistedAttempts = await attemptRepository.ListAsync(cancellationToken);
        var allAttempts = activeAttempts
            .Concat(persistedAttempts)
            .GroupBy(attempt => attempt.Id, StringComparer.OrdinalIgnoreCase)
            .Select(group => group.First())
            .ToList();

        var gradeEntries = await gradeLogRepository.ListAsync(cancellationToken);
        var committedAttemptIds = gradeEntries.Select(e => e.AttemptId).ToHashSet(StringComparer.OrdinalIgnoreCase);

        var topicIds = catalog.Topics.Select(t => t.Id).ToList();
        var recommendations = new List<NavigationRecommendation>();

        foreach (var topicId in topicIds)
        {
            var areaIds = catalog.Areas
                .Where(a => a.TopicIds.Contains(topicId, StringComparer.OrdinalIgnoreCase))
                .Select(a => a.Id)
                .ToList();

            var topicAssessments = catalog.Assessments
                .Where(a => a.TopicIds.Contains(topicId, StringComparer.OrdinalIgnoreCase))
                .ToList();

            // Evidence
            var learnAttempts = allAttempts
                .Where(a => a.Status == AttemptStatus.Completed && topicAssessments.Any(ta => string.Equals(ta.Id, a.AssessmentId, StringComparison.OrdinalIgnoreCase)))
                .Where(a => topicAssessments.First(ta => string.Equals(ta.Id, a.AssessmentId, StringComparison.OrdinalIgnoreCase)).AssessmentType is AssessmentType.ConceptLesson or AssessmentType.WorkedExample or AssessmentType.InteractiveExploration)
                .ToList();

            var recallAttempts = allAttempts
                .Where(a => a.Status == AttemptStatus.Completed && topicAssessments.Any(ta => string.Equals(ta.Id, a.AssessmentId, StringComparison.OrdinalIgnoreCase)))
                .Where(a => topicAssessments.First(ta => string.Equals(ta.Id, a.AssessmentId, StringComparison.OrdinalIgnoreCase)).AssessmentType == AssessmentType.RecallDrill)
                .ToList();

            var masteryAttempts = allAttempts
                .Where(a => a.Status == AttemptStatus.Completed && topicAssessments.Any(ta => string.Equals(ta.Id, a.AssessmentId, StringComparison.OrdinalIgnoreCase)))
                .Where(a => 
                {
                    var assessmentType = topicAssessments.First(ta => string.Equals(ta.Id, a.AssessmentId, StringComparison.OrdinalIgnoreCase)).AssessmentType;
                    if (assessmentType is not (AssessmentType.Quiz or AssessmentType.Test)) return false;
                    
                    if (a.Mode == AssessmentMode.Practice && !committedAttemptIds.Contains(a.Id)) return false;
                    
                    return true;
                })
                .Select(a => new { Attempt = a, Score = GetScore(a, gradeEntries, topicAssessments.First(ta => string.Equals(ta.Id, a.AssessmentId, StringComparison.OrdinalIgnoreCase))) })
                .OrderByDescending(x => x.Attempt.CompletedAt ?? x.Attempt.StartedAt)
                .ToList();

            var learnCount = learnAttempts.Count;
            var recallCount = recallAttempts.Count;
            var eligibleMasteryCount = masteryAttempts.Count;

            string state;
            string recommendedGoal;
            List<string> recommendedActivityTypes;
            decimal? masteryPercent = null;
            bool provisionalMastery = false;

            if (learnCount < 2)
            {
                state = "learn";
                recommendedGoal = "learn";
            }
            else if (recallCount == 0)
            {
                state = "recall";
                recommendedGoal = "recall";
            }
            else if (eligibleMasteryCount == 0)
            {
                state = "practice";
                recommendedGoal = "practice";
            }
            else if (eligibleMasteryCount == 1)
            {
                masteryPercent = masteryAttempts[0].Score;
                if (masteryPercent < 80)
                {
                    state = "review";
                    var lastLowScoreTime = masteryAttempts[0].Attempt.CompletedAt ?? masteryAttempts[0].Attempt.StartedAt;
                    var recallAfterLowScore = recallAttempts.Any(r => (r.CompletedAt ?? r.StartedAt) > lastLowScoreTime);
                    recommendedGoal = recallAfterLowScore ? "practice" : "recall";
                }
                else
                {
                    state = "practice";
                    recommendedGoal = "practice";
                    provisionalMastery = true;
                }
            }
            else
            {
                var latestTwo = masteryAttempts.Take(2).ToList();
                masteryPercent = latestTwo.Average(x => x.Score);

                if (masteryPercent < 80)
                {
                    state = "review";
                    var mostRecentLowScore = masteryAttempts.FirstOrDefault(x => x.Score < 80);
                    if (mostRecentLowScore != null)
                    {
                        var lastLowScoreTime = mostRecentLowScore.Attempt.CompletedAt ?? mostRecentLowScore.Attempt.StartedAt;
                        var recallAfterLowScore = recallAttempts.Any(r => (r.CompletedAt ?? r.StartedAt) > lastLowScoreTime);
                        recommendedGoal = recallAfterLowScore ? "practice" : "recall";
                    }
                    else
                    {
                        recommendedGoal = "recall";
                    }
                }
                else
                {
                    state = "evaluate";
                    recommendedGoal = "evaluate";
                }
            }

            recommendedActivityTypes = GetActivityTypesForGoal(recommendedGoal);

            var suggestedAssessmentIds = new List<string>();
            foreach (var activityType in recommendedActivityTypes)
            {
                var candidates = topicAssessments
                    .Where(a => string.Equals(a.ActivityType, activityType, StringComparison.OrdinalIgnoreCase))
                    .Select(a => a.Id)
                    .ToList();
                if (candidates.Count > 0)
                {
                    suggestedAssessmentIds.AddRange(candidates);
                    break;
                }
            }

            // Fallback chain
            if (suggestedAssessmentIds.Count == 0)
            {
                var fallbackChain = GetFallbackChain(recommendedGoal);
                foreach (var fallbackActivity in fallbackChain)
                {
                    var candidates = topicAssessments
                        .Where(a => string.Equals(a.ActivityType, fallbackActivity, StringComparison.OrdinalIgnoreCase))
                        .Select(a => a.Id)
                        .ToList();
                    if (candidates.Count > 0)
                    {
                        suggestedAssessmentIds.AddRange(candidates);
                        break;
                    }
                }
            }

            recommendations.Add(new NavigationRecommendation(
                topicId,
                areaIds,
                state,
                recommendedGoal,
                recommendedActivityTypes,
                suggestedAssessmentIds,
                learnCount,
                recallCount,
                eligibleMasteryCount,
                masteryPercent,
                provisionalMastery
            ));
        }

        return recommendations;
    }

    private decimal GetScore(Attempt attempt, IReadOnlyList<GradeLogEntry> entries, NavigationAssessmentSummary assessmentSummary)
    {
        var entry = entries.FirstOrDefault(e => string.Equals(e.AttemptId, attempt.Id, StringComparison.OrdinalIgnoreCase));
        if (entry != null)
        {
            return entry.PercentScore;
        }

        var correctCount = attempt.Answers.Count(answer => answer.Evaluation?.IsCorrect == true);
        var totalQuestions = attempt.QuestionOrder.Count;
        return totalQuestions == 0 ? 0 : Math.Round(correctCount * 100m / totalQuestions, 2);
    }

    private static List<string> GetActivityTypesForGoal(string goal)
    {
        return goal switch
        {
            "learn" => ["conceptLesson", "guidedWorkedExample", "interactiveExploration"],
            "recall" => ["mixedRecallSet", "clozeDrill", "recognitionDrill"],
            "practice" => ["focusedPractice", "mixedPractice"],
            "apply" => ["guidedProject", "codingApplication", "circuitApplication"],
            "evaluate" => ["masteryCheck", "formalTest"],
            "reflect" => ["selfReview"],
            _ => []
        };
    }

    private static List<string> GetFallbackChain(string goal)
    {
        return goal switch
        {
            "learn" => ["conceptLesson", "guidedWorkedExample", "interactiveExploration"],
            "recall" => ["mixedRecallSet", "clozeDrill", "recognitionDrill"],
            "practice" => ["focusedPractice", "mixedPractice"],
            "review" => ["mixedRecallSet", "clozeDrill", "recognitionDrill", "focusedPractice", "mixedPractice", "conceptLesson", "guidedWorkedExample", "interactiveExploration"],
            "evaluate" => ["masteryCheck", "formalTest", "focusedPractice", "mixedPractice"],
            _ => []
        };
    }
}
