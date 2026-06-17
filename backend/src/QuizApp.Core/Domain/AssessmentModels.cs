namespace QuizApp.Core.Domain;

public enum AssessmentType
{
    Unknown,
    Quiz,
    Test,
    WorkedExample,
    GuidedProject,
    RecallDrill
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
    Code,
    SymbolicResponse
}

public enum QuestionOrderMode
{
    Randomized,
    Static
}

public enum RecallItemType
{
    Unknown,
    Typed,
    Symbolic,
    Flashcard,
    Cloze
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
    int? AttemptQuestionCount,
    int? QuestionTimerSeconds,
    int? AssessmentTimerSeconds,
    IReadOnlyList<QuestionDefinition> Questions)
{
    public IReadOnlyList<WorkedExampleDefinition> WorkedExamples { get; init; } = Array.Empty<WorkedExampleDefinition>();
    public GuidedProjectDefinition? GuidedProject { get; init; }
    public IReadOnlyList<RecallItemDefinition> Items { get; init; } = Array.Empty<RecallItemDefinition>();
}

public sealed record RecallItemDefinition(
    string Id,
    RecallItemType Type,
    string Prompt,
    RecallItemAnswerDefinition Answer,
    string? Explanation,
    IReadOnlyList<string> Tags);

public sealed record RecallItemAnswerDefinition(
    string? Expected,
    string? ExpectedLatex,
    IReadOnlyList<string> Aliases,
    IReadOnlyList<MediaAsset> Media);

public sealed record GuidedProjectDefinition(
    string Language,
    string Instructions,
    IReadOnlyList<GuidedProjectFileDefinition> Files,
    IReadOnlyList<GuidedProjectCheckDefinition> RequiredChecks,
    IReadOnlyList<GuidedProjectCheckDefinition> BonusChecks);

public sealed record GuidedProjectFileDefinition(
    string Path,
    string Content,
    bool ReadOnly);

public sealed record GuidedProjectCheckDefinition(
    string Id,
    string Title,
    string Description,
    string TestCode,
    IReadOnlyList<string> ExpectedOutputContains);

public sealed record GuidedProjectSession(
    string AttemptId,
    string AssessmentId,
    IReadOnlyList<GuidedProjectFileState> Files,
    IReadOnlyList<GuidedProjectCheckResult> CheckResults,
    DateTimeOffset UpdatedAt);

public sealed record GuidedProjectFileState(
    string Path,
    string Content,
    bool ReadOnly);

public sealed record GuidedProjectCheckResult(
    string CheckId,
    string Title,
    bool Required,
    bool Passed,
    string? Output,
    string? CompileOutput,
    string? Error,
    DateTimeOffset RanAt);

public sealed record GuidedProjectRunResult(
    GuidedProjectSession Session,
    bool AllRequiredPassed);

public sealed record WorkedExampleDefinition(
    string Id,
    string Title,
    string Problem,
    IReadOnlyList<WorkedExampleStepDefinition> Steps);

public sealed record WorkedExampleStepDefinition(
    string Id,
    string Title,
    string Instruction,
    string? Hint,
    QuestionDefinition Question);

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
    IReadOnlyList<MediaAsset> Media)
{
    public string? ExpectedLatex { get; init; }
    public string? EquivalenceMode { get; init; }
    public IReadOnlyList<string> Variables { get; init; } = Array.Empty<string>();
    public decimal? Tolerance { get; init; }
    public string? SymbolicExpectedLatex { get; init; }
    public string? SymbolicEquivalenceMode { get; init; }
    public IReadOnlyList<string> SymbolicVariables { get; init; } = Array.Empty<string>();
    public decimal? SymbolicTolerance { get; init; }
    public IReadOnlyList<string> KeyPoints { get; init; } = Array.Empty<string>();
}

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
    public string? SymbolicLatex { get; init; }
}

public sealed record AnswerEvaluation(
    string QuestionId,
    bool IsCorrect,
    string? Explanation,
    string? ExpectedAnswer)
{
    public CodeFeedback? CodeFeedback { get; init; }
    public SymbolicFeedback? SymbolicFeedback { get; init; }
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

public sealed record SymbolicFeedback(
    bool ParseSucceeded,
    string? NormalizedSubmitted,
    string? NormalizedExpected,
    string EquivalenceMode,
    string? Reason);

public sealed record AssessmentSummary(
    string Id,
    string Title,
    AssessmentType AssessmentType,
    string CategoryId,
    IReadOnlyList<string> SubcategoryIds,
    int QuestionCount,
    int AuthoredQuestionCount = 0,
    int? AttemptQuestionCount = null);
