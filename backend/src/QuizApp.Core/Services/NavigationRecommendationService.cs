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

        // Progression is guidance rather than access control. A completed assessment supplies
        // completion evidence for each topic it teaches; an eligible topic has no unmet edges.
        var completedAssessmentIds = allAttempts
            .Where(attempt => attempt.Status == AttemptStatus.Completed)
            .Select(attempt => attempt.AssessmentId)
            .ToHashSet(StringComparer.OrdinalIgnoreCase);
        var completedTopicIds = catalog.Assessments
            .Where(assessment => completedAssessmentIds.Contains(assessment.Id))
            .Select(assessment => assessment.TopicId)
            .ToHashSet(StringComparer.OrdinalIgnoreCase);
        var topicsById = catalog.Topics.ToDictionary(topic => topic.Id, StringComparer.OrdinalIgnoreCase);
        var unmetPrerequisitesByTopic = catalog.Topics.ToDictionary(
            topic => topic.Id,
            topic => topic.Prerequisites
                .Where(prerequisiteId => !completedTopicIds.Contains(prerequisiteId))
                .ToList(),
            StringComparer.OrdinalIgnoreCase);
        var nextTopicIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var categoryTopics in catalog.Topics.GroupBy(topic => topic.SubjectId, StringComparer.OrdinalIgnoreCase))
        {
            var eligible = categoryTopics
                .Where(topic => !completedTopicIds.Contains(topic.Id) && unmetPrerequisitesByTopic[topic.Id].Count == 0)
                .OrderBy(topic => topic.ProgressionIndex)
                .ToList();
            if (eligible.Count == 0) continue;

            // The first entry-point follows the curated category order. Once a topic
            // explicitly declares prerequisites, every newly eligible branch is surfaced.
            var branches = eligible.Where(topic => topic.Prerequisites.Count > 0).ToList();
            if (branches.Count > 0)
                nextTopicIds.UnionWith(branches.Select(topic => topic.Id));
            else
                nextTopicIds.Add(eligible[0].Id);
        }

        var topicIds = catalog.Topics.Select(t => t.Id).ToList();
        var recommendations = new List<NavigationRecommendation>();

        foreach (var topicId in topicIds)
        {
            var topic = topicsById[topicId];
            var unmetPrerequisites = unmetPrerequisitesByTopic[topicId];
            var isEligible = unmetPrerequisites.Count == 0;
            var isNextRecommended = nextTopicIds.Contains(topicId);
            var areaIds = catalog.Areas
                .Where(a => a.TopicIds.Contains(topicId, StringComparer.OrdinalIgnoreCase))
                .Select(a => a.Id)
                .ToList();

            var topicAssessments = catalog.Assessments
                .Where(a => string.Equals(a.TopicId, topicId, StringComparison.OrdinalIgnoreCase))
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
                var lastAttemptTime = masteryAttempts[0].Attempt.CompletedAt ?? masteryAttempts[0].Attempt.StartedAt;
                var daysSinceLastAttempt = (DateTimeOffset.UtcNow - lastAttemptTime).TotalDays;

                if (masteryPercent < 90 || daysSinceLastAttempt > 14)
                {
                    state = "review";
                    var recallAfterLowScore = recallAttempts.Any(r => (r.CompletedAt ?? r.StartedAt) > lastAttemptTime);
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
                var lastAttemptTime = latestTwo[0].Attempt.CompletedAt ?? latestTwo[0].Attempt.StartedAt;
                var daysSinceLastAttempt = (DateTimeOffset.UtcNow - lastAttemptTime).TotalDays;

                if (masteryPercent < 90 || daysSinceLastAttempt > 14)
                {
                    state = "review";
                    var mostRecentLowScore = masteryAttempts.FirstOrDefault(x => x.Score < 90);
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
                    .OrderBy(a => a.HasCompletedAttempt ? 1 : 0)
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
                        .OrderBy(a => a.HasCompletedAttempt ? 1 : 0)
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
                provisionalMastery,
                topic.Prerequisites,
                topic.Prerequisites.Select(id => topicsById.TryGetValue(id, out var prerequisite) ? prerequisite.Title : id).ToList(),
                unmetPrerequisites,
                unmetPrerequisites.Select(id => topicsById.TryGetValue(id, out var prerequisite) ? prerequisite.Title : id).ToList(),
                isEligible,
                isNextRecommended,
                BuildProgressionReason(topic, completedTopicIds.Contains(topicId), unmetPrerequisites.Select(id => topicsById.TryGetValue(id, out var prerequisite) ? prerequisite.Title : id).ToList(), isNextRecommended)
            ));
        }

        return recommendations;
    }

    private static string BuildProgressionReason(
        NavigationTopic topic,
        bool isCompleted,
        IReadOnlyList<string> unmetPrerequisiteTitles,
        bool isNextRecommended)
    {
        if (unmetPrerequisiteTitles.Count > 0)
            return $"Complete {string.Join(", ", unmetPrerequisiteTitles)} before this topic is recommended.";

        if (isNextRecommended)
            return topic.Prerequisites.Count == 0
                ? "This is an available starting topic for this curriculum."
                : "Its prerequisite topics are complete, so this is the next recommended topic.";

        return isCompleted
            ? "You have completion evidence for this topic."
            : "This topic is available when you are ready.";
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
            "learn" => ["conceptLesson", "glossary", "guidedWorkedExample", "interactiveExploration"],
            "recall" => ["mixedRecallSet", "clozeDrill", "recognitionDrill"],
            "practice" => ["focusedPractice", "mixedPractice", "directedProject"],
            "apply" => ["guidedProject", "codingApplication", "circuitApplication"],
            "evaluate" => ["masteryCheck", "formalTest", "guidedProject"],
            "reflect" => ["selfReview"],
            _ => []
        };
    }

    private static List<string> GetFallbackChain(string goal)
    {
        return goal switch
        {
            "learn" => ["conceptLesson", "glossary", "guidedWorkedExample", "interactiveExploration"],
            "recall" => ["mixedRecallSet", "clozeDrill", "recognitionDrill"],
            "practice" => ["focusedPractice", "mixedPractice", "directedProject"],
            "review" => ["mixedRecallSet", "clozeDrill", "recognitionDrill", "focusedPractice", "mixedPractice", "directedProject", "conceptLesson", "guidedWorkedExample", "interactiveExploration"],
            "evaluate" => ["masteryCheck", "formalTest", "guidedProject", "focusedPractice", "mixedPractice"],
            _ => []
        };
    }
}
