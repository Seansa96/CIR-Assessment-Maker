using QuizApp.Core.Domain;

namespace QuizApp.Api.Contracts;

public sealed record ValidateAssessmentFileRequest(string FileName);

public sealed record StartAttemptRequest(string AssessmentId, AssessmentMode? Mode);

public sealed record SubmitAnswerRequest(
    string QuestionId,
    string? ChoiceId,
    IReadOnlyList<string>? ChoiceIds,
    string? FreeResponseText,
    bool? SelfCheckCorrect)
{
    public SubmittedAnswer ToDomain()
    {
        return new SubmittedAnswer(
            QuestionId,
            ChoiceId,
            ChoiceIds ?? Array.Empty<string>(),
            FreeResponseText,
            SelfCheckCorrect);
    }
}

public sealed record CommitGradeRequest(string AttemptId);
