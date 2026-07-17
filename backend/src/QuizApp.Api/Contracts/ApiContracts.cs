using QuizApp.Core.Domain;
using System.Text.Json;

namespace QuizApp.Api.Contracts;

public sealed record ValidateAssessmentFileRequest(string FileName);

public sealed record StartAttemptRequest(string AssessmentId, AssessmentMode? Mode);

public sealed record AttemptSessionResponse(
    Attempt Attempt,
    AssessmentDefinition Assessment,
    AttemptResults Results);

public sealed record SubmitAnswerRequest(
    string QuestionId,
    string? ChoiceId,
    IReadOnlyList<string>? ChoiceIds,
    string? FreeResponseText,
    bool? SelfCheckCorrect,
    decimal? NumericValue,
    string? CodeText,
    string? SymbolicLatex,
    SubmittedCircuitAnswer? CircuitAnswer = null)
{
    public SubmittedAnswer ToDomain()
    {
        return new SubmittedAnswer(
            QuestionId,
            ChoiceId,
            ChoiceIds ?? Array.Empty<string>(),
            FreeResponseText,
            SelfCheckCorrect,
            NumericValue)
        {
            CodeText = CodeText,
            SymbolicLatex = SymbolicLatex,
            CircuitAnswer = CircuitAnswer
        };
    }
}

public sealed record CommitGradeRequest(string AttemptId);

public sealed record BulkDeleteAttemptsRequest(IReadOnlyList<string>? AttemptIds);

public sealed record CreateAssessmentReportRequest(
    string AssessmentId,
    string AttemptId,
    string? ContextId,
    string Kind,
    string Comment);

public sealed record UpdateAssessmentReportStatusRequest(string Status);

public sealed record RevealRecallItemRequest(string? UserResponse);

public sealed record RateRecallItemRequest(RecallRating Rating);

public sealed record UpdateLearningSectionStateRequest(
    bool Visited,
    bool InteractionChanged,
    IReadOnlyDictionary<string, JsonElement>? ControlValues);

public sealed record UpdateDirectedProjectStepStateRequest(
    bool Visited,
    bool Completed,
    IReadOnlyList<string>? CompletedChecklistItemIds,
    string? Notes);

public sealed record GuidedProjectFileStateRequest(
    string Path,
    string Content);

public sealed record SaveGuidedProjectFilesRequest(
    IReadOnlyList<GuidedProjectFileStateRequest>? Files)
{
    public IReadOnlyList<GuidedProjectFileState> ToDomain()
    {
        return (Files ?? Array.Empty<GuidedProjectFileStateRequest>())
            .Select(file => new GuidedProjectFileState(file.Path, file.Content, false))
            .ToList();
    }
}

public sealed record SaveAssessmentRequest(
    string Id,
    string Title,
    AssessmentType AssessmentType,
    string CategoryId,
    string TopicId,
    AssessmentMode ModeDefault,
    bool RandomizeQuestions,
    int? AttemptQuestionCount,
    int? QuestionTimerSeconds,
    int? AssessmentTimerSeconds,
    QuestionSelectionDefinition? QuestionSelection,
    IReadOnlyList<QuestionDefinition>? Questions,
    IReadOnlyList<WorkedExampleDefinition>? WorkedExamples,
    GuidedProjectDefinition? GuidedProject,
    IReadOnlyList<RecallItemDefinition>? Items,
    ConceptLessonDefinition? Lesson,
    InteractiveExplorationDefinition? Exploration,
    DirectedProjectDefinition? DirectedProject,
    NavigationMetadata? Navigation = null)
{
    public AssessmentDefinition ToDomain()
    {
        return new AssessmentDefinition(
            1,
            Id.Trim(),
            Title.Trim(),
            AssessmentType,
            CategoryId.Trim(),
            TopicId.Trim(),
            ModeDefault,
            RandomizeQuestions,
            AttemptQuestionCount,
            QuestionTimerSeconds,
            AssessmentTimerSeconds,
            Questions ?? Array.Empty<QuestionDefinition>(),
            QuestionSelection)
        {
            WorkedExamples = WorkedExamples ?? Array.Empty<WorkedExampleDefinition>(),
            GuidedProject = GuidedProject,
            Items = Items ?? Array.Empty<RecallItemDefinition>(),
            Lesson = Lesson,
            Exploration = Exploration,
            DirectedProject = DirectedProject,
            Navigation = Navigation
        };
    }
}
