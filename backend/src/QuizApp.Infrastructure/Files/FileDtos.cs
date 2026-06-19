namespace QuizApp.Infrastructure.Files;

internal sealed class CategoryFileDto
{
    public int SchemaVersion { get; set; }
    public string? Id { get; set; }
    public string? Title { get; set; }
    public string? Description { get; set; }
    public List<SubCategoryFileDto>? Subcategories { get; set; }
}

internal sealed class SubCategoryFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public string? Description { get; set; }
}

internal sealed class SettingsFileDto
{
    public int SchemaVersion { get; set; } = 1;
    public string? DefaultMode { get; set; }
    public string? DefaultQuestionOrder { get; set; }
    public int DefaultQuizLength { get; set; }
    public int DefaultTestLength { get; set; }
    public int? QuestionTimerSeconds { get; set; }
    public int? AssessmentTimerSeconds { get; set; }
    public bool CommitScoredAttemptsAutomatically { get; set; }
    public string? CodeRunnerBaseUrl { get; set; }
    public int? CodeRunnerCompileTimeoutMs { get; set; }
    public int? CodeRunnerRunTimeoutMs { get; set; }
}

internal sealed class AssessmentFileDto
{
    public int SchemaVersion { get; set; }
    public string? Id { get; set; }
    public string? Title { get; set; }
    public string? AssessmentType { get; set; }
    public string? CategoryId { get; set; }
    public List<string>? SubcategoryIds { get; set; }
    public string? ModeDefault { get; set; }
    public bool? RandomizeQuestions { get; set; }
    public int? AttemptQuestionCount { get; set; }
    public int? QuestionTimerSeconds { get; set; }
    public int? AssessmentTimerSeconds { get; set; }
    public List<QuestionFileDto>? Questions { get; set; }
    public List<WorkedExampleFileDto>? WorkedExamples { get; set; }
    public GuidedProjectFileDto? GuidedProject { get; set; }
    public List<RecallItemFileDto>? Items { get; set; }
    public NavigationFileDto? Navigation { get; set; }
}

internal sealed class NavigationFileDto
{
    public string? LearningGoal { get; set; }
    public string? ActivityType { get; set; }
    public List<string>? Tags { get; set; }
}


internal sealed class RecallItemFileDto
{
    public string? Id { get; set; }
    public string? Type { get; set; }
    public string? Prompt { get; set; }
    public RecallItemAnswerFileDto? Answer { get; set; }
    public string? Explanation { get; set; }
    public List<string>? Tags { get; set; }
}

internal sealed class RecallItemAnswerFileDto
{
    public string? Expected { get; set; }
    public string? ExpectedLatex { get; set; }
    public List<string>? Aliases { get; set; }
    public List<MediaFileDto>? Media { get; set; }
}

internal sealed class GuidedProjectFileDto
{
    public string? Language { get; set; }
    public string? Instructions { get; set; }
    public List<GuidedProjectSourceFileDto>? Files { get; set; }
    public List<GuidedProjectCheckFileDto>? RequiredChecks { get; set; }
    public List<GuidedProjectCheckFileDto>? BonusChecks { get; set; }
}

internal sealed class GuidedProjectSourceFileDto
{
    public string? Path { get; set; }
    public string? Content { get; set; }
    public bool ReadOnly { get; set; }
}

internal sealed class GuidedProjectCheckFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public string? Description { get; set; }
    public string? TestCode { get; set; }
    public List<string>? ExpectedOutputContains { get; set; }
}

internal sealed class WorkedExampleFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public string? Problem { get; set; }
    public List<WorkedExampleStepFileDto>? Steps { get; set; }
}

internal sealed class WorkedExampleStepFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public string? Instruction { get; set; }
    public string? Hint { get; set; }
    public string? Type { get; set; }
    public string? Prompt { get; set; }
    public List<ChoiceFileDto>? Choices { get; set; }
    public AnswerFileDto? Answer { get; set; }
    public string? Explanation { get; set; }
    public List<MediaFileDto>? Media { get; set; }
    public string? Language { get; set; }
    public string? FunctionName { get; set; }
    public string? StarterCode { get; set; }
    public List<CodeQuestionTestFileDto>? Tests { get; set; }
}

internal sealed class QuestionFileDto
{
    public string? Id { get; set; }
    public string? Type { get; set; }
    public string? Prompt { get; set; }
    public List<ChoiceFileDto>? Choices { get; set; }
    public AnswerFileDto? Answer { get; set; }
    public string? Explanation { get; set; }
    public List<MediaFileDto>? Media { get; set; }
    public string? Language { get; set; }
    public string? FunctionName { get; set; }
    public string? StarterCode { get; set; }
    public List<CodeQuestionTestFileDto>? Tests { get; set; }
    public CircuitQuestionFileDto? CircuitQuestion { get; set; }
}

internal sealed class ChoiceFileDto
{
    public string? Id { get; set; }
    public string? Text { get; set; }
    public List<MediaFileDto>? Media { get; set; }
}

internal sealed class AnswerFileDto
{
    public string? ChoiceId { get; set; }
    public List<string>? ChoiceIds { get; set; }
    public string? Expected { get; set; }
    public string? GradingMode { get; set; }
    public string? ExpectedLatex { get; set; }
    public string? EquivalenceMode { get; set; }
    public List<string>? Variables { get; set; }
    public decimal? Value { get; set; }
    public decimal? Tolerance { get; set; }
    public List<MediaFileDto>? Media { get; set; }
    public List<string>? KeyPoints { get; set; }
    public CircuitAnswerFileDto? CircuitAnswer { get; set; }
}

internal sealed class MediaFileDto
{
    public string? Type { get; set; }
    public string? Src { get; set; }
    public string? Alt { get; set; }
    public string? Caption { get; set; }
}

internal sealed class CodeQuestionTestFileDto
{
    public string? Input { get; set; }
    public string? Expected { get; set; }
}

internal sealed class CircuitQuestionFileDto
{
    public int SchemaVersion { get; set; }
    public int CatalogVersion { get; set; }
    public string? InteractionMode { get; set; }
    public List<string>? PaletteSymbolIds { get; set; }
    public List<string>? EditableProperties { get; set; }
    public CircuitDiagramFileDto? Diagram { get; set; }
}

internal sealed class CircuitDiagramFileDto
{
    public int Width { get; set; }
    public int Height { get; set; }
    public List<CircuitComponentInstanceFileDto>? Components { get; set; }
    public List<CircuitNodeFileDto>? Nodes { get; set; }
    public List<CircuitWireFileDto>? Wires { get; set; }
    public List<CircuitAnnotationFileDto>? Annotations { get; set; }
}

internal sealed class CircuitComponentInstanceFileDto
{
    public string? Id { get; set; }
    public string? SymbolId { get; set; }
    public decimal X { get; set; }
    public decimal Y { get; set; }
    public decimal Rotation { get; set; }
    public string? Value { get; set; }
    public string? Label { get; set; }
    public Dictionary<string, string>? PropertyOverrides { get; set; }
}

internal sealed class CircuitNodeFileDto
{
    public string? Id { get; set; }
    public string? Label { get; set; }
    public decimal? X { get; set; }
    public decimal? Y { get; set; }
}

internal sealed class CircuitWireFileDto
{
    public string? Id { get; set; }
    public string? SourceId { get; set; }
    public string? TargetId { get; set; }
    public List<CircuitPointFileDto>? RoutePoints { get; set; }
}

internal sealed class CircuitPointFileDto
{
    public decimal X { get; set; }
    public decimal Y { get; set; }
}

internal sealed class CircuitAnnotationFileDto
{
    public string? Id { get; set; }
    public string? Type { get; set; }
    public string? Text { get; set; }
    public decimal X { get; set; }
    public decimal Y { get; set; }
}

internal sealed class CircuitAnswerFileDto
{
    public CircuitTopologyFileDto? Topology { get; set; }
    public List<string>? SelectedTargetIds { get; set; }
    public CircuitMeterPlacementFileDto? MeterPlacement { get; set; }
    public Dictionary<string, ExpectedValueFileDto>? ExpectedValues { get; set; }
}

internal sealed class CircuitTopologyFileDto
{
    public List<RequiredComponentFileDto>? RequiredComponents { get; set; }
    public string? ConnectionMode { get; set; }
}

internal sealed class RequiredComponentFileDto
{
    public string? SymbolId { get; set; }
    public int Count { get; set; }
}

internal sealed class CircuitMeterPlacementFileDto
{
    public string? MeterType { get; set; }
    public string? TargetBranchId { get; set; }
    public List<string>? TargetNodeIds { get; set; }
    public bool? RequirePolarity { get; set; }
    public string? PositiveTerminalId { get; set; }
    public string? NegativeTerminalId { get; set; }
}

internal sealed class ExpectedValueFileDto
{
    public string? Mode { get; set; }
    public string? ExpectedText { get; set; }
    public decimal? NumericValue { get; set; }
    public decimal? NumericTolerance { get; set; }
    public string? SymbolicExpectedLatex { get; set; }
    public string? SymbolicEquivalenceMode { get; set; }
    public List<string>? SymbolicVariables { get; set; }
    public decimal? SymbolicTolerance { get; set; }
}
