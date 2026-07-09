namespace QuizApp.Core.Domain;

public enum AssessmentType
{
    Unknown,
    Quiz,
    Test,
    WorkedExample,
    GuidedProject,
    RecallDrill,
    ConceptLesson,
    InteractiveExploration,
    DirectedProject
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
    SymbolicResponse,
    Circuit,
    Multipart,
    GraphingResponse
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
    IReadOnlyList<SubCategory> Subcategories,
    string? Description = null);

public sealed record SubCategory(string Id, string Title, string? Description = null);

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

public sealed record NavigationMetadata(
    string? LearningGoal,
    string? ActivityType,
    IReadOnlyList<string> Tags);

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
    public ConceptLessonDefinition? Lesson { get; init; }
    public InteractiveExplorationDefinition? Exploration { get; init; }
    public DirectedProjectDefinition? DirectedProject { get; init; }
    public NavigationMetadata? Navigation { get; init; }
    public IReadOnlyList<string> Skills { get; init; } = Array.Empty<string>();
}

public sealed record ConceptLessonDefinition(
    string Introduction,
    IReadOnlyList<LearningSectionDefinition> Sections);

public sealed record InteractiveExplorationDefinition(
    string Introduction,
    IReadOnlyList<ExplorationSectionDefinition> Sections);

public sealed record LearningSectionDefinition(
    string Id,
    string Title,
    bool Required,
    string Content,
    IReadOnlyList<MediaAsset> Media,
    QuestionDefinition? Check);

public sealed record ExplorationSectionDefinition(
    string Id,
    string Title,
    bool Required,
    string Instruction,
    IReadOnlyList<ExplorationControlDefinition> Controls,
    IReadOnlyList<ExplorationViewDefinition> Views,
    QuestionDefinition? Check);

public sealed record ExplorationControlDefinition(
    string Id,
    string Type,
    string Label,
    decimal? Min = null,
    decimal? Max = null,
    decimal? Step = null,
    string? DefaultValue = null,
    IReadOnlyList<ExplorationOptionDefinition>? Options = null);

public sealed record ExplorationOptionDefinition(string Value, string Label);

public sealed record ExplorationViewDefinition(
    string Id,
    string Type,
    string Label,
    string? Expression = null,
    string? Condition = null,
    string? Content = null,
    string? InputControlId = null,
    decimal? Start = null,
    decimal? End = null,
    decimal? Step = null);

public sealed record RecallItemDefinition(
    string Id,
    RecallItemType Type,
    string Prompt,
    RecallItemAnswerDefinition Answer,
    string? Explanation,
    IReadOnlyList<string> Tags)
{
    public IReadOnlyList<string> Skills { get; init; } = Array.Empty<string>();
}

public sealed record RecallItemAnswerDefinition(
    string? Expected,
    string? ExpectedLatex,
    IReadOnlyList<string> Aliases,
    IReadOnlyList<MediaAsset> Media);

public sealed record GuidedProjectDefinition(
    string Language,
    string? ProjectKind,
    string? RunnerMode,
    string Instructions,
    GuidedProjectWorkspaceDefinition? Workspace,
    IReadOnlyList<GuidedProjectFileDefinition> Files,
    IReadOnlyList<GuidedProjectFixtureDefinition> Fixtures,
    IReadOnlyList<GuidedProjectScenarioDefinition> Scenarios,
    IReadOnlyList<string> Diagnostics,
    IReadOnlyList<GuidedProjectCheckDefinition> RequiredChecks,
    IReadOnlyList<GuidedProjectCheckDefinition> BonusChecks);

public sealed record GuidedProjectWorkspaceDefinition(
    string? BuildProfile,
    string? EntryPoint,
    string? LabProfile,
    IReadOnlyList<string> SourceGlobs,
    IReadOnlyList<string> IncludePaths,
    IReadOnlyList<string> WritablePaths,
    IReadOnlyList<string> AllowedBaseImages);

public sealed record GuidedProjectFixtureDefinition(
    string Path,
    string Content,
    bool ReadOnly);

public sealed record GuidedProjectScenarioDefinition(
    string Id,
    string Type,
    string? LearnerRole,
    IReadOnlyList<GuidedProjectNetworkEventDefinition> Events);

public sealed record GuidedProjectNetworkEventDefinition(
    string Type,
    string? Peer,
    string? From,
    string? Text);

public sealed record GuidedProjectFileDefinition(
    string Path,
    string Content,
    bool ReadOnly);

public sealed record GuidedProjectCheckDefinition(
    string Id,
    string Title,
    string Description,
    string? TestCode,
    IReadOnlyList<string>? ExpectedOutputContains,
    GuidedProjectCheckRunDefinition? Run,
    GuidedProjectCheckExpectDefinition? Expect);

public sealed record GuidedProjectCheckRunDefinition(
    IReadOnlyList<string> Arguments,
    string? Stdin,
    string? Scenario);

public sealed record GuidedProjectCheckExpectDefinition(
    IReadOnlyList<string> StdoutContains,
    IReadOnlyList<GuidedProjectCheckFileExpectation> Files);

public sealed record GuidedProjectCheckFileExpectation(
    string Path,
    IReadOnlyList<string> TextContains);

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
    DateTimeOffset RanAt)
{
    public GuidedProjectBuildStageResult? Build { get; init; }
    public GuidedProjectProcessStageResult? Run { get; init; }
    public IReadOnlyList<GuidedProjectFileAssertionResult>? Files { get; init; }
    public IReadOnlyList<GuidedProjectNetworkEventResult>? NetworkEvents { get; init; }
    public IReadOnlyList<GuidedProjectDiagnosticFinding>? Diagnostics { get; init; }
    public string? FailureReason { get; init; }
}

public sealed record GuidedProjectBuildStageResult(
    bool Succeeded,
    string? Output);

public sealed record GuidedProjectProcessStageResult(
    bool Succeeded,
    string? Stdout,
    string? Stderr,
    int? ExitCode);

public sealed record GuidedProjectFileAssertionResult(
    string Path,
    bool Passed,
    string? ActualText,
    string? Error);

public sealed record GuidedProjectNetworkEventResult(
    string Type,
    bool Passed,
    string? ExpectedText,
    string? ActualText,
    string? Error);

public sealed record GuidedProjectDiagnosticFinding(
    string Category,
    string Message,
    string? FilePath,
    int? LineNumber);

public sealed record GuidedProjectRunResult(
    GuidedProjectSession Session,
    bool AllRequiredPassed);

// ─── Directed Project ──────────────────────────────────────────────────────

public sealed record DirectedProjectDefinition(
    string Summary,
    IReadOnlyList<string> Outcomes,
    IReadOnlyList<DirectedProjectPhaseDefinition> Phases)
{
    public int? EstimatedTimeMinutes { get; init; }
    public DirectedProjectEnvironmentDefinition? Environment { get; init; }
    public IReadOnlyList<DirectedProjectResourceDefinition> Resources { get; init; } = Array.Empty<DirectedProjectResourceDefinition>();
}

public sealed record DirectedProjectEnvironmentDefinition(
    string Name)
{
    public IReadOnlyList<string> Platform { get; init; } = Array.Empty<string>();
    public string? ToolVersion { get; init; }
    public IReadOnlyList<string> RequiredAccounts { get; init; } = Array.Empty<string>();
    public IReadOnlyList<string> Prerequisites { get; init; } = Array.Empty<string>();
    public IReadOnlyList<DirectedProjectResourceDefinition> InstallLinks { get; init; } = Array.Empty<DirectedProjectResourceDefinition>();
}

public sealed record DirectedProjectResourceDefinition(
    string Label,
    string Kind)
{
    /// <summary>URL for external resources.</summary>
    public string? Url { get; init; }
    /// <summary>Category/subcategory target for internal resources.</summary>
    public string? Target { get; init; }
}

public sealed record DirectedProjectPhaseDefinition(
    string Id,
    string Title,
    bool Required,
    IReadOnlyList<DirectedProjectStepDefinition> Steps)
{
    public string? Goal { get; init; }
}

public sealed record DirectedProjectStepDefinition(
    string Id,
    string Title,
    string Instruction)
{
    public string? ExpectedObservation { get; init; }
    public IReadOnlyList<DirectedProjectCommandDefinition> Commands { get; init; } = Array.Empty<DirectedProjectCommandDefinition>();
    public IReadOnlyList<DirectedProjectFileDefinition> Files { get; init; } = Array.Empty<DirectedProjectFileDefinition>();
    public IReadOnlyList<MediaAsset> Media { get; init; } = Array.Empty<MediaAsset>();
    public IReadOnlyList<DirectedProjectChecklistItemDefinition> Checklist { get; init; } = Array.Empty<DirectedProjectChecklistItemDefinition>();
    public IReadOnlyList<DirectedProjectTroubleshootingDefinition> Troubleshooting { get; init; } = Array.Empty<DirectedProjectTroubleshootingDefinition>();
    public IReadOnlyList<DirectedProjectResourceDefinition> Resources { get; init; } = Array.Empty<DirectedProjectResourceDefinition>();
    public string? NotesPrompt { get; init; }
}

public sealed record DirectedProjectChecklistItemDefinition(
    string Id,
    string Text);

public sealed record DirectedProjectTroubleshootingDefinition(
    string Problem,
    string Suggestion);

public sealed record DirectedProjectCommandDefinition(
    string Label,
    string Command)
{
    public string? Shell { get; init; }
    public string? WorkingDirectory { get; init; }
    public string? ExpectedOutput { get; init; }
    public string? Notes { get; init; }
}

public sealed record DirectedProjectFileDefinition(
    string Path,
    string Purpose)
{
    public string? SuggestedContent { get; init; }
    public bool ReadOnly { get; init; }
}

// ─── Worked Example ─────────────────────────────────────────────────────────

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
    public CircuitQuestionDefinition? CircuitQuestion { get; init; }
    public IReadOnlyList<MultipartPartDefinition> Parts { get; init; } = Array.Empty<MultipartPartDefinition>();
    public IReadOnlyList<string> Skills { get; init; } = Array.Empty<string>();
}

public sealed record MultipartPartDefinition(
    string Id,
    QuestionType Type,
    string Prompt,
    IReadOnlyList<ChoiceOption> Choices,
    AnswerDefinition Answer,
    string? Explanation,
    IReadOnlyList<MediaAsset> Media)
{
    public CodeQuestionDefinition? CodeQuestion { get; init; }
    public CircuitQuestionDefinition? CircuitQuestion { get; init; }
    public IReadOnlyList<string> Skills { get; init; } = Array.Empty<string>();
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
    public CircuitAnswerDefinition? CircuitAnswer { get; init; }
    public GraphingAnswerDefinition? GraphingAnswer { get; init; }
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
    public SubmittedCircuitAnswer? CircuitAnswer { get; init; }
    public SubmittedGraphAnswer? GraphingAnswer { get; init; }
    public IReadOnlyList<SubmittedAnswer> PartAnswers { get; init; } = Array.Empty<SubmittedAnswer>();
}

public sealed record AnswerEvaluation(
    string QuestionId,
    bool IsCorrect,
    string? Explanation,
    string? ExpectedAnswer)
{
    public CodeFeedback? CodeFeedback { get; init; }
    public SymbolicFeedback? SymbolicFeedback { get; init; }
    public CircuitFeedback? CircuitFeedback { get; init; }
    public GraphFeedback? GraphFeedback { get; init; }
    public decimal EarnedPoints { get; init; }
    public decimal PossiblePoints { get; init; }
    public IReadOnlyList<AnswerEvaluation> PartEvaluations { get; init; } = Array.Empty<AnswerEvaluation>();
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
    int? AttemptQuestionCount = null,
    bool HasCompletedAttempt = false)
{
    public IReadOnlyList<string> AreaIds { get; init; } = Array.Empty<string>();
    public string? LearningGoal { get; init; }
    public string? ActivityType { get; init; }
    public IReadOnlyList<string> Tags { get; init; } = Array.Empty<string>();
    public IReadOnlyList<string> Skills { get; init; } = Array.Empty<string>();
}

public sealed record CircuitQuestionDefinition(
    int SchemaVersion,
    int CatalogVersion,
    string InteractionMode,
    IReadOnlyList<string> PaletteSymbolIds,
    IReadOnlyList<string> EditableProperties,
    CircuitDiagramDefinition Diagram);

public sealed record CircuitDiagramDefinition(
    int Width,
    int Height,
    IReadOnlyList<CircuitComponentInstance> Components,
    IReadOnlyList<CircuitNodeDefinition> Nodes,
    IReadOnlyList<CircuitWireDefinition> Wires,
    IReadOnlyList<CircuitAnnotationDefinition> Annotations);

public sealed record CircuitComponentInstance(
    string Id,
    string SymbolId,
    decimal X,
    decimal Y,
    decimal Rotation,
    string? Value = null,
    string? Label = null,
    IReadOnlyDictionary<string, string>? PropertyOverrides = null);

public sealed record CircuitNodeDefinition(
    string Id,
    string? Label = null,
    decimal? X = null,
    decimal? Y = null);

public sealed record CircuitWireDefinition(
    string Id,
    string SourceId,
    string TargetId,
    IReadOnlyList<CircuitPoint>? RoutePoints = null);

public sealed record CircuitPoint(decimal X, decimal Y);

public sealed record CircuitAnnotationDefinition(
    string Id,
    string Type,
    string Text,
    decimal X,
    decimal Y);

public sealed record CircuitAnswerDefinition(
    CircuitTopologyDefinition? Topology,
    IReadOnlyList<string>? SelectedTargetIds = null,
    CircuitMeterPlacementDefinition? MeterPlacement = null,
    IReadOnlyDictionary<string, ExpectedValueDefinition>? ExpectedValues = null);

public sealed record CircuitTopologyDefinition(
    IReadOnlyList<RequiredComponentDefinition> RequiredComponents,
    string ConnectionMode);

public sealed record RequiredComponentDefinition(
    string SymbolId,
    int Count);

public sealed record CircuitMeterPlacementDefinition(
    string MeterType,
    string? TargetBranchId = null,
    IReadOnlyList<string>? TargetNodeIds = null,
    bool? RequirePolarity = null,
    string? PositiveTerminalId = null,
    string? NegativeTerminalId = null);

public sealed record ExpectedValueDefinition(
    string Mode,
    string? ExpectedText = null,
    decimal? NumericValue = null,
    decimal? NumericTolerance = null,
    string? SymbolicExpectedLatex = null,
    string? SymbolicEquivalenceMode = null,
    IReadOnlyList<string>? SymbolicVariables = null,
    decimal? SymbolicTolerance = null);

public sealed record SubmittedCircuitAnswer(
    IReadOnlyList<string>? SelectedComponentIds = null,
    IReadOnlyList<string>? SelectedNodeIds = null,
    IReadOnlyList<string>? SelectedBranchIds = null,
    string? MeterType = null,
    string? MeterTargetBranchId = null,
    IReadOnlyList<string>? MeterTargetNodeIds = null,
    string? MeterPositiveTerminalId = null,
    string? MeterNegativeTerminalId = null,
    IReadOnlyDictionary<string, string>? Values = null,
    CircuitDiagramDefinition? BuiltDiagram = null);

public sealed record CircuitFeedback(
    IReadOnlyList<string> MissingComponents,
    IReadOnlyList<string> ExtraComponents,
    IReadOnlyList<string> IncorrectComponentTypes,
    IReadOnlyList<string> MissingConnections,
    IReadOnlyList<string> ExtraConnections,
    IReadOnlyList<string> IncorrectSelectedTargets,
    bool? IncorrectMeterPlacement,
    bool? IncorrectPolarity,
    IReadOnlyDictionary<string, string> IncorrectValues,
    IReadOnlyList<string> ExpectedHighlightTargetIds);

// ─── Graphing Question ──────────────────────────────────────────────────────

public sealed record GraphingAnswerDefinition(
    IReadOnlyList<ExpectedGraphFeature> Features
);

public sealed record ExpectedGraphFeature(
    string Type, 
    decimal? X,
    decimal? Y,
    decimal? Value,
    string? StringValue,
    decimal Tolerance,
    decimal Weight
);

public sealed record SubmittedGraphAnswer(
    string Shape,
    IReadOnlyList<GraphPoint> Points,
    string? Expression = null
);

public sealed record GraphPoint(decimal X, decimal Y);

public sealed record GraphFeedback(
    IReadOnlyList<GraphFeatureEvaluation> FeatureEvaluations
);

public sealed record GraphFeatureEvaluation(
    string FeatureType,
    bool Passed,
    string Message
);
