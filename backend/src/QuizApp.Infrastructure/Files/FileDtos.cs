namespace QuizApp.Infrastructure.Files;

public sealed class CategoryFileDto
{
    public int SchemaVersion { get; set; }
    public string? Id { get; set; }
    public string? Title { get; set; }
    public string? Description { get; set; }
    public string? AuthoringProfile { get; set; }
    public bool? DirectedProjectEligible { get; set; }
    public List<SubCategoryFileDto>? Subcategories { get; set; }
}

public sealed class SubCategoryFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public string? Description { get; set; }
    public List<string>? PrerequisiteIds { get; set; }
}

public sealed class SettingsFileDto
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

public sealed class AssessmentFileDto
{
    public int SchemaVersion { get; set; }
    public string? Id { get; set; }
    public string? Title { get; set; }
    public string? AssessmentType { get; set; }
    public string? CategoryId { get; set; }
    public string? TopicId { get; set; }
    public string? ModeDefault { get; set; }
    public bool? RandomizeQuestions { get; set; }
    public int? AttemptQuestionCount { get; set; }
    public int? QuestionTimerSeconds { get; set; }
    public int? AssessmentTimerSeconds { get; set; }
    public QuestionSelectionFileDto? QuestionSelection { get; set; }
    public List<QuestionFileDto>? Questions { get; set; }
    public List<WorkedExampleFileDto>? WorkedExamples { get; set; }
    public GuidedProjectFileDto? GuidedProject { get; set; }
    public List<RecallItemFileDto>? Items { get; set; }
    public GlossaryFileDto? Glossary { get; set; }
    public ConceptLessonFileDto? Lesson { get; set; }
    public InteractiveExplorationFileDto? Exploration { get; set; }
    public DirectedProjectFileDto? DirectedProject { get; set; }
    public SandboxFileDto? Sandbox { get; set; }
    public NavigationFileDto? Navigation { get; set; }
    public List<string>? Skills { get; set; }
    public AssessmentAuthoringFileDto? Authoring { get; set; }
}

public sealed class AssessmentAuthoringFileDto
{
    public string? VisualRequirement { get; set; }
    public string? VisualRationale { get; set; }
    public string? DifficultyTier { get; set; }
    public string? ExceptionReason { get; set; }
    public PhysicsModelAuthoringFileDto? PhysicsModel { get; set; }
}

public sealed class PhysicsModelAuthoringFileDto
{
    public string? ModelId { get; set; }
    public string? ModelRole { get; set; }
    public List<string>? RequiredRepresentations { get; set; }
}

public sealed class SandboxFileDto
{
    public string? Language { get; set; }
    public string? Image { get; set; }
    public string? InitialCommand { get; set; }
    public string? Instructions { get; set; }
    public bool? ReadOnlyFileSystem { get; set; }
    public List<SandboxWorkspaceFileDto>? Files { get; set; }
}

public sealed class SandboxWorkspaceFileDto
{
    public string? Path { get; set; }
    public string? Content { get; set; }
    public bool? ReadOnly { get; set; }
}

public sealed class QuestionSelectionFileDto
{
    public string? Mode { get; set; }
    public List<QuestionSelectionSlotFileDto>? Slots { get; set; }
}

public sealed class QuestionSelectionSlotFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public List<string>? QuestionIds { get; set; }
}

public sealed class ConceptLessonFileDto
{
    public string? Introduction { get; set; }
    public List<LearningSectionFileDto>? Sections { get; set; }
}

public sealed class GlossaryFileDto
{
    public string? Introduction { get; set; }
    public List<GlossarySectionFileDto>? Sections { get; set; }
}

public sealed class GlossarySectionFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public bool? Required { get; set; }
    public string? Content { get; set; }
    public List<GlossaryEntryFileDto>? Entries { get; set; }
}

public sealed class GlossaryEntryFileDto
{
    public string? Id { get; set; }
    public string? Term { get; set; }
    public string? Definition { get; set; }
    public string? Notation { get; set; }
    public List<string>? Examples { get; set; }
    public List<string>? Aliases { get; set; }
    public List<MediaFileDto>? Media { get; set; }
    public List<string>? Tags { get; set; }
    public List<RecallItemFileDto>? Drills { get; set; }
}

public sealed class LearningSectionFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public bool? Required { get; set; }
    public string? Content { get; set; }
    public List<MediaFileDto>? Media { get; set; }
    public QuestionFileDto? Check { get; set; }
}

public sealed class InteractiveExplorationFileDto
{
    public string? Introduction { get; set; }
    public List<ExplorationSectionFileDto>? Sections { get; set; }
}

public sealed class ExplorationSectionFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public bool? Required { get; set; }
    public string? Instruction { get; set; }
    public List<ExplorationControlFileDto>? Controls { get; set; }
    public List<ExplorationViewFileDto>? Views { get; set; }
    public QuestionFileDto? Check { get; set; }
}

public sealed class ExplorationControlFileDto
{
    public string? Id { get; set; }
    public string? Type { get; set; }
    public string? Label { get; set; }
    public decimal? Min { get; set; }
    public decimal? Max { get; set; }
    public decimal? Step { get; set; }
    public string? DefaultValue { get; set; }
    public List<ExplorationOptionFileDto>? Options { get; set; }
}

public sealed class ExplorationOptionFileDto
{
    public string? Value { get; set; }
    public string? Label { get; set; }
}

public sealed class ExplorationViewFileDto
{
    public string? Id { get; set; }
    public string? Type { get; set; }
    public string? Label { get; set; }
    public string? Expression { get; set; }
    public string? Condition { get; set; }
    public string? Content { get; set; }
    public string? InputControlId { get; set; }
    public decimal? Start { get; set; }
    public decimal? End { get; set; }
    public decimal? Step { get; set; }
}

public sealed class NavigationFileDto
{
    public string? LearningGoal { get; set; }
    public string? ActivityType { get; set; }
    public List<string>? Tags { get; set; }
}

// ─── Directed Project DTOs ───────────────────────────────────────────────────

public sealed class DirectedProjectFileDto
{
    public string? Summary { get; set; }
    public int? EstimatedTimeMinutes { get; set; }
    public DirectedProjectEnvironmentFileDto? Environment { get; set; }
    public List<string>? Outcomes { get; set; }
    public List<DirectedProjectResourceFileDto>? Resources { get; set; }
    public List<DirectedProjectPhaseFileDto>? Phases { get; set; }
}

public sealed class DirectedProjectEnvironmentFileDto
{
    public string? Name { get; set; }
    public List<string>? Platform { get; set; }
    public string? ToolVersion { get; set; }
    public List<string>? RequiredAccounts { get; set; }
    public List<string>? Prerequisites { get; set; }
    public List<DirectedProjectResourceFileDto>? InstallLinks { get; set; }
}

public sealed class DirectedProjectResourceFileDto
{
    public string? Label { get; set; }
    public string? Kind { get; set; }
    public string? Url { get; set; }
    public string? Target { get; set; }
}

public sealed class DirectedProjectPhaseFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public bool? Required { get; set; }
    public string? Goal { get; set; }
    public List<DirectedProjectStepFileDto>? Steps { get; set; }
}

public sealed class DirectedProjectStepFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public string? Instruction { get; set; }
    public string? ExpectedObservation { get; set; }
    public List<DirectedProjectCommandFileDto>? Commands { get; set; }
    public List<DirectedProjectFileReferenceFileDto>? Files { get; set; }
    public List<MediaFileDto>? Media { get; set; }
    public List<DirectedProjectChecklistItemFileDto>? Checklist { get; set; }
    public List<DirectedProjectTroubleshootingFileDto>? Troubleshooting { get; set; }
    public List<DirectedProjectResourceFileDto>? Resources { get; set; }
}

public sealed class DirectedProjectChecklistItemFileDto
{
    public string? Id { get; set; }
    public string? Text { get; set; }
}

public sealed class DirectedProjectTroubleshootingFileDto
{
    public string? Problem { get; set; }
    public string? Suggestion { get; set; }
}

public sealed class DirectedProjectCommandFileDto
{
    public string? Label { get; set; }
    public string? Command { get; set; }
    public string? Shell { get; set; }
    public string? WorkingDirectory { get; set; }
    public string? ExpectedOutput { get; set; }
    public string? Notes { get; set; }
}

public sealed class DirectedProjectFileReferenceFileDto
{
    public string? Path { get; set; }
    public string? Purpose { get; set; }
    public string? SuggestedContent { get; set; }
    public bool ReadOnly { get; set; }
}

// ─── Recall Item DTOs ────────────────────────────────────────────────────────

public sealed class RecallItemFileDto
{
    public string? Id { get; set; }
    public string? Type { get; set; }
    public string? Prompt { get; set; }
    public RecallItemAnswerFileDto? Answer { get; set; }
    public string? Explanation { get; set; }
    public List<string>? Tags { get; set; }
    public List<string>? Skills { get; set; }
    public List<ChoiceFileDto>? Choices { get; set; }
}

public sealed class RecallItemAnswerFileDto
{
    public string? Expected { get; set; }
    public string? ExpectedLatex { get; set; }
    public List<string>? Aliases { get; set; }
    public List<MediaFileDto>? Media { get; set; }
    public string? ChoiceId { get; set; }
}

public sealed class GuidedProjectFileDto
{
    public string? Language { get; set; }
    public string? ProjectKind { get; set; }
    public string? RunnerMode { get; set; }
    public string? Instructions { get; set; }
    public GuidedProjectWorkspaceFileDto? Workspace { get; set; }
    public List<GuidedProjectSourceFileDto>? Files { get; set; }
    public List<GuidedProjectFixtureFileDto>? Fixtures { get; set; }
    public List<GuidedProjectScenarioFileDto>? Scenarios { get; set; }
    public List<string>? Diagnostics { get; set; }
    public List<GuidedProjectCheckFileDto>? RequiredChecks { get; set; }
    public List<GuidedProjectCheckFileDto>? BonusChecks { get; set; }
}

public sealed class GuidedProjectSourceFileDto
{
    public string? Path { get; set; }
    public string? Content { get; set; }
    public bool ReadOnly { get; set; }
}

public sealed class GuidedProjectFixtureFileDto
{
    public string? Path { get; set; }
    public string? Content { get; set; }
    public bool ReadOnly { get; set; }
}

public sealed class GuidedProjectScenarioFileDto
{
    public string? Id { get; set; }
    public string? Type { get; set; }
    public string? LearnerRole { get; set; }
    public List<GuidedProjectNetworkEventFileDto>? Events { get; set; }
}

public sealed class GuidedProjectNetworkEventFileDto
{
    public string? Type { get; set; }
    public string? Peer { get; set; }
    public string? From { get; set; }
    public string? Text { get; set; }
}

public sealed class GuidedProjectWorkspaceFileDto
{
    public string? BuildProfile { get; set; }
    public string? EntryPoint { get; set; }
    public string? LabProfile { get; set; }
    public List<string>? SourceGlobs { get; set; }
    public List<string>? IncludePaths { get; set; }
    public List<string>? WritablePaths { get; set; }
    public List<string>? AllowedBaseImages { get; set; }
}

public sealed class GuidedProjectCheckFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public string? Description { get; set; }
    public string? TestCode { get; set; }
    public List<string>? ExpectedOutputContains { get; set; }
    public GuidedProjectCheckRunFileDto? Run { get; set; }
    public GuidedProjectCheckExpectFileDto? Expect { get; set; }
}

public sealed class GuidedProjectCheckRunFileDto
{
    public List<string>? Arguments { get; set; }
    public string? Stdin { get; set; }
    public string? Scenario { get; set; }
}

public sealed class GuidedProjectCheckExpectFileDto
{
    public List<string>? StdoutContains { get; set; }
    public List<GuidedProjectFileExpectationFileDto>? Files { get; set; }
}

public sealed class GuidedProjectFileExpectationFileDto
{
    public string? Path { get; set; }
    public List<string>? TextContains { get; set; }
}

public sealed class WorkedExampleFileDto
{
    public string? Id { get; set; }
    public string? Title { get; set; }
    public string? Problem { get; set; }
    public List<WorkedExampleStepFileDto>? Steps { get; set; }
}

public sealed class WorkedExampleStepFileDto
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
    public string? ExecutionMode { get; set; }
    public string? StarterCode { get; set; }
    public List<CodeQuestionTestFileDto>? Tests { get; set; }
    public List<IssueSignalFileDto>? IssueSignals { get; set; }
}

public sealed class QuestionFileDto
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
    public string? ExecutionMode { get; set; }
    public string? StarterCode { get; set; }
    public List<CodeQuestionTestFileDto>? Tests { get; set; }
    public CircuitQuestionFileDto? CircuitQuestion { get; set; }
    public GraphingQuestionFileDto? GraphingQuestion { get; set; }
    public List<string>? Skills { get; set; }
    public List<string>? DifficultyDimensions { get; set; }
    public List<string>? SubjectDifficultyTags { get; set; }
    public string? DifficultyEvidence { get; set; }
    public List<string>? PrerequisiteObjectiveIds { get; set; }
    public List<string>? ExtensionObjectiveIds { get; set; }
    public List<MultipartPartFileDto>? Parts { get; set; }
    public List<IssueSignalFileDto>? IssueSignals { get; set; }
}

public sealed class MultipartPartFileDto
{
    public string? Id { get; set; }
    public string? Type { get; set; }
    public string? Prompt { get; set; }
    public List<ChoiceFileDto>? Choices { get; set; }
    public AnswerFileDto? Answer { get; set; }
    public string? Explanation { get; set; }
    public List<MediaFileDto>? Media { get; set; }
    public List<string>? Skills { get; set; }
    public List<IssueSignalFileDto>? IssueSignals { get; set; }
}

public sealed class ChoiceFileDto
{
    public string? Id { get; set; }
    public string? Text { get; set; }
    public List<MediaFileDto>? Media { get; set; }
    public List<IssueSignalFileDto>? IssueSignals { get; set; }
}

public sealed class IssueSignalFileDto
{
    public string? Id { get; set; }
    public List<string>? Domains { get; set; }
}

public sealed class AnswerFileDto
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
    public GraphingAnswerFileDto? GraphingAnswer { get; set; }
}

public sealed class MediaFileDto
{
    public string? Type { get; set; }
    public string? Src { get; set; }
    public string? Alt { get; set; }
    public string? Caption { get; set; }
}

public sealed class CodeQuestionTestFileDto
{
    public string? Input { get; set; }
    public string? Expected { get; set; }
}

public sealed class CircuitQuestionFileDto
{
    public int SchemaVersion { get; set; }
    public int CatalogVersion { get; set; }
    public string? InteractionMode { get; set; }
    public List<string>? PaletteSymbolIds { get; set; }
    public List<string>? EditableProperties { get; set; }
    public CircuitDiagramFileDto? Diagram { get; set; }
}

public sealed class CircuitDiagramFileDto
{
    public int Width { get; set; }
    public int Height { get; set; }
    public List<CircuitComponentInstanceFileDto>? Components { get; set; }
    public List<CircuitNodeFileDto>? Nodes { get; set; }
    public List<CircuitWireFileDto>? Wires { get; set; }
    public List<CircuitAnnotationFileDto>? Annotations { get; set; }
}

public sealed class CircuitComponentInstanceFileDto
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

public sealed class CircuitNodeFileDto
{
    public string? Id { get; set; }
    public string? Label { get; set; }
    public decimal? X { get; set; }
    public decimal? Y { get; set; }
}

public sealed class CircuitWireFileDto
{
    public string? Id { get; set; }
    public string? SourceId { get; set; }
    public string? TargetId { get; set; }
    public List<CircuitPointFileDto>? RoutePoints { get; set; }
}

public sealed class CircuitPointFileDto
{
    public decimal X { get; set; }
    public decimal Y { get; set; }
}

public sealed class CircuitAnnotationFileDto
{
    public string? Id { get; set; }
    public string? Type { get; set; }
    public string? Text { get; set; }
    public decimal X { get; set; }
    public decimal Y { get; set; }
}

public sealed class CircuitAnswerFileDto
{
    public CircuitTopologyFileDto? Topology { get; set; }
    public List<string>? SelectedTargetIds { get; set; }
    public CircuitMeterPlacementFileDto? MeterPlacement { get; set; }
    public Dictionary<string, ExpectedValueFileDto>? ExpectedValues { get; set; }
}

public sealed class CircuitTopologyFileDto
{
    public List<RequiredComponentFileDto>? RequiredComponents { get; set; }
    public string? ConnectionMode { get; set; }
}

public sealed class RequiredComponentFileDto
{
    public string? SymbolId { get; set; }
    public int Count { get; set; }
}

public sealed class CircuitMeterPlacementFileDto
{
    public string? MeterType { get; set; }
    public string? TargetBranchId { get; set; }
    public List<string>? TargetNodeIds { get; set; }
    public bool? RequirePolarity { get; set; }
    public string? PositiveTerminalId { get; set; }
    public string? NegativeTerminalId { get; set; }
}

public sealed class ExpectedValueFileDto
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

// ─── Graphing DTOs ───────────────────────────────────────────────────────────

public sealed class GraphingQuestionFileDto
{
    public string? GridType { get; set; }
    public string? InteractionMode { get; set; }
}


public sealed class GraphingAnswerFileDto
{
    public List<ExpectedGraphFeatureFileDto>? Features { get; set; }
}

public sealed class ExpectedGraphFeatureFileDto
{
    public string? Type { get; set; }
    public decimal? X { get; set; }
    public decimal? Y { get; set; }
    public decimal? Value { get; set; }
    public string? StringValue { get; set; }
    public decimal? Tolerance { get; set; }
    public decimal? Weight { get; set; }
}
