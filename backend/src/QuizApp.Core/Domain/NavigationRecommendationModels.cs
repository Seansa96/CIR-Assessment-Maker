namespace QuizApp.Core.Domain;

public sealed record NavigationRecommendation(
    string TopicId,
    IReadOnlyList<string> AreaIds,
    string State,
    string RecommendedLearningGoal,
    IReadOnlyList<string> RecommendedActivityTypes,
    IReadOnlyList<string> SuggestedAssessmentIds,
    int CompletedLearnCount,
    int CompletedRecallCount,
    int EligibleMasteryAttemptCount,
    decimal? MasteryPercent,
    bool ProvisionalMastery);
