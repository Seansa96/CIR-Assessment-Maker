namespace QuizApp.Core.Domain;

public enum AttemptStatus
{
    Unknown,
    InProgress,
    Paused,
    Completed,
    Abandoned
}

public sealed record Attempt(
    string Id,
    string AssessmentId,
    AssessmentMode Mode,
    AttemptStatus Status,
    IReadOnlyList<string> QuestionOrder,
    IReadOnlyList<AttemptAnswer> Answers,
    DateTimeOffset StartedAt,
    DateTimeOffset? PausedAt,
    DateTimeOffset? CompletedAt,
    DateTimeOffset? AbandonedAt);

public sealed record AttemptAnswer(
    string QuestionId,
    SubmittedAnswer Answer,
    AnswerEvaluation? Evaluation,
    DateTimeOffset SubmittedAt);

public sealed record AttemptResults(
    string AttemptId,
    string AssessmentId,
    string AssessmentTitle,
    AssessmentMode Mode,
    AttemptStatus Status,
    int CorrectCount,
    int TotalQuestions,
    decimal PercentScore,
    bool IsComplete,
    IReadOnlyList<QuestionResult> Questions);

public sealed record QuestionResult(
    string QuestionId,
    string Prompt,
    QuestionType Type,
    IReadOnlyList<MediaAsset> Media,
    SubmittedAnswer? SubmittedAnswer,
    bool? IsCorrect,
    string? Explanation,
    string? ExpectedAnswer,
    CodeFeedback? CodeFeedback);

public sealed record GradeLogEntry(
    string Id,
    string AttemptId,
    string AssessmentId,
    string AssessmentTitle,
    AssessmentMode Mode,
    int CorrectCount,
    int TotalQuestions,
    decimal PercentScore,
    DateTimeOffset CommittedAt);

public sealed record GradeLogSummary(
    int EntryCount,
    decimal? AveragePercentScore,
    IReadOnlyList<GradeLogEntry> Entries);
