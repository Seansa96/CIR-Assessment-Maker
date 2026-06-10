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
    FreeResponse,
    NumericResponse,
    Code
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
    bool CommitScoredAttemptsAutomatically)
{
    public string CodeRunnerBaseUrl { get; init; } = "http://localhost:2000/api/v2";
    public int CodeRunnerCompileTimeoutMs { get; init; } = 10000;
    public int CodeRunnerRunTimeoutMs { get; init; } = 3000;
}

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
    string? Explanation,
    IReadOnlyList<MediaAsset> Media)
{
    public CodeQuestionDefinition? CodeQuestion { get; init; }
}

public sealed record ChoiceOption(
    string Id,
    string Text,
    IReadOnlyList<MediaAsset> Media);

public sealed record AnswerDefinition(
    string? ChoiceId,
    IReadOnlyList<string> ChoiceIds,
    string? Expected,
    string? GradingMode,
    decimal? NumericValue,
    decimal? NumericTolerance,
    IReadOnlyList<MediaAsset> Media);

public sealed record MediaAsset(
    string Type,
    string Src,
    string Alt,
    string? Caption);

public sealed record CodeQuestionDefinition(
    string Language,
    string FunctionName,
    string StarterCode,
    IReadOnlyList<CodeQuestionTest> Tests);

public sealed record CodeQuestionTest(
    string Input,
    string Expected);

public sealed record SubmittedAnswer(
    string QuestionId,
    string? ChoiceId,
    IReadOnlyList<string> ChoiceIds,
    string? FreeResponseText,
    bool? SelfCheckCorrect,
    decimal? NumericValue)
{
    public string? CodeText { get; init; }
}

public sealed record AnswerEvaluation(
    string QuestionId,
    bool IsCorrect,
    string? Explanation,
    string? ExpectedAnswer)
{
    public CodeFeedback? CodeFeedback { get; init; }
}

public sealed record CodeFeedback(
    IReadOnlyList<CodeTestResult> Tests,
    string? CompileOutput,
    string? RunOutput,
    string? Error);

public sealed record CodeTestResult(
    int Index,
    string Input,
    string Expected,
    string? Actual,
    bool Passed);

public sealed record AssessmentSummary(
    string Id,
    string Title,
    AssessmentType AssessmentType,
    string CategoryId,
    IReadOnlyList<string> SubcategoryIds,
    int QuestionCount);
