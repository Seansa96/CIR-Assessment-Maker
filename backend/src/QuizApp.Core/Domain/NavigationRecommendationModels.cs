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
    bool ProvisionalMastery,
    IReadOnlyList<string>? PrerequisiteTopicIds = null,
    IReadOnlyList<string>? PrerequisiteTitles = null,
    IReadOnlyList<string>? UnmetPrerequisiteTopicIds = null,
    IReadOnlyList<string>? UnmetPrerequisiteTitles = null,
    bool IsEligible = true,
    bool IsNextRecommended = false,
    string? ProgressionReason = null)
{
    public IReadOnlyList<string> Prerequisites => PrerequisiteTopicIds ?? Array.Empty<string>();
    public IReadOnlyList<string> PrerequisiteTopicLabels => PrerequisiteTitles ?? Array.Empty<string>();
    public IReadOnlyList<string> UnmetPrerequisites => UnmetPrerequisiteTopicIds ?? Array.Empty<string>();
    public IReadOnlyList<string> UnmetPrerequisiteTopicLabels => UnmetPrerequisiteTitles ?? Array.Empty<string>();
}
