using QuizApp.Core.Domain;

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
    string? SymbolicLatex)
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
            SymbolicLatex = SymbolicLatex
        };
    }
}

public sealed record CommitGradeRequest(string AttemptId);

public sealed record BulkDeleteAttemptsRequest(IReadOnlyList<string>? AttemptIds);

public sealed record RevealRecallItemRequest(string? UserResponse);

public sealed record RateRecallItemRequest(RecallRating Rating);

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
    IReadOnlyList<string>? SubcategoryIds,
    AssessmentMode ModeDefault,
    bool RandomizeQuestions,
    int? AttemptQuestionCount,
    int? QuestionTimerSeconds,
    int? AssessmentTimerSeconds,
    IReadOnlyList<QuestionDefinition>? Questions,
    IReadOnlyList<WorkedExampleDefinition>? WorkedExamples,
    GuidedProjectDefinition? GuidedProject,
    IReadOnlyList<RecallItemDefinition>? Items)
{
    public AssessmentDefinition ToDomain()
    {
        return new AssessmentDefinition(
            1,
            Id.Trim(),
            Title.Trim(),
            AssessmentType,
            CategoryId.Trim(),
            SubcategoryIds ?? Array.Empty<string>(),
            ModeDefault,
            RandomizeQuestions,
            AttemptQuestionCount,
            QuestionTimerSeconds,
            AssessmentTimerSeconds,
            Questions ?? Array.Empty<QuestionDefinition>())
        {
            WorkedExamples = WorkedExamples ?? Array.Empty<WorkedExampleDefinition>(),
            GuidedProject = GuidedProject,
            Items = Items ?? Array.Empty<RecallItemDefinition>()
        };
    }
}
