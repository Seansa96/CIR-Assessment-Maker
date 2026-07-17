namespace QuizApp.Core.Domain;

/// <summary>Navigation catalog returned by GET /api/navigation/catalog.</summary>
public sealed record NavigationCatalog(
    IReadOnlyList<NavigationSubject> Subjects,
    IReadOnlyList<NavigationArea> Areas,
    IReadOnlyList<NavigationTopic> Topics,
    IReadOnlyList<NavigationGoal> Goals,
    IReadOnlyList<NavigationAssessmentSummary> Assessments);

public sealed record NavigationSubject(
    string Id,
    string Title,
    string? Description = null);

public sealed record NavigationArea(
    string Id,
    string Title,
    IReadOnlyList<string> SubjectIds,
    IReadOnlyList<string> TopicIds,
    string? Description = null,
    int Index = 0);

public sealed record NavigationTopic(
    string Id,
    string Title,
    string SubjectId,
    string? Description = null,
    IReadOnlyList<string>? PrerequisiteIds = null,
    int ProgressionIndex = 0)
{
    public IReadOnlyList<string> Prerequisites => PrerequisiteIds ?? Array.Empty<string>();
}

public sealed record NavigationGoal(
    string Id,
    string Label,
    IReadOnlyList<string> ActivityTypes);

public sealed record NavigationAssessmentSummary(
    string Id,
    string Title,
    AssessmentType AssessmentType,
    string SubjectId,
    string AreaId,
    string TopicId,
    string LearningGoal,
    string ActivityType,
    IReadOnlyList<string> Tags,
    int QuestionCount,
    int AuthoredQuestionCount,
    int? AttemptQuestionCount,
    bool HasCompletedAttempt,
    IReadOnlyList<string> Skills)
{
    [System.Text.Json.Serialization.JsonIgnore]
    public IReadOnlyList<string> AreaIds => string.IsNullOrWhiteSpace(AreaId) ? Array.Empty<string>() : [AreaId];
    [System.Text.Json.Serialization.JsonIgnore]
    public IReadOnlyList<string> TopicIds => string.IsNullOrWhiteSpace(TopicId) ? Array.Empty<string>() : [TopicId];
}

/// <summary>Known learning-goal IDs.</summary>
public static class LearningGoals
{
    public const string Learn    = "learn";
    public const string Recall   = "recall";
    public const string Practice = "practice";
    public const string Apply    = "apply";
    public const string Evaluate = "evaluate";
    public const string Reflect  = "reflect";

    public static readonly IReadOnlyList<(string Id, string Label, string[] ActivityTypes)> All =
    [
        (Learn,    "Learn",    ["conceptLesson", "glossary", "guidedWorkedExample", "interactiveExploration", "directedProject"]),
        (Recall,   "Recall",   ["recognitionDrill", "clozeDrill", "mixedRecallSet"]),
        (Practice, "Practice", ["focusedPractice", "mixedPractice", "directedProject"]),
        (Apply,    "Apply",    ["sandbox", "guidedProject", "codingApplication", "circuitApplication"]),
        (Evaluate, "Evaluate", ["masteryCheck", "formalTest", "guidedProject"]),
        (Reflect,  "Reflect",  ["selfReview"]),
    ];
}

/// <summary>Infers navigation metadata from assessment type and recall-item mix when not explicitly authored.</summary>
public static class NavigationInference
{
    public static NavigationMetadata Infer(AssessmentDefinition assessment)
    {
        if (assessment.Navigation is { LearningGoal: not null, ActivityType: not null })
        {
            return assessment.Navigation with
            {
                Tags = assessment.Navigation.Tags ?? Array.Empty<string>()
            };
        }

        var (goal, activity) = InferGoalActivity(assessment);
        return new NavigationMetadata(
            assessment.Navigation?.LearningGoal ?? goal,
            assessment.Navigation?.ActivityType ?? activity,
            assessment.Navigation?.Tags ?? Array.Empty<string>());
    }

    private static (string Goal, string Activity) InferGoalActivity(AssessmentDefinition a)
    {
        return a.AssessmentType switch
        {
            AssessmentType.WorkedExample  => (LearningGoals.Learn, "guidedWorkedExample"),
            AssessmentType.ConceptLesson => (LearningGoals.Learn, "conceptLesson"),
            AssessmentType.Glossary => (LearningGoals.Learn, "glossary"),
            AssessmentType.InteractiveExploration => (LearningGoals.Learn, "interactiveExploration"),
            AssessmentType.DirectedProject => (LearningGoals.Practice, "directedProject"),
            AssessmentType.GuidedProject  => (LearningGoals.Evaluate, "guidedProject"),
            AssessmentType.Sandbox        => (LearningGoals.Apply, "sandbox"),
            AssessmentType.Test           => (LearningGoals.Evaluate, "formalTest"),
            AssessmentType.Quiz           => (LearningGoals.Practice, "focusedPractice"),
            AssessmentType.RecallDrill    => InferRecallDrill(a),
            _                             => (LearningGoals.Practice, "focusedPractice")
        };
    }

    private static (string Goal, string Activity) InferRecallDrill(AssessmentDefinition a)
    {
        if (a.Items.Count == 0)
            return (LearningGoals.Recall, "mixedRecallSet");

        var types = a.Items.Select(i => i.Type).Distinct().ToList();

        if (types.Count == 1 && types[0] == RecallItemType.Cloze)
            return (LearningGoals.Recall, "clozeDrill");

        if (types.Count == 1 && types[0] == RecallItemType.Flashcard)
            return (LearningGoals.Recall, "recognitionDrill");

        return (LearningGoals.Recall, "mixedRecallSet");
    }
}
