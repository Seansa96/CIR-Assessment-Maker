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

public sealed record SaveAssessmentRequest(
    string Id,
    string Title,
    AssessmentType AssessmentType,
    string CategoryId,
    IReadOnlyList<string>? SubcategoryIds,
    AssessmentMode ModeDefault,
    bool RandomizeQuestions,
    int? QuestionTimerSeconds,
    int? AssessmentTimerSeconds,
    IReadOnlyList<QuestionDefinition>? Questions,
    IReadOnlyList<WorkedExampleDefinition>? WorkedExamples)
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
            QuestionTimerSeconds,
            AssessmentTimerSeconds,
            Questions ?? Array.Empty<QuestionDefinition>())
        {
            WorkedExamples = WorkedExamples ?? Array.Empty<WorkedExampleDefinition>()
        };
    }
}
