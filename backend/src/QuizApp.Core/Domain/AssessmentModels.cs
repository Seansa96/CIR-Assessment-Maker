namespace QuizApp.Core.Domain;

public enum AssessmentType
{
    Unknown,
    Quiz,
    Test
}

public enum AssessmentMode
{
    Practice,
    Scored
}

public enum QuestionType
{
    Unknown,
    MultipleChoice,
    SelectAll,
    FreeResponse
}

public enum QuestionOrderMode
{
    Randomized,
    Static
}

public sealed record Category(
    int SchemaVersion,
    string Id,
    string Title,
    IReadOnlyList<SubCategory> Subcategories);

public sealed record SubCategory(string Id, string Title);

public sealed record AppSettings(
    int SchemaVersion,
    AssessmentMode DefaultMode,
    QuestionOrderMode DefaultQuestionOrder,
    int DefaultQuizLength,
    int DefaultTestLength,
    int? QuestionTimerSeconds,
    int? AssessmentTimerSeconds,
    bool CommitScoredAttemptsAutomatically);

public sealed record AssessmentDefinition(
    int SchemaVersion,
    string Id,
    string Title,
    AssessmentType AssessmentType,
    string CategoryId,
    IReadOnlyList<string> SubcategoryIds,
    AssessmentMode ModeDefault,
    bool RandomizeQuestions,
    int? QuestionTimerSeconds,
    int? AssessmentTimerSeconds,
    IReadOnlyList<QuestionDefinition> Questions);

public sealed record QuestionDefinition(
    string Id,
    QuestionType Type,
    string Prompt,
    IReadOnlyList<ChoiceOption> Choices,
    AnswerDefinition Answer,
    string? Explanation);

public sealed record ChoiceOption(string Id, string Text);

public sealed record AnswerDefinition(
    string? ChoiceId,
    IReadOnlyList<string> ChoiceIds,
    string? Expected,
    string? GradingMode);

public sealed record SubmittedAnswer(
    string QuestionId,
    string? ChoiceId,
    IReadOnlyList<string> ChoiceIds,
    string? FreeResponseText,
    bool? SelfCheckCorrect);

public sealed record AnswerEvaluation(
    string QuestionId,
    bool IsCorrect,
    string? Explanation,
    string? ExpectedAnswer);

public sealed record AssessmentSummary(
    string Id,
    string Title,
    AssessmentType AssessmentType,
    string CategoryId,
    IReadOnlyList<string> SubcategoryIds,
    int QuestionCount);
