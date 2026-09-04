using QuizApp.Core.Domain;

namespace QuizApp.Infrastructure.Files;

public static class FileDtoMapper
{
    public static Category ToDomain(this CategoryFileDto dto)
    {
        return new Category(
            dto.SchemaVersion,
            dto.Id ?? string.Empty,
            dto.Title ?? string.Empty,
            (dto.Subcategories ?? new List<SubCategoryFileDto>())
                .Select(subcategory => new SubCategory(
                    subcategory.Id ?? string.Empty,
                    subcategory.Title ?? string.Empty,
                    subcategory.Description)
                {
                    PrerequisiteIds = subcategory.PrerequisiteIds ?? new List<string>()
                })
                .ToList(),
            dto.Description)
        {
            AuthoringProfile = ParseAuthoringProfile(dto.AuthoringProfile),
            DirectedProjectEligible = dto.DirectedProjectEligible ?? false
        };
    }

    public static AppSettings ToDomain(this SettingsFileDto dto)
    {
        return new AppSettings(
            dto.SchemaVersion <= 0 ? 1 : dto.SchemaVersion,
            ParseMode(dto.DefaultMode, AssessmentMode.Practice),
            ParseQuestionOrder(dto.DefaultQuestionOrder),
            dto.DefaultQuizLength <= 0 ? 15 : dto.DefaultQuizLength,
            dto.DefaultTestLength <= 0 ? 25 : dto.DefaultTestLength,
            dto.QuestionTimerSeconds,
            dto.AssessmentTimerSeconds,
            dto.CommitScoredAttemptsAutomatically)
        {
            CodeRunnerBaseUrl = string.IsNullOrWhiteSpace(dto.CodeRunnerBaseUrl) ? "http://localhost:2000/api/v2" : dto.CodeRunnerBaseUrl,
            CodeRunnerCompileTimeoutMs = dto.CodeRunnerCompileTimeoutMs is > 0 ? dto.CodeRunnerCompileTimeoutMs.Value : 10000,
            CodeRunnerRunTimeoutMs = dto.CodeRunnerRunTimeoutMs is > 0 ? dto.CodeRunnerRunTimeoutMs.Value : 3000
        };
    }

    public static SettingsFileDto ToDto(this AppSettings settings)
    {
        return new SettingsFileDto
        {
            SchemaVersion = settings.SchemaVersion,
            DefaultMode = ToWireValue(settings.DefaultMode),
            DefaultQuestionOrder = settings.DefaultQuestionOrder is QuestionOrderMode.Randomized ? "randomized" : "static",
            DefaultQuizLength = settings.DefaultQuizLength,
            DefaultTestLength = settings.DefaultTestLength,
            QuestionTimerSeconds = settings.QuestionTimerSeconds,
            AssessmentTimerSeconds = settings.AssessmentTimerSeconds,
            CommitScoredAttemptsAutomatically = settings.CommitScoredAttemptsAutomatically,
            CodeRunnerBaseUrl = settings.CodeRunnerBaseUrl,
            CodeRunnerCompileTimeoutMs = settings.CodeRunnerCompileTimeoutMs,
            CodeRunnerRunTimeoutMs = settings.CodeRunnerRunTimeoutMs
        };
    }

    public static AssessmentDefinition ToDomain(this AssessmentFileDto dto)
    {
        return new AssessmentDefinition(
            dto.SchemaVersion,
            dto.Id ?? string.Empty,
            dto.Title ?? string.Empty,
            ParseAssessmentType(dto.AssessmentType),
            dto.CategoryId ?? string.Empty,
            dto.TopicId ?? string.Empty,
            ParseMode(dto.ModeDefault, AssessmentMode.Practice),
            dto.RandomizeQuestions ?? true,
            dto.AttemptQuestionCount,
            dto.QuestionTimerSeconds,
            dto.AssessmentTimerSeconds,
            (dto.Questions ?? new List<QuestionFileDto>()).Select(ToDomain).ToList(),
            dto.QuestionSelection is null ? null : ToDomain(dto.QuestionSelection))
        {
            WorkedExamples = (dto.WorkedExamples ?? new List<WorkedExampleFileDto>()).Select(ToDomain).ToList(),
            GuidedProject = dto.GuidedProject is null ? null : ToDomain(dto.GuidedProject),
            Items = (dto.Items ?? new List<RecallItemFileDto>()).Select(ToDomain).ToList(),
            Glossary = dto.Glossary is null ? null : ToDomain(dto.Glossary),
            Lesson = dto.Lesson is null ? null : ToDomain(dto.Lesson),
            Exploration = dto.Exploration is null ? null : ToDomain(dto.Exploration),
            DirectedProject = dto.DirectedProject is null ? null : ToDomain(dto.DirectedProject),
            Sandbox = dto.Sandbox is null ? null : new SandboxDefinition(
                dto.Sandbox.Language ?? string.Empty,
                dto.Sandbox.Image ?? string.Empty,
                dto.Sandbox.InitialCommand ?? string.Empty,
                dto.Sandbox.Instructions ?? string.Empty,
                dto.Sandbox.ReadOnlyFileSystem ?? false)
            {
                Files = (dto.Sandbox.Files ?? new List<SandboxWorkspaceFileDto>())
                    .Select(f => new SandboxFileDefinition(
                        f.Path ?? string.Empty,
                        f.Content ?? string.Empty,
                        f.ReadOnly ?? false))
                    .ToList()
            },
            Navigation = dto.Navigation is null ? null : new NavigationMetadata(
                dto.Navigation.LearningGoal,
                dto.Navigation.ActivityType,
                dto.Navigation.Tags ?? new List<string>()),
            Skills = dto.Skills ?? new List<string>()
            ,Authoring = dto.Authoring is null ? null : new AssessmentAuthoringMetadata(
                ParseVisualRequirement(dto.Authoring.VisualRequirement),
                dto.Authoring.VisualRationale,
                ParseDifficultyTier(dto.Authoring.DifficultyTier),
                dto.Authoring.ExceptionReason,
                dto.Authoring.PhysicsModel is null ? null : new PhysicsModelAuthoringMetadata
                {
                    ModelId = ParsePhysicsAnalysisModel(dto.Authoring.PhysicsModel.ModelId),
                    ModelRole = ParsePhysicsModelRole(dto.Authoring.PhysicsModel.ModelRole),
                    RequiredRepresentations = (dto.Authoring.PhysicsModel.RequiredRepresentations ?? new List<string>())
                        .Select(ParsePhysicsRepresentation)
                        .Where(representation => representation is not null)
                        .Select(representation => representation!.Value)
                        .ToList()
                })
        };
    }

    public static AssessmentFileDto ToDto(this AssessmentDefinition assessment)
    {
        return new AssessmentFileDto
        {
            SchemaVersion = assessment.SchemaVersion,
            Id = assessment.Id,
            Title = assessment.Title,
            AssessmentType = ToWireValue(assessment.AssessmentType),
            CategoryId = assessment.CategoryId,
            TopicId = assessment.TopicId,
            ModeDefault = ToWireValue(assessment.ModeDefault),
            RandomizeQuestions = assessment.RandomizeQuestions,
            AttemptQuestionCount = assessment.AttemptQuestionCount,
            QuestionTimerSeconds = assessment.QuestionTimerSeconds,
            AssessmentTimerSeconds = assessment.AssessmentTimerSeconds,
            QuestionSelection = assessment.QuestionSelection is null ? null : ToDto(assessment.QuestionSelection),
            Questions = assessment.Questions.Select(ToDto).ToList(),
            WorkedExamples = assessment.WorkedExamples.Select(ToDto).ToList(),
            GuidedProject = assessment.GuidedProject is null ? null : ToDto(assessment.GuidedProject),
            Items = assessment.Items.Select(ToDto).ToList(),
            Glossary = assessment.Glossary is null ? null : ToDto(assessment.Glossary),
            Lesson = assessment.Lesson is null ? null : ToDto(assessment.Lesson),
            Exploration = assessment.Exploration is null ? null : ToDto(assessment.Exploration),
            DirectedProject = assessment.DirectedProject is null ? null : ToDto(assessment.DirectedProject),
            Sandbox = assessment.Sandbox is null ? null : new SandboxFileDto
            {
                Language = assessment.Sandbox.Language,
                Image = assessment.Sandbox.Image,
                InitialCommand = assessment.Sandbox.InitialCommand,
                Instructions = assessment.Sandbox.Instructions,
                ReadOnlyFileSystem = assessment.Sandbox.ReadOnlyFileSystem,
                Files = assessment.Sandbox.Files.Select(f => new SandboxWorkspaceFileDto
                {
                    Path = f.Path,
                    Content = f.Content,
                    ReadOnly = f.ReadOnly
                }).ToList()
            },
            Navigation = assessment.Navigation is null ? null : new NavigationFileDto
            {
                LearningGoal = assessment.Navigation.LearningGoal,
                ActivityType = assessment.Navigation.ActivityType,
                Tags = assessment.Navigation.Tags.ToList()
            },
            Skills = assessment.Skills.ToList()
            ,Authoring = assessment.Authoring is null ? null : new AssessmentAuthoringFileDto
            {
                VisualRequirement = ToWireValue(assessment.Authoring.VisualRequirement),
                VisualRationale = assessment.Authoring.VisualRationale,
                DifficultyTier = ToWireValue(assessment.Authoring.DifficultyTier),
                ExceptionReason = assessment.Authoring.ExceptionReason,
                PhysicsModel = assessment.Authoring.PhysicsModel is null ? null : new PhysicsModelAuthoringFileDto
                {
                    ModelId = ToWireValue(assessment.Authoring.PhysicsModel.ModelId),
                    ModelRole = ToWireValue(assessment.Authoring.PhysicsModel.ModelRole),
                    RequiredRepresentations = assessment.Authoring.PhysicsModel.RequiredRepresentations.Select(ToWireValue).ToList()
                }
            }
        };
    }

    private static QuestionSelectionDefinition ToDomain(QuestionSelectionFileDto dto)
    {
        return new QuestionSelectionDefinition(
            ParseQuestionSelectionMode(dto.Mode),
            (dto.Slots ?? new List<QuestionSelectionSlotFileDto>()).Select(ToDomain).ToList());
    }

    private static QuestionSelectionSlotDefinition ToDomain(QuestionSelectionSlotFileDto dto)
    {
        return new QuestionSelectionSlotDefinition(
            dto.Id ?? string.Empty,
            dto.Title,
            dto.QuestionIds ?? new List<string>());
    }

    private static QuestionSelectionFileDto ToDto(QuestionSelectionDefinition selection)
    {
        return new QuestionSelectionFileDto
        {
            Mode = selection.Mode is QuestionSelectionMode.OrderedVariants ? "orderedVariants" : "unknown",
            Slots = selection.Slots.Select(ToDto).ToList()
        };
    }

    private static QuestionSelectionSlotFileDto ToDto(QuestionSelectionSlotDefinition slot)
    {
        return new QuestionSelectionSlotFileDto
        {
            Id = slot.Id,
            Title = slot.Title,
            QuestionIds = slot.QuestionIds.ToList()
        };
    }

    private static ConceptLessonDefinition ToDomain(ConceptLessonFileDto dto)
    {
        return new ConceptLessonDefinition(
            dto.Introduction ?? string.Empty,
            (dto.Sections ?? new List<LearningSectionFileDto>())
                .Select(section => new LearningSectionDefinition(
                    section.Id ?? string.Empty,
                    section.Title ?? string.Empty,
                    section.Required ?? true,
                    section.Content ?? string.Empty,
                    (section.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList(),
                    section.Check is null ? null : ToDomain(section.Check)))
                .ToList());
    }

    private static GlossaryDefinition ToDomain(GlossaryFileDto dto)
    {
        return new GlossaryDefinition(
            dto.Introduction ?? string.Empty,
            (dto.Sections ?? new List<GlossarySectionFileDto>())
                .Select(section => new GlossarySectionDefinition(
                    section.Id ?? string.Empty,
                    section.Title ?? string.Empty,
                    section.Required ?? true,
                    section.Content ?? string.Empty,
                    (section.Entries ?? new List<GlossaryEntryFileDto>())
                        .Select(entry => new GlossaryEntryDefinition(
                            entry.Id ?? string.Empty,
                            entry.Term ?? string.Empty,
                            entry.Definition ?? string.Empty,
                            entry.Notation,
                            entry.Examples ?? new List<string>(),
                            entry.Aliases ?? new List<string>(),
                            (entry.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList(),
                            entry.Tags ?? new List<string>(),
                            (entry.Drills ?? new List<RecallItemFileDto>()).Select(ToDomain).ToList()))
                        .ToList()))
                .ToList());
    }

    private static GlossaryFileDto ToDto(GlossaryDefinition glossary)
    {
        return new GlossaryFileDto
        {
            Introduction = glossary.Introduction,
            Sections = glossary.Sections.Select(section => new GlossarySectionFileDto
            {
                Id = section.Id,
                Title = section.Title,
                Required = section.Required,
                Content = section.Content,
                Entries = section.Entries.Select(entry => new GlossaryEntryFileDto
                {
                    Id = entry.Id,
                    Term = entry.Term,
                    Definition = entry.Definition,
                    Notation = entry.Notation,
                    Examples = entry.Examples.ToList(),
                    Aliases = entry.Aliases.ToList(),
                    Media = entry.Media.Select(ToDto).ToList(),
                    Tags = entry.Tags.ToList(),
                    Drills = entry.Drills.Select(ToDto).ToList()
                }).ToList()
            }).ToList()
        };
    }

    private static ConceptLessonFileDto ToDto(ConceptLessonDefinition lesson)
    {
        return new ConceptLessonFileDto
        {
            Introduction = lesson.Introduction,
            Sections = lesson.Sections.Select(section => new LearningSectionFileDto
            {
                Id = section.Id,
                Title = section.Title,
                Required = section.Required,
                Content = section.Content,
                Media = section.Media.Select(ToDto).ToList(),
                Check = section.Check is null ? null : ToDto(section.Check)
            }).ToList()
        };
    }

    private static InteractiveExplorationDefinition ToDomain(InteractiveExplorationFileDto dto)
    {
        return new InteractiveExplorationDefinition(
            dto.Introduction ?? string.Empty,
            (dto.Sections ?? new List<ExplorationSectionFileDto>())
                .Select(section => new ExplorationSectionDefinition(
                    section.Id ?? string.Empty,
                    section.Title ?? string.Empty,
                    section.Required ?? true,
                    section.Instruction ?? string.Empty,
                    (section.Controls ?? new List<ExplorationControlFileDto>())
                        .Select(control => new ExplorationControlDefinition(
                            control.Id ?? string.Empty,
                            control.Type ?? string.Empty,
                            control.Label ?? string.Empty,
                            control.Min,
                            control.Max,
                            control.Step,
                            control.DefaultValue,
                            (control.Options ?? new List<ExplorationOptionFileDto>())
                                .Select(option => new ExplorationOptionDefinition(option.Value ?? string.Empty, option.Label ?? string.Empty))
                                .ToList()))
                        .ToList(),
                    (section.Views ?? new List<ExplorationViewFileDto>())
                        .Select(view => new ExplorationViewDefinition(
                            view.Id ?? string.Empty,
                            view.Type ?? string.Empty,
                            view.Label ?? string.Empty,
                            view.Expression,
                            view.Condition,
                            view.Content,
                            view.InputControlId,
                            view.Start,
                            view.End,
                            view.Step))
                        .ToList(),
                    section.Check is null ? null : ToDomain(section.Check)))
                .ToList());
    }

    private static InteractiveExplorationFileDto ToDto(InteractiveExplorationDefinition exploration)
    {
        return new InteractiveExplorationFileDto
        {
            Introduction = exploration.Introduction,
            Sections = exploration.Sections.Select(section => new ExplorationSectionFileDto
            {
                Id = section.Id,
                Title = section.Title,
                Required = section.Required,
                Instruction = section.Instruction,
                Controls = section.Controls.Select(control => new ExplorationControlFileDto
                {
                    Id = control.Id,
                    Type = control.Type,
                    Label = control.Label,
                    Min = control.Min,
                    Max = control.Max,
                    Step = control.Step,
                    DefaultValue = control.DefaultValue,
                    Options = control.Options?.Select(option => new ExplorationOptionFileDto
                    {
                        Value = option.Value,
                        Label = option.Label
                    }).ToList()
                }).ToList(),
                Views = section.Views.Select(view => new ExplorationViewFileDto
                {
                    Id = view.Id,
                    Type = view.Type,
                    Label = view.Label,
                    Expression = view.Expression,
                    Condition = view.Condition,
                    Content = view.Content,
                    InputControlId = view.InputControlId,
                    Start = view.Start,
                    End = view.End,
                    Step = view.Step
                }).ToList(),
                Check = section.Check is null ? null : ToDto(section.Check)
            }).ToList()
        };
    }

    private static RecallItemDefinition ToDomain(RecallItemFileDto dto)
    {
        return new RecallItemDefinition(
            dto.Id ?? string.Empty,
            ParseRecallItemType(dto.Type),
            dto.Prompt ?? string.Empty,
            new RecallItemAnswerDefinition(
                dto.Answer?.Expected,
                dto.Answer?.ExpectedLatex,
                dto.Answer?.Aliases ?? new List<string>(),
                (dto.Answer?.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList()),
            dto.Explanation,
            dto.Tags ?? new List<string>())
        {
            Skills = dto.Skills ?? new List<string>(),
            IssueSignals = ToDomain(dto.IssueSignals),
            Choices = (dto.Choices ?? new List<ChoiceFileDto>())
                .Select(choice => new ChoiceOption(
                    choice.Id ?? string.Empty,
                    choice.Text ?? string.Empty,
                    (choice.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList()))
                .ToList(),
            ChoiceId = dto.Answer?.ChoiceId
        };
    }

    private static RecallItemFileDto ToDto(RecallItemDefinition item)
    {
        return new RecallItemFileDto
        {
            Id = item.Id,
            Type = ToWireValue(item.Type),
            Prompt = item.Prompt,
            Answer = new RecallItemAnswerFileDto
            {
                Expected = item.Answer.Expected,
                ExpectedLatex = item.Answer.ExpectedLatex,
                Aliases = item.Answer.Aliases.ToList(),
                Media = item.Answer.Media.Select(ToDto).ToList(),
                ChoiceId = item.ChoiceId
            },
            Explanation = item.Explanation,
            Tags = item.Tags.ToList(),
            Skills = item.Skills.ToList(),
            IssueSignals = ToDto(item.IssueSignals),
            Choices = item.Choices.Select(choice => new ChoiceFileDto
            {
                Id = choice.Id,
                Text = choice.Text,
                Media = choice.Media.Select(ToDto).ToList()
            }).ToList()
        };
    }

    private static GuidedProjectDefinition ToDomain(GuidedProjectFileDto dto)
    {
        return new GuidedProjectDefinition(
            dto.Language ?? string.Empty,
            dto.ProjectKind,
            dto.RunnerMode,
            dto.Instructions ?? string.Empty,
            dto.Workspace is null ? null : new GuidedProjectWorkspaceDefinition(
                dto.Workspace.BuildProfile,
                dto.Workspace.EntryPoint,
                dto.Workspace.LabProfile,
                dto.Workspace.SourceGlobs ?? new List<string>(),
                dto.Workspace.IncludePaths ?? new List<string>(),
                dto.Workspace.WritablePaths ?? new List<string>(),
                dto.Workspace.AllowedBaseImages ?? new List<string>()),
            (dto.Files ?? new List<GuidedProjectSourceFileDto>())
                .Select(file => new GuidedProjectFileDefinition(
                    file.Path ?? string.Empty,
                    file.Content ?? string.Empty,
                    file.ReadOnly))
                .ToList(),
            (dto.Fixtures ?? new List<GuidedProjectFixtureFileDto>())
                .Select(fixture => new GuidedProjectFixtureDefinition(
                    fixture.Path ?? string.Empty,
                    fixture.Content ?? string.Empty,
                    fixture.ReadOnly))
                .ToList(),
            (dto.Scenarios ?? new List<GuidedProjectScenarioFileDto>())
                .Select(scenario => new GuidedProjectScenarioDefinition(
                    scenario.Id ?? string.Empty,
                    scenario.Type ?? string.Empty,
                    scenario.LearnerRole,
                    (scenario.Events ?? new List<GuidedProjectNetworkEventFileDto>())
                        .Select(evt => new GuidedProjectNetworkEventDefinition(
                            evt.Type ?? string.Empty,
                            evt.Peer,
                            evt.From,
                            evt.Text))
                        .ToList()))
                .ToList(),
            dto.Diagnostics ?? new List<string>(),
            (dto.RequiredChecks ?? new List<GuidedProjectCheckFileDto>()).Select(ToDomain).ToList(),
            (dto.BonusChecks ?? new List<GuidedProjectCheckFileDto>()).Select(ToDomain).ToList());
    }

    private static GuidedProjectFileDto ToDto(GuidedProjectDefinition project)
    {
        return new GuidedProjectFileDto
        {
            Language = project.Language,
            ProjectKind = project.ProjectKind,
            RunnerMode = project.RunnerMode,
            Instructions = project.Instructions,
            Workspace = project.Workspace is null ? null : new GuidedProjectWorkspaceFileDto
            {
                BuildProfile = project.Workspace.BuildProfile,
                EntryPoint = project.Workspace.EntryPoint,
                LabProfile = project.Workspace.LabProfile,
                SourceGlobs = project.Workspace.SourceGlobs.ToList(),
                IncludePaths = project.Workspace.IncludePaths.ToList(),
                WritablePaths = project.Workspace.WritablePaths.ToList(),
                AllowedBaseImages = project.Workspace.AllowedBaseImages.ToList()
            },
            Files = project.Files.Select(file => new GuidedProjectSourceFileDto
            {
                Path = file.Path,
                Content = file.Content,
                ReadOnly = file.ReadOnly
            }).ToList(),
            Fixtures = project.Fixtures.Select(fixture => new GuidedProjectFixtureFileDto
            {
                Path = fixture.Path,
                Content = fixture.Content,
                ReadOnly = fixture.ReadOnly
            }).ToList(),
            Scenarios = project.Scenarios.Select(scenario => new GuidedProjectScenarioFileDto
            {
                Id = scenario.Id,
                Type = scenario.Type,
                LearnerRole = scenario.LearnerRole,
                Events = scenario.Events.Select(evt => new GuidedProjectNetworkEventFileDto
                {
                    Type = evt.Type,
                    Peer = evt.Peer,
                    From = evt.From,
                    Text = evt.Text
                }).ToList()
            }).ToList(),
            Diagnostics = project.Diagnostics.ToList(),
            RequiredChecks = project.RequiredChecks.Select(ToDto).ToList(),
            BonusChecks = project.BonusChecks.Select(ToDto).ToList()
        };
    }

    private static GuidedProjectCheckDefinition ToDomain(GuidedProjectCheckFileDto dto)
    {
        return new GuidedProjectCheckDefinition(
            dto.Id ?? string.Empty,
            dto.Title ?? string.Empty,
            dto.Description ?? string.Empty,
            dto.TestCode,
            dto.ExpectedOutputContains?.ToList(),
            dto.Run is null ? null : new GuidedProjectCheckRunDefinition(
                dto.Run.Arguments ?? new List<string>(),
                dto.Run.Stdin,
                dto.Run.Scenario),
            dto.Expect is null ? null : new GuidedProjectCheckExpectDefinition(
                dto.Expect.StdoutContains ?? new List<string>(),
                (dto.Expect.Files ?? new List<GuidedProjectFileExpectationFileDto>())
                    .Select(file => new GuidedProjectCheckFileExpectation(
                        file.Path ?? string.Empty,
                        file.TextContains ?? new List<string>()))
                    .ToList()));
    }

    private static GuidedProjectCheckFileDto ToDto(GuidedProjectCheckDefinition check)
    {
        return new GuidedProjectCheckFileDto
        {
            Id = check.Id,
            Title = check.Title,
            Description = check.Description,
            TestCode = check.TestCode,
            ExpectedOutputContains = check.ExpectedOutputContains?.ToList(),
            Run = check.Run is null ? null : new GuidedProjectCheckRunFileDto
            {
                Arguments = check.Run.Arguments.ToList(),
                Stdin = check.Run.Stdin,
                Scenario = check.Run.Scenario
            },
            Expect = check.Expect is null ? null : new GuidedProjectCheckExpectFileDto
            {
                StdoutContains = check.Expect.StdoutContains.ToList(),
                Files = check.Expect.Files.Select(file => new GuidedProjectFileExpectationFileDto
                {
                    Path = file.Path,
                    TextContains = file.TextContains.ToList()
                }).ToList()
            }
        };
    }

    private static WorkedExampleDefinition ToDomain(WorkedExampleFileDto dto)
    {
        return new WorkedExampleDefinition(
            dto.Id ?? string.Empty,
            dto.Title ?? string.Empty,
            dto.Problem ?? string.Empty,
            (dto.Steps ?? new List<WorkedExampleStepFileDto>()).Select(ToDomain).ToList());
    }

    private static WorkedExampleFileDto ToDto(WorkedExampleDefinition workedExample)
    {
        return new WorkedExampleFileDto
        {
            Id = workedExample.Id,
            Title = workedExample.Title,
            Problem = workedExample.Problem,
            Steps = workedExample.Steps.Select(ToDto).ToList()
        };
    }

    private static WorkedExampleStepDefinition ToDomain(WorkedExampleStepFileDto dto)
    {
        var question = ToDomain(new QuestionFileDto
        {
            Id = dto.Id,
            Type = dto.Type,
            Prompt = dto.Prompt,
            Choices = dto.Choices,
            Answer = dto.Answer,
            Explanation = dto.Explanation,
            Media = dto.Media,
            Language = dto.Language,
            FunctionName = dto.FunctionName,
            ExecutionMode = dto.ExecutionMode,
            StarterCode = dto.StarterCode,
            Tests = dto.Tests,
            IssueSignals = dto.IssueSignals
        });

        return new WorkedExampleStepDefinition(
            dto.Id ?? string.Empty,
            dto.Title ?? string.Empty,
            dto.Instruction ?? string.Empty,
            dto.Hint,
            question);
    }

    private static WorkedExampleStepFileDto ToDto(WorkedExampleStepDefinition step)
    {
        var question = ToDto(step.Question);
        return new WorkedExampleStepFileDto
        {
            Id = step.Id,
            Title = step.Title,
            Instruction = step.Instruction,
            Hint = step.Hint,
            Type = question.Type,
            Prompt = question.Prompt,
            Choices = question.Choices,
            Answer = question.Answer,
            Explanation = question.Explanation,
            Media = question.Media,
            Language = question.Language,
            FunctionName = question.FunctionName,
            ExecutionMode = question.ExecutionMode,
            StarterCode = question.StarterCode,
            Tests = question.Tests,
            IssueSignals = question.IssueSignals
        };
    }

    private static QuestionDefinition ToDomain(QuestionFileDto dto)
    {
        var type = ParseQuestionType(dto.Type);
        return new QuestionDefinition(
            dto.Id ?? string.Empty,
            type,
            dto.Prompt ?? string.Empty,
            (dto.Choices ?? new List<ChoiceFileDto>()).Select(ToDomain).ToList(),
            ToDomain(dto.Answer),
            dto.Explanation,
            (dto.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList())
        {
            CodeQuestion = ToCodeQuestion(dto),
            CircuitQuestion = ToDomain(dto.CircuitQuestion),
            GraphingQuestion = ToDomain(dto.GraphingQuestion),
            Skills = dto.Skills ?? new List<string>(),
            DifficultyDimensions = (dto.DifficultyDimensions ?? new List<string>()).Select(ParseDifficultyDimension).ToList(),
            SubjectDifficultyTags = dto.SubjectDifficultyTags ?? new List<string>(),
            DifficultyEvidence = dto.DifficultyEvidence,
            PrerequisiteObjectiveIds = dto.PrerequisiteObjectiveIds ?? new List<string>(),
            ExtensionObjectiveIds = dto.ExtensionObjectiveIds ?? new List<string>()
            ,
            Parts = (dto.Parts ?? new List<MultipartPartFileDto>()).Select(ToDomain).ToList(),
            IssueSignals = ToDomain(dto.IssueSignals)
        };
    }

    private static QuestionFileDto ToDto(QuestionDefinition question)
    {
        return new QuestionFileDto
        {
            Id = question.Id,
            Type = ToWireValue(question.Type),
            Prompt = question.Prompt,
            Choices = question.Choices.Select(ToDto).ToList(),
            Answer = ToDto(question.Answer),
            Explanation = question.Explanation,
            Media = question.Media.Select(ToDto).ToList(),
            Language = question.CodeQuestion?.Language,
            FunctionName = question.CodeQuestion?.FunctionName,
            ExecutionMode = ToWireValue(question.CodeQuestion?.ExecutionMode ?? CodeExecutionMode.Unspecified),
            StarterCode = question.CodeQuestion?.StarterCode,
            Tests = question.CodeQuestion?.Tests.Select(test => new CodeQuestionTestFileDto
            {
                Input = test.Input,
                Expected = test.Expected
            }).ToList(),
            CircuitQuestion = ToDto(question.CircuitQuestion),
            GraphingQuestion = ToDto(question.GraphingQuestion),
            Skills = question.Skills.ToList(),
            DifficultyDimensions = question.DifficultyDimensions.Select(ToWireValue).ToList(),
            SubjectDifficultyTags = question.SubjectDifficultyTags.ToList(),
            DifficultyEvidence = question.DifficultyEvidence,
            PrerequisiteObjectiveIds = question.PrerequisiteObjectiveIds.ToList(),
            ExtensionObjectiveIds = question.ExtensionObjectiveIds.ToList()
            ,
            Parts = question.Parts.Select(ToDto).ToList(),
            IssueSignals = ToDto(question.IssueSignals)
        };
    }

    private static MultipartPartDefinition ToDomain(MultipartPartFileDto dto) => new(
        dto.Id ?? string.Empty,
        ParseQuestionType(dto.Type),
        dto.Prompt ?? string.Empty,
        (dto.Choices ?? new List<ChoiceFileDto>()).Select(ToDomain).ToList(),
        ToDomain(dto.Answer),
        dto.Explanation,
        (dto.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList())
    {
        Skills = dto.Skills ?? new List<string>(),
        IssueSignals = ToDomain(dto.IssueSignals)
    };

    private static MultipartPartFileDto ToDto(MultipartPartDefinition part) => new()
    {
        Id = part.Id,
        Type = ToWireValue(part.Type),
        Prompt = part.Prompt,
        Choices = part.Choices.Select(ToDto).ToList(),
        Answer = ToDto(part.Answer),
        Explanation = part.Explanation,
        Media = part.Media.Select(ToDto).ToList(),
        Skills = part.Skills.ToList(),
        IssueSignals = ToDto(part.IssueSignals)
    };

    private static IReadOnlyList<IssueSignal> ToDomain(List<IssueSignalFileDto>? signals) =>
        (signals ?? new List<IssueSignalFileDto>())
            .Where(signal => !string.IsNullOrWhiteSpace(signal.Id))
            .Select(signal => new IssueSignal(signal.Id!, signal.Domains ?? new List<string>()))
            .ToList();

    private static List<IssueSignalFileDto> ToDto(IReadOnlyList<IssueSignal> signals) => signals
        .Select(signal => new IssueSignalFileDto { Id = signal.Id, Domains = signal.Domains.ToList() })
        .ToList();

    private static ChoiceOption ToDomain(ChoiceFileDto dto) => new(
        dto.Id ?? string.Empty,
        dto.Text ?? string.Empty,
        (dto.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList())
    {
        IssueSignals = ToDomain(dto.IssueSignals)
    };

    private static ChoiceFileDto ToDto(ChoiceOption choice) => new()
    {
        Id = choice.Id,
        Text = choice.Text,
        Media = choice.Media.Select(ToDto).ToList(),
        IssueSignals = ToDto(choice.IssueSignals)
    };

    private static AnswerDefinition ToDomain(AnswerFileDto? dto) => new(
        dto?.ChoiceId,
        dto?.ChoiceIds ?? new List<string>(),
        dto?.Expected,
        dto?.GradingMode,
        dto?.Value,
        dto?.Tolerance,
        (dto?.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList())
    {
        ExpectedLatex = dto?.ExpectedLatex,
        EquivalenceMode = dto?.EquivalenceMode,
        Variables = dto?.Variables ?? new List<string>(),
        Tolerance = dto?.Tolerance,
        SymbolicExpectedLatex = dto?.ExpectedLatex,
        SymbolicEquivalenceMode = dto?.EquivalenceMode,
        SymbolicVariables = dto?.Variables ?? new List<string>(),
        SymbolicTolerance = dto?.Tolerance,
        KeyPoints = dto?.KeyPoints ?? new List<string>(),
        CircuitAnswer = ToDomain(dto?.CircuitAnswer),
        GraphingAnswer = ToDomain(dto?.GraphingAnswer)
    };

    private static AnswerFileDto ToDto(AnswerDefinition answer) => new()
    {
        ChoiceId = answer.ChoiceId,
        ChoiceIds = answer.ChoiceIds.ToList(),
        Expected = answer.Expected,
        GradingMode = answer.GradingMode,
        ExpectedLatex = answer.SymbolicExpectedLatex ?? answer.ExpectedLatex,
        EquivalenceMode = answer.SymbolicEquivalenceMode ?? answer.EquivalenceMode,
        Variables = (answer.SymbolicVariables.Count > 0 ? answer.SymbolicVariables : answer.Variables).ToList(),
        Value = answer.NumericValue,
        Tolerance = answer.NumericTolerance ?? answer.SymbolicTolerance ?? answer.Tolerance,
        Media = answer.Media.Select(ToDto).ToList(),
        KeyPoints = answer.KeyPoints.ToList(),
        CircuitAnswer = ToDto(answer.CircuitAnswer),
        GraphingAnswer = ToDto(answer.GraphingAnswer)
    };

    private static CodeQuestionDefinition? ToCodeQuestion(QuestionFileDto dto)
    {
        if (ParseQuestionType(dto.Type) is not QuestionType.Code)
        {
            return null;
        }

        return new CodeQuestionDefinition(
            dto.Language ?? string.Empty,
            dto.FunctionName ?? string.Empty,
            dto.StarterCode ?? string.Empty,
            (dto.Tests ?? new List<CodeQuestionTestFileDto>())
                .Select(test => new CodeQuestionTest(test.Input ?? string.Empty, test.Expected ?? string.Empty))
                .ToList())
        {
            ExecutionMode = ParseCodeExecutionMode(dto.ExecutionMode, dto.FunctionName)
        };
    }

    private static MediaAsset ToDomain(MediaFileDto dto)
    {
        return new MediaAsset(
            dto.Type ?? string.Empty,
            dto.Src ?? string.Empty,
            dto.Alt ?? string.Empty,
            dto.Caption);
    }

    private static MediaFileDto ToDto(MediaAsset media)
    {
        return new MediaFileDto
        {
            Type = media.Type,
            Src = media.Src,
            Alt = media.Alt,
            Caption = media.Caption
        };
    }

    private static AssessmentType ParseAssessmentType(string? value)
    {
        return Normalize(value) switch
        {
            "quiz" => AssessmentType.Quiz,
            "test" => AssessmentType.Test,
            "workedexample" => AssessmentType.WorkedExample,
            "guidedproject" => AssessmentType.GuidedProject,
            "recalldrill" => AssessmentType.RecallDrill,
            "glossary" => AssessmentType.Glossary,
            "conceptlesson" => AssessmentType.ConceptLesson,
            "interactiveexploration" => AssessmentType.InteractiveExploration,
            "directedproject" => AssessmentType.DirectedProject,
            "sandbox" => AssessmentType.Sandbox,
            _ => AssessmentType.Unknown
        };
    }

    private static AuthoringProfile ParseAuthoringProfile(string? value) => value?.Trim().ToLowerInvariant() switch
    {
        "stem" => AuthoringProfile.Stem,
        "nonstem" or "non-stem" => AuthoringProfile.NonStem,
        _ => AuthoringProfile.Unknown
    };

    private static VisualRequirement ParseVisualRequirement(string? value) => value?.Trim().ToLowerInvariant() switch
    {
        "required" => VisualRequirement.Required,
        "notapplicable" or "not-applicable" => VisualRequirement.NotApplicable,
        _ => VisualRequirement.Unspecified
    };

    private static PhysicsAnalysisModel ParsePhysicsAnalysisModel(string? value) => value?.Trim().ToLowerInvariant() switch
    {
        "forcemodel" or "force-model" => PhysicsAnalysisModel.ForceModel,
        "freebodydiagram" or "free-body-diagram" => PhysicsAnalysisModel.FreeBodyDiagram,
        "inclinedplane" or "inclined-plane" => PhysicsAnalysisModel.InclinedPlane,
        "connectedsystem" or "connected-system" => PhysicsAnalysisModel.ConnectedSystem,
        "staticequilibrium" or "static-equilibrium" => PhysicsAnalysisModel.StaticEquilibrium,
        "friction" => PhysicsAnalysisModel.Friction,
        "uniformcircularmotion" or "uniform-circular-motion" => PhysicsAnalysisModel.UniformCircularMotion,
        _ => PhysicsAnalysisModel.Unspecified
    };

    private static PhysicsModelRole ParsePhysicsModelRole(string? value) => value?.Trim().ToLowerInvariant() switch
    {
        "foundation" => PhysicsModelRole.Foundation,
        "application" => PhysicsModelRole.Application,
        "synthesis" => PhysicsModelRole.Synthesis,
        _ => PhysicsModelRole.Unspecified
    };

    private static PhysicsRepresentation? ParsePhysicsRepresentation(string? value) => value?.Trim().ToLowerInvariant() switch
    {
        "systemboundary" or "system-boundary" => PhysicsRepresentation.SystemBoundary,
        "freebodydiagram" or "free-body-diagram" => PhysicsRepresentation.FreeBodyDiagram,
        "coordinateaxes" or "coordinate-axes" => PhysicsRepresentation.CoordinateAxes,
        "forcecomponents" or "force-components" => PhysicsRepresentation.ForceComponents,
        "motionconstraint" or "motion-constraint" => PhysicsRepresentation.MotionConstraint,
        "interactionpair" or "interaction-pair" => PhysicsRepresentation.InteractionPair,
        "radialdirection" or "radial-direction" => PhysicsRepresentation.RadialDirection,
        _ => null
    };

    private static AssessmentDifficultyTier ParseDifficultyTier(string? value) => value?.Trim().ToLowerInvariant() switch
    {
        "easy" => AssessmentDifficultyTier.Easy,
        "hard" => AssessmentDifficultyTier.Hard,
        "olympiad" => AssessmentDifficultyTier.Olympiad,
        _ => AssessmentDifficultyTier.Unspecified
    };

    private static DifficultyDimension ParseDifficultyDimension(string? value) => Normalize(value) switch
    {
        "simplification" => DifficultyDimension.Simplification,
        "identitycreation" or "identityconstruction" => DifficultyDimension.IdentityConstruction,
        "auxiliarytechnique" => DifficultyDimension.AuxiliaryTechnique,
        "modelorderivation" => DifficultyDimension.ModelOrDerivation,
        "domaincondition" => DifficultyDimension.DomainCondition,
        "casepartition" => DifficultyDimension.CasePartition,
        "parameterthreshold" => DifficultyDimension.ParameterThreshold,
        "reversereasoning" => DifficultyDimension.ReverseReasoning,
        "proofjustification" => DifficultyDimension.ProofJustification,
        "representationtransfer" => DifficultyDimension.RepresentationTransfer,
        "errordiagnosis" => DifficultyDimension.ErrorDiagnosis,
        "estimationorbounds" => DifficultyDimension.EstimationOrBounds,
        "globallocalreasoning" => DifficultyDimension.GlobalLocalReasoning,
        "counterexampleorconstruction" => DifficultyDimension.CounterexampleOrConstruction,
        _ => DifficultyDimension.Unknown
    };

    private static RecallItemType ParseRecallItemType(string? value)
    {
        return Normalize(value) switch
        {
            "typed" => RecallItemType.Typed,
            "symbolic" => RecallItemType.Symbolic,
            "flashcard" => RecallItemType.Flashcard,
            "cloze" => RecallItemType.Cloze,
            "recognition" => RecallItemType.Recognition,
            _ => RecallItemType.Unknown
        };
    }

    private static QuestionType ParseQuestionType(string? value)
    {
        return Normalize(value) switch
        {
            "multiplechoice" => QuestionType.MultipleChoice,
            "selectall" => QuestionType.SelectAll,
            "freeresponse" => QuestionType.FreeResponse,
            "numericresponse" => QuestionType.NumericResponse,
            "code" => QuestionType.Code,
            "symbolicresponse" => QuestionType.SymbolicResponse,
            "circuit" => QuestionType.Circuit,
            "multipart" => QuestionType.Multipart,
            "graphingresponse" => QuestionType.GraphingResponse,
            _ => QuestionType.Unknown
        };
    }

    private static CodeExecutionMode ParseCodeExecutionMode(string? value, string? functionName)
    {
        return Normalize(value) switch
        {
            "function" => CodeExecutionMode.Function,
            "program" => CodeExecutionMode.Program,
            _ when string.Equals(functionName, "main", StringComparison.OrdinalIgnoreCase) => CodeExecutionMode.Program,
            _ => CodeExecutionMode.Function
        };
    }

    private static AssessmentMode ParseMode(string? value, AssessmentMode fallback)
    {
        return Normalize(value) switch
        {
            "practice" => AssessmentMode.Practice,
            "scored" => AssessmentMode.Scored,
            _ => fallback
        };
    }

    private static QuestionOrderMode ParseQuestionOrder(string? value)
    {
        return Normalize(value) switch
        {
            "static" => QuestionOrderMode.Static,
            _ => QuestionOrderMode.Randomized
        };
    }

    private static QuestionSelectionMode ParseQuestionSelectionMode(string? value)
    {
        return Normalize(value) switch
        {
            "" => QuestionSelectionMode.OrderedVariants,
            "orderedvariant" => QuestionSelectionMode.OrderedVariants,
            "orderedvariants" => QuestionSelectionMode.OrderedVariants,
            _ => QuestionSelectionMode.Unknown
        };
    }

    private static string ToWireValue(AssessmentMode mode)
    {
        return mode is AssessmentMode.Scored ? "scored" : "practice";
    }

    private static string ToWireValue(CodeExecutionMode mode) => mode switch
    {
        CodeExecutionMode.Function => "function",
        CodeExecutionMode.Program => "program",
        _ => "unspecified"
    };

    private static string ToWireValue(AuthoringProfile profile) => profile switch
    {
        AuthoringProfile.Stem => "stem",
        AuthoringProfile.NonStem => "nonStem",
        _ => "unknown"
    };

    private static string ToWireValue(VisualRequirement requirement) => requirement switch
    {
        VisualRequirement.Required => "required",
        VisualRequirement.NotApplicable => "notApplicable",
        _ => "unspecified"
    };

    private static string ToWireValue(AssessmentDifficultyTier tier) => tier switch
    {
        AssessmentDifficultyTier.Easy => "easy",
        AssessmentDifficultyTier.Hard => "hard",
        AssessmentDifficultyTier.Olympiad => "olympiad",
        _ => "unspecified"
    };

    private static string ToWireValue(PhysicsAnalysisModel model) => model switch
    {
        PhysicsAnalysisModel.ForceModel => "forceModel",
        PhysicsAnalysisModel.FreeBodyDiagram => "freeBodyDiagram",
        PhysicsAnalysisModel.InclinedPlane => "inclinedPlane",
        PhysicsAnalysisModel.ConnectedSystem => "connectedSystem",
        PhysicsAnalysisModel.StaticEquilibrium => "staticEquilibrium",
        PhysicsAnalysisModel.Friction => "friction",
        PhysicsAnalysisModel.UniformCircularMotion => "uniformCircularMotion",
        _ => "unspecified"
    };

    private static string ToWireValue(PhysicsModelRole role) => role switch
    {
        PhysicsModelRole.Foundation => "foundation",
        PhysicsModelRole.Application => "application",
        PhysicsModelRole.Synthesis => "synthesis",
        _ => "unspecified"
    };

    private static string ToWireValue(PhysicsRepresentation representation) => representation switch
    {
        PhysicsRepresentation.SystemBoundary => "systemBoundary",
        PhysicsRepresentation.FreeBodyDiagram => "freeBodyDiagram",
        PhysicsRepresentation.CoordinateAxes => "coordinateAxes",
        PhysicsRepresentation.ForceComponents => "forceComponents",
        PhysicsRepresentation.MotionConstraint => "motionConstraint",
        PhysicsRepresentation.InteractionPair => "interactionPair",
        PhysicsRepresentation.RadialDirection => "radialDirection",
        _ => "unknown"
    };

    private static string ToWireValue(DifficultyDimension dimension) => dimension switch
    {
        DifficultyDimension.Simplification => "simplification",
        DifficultyDimension.IdentityConstruction => "identityConstruction",
        DifficultyDimension.AuxiliaryTechnique => "auxiliaryTechnique",
        DifficultyDimension.ModelOrDerivation => "modelOrDerivation",
        DifficultyDimension.DomainCondition => "domainCondition",
        DifficultyDimension.CasePartition => "casePartition",
        DifficultyDimension.ParameterThreshold => "parameterThreshold",
        DifficultyDimension.ReverseReasoning => "reverseReasoning",
        DifficultyDimension.ProofJustification => "proofJustification",
        DifficultyDimension.RepresentationTransfer => "representationTransfer",
        DifficultyDimension.ErrorDiagnosis => "errorDiagnosis",
        DifficultyDimension.EstimationOrBounds => "estimationOrBounds",
        DifficultyDimension.GlobalLocalReasoning => "globalLocalReasoning",
        DifficultyDimension.CounterexampleOrConstruction => "counterexampleOrConstruction",
        _ => "unknown"
    };

    private static string ToWireValue(AssessmentType assessmentType)
    {
        return assessmentType switch
        {
            AssessmentType.Test => "test",
            AssessmentType.WorkedExample => "workedExample",
            AssessmentType.GuidedProject => "guidedProject",
            AssessmentType.RecallDrill => "recallDrill",
            AssessmentType.Glossary => "glossary",
            AssessmentType.ConceptLesson => "conceptLesson",
            AssessmentType.InteractiveExploration => "interactiveExploration",
            AssessmentType.DirectedProject => "directedProject",
            AssessmentType.Sandbox => "sandbox",
            _ => "quiz"
        };
    }

    private static string ToWireValue(RecallItemType itemType)
    {
        return itemType switch
        {
            RecallItemType.Symbolic => "symbolic",
            RecallItemType.Flashcard => "flashcard",
            RecallItemType.Cloze => "cloze",
            RecallItemType.Recognition => "recognition",
            RecallItemType.Typed => "typed",
            _ => "typed"
        };
    }

    private static string ToWireValue(QuestionType questionType)
    {
        return questionType switch
        {
            QuestionType.SelectAll => "selectAll",
            QuestionType.FreeResponse => "freeResponse",
            QuestionType.NumericResponse => "numericResponse",
            QuestionType.Code => "code",
            QuestionType.SymbolicResponse => "symbolicResponse",
            QuestionType.Circuit => "circuit",
            QuestionType.Multipart => "multipart",
            QuestionType.GraphingResponse => "graphingResponse",
            _ => "multipleChoice"
        };
    }

    private static string Normalize(string? value)
    {
        return string.Concat((value ?? string.Empty).Where(char.IsLetterOrDigit)).ToLowerInvariant();
    }

    private static CircuitQuestionDefinition? ToDomain(CircuitQuestionFileDto? dto)
    {
        if (dto is null) return null;
        return new CircuitQuestionDefinition(
            dto.SchemaVersion,
            dto.CatalogVersion,
            dto.InteractionMode ?? "select",
            dto.PaletteSymbolIds ?? new List<string>(),
            dto.EditableProperties ?? new List<string>(),
            ToDomain(dto.Diagram) ?? new CircuitDiagramDefinition(900, 520, Array.Empty<CircuitComponentInstance>(), Array.Empty<CircuitNodeDefinition>(), Array.Empty<CircuitWireDefinition>(), Array.Empty<CircuitAnnotationDefinition>())
        );
    }

    private static CircuitDiagramDefinition? ToDomain(CircuitDiagramFileDto? dto)
    {
        if (dto is null) return null;
        return new CircuitDiagramDefinition(
            dto.Width <= 0 ? 900 : dto.Width,
            dto.Height <= 0 ? 520 : dto.Height,
            (dto.Components ?? new List<CircuitComponentInstanceFileDto>()).Select(ToDomain).ToList(),
            (dto.Nodes ?? new List<CircuitNodeFileDto>()).Select(ToDomain).ToList(),
            (dto.Wires ?? new List<CircuitWireFileDto>()).Select(ToDomain).ToList(),
            (dto.Annotations ?? new List<CircuitAnnotationFileDto>()).Select(ToDomain).ToList()
        );
    }

    private static CircuitComponentInstance ToDomain(CircuitComponentInstanceFileDto dto)
    {
        return new CircuitComponentInstance(
            dto.Id ?? string.Empty,
            dto.SymbolId ?? string.Empty,
            dto.X,
            dto.Y,
            dto.Rotation,
            dto.Value,
            dto.Label,
            dto.PropertyOverrides ?? new Dictionary<string, string>()
        );
    }

    private static CircuitNodeDefinition ToDomain(CircuitNodeFileDto dto)
    {
        return new CircuitNodeDefinition(dto.Id ?? string.Empty, dto.Label, dto.X, dto.Y);
    }

    private static CircuitWireDefinition ToDomain(CircuitWireFileDto dto)
    {
        return new CircuitWireDefinition(
            dto.Id ?? string.Empty,
            dto.SourceId ?? string.Empty,
            dto.TargetId ?? string.Empty,
            (dto.RoutePoints ?? new List<CircuitPointFileDto>()).Select(ToDomain).ToList()
        );
    }

    private static CircuitPoint ToDomain(CircuitPointFileDto dto)
    {
        return new CircuitPoint(dto.X, dto.Y);
    }

    private static CircuitAnnotationDefinition? ToDomain(CircuitAnnotationFileDto? dto)
    {
        if (dto is null) return null;
        return new CircuitAnnotationDefinition(
            dto.Id ?? string.Empty,
            dto.Type ?? string.Empty,
            dto.Text ?? string.Empty,
            dto.X,
            dto.Y
        );
    }

    private static GraphingQuestionDefinition? ToDomain(GraphingQuestionFileDto? dto)
    {
        if (dto is null) return null;
        return new GraphingQuestionDefinition(
            dto.GridType ?? "cartesian",
            dto.InteractionMode ?? "drag"
        );
    }

    private static GraphingQuestionFileDto? ToDto(GraphingQuestionDefinition? domain)
    {
        if (domain is null) return null;
        return new GraphingQuestionFileDto
        {
            GridType = domain.GridType,
            InteractionMode = domain.InteractionMode
        };
    }

    private static CircuitAnswerDefinition? ToDomain(CircuitAnswerFileDto? dto)
    {
        if (dto is null) return null;
        return new CircuitAnswerDefinition(
            ToDomain(dto.Topology),
            dto.SelectedTargetIds,
            ToDomain(dto.MeterPlacement),
            dto.ExpectedValues?.ToDictionary(p => p.Key, p => ToDomain(p.Value))
        );
    }

    private static CircuitTopologyDefinition? ToDomain(CircuitTopologyFileDto? dto)
    {
        if (dto is null) return null;
        return new CircuitTopologyDefinition(
            (dto.RequiredComponents ?? new List<RequiredComponentFileDto>()).Select(ToDomain).ToList(),
            dto.ConnectionMode ?? "graphIsomorphism"
        );
    }

    private static RequiredComponentDefinition ToDomain(RequiredComponentFileDto dto)
    {
        return new RequiredComponentDefinition(dto.SymbolId ?? string.Empty, dto.Count);
    }

    private static CircuitMeterPlacementDefinition? ToDomain(CircuitMeterPlacementFileDto? dto)
    {
        if (dto is null) return null;
        return new CircuitMeterPlacementDefinition(
            dto.MeterType ?? string.Empty,
            dto.TargetBranchId,
            dto.TargetNodeIds,
            dto.RequirePolarity,
            dto.PositiveTerminalId,
            dto.NegativeTerminalId
        );
    }

    private static ExpectedValueDefinition ToDomain(ExpectedValueFileDto dto)
    {
        return new ExpectedValueDefinition(
            dto.Mode ?? "text",
            dto.ExpectedText,
            dto.NumericValue,
            dto.NumericTolerance,
            dto.SymbolicExpectedLatex,
            dto.SymbolicEquivalenceMode,
            dto.SymbolicVariables,
            dto.SymbolicTolerance
        );
    }

    private static GraphingAnswerDefinition? ToDomain(GraphingAnswerFileDto? dto)
    {
        if (dto is null) return null;
        return new GraphingAnswerDefinition(
            (dto.Features ?? new List<ExpectedGraphFeatureFileDto>()).Select(ToDomain).ToList()
        );
    }

    private static ExpectedGraphFeature ToDomain(ExpectedGraphFeatureFileDto dto)
    {
        return new ExpectedGraphFeature(
            dto.Type ?? string.Empty,
            dto.X,
            dto.Y,
            dto.Value,
            dto.StringValue,
            dto.Tolerance ?? 0,
            dto.Weight ?? 0
        );
    }

    private static CircuitQuestionFileDto? ToDto(CircuitQuestionDefinition? domain)
    {
        if (domain is null) return null;
        return new CircuitQuestionFileDto
        {
            SchemaVersion = domain.SchemaVersion,
            CatalogVersion = domain.CatalogVersion,
            InteractionMode = domain.InteractionMode,
            PaletteSymbolIds = domain.PaletteSymbolIds.ToList(),
            EditableProperties = domain.EditableProperties.ToList(),
            Diagram = ToDto(domain.Diagram)
        };
    }

    private static CircuitDiagramFileDto? ToDto(CircuitDiagramDefinition? domain)
    {
        if (domain is null) return null;
        return new CircuitDiagramFileDto
        {
            Width = domain.Width,
            Height = domain.Height,
            Components = domain.Components.Select(ToDto).ToList(),
            Nodes = domain.Nodes.Select(ToDto).ToList(),
            Wires = domain.Wires.Select(ToDto).ToList(),
            Annotations = domain.Annotations.Select(ToDto).ToList()
        };
    }

    private static CircuitComponentInstanceFileDto ToDto(CircuitComponentInstance domain)
    {
        return new CircuitComponentInstanceFileDto
        {
            Id = domain.Id,
            SymbolId = domain.SymbolId,
            X = domain.X,
            Y = domain.Y,
            Rotation = domain.Rotation,
            Value = domain.Value,
            Label = domain.Label,
            PropertyOverrides = domain.PropertyOverrides?.ToDictionary(p => p.Key, p => p.Value)
        };
    }

    private static CircuitNodeFileDto ToDto(CircuitNodeDefinition domain)
    {
        return new CircuitNodeFileDto { Id = domain.Id, Label = domain.Label, X = domain.X, Y = domain.Y };
    }

    private static CircuitWireFileDto ToDto(CircuitWireDefinition domain)
    {
        return new CircuitWireFileDto
        {
            Id = domain.Id,
            SourceId = domain.SourceId,
            TargetId = domain.TargetId,
            RoutePoints = domain.RoutePoints?.Select(ToDto).ToList()
        };
    }

    private static CircuitPointFileDto ToDto(CircuitPoint domain)
    {
        return new CircuitPointFileDto { X = domain.X, Y = domain.Y };
    }

    private static CircuitAnnotationFileDto ToDto(CircuitAnnotationDefinition domain)
    {
        return new CircuitAnnotationFileDto
        {
            Id = domain.Id,
            Type = domain.Type,
            Text = domain.Text,
            X = domain.X,
            Y = domain.Y
        };
    }

    private static CircuitAnswerFileDto? ToDto(CircuitAnswerDefinition? domain)
    {
        if (domain is null) return null;
        return new CircuitAnswerFileDto
        {
            Topology = ToDto(domain.Topology),
            SelectedTargetIds = domain.SelectedTargetIds?.ToList(),
            MeterPlacement = ToDto(domain.MeterPlacement),
            ExpectedValues = domain.ExpectedValues?.ToDictionary(p => p.Key, p => ToDto(p.Value))
        };
    }

    private static CircuitTopologyFileDto? ToDto(CircuitTopologyDefinition? domain)
    {
        if (domain is null) return null;
        return new CircuitTopologyFileDto
        {
            RequiredComponents = domain.RequiredComponents.Select(ToDto).ToList(),
            ConnectionMode = domain.ConnectionMode
        };
    }

    private static RequiredComponentFileDto ToDto(RequiredComponentDefinition domain)
    {
        return new RequiredComponentFileDto { SymbolId = domain.SymbolId, Count = domain.Count };
    }

    private static CircuitMeterPlacementFileDto? ToDto(CircuitMeterPlacementDefinition? domain)
    {
        if (domain is null) return null;
        return new CircuitMeterPlacementFileDto
        {
            MeterType = domain.MeterType,
            TargetBranchId = domain.TargetBranchId,
            TargetNodeIds = domain.TargetNodeIds?.ToList(),
            RequirePolarity = domain.RequirePolarity,
            PositiveTerminalId = domain.PositiveTerminalId,
            NegativeTerminalId = domain.NegativeTerminalId
        };
    }

    private static ExpectedValueFileDto ToDto(ExpectedValueDefinition domain)
    {
        return new ExpectedValueFileDto
        {
            Mode = domain.Mode,
            ExpectedText = domain.ExpectedText,
            NumericValue = domain.NumericValue,
            NumericTolerance = domain.NumericTolerance,
            SymbolicExpectedLatex = domain.SymbolicExpectedLatex,
            SymbolicEquivalenceMode = domain.SymbolicEquivalenceMode,
            SymbolicVariables = domain.SymbolicVariables?.ToList(),
            SymbolicTolerance = domain.SymbolicTolerance
        };
    }

    private static GraphingAnswerFileDto? ToDto(GraphingAnswerDefinition? domain)
    {
        if (domain is null) return null;
        return new GraphingAnswerFileDto
        {
            Features = domain.Features.Select(ToDto).ToList()
        };
    }

    private static ExpectedGraphFeatureFileDto ToDto(ExpectedGraphFeature domain)
    {
        return new ExpectedGraphFeatureFileDto
        {
            Type = domain.Type,
            X = domain.X,
            Y = domain.Y,
            Value = domain.Value,
            StringValue = domain.StringValue,
            Tolerance = domain.Tolerance,
            Weight = domain.Weight
        };
    }

    // ─── Directed Project Mappers ──────────────────────────────────────────────────────

    private static DirectedProjectDefinition ToDomain(DirectedProjectFileDto dto)
    {
        return new DirectedProjectDefinition(
            dto.Summary ?? string.Empty,
            dto.Outcomes ?? new List<string>(),
            (dto.Phases ?? new List<DirectedProjectPhaseFileDto>()).Select(ToDomain).ToList())
        {
            EstimatedTimeMinutes = dto.EstimatedTimeMinutes,
            Environment = dto.Environment is null ? null : ToDomain(dto.Environment),
            Resources = (dto.Resources ?? new List<DirectedProjectResourceFileDto>()).Select(ToDomain).ToList()
        };
    }

    private static DirectedProjectEnvironmentDefinition ToDomain(DirectedProjectEnvironmentFileDto dto)
    {
        return new DirectedProjectEnvironmentDefinition(dto.Name ?? string.Empty)
        {
            Platform = dto.Platform ?? new List<string>(),
            ToolVersion = dto.ToolVersion,
            RequiredAccounts = dto.RequiredAccounts ?? new List<string>(),
            Prerequisites = dto.Prerequisites ?? new List<string>(),
            InstallLinks = (dto.InstallLinks ?? new List<DirectedProjectResourceFileDto>()).Select(ToDomain).ToList()
        };
    }

    private static DirectedProjectResourceDefinition ToDomain(DirectedProjectResourceFileDto dto)
    {
        return new DirectedProjectResourceDefinition(
            dto.Label ?? string.Empty,
            dto.Kind ?? "external")
        {
            Url = dto.Url,
            Target = dto.Target
        };
    }

    private static DirectedProjectPhaseDefinition ToDomain(DirectedProjectPhaseFileDto dto)
    {
        return new DirectedProjectPhaseDefinition(
            dto.Id ?? string.Empty,
            dto.Title ?? string.Empty,
            dto.Required ?? true,
            (dto.Steps ?? new List<DirectedProjectStepFileDto>()).Select(ToDomain).ToList())
        {
            Goal = dto.Goal
        };
    }

    private static DirectedProjectStepDefinition ToDomain(DirectedProjectStepFileDto dto)
    {
        return new DirectedProjectStepDefinition(
            dto.Id ?? string.Empty,
            dto.Title ?? string.Empty,
            dto.Instruction ?? string.Empty)
        {
            ExpectedObservation = dto.ExpectedObservation,
            Commands = (dto.Commands ?? new List<DirectedProjectCommandFileDto>()).Select(ToDomain).ToList(),
            Files = (dto.Files ?? new List<DirectedProjectFileReferenceFileDto>()).Select(ToDomain).ToList(),
            Media = (dto.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList(),
            Checklist = (dto.Checklist ?? new List<DirectedProjectChecklistItemFileDto>()).Select(ToDomain).ToList(),
            Troubleshooting = (dto.Troubleshooting ?? new List<DirectedProjectTroubleshootingFileDto>()).Select(ToDomain).ToList(),
            Resources = (dto.Resources ?? new List<DirectedProjectResourceFileDto>()).Select(ToDomain).ToList()
        };
    }

    private static DirectedProjectChecklistItemDefinition ToDomain(DirectedProjectChecklistItemFileDto dto)
        => new(dto.Id ?? string.Empty, dto.Text ?? string.Empty);

    private static DirectedProjectTroubleshootingDefinition ToDomain(DirectedProjectTroubleshootingFileDto dto)
        => new(dto.Problem ?? string.Empty, dto.Suggestion ?? string.Empty);

    private static DirectedProjectCommandDefinition ToDomain(DirectedProjectCommandFileDto dto)
    {
        return new DirectedProjectCommandDefinition(
            dto.Label ?? string.Empty,
            dto.Command ?? string.Empty)
        {
            Shell = dto.Shell,
            WorkingDirectory = dto.WorkingDirectory,
            ExpectedOutput = dto.ExpectedOutput,
            Notes = dto.Notes
        };
    }

    private static DirectedProjectFileDefinition ToDomain(DirectedProjectFileReferenceFileDto dto)
    {
        return new DirectedProjectFileDefinition(
            dto.Path ?? string.Empty,
            dto.Purpose ?? string.Empty)
        {
            SuggestedContent = dto.SuggestedContent,
            ReadOnly = dto.ReadOnly
        };
    }

    private static DirectedProjectFileDto ToDto(DirectedProjectDefinition domain)
    {
        return new DirectedProjectFileDto
        {
            Summary = domain.Summary,
            EstimatedTimeMinutes = domain.EstimatedTimeMinutes,
            Environment = domain.Environment is null ? null : ToDto(domain.Environment),
            Outcomes = domain.Outcomes.ToList(),
            Resources = domain.Resources.Select(ToDto).ToList(),
            Phases = domain.Phases.Select(ToDto).ToList()
        };
    }

    private static DirectedProjectEnvironmentFileDto ToDto(DirectedProjectEnvironmentDefinition domain)
    {
        return new DirectedProjectEnvironmentFileDto
        {
            Name = domain.Name,
            Platform = domain.Platform.ToList(),
            ToolVersion = domain.ToolVersion,
            RequiredAccounts = domain.RequiredAccounts.ToList(),
            Prerequisites = domain.Prerequisites.ToList(),
            InstallLinks = domain.InstallLinks.Select(ToDto).ToList()
        };
    }

    private static DirectedProjectResourceFileDto ToDto(DirectedProjectResourceDefinition domain)
    {
        return new DirectedProjectResourceFileDto
        {
            Label = domain.Label,
            Kind = domain.Kind,
            Url = domain.Url,
            Target = domain.Target
        };
    }

    private static DirectedProjectPhaseFileDto ToDto(DirectedProjectPhaseDefinition domain)
    {
        return new DirectedProjectPhaseFileDto
        {
            Id = domain.Id,
            Title = domain.Title,
            Required = domain.Required,
            Goal = domain.Goal,
            Steps = domain.Steps.Select(ToDto).ToList()
        };
    }

    private static DirectedProjectStepFileDto ToDto(DirectedProjectStepDefinition domain)
    {
        return new DirectedProjectStepFileDto
        {
            Id = domain.Id,
            Title = domain.Title,
            Instruction = domain.Instruction,
            ExpectedObservation = domain.ExpectedObservation,
            Commands = domain.Commands.Select(ToDto).ToList(),
            Files = domain.Files.Select(ToDto).ToList(),
            Media = domain.Media.Select(ToDto).ToList(),
            Checklist = domain.Checklist.Select(ToDto).ToList(),
            Troubleshooting = domain.Troubleshooting.Select(ToDto).ToList(),
            Resources = domain.Resources.Select(ToDto).ToList()
        };
    }

    private static DirectedProjectChecklistItemFileDto ToDto(DirectedProjectChecklistItemDefinition domain)
        => new() { Id = domain.Id, Text = domain.Text };

    private static DirectedProjectTroubleshootingFileDto ToDto(DirectedProjectTroubleshootingDefinition domain)
        => new() { Problem = domain.Problem, Suggestion = domain.Suggestion };

    private static DirectedProjectCommandFileDto ToDto(DirectedProjectCommandDefinition domain)
    {
        return new DirectedProjectCommandFileDto
        {
            Label = domain.Label,
            Command = domain.Command,
            Shell = domain.Shell,
            WorkingDirectory = domain.WorkingDirectory,
            ExpectedOutput = domain.ExpectedOutput,
            Notes = domain.Notes
        };
    }

    private static DirectedProjectFileReferenceFileDto ToDto(DirectedProjectFileDefinition domain)
    {
        return new DirectedProjectFileReferenceFileDto
        {
            Path = domain.Path,
            Purpose = domain.Purpose,
            SuggestedContent = domain.SuggestedContent,
            ReadOnly = domain.ReadOnly
        };
    }
}
