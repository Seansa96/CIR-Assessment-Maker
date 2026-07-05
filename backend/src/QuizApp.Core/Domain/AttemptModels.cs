using System.Text.Json;

namespace QuizApp.Core.Domain;

public enum AttemptStatus
{
    Unknown,
    InProgress,
    Paused,
    Completed,
    Abandoned
}

public enum RecallRating
{
    Unknown,
    Easy,
    Correct,
    NeedsReview,
    ForgotCompletely
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
    DateTimeOffset? AbandonedAt)
{
    public IReadOnlyList<RecallItemAttempt> RecallItems { get; init; } = Array.Empty<RecallItemAttempt>();
    public IReadOnlyList<LearningSectionAttempt> LearningSections { get; init; } = Array.Empty<LearningSectionAttempt>();
}

public sealed record LearningSectionAttempt(
    string SectionId,
    bool Visited,
    bool InteractionChanged,
    bool Completed,
    IReadOnlyDictionary<string, JsonElement> ControlValues,
    DateTimeOffset UpdatedAt);

public sealed record AttemptAnswer(
    string QuestionId,
    SubmittedAnswer Answer,
    AnswerEvaluation? Evaluation,
    DateTimeOffset SubmittedAt,
    bool? UserOverriddenCorrect = null);

public sealed record RecallItemAttempt(
    string ItemId,
    string? UserResponse,
    bool AnswerRevealed,
    RecallRating Rating,
    DateTimeOffset UpdatedAt);

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
    IReadOnlyList<QuestionResult> Questions)
{
    public AssessmentType AssessmentType { get; init; } = AssessmentType.Unknown;
    public decimal EarnedPoints { get; init; }
    public decimal PossiblePoints { get; init; }
    public bool HasPendingSelfChecks { get; init; }
    public RecallDrillSummary? RecallSummary { get; init; }
    public IReadOnlyList<RecallItemResult> RecallItems { get; init; } = Array.Empty<RecallItemResult>();
    public IReadOnlyList<LearningSectionResult> LearningSections { get; init; } = Array.Empty<LearningSectionResult>();
}

public sealed record LearningSectionResult(
    string SectionId,
    string Title,
    bool Required,
    bool Visited,
    bool InteractionChanged,
    bool Completed,
    bool Unlocked,
    IReadOnlyDictionary<string, JsonElement> ControlValues,
    QuestionResult? Check);

public sealed record RecallDrillSummary(
    int ItemsReviewed,
    int EasyCount,
    int CorrectCount,
    int NeedsReviewCount,
    int ForgotCompletelyCount,
    IReadOnlyList<string> WeakTags);

public sealed record RecallItemResult(
    string ItemId,
    RecallItemType Type,
    string Prompt,
    string? UserResponse,
    bool AnswerRevealed,
    RecallRating Rating,
    string? Expected,
    string? ExpectedLatex,
    IReadOnlyList<string> Aliases,
    string? Explanation,
    IReadOnlyList<string> Tags,
    IReadOnlyList<MediaAsset> Media);

public sealed record QuestionResult(
    string QuestionId,
    string Prompt,
    QuestionType Type,
    IReadOnlyList<MediaAsset> Media,
    SubmittedAnswer? SubmittedAnswer,
    bool? IsCorrect,
    string? Explanation,
    string? ExpectedAnswer,
    CodeFeedback? CodeFeedback,
    SymbolicFeedback? SymbolicFeedback,
    CircuitFeedback? CircuitFeedback = null,
    bool? UserOverriddenCorrect = null)
{
    public string? Title { get; init; }
    public string? Instruction { get; init; }
    public string? Hint { get; init; }
    public string? ExampleId { get; init; }
    public string? ExampleTitle { get; init; }
    public string? Problem { get; init; }
    public IReadOnlyList<string> KeyPoints { get; init; } = Array.Empty<string>();
    public bool IsPendingSelfCheck { get; init; }
    public decimal EarnedPoints { get; init; }
    public decimal PossiblePoints { get; init; }
    public IReadOnlyList<QuestionResult> PartResults { get; init; } = Array.Empty<QuestionResult>();
}

public sealed record GradeLogEntry(
    string Id,
    string AttemptId,
    string AssessmentId,
    string AssessmentTitle,
    AssessmentMode Mode,
    int CorrectCount,
    int TotalQuestions,
    decimal PercentScore,
    DateTimeOffset CommittedAt)
{
    public decimal EarnedPoints { get; init; }
    public decimal PossiblePoints { get; init; }
}

public sealed record GradeLogSummary(
    int EntryCount,
    decimal? AveragePercentScore,
    IReadOnlyList<GradeLogEntry> Entries);
