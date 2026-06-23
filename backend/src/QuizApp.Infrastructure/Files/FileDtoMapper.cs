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
                    subcategory.Description))
                .ToList(),
            dto.Description);
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
            dto.SubcategoryIds ?? new List<string>(),
            ParseMode(dto.ModeDefault, AssessmentMode.Practice),
            dto.RandomizeQuestions ?? true,
            dto.AttemptQuestionCount,
            dto.QuestionTimerSeconds,
            dto.AssessmentTimerSeconds,
            (dto.Questions ?? new List<QuestionFileDto>()).Select(ToDomain).ToList())
        {
            WorkedExamples = (dto.WorkedExamples ?? new List<WorkedExampleFileDto>()).Select(ToDomain).ToList(),
            GuidedProject = dto.GuidedProject is null ? null : ToDomain(dto.GuidedProject),
            Items = (dto.Items ?? new List<RecallItemFileDto>()).Select(ToDomain).ToList(),
            Lesson = dto.Lesson is null ? null : ToDomain(dto.Lesson),
            Exploration = dto.Exploration is null ? null : ToDomain(dto.Exploration),
            Navigation = dto.Navigation is null ? null : new NavigationMetadata(
                dto.Navigation.LearningGoal,
                dto.Navigation.ActivityType,
                dto.Navigation.Tags ?? new List<string>())
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
            SubcategoryIds = assessment.SubcategoryIds.ToList(),
            ModeDefault = ToWireValue(assessment.ModeDefault),
            RandomizeQuestions = assessment.RandomizeQuestions,
            AttemptQuestionCount = assessment.AttemptQuestionCount,
            QuestionTimerSeconds = assessment.QuestionTimerSeconds,
            AssessmentTimerSeconds = assessment.AssessmentTimerSeconds,
            Questions = assessment.Questions.Select(ToDto).ToList(),
            WorkedExamples = assessment.WorkedExamples.Select(ToDto).ToList(),
            GuidedProject = assessment.GuidedProject is null ? null : ToDto(assessment.GuidedProject),
            Items = assessment.Items.Select(ToDto).ToList(),
            Lesson = assessment.Lesson is null ? null : ToDto(assessment.Lesson),
            Exploration = assessment.Exploration is null ? null : ToDto(assessment.Exploration),
            Navigation = assessment.Navigation is null ? null : new NavigationFileDto
            {
                LearningGoal = assessment.Navigation.LearningGoal,
                ActivityType = assessment.Navigation.ActivityType,
                Tags = assessment.Navigation.Tags.ToList()
            }
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
            dto.Tags ?? new List<string>());
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
                Media = item.Answer.Media.Select(ToDto).ToList()
            },
            Explanation = item.Explanation,
            Tags = item.Tags.ToList()
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
            StarterCode = dto.StarterCode,
            Tests = dto.Tests
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
            StarterCode = question.StarterCode,
            Tests = question.Tests
        };
    }

    private static QuestionDefinition ToDomain(QuestionFileDto dto)
    {
        var type = ParseQuestionType(dto.Type);
        return new QuestionDefinition(
            dto.Id ?? string.Empty,
            type,
            dto.Prompt ?? string.Empty,
            (dto.Choices ?? new List<ChoiceFileDto>())
                .Select(choice => new ChoiceOption(
                    choice.Id ?? string.Empty,
                    choice.Text ?? string.Empty,
                    (choice.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList()))
                .ToList(),
            new AnswerDefinition(
                dto.Answer?.ChoiceId,
                dto.Answer?.ChoiceIds ?? new List<string>(),
                dto.Answer?.Expected,
                dto.Answer?.GradingMode,
                dto.Answer?.Value,
                dto.Answer?.Tolerance,
                (dto.Answer?.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList())
            {
                ExpectedLatex = dto.Answer?.ExpectedLatex,
                EquivalenceMode = dto.Answer?.EquivalenceMode,
                Variables = dto.Answer?.Variables ?? new List<string>(),
                Tolerance = dto.Answer?.Tolerance,
                SymbolicExpectedLatex = dto.Answer?.ExpectedLatex,
                SymbolicEquivalenceMode = dto.Answer?.EquivalenceMode,
                SymbolicVariables = dto.Answer?.Variables ?? new List<string>(),
                SymbolicTolerance = dto.Answer?.Tolerance,
                KeyPoints = dto.Answer?.KeyPoints ?? new List<string>(),
                CircuitAnswer = ToDomain(dto.Answer?.CircuitAnswer)
            },
            dto.Explanation,
            (dto.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList())
        {
            CodeQuestion = ToCodeQuestion(dto),
            CircuitQuestion = ToDomain(dto.CircuitQuestion)
        };
    }

    private static QuestionFileDto ToDto(QuestionDefinition question)
    {
        return new QuestionFileDto
        {
            Id = question.Id,
            Type = ToWireValue(question.Type),
            Prompt = question.Prompt,
            Choices = question.Choices.Select(choice => new ChoiceFileDto
            {
                Id = choice.Id,
                Text = choice.Text,
                Media = choice.Media.Select(ToDto).ToList()
            }).ToList(),
            Answer = new AnswerFileDto
            {
                ChoiceId = question.Answer.ChoiceId,
                ChoiceIds = question.Answer.ChoiceIds.ToList(),
                Expected = question.Answer.Expected,
                GradingMode = question.Answer.GradingMode,
                ExpectedLatex = question.Answer.SymbolicExpectedLatex ?? question.Answer.ExpectedLatex,
                EquivalenceMode = question.Answer.SymbolicEquivalenceMode ?? question.Answer.EquivalenceMode,
                Variables = (question.Answer.SymbolicVariables.Count > 0 ? question.Answer.SymbolicVariables : question.Answer.Variables).ToList(),
                Value = question.Answer.NumericValue,
                Tolerance = question.Answer.NumericTolerance ?? question.Answer.SymbolicTolerance ?? question.Answer.Tolerance,
                Media = question.Answer.Media.Select(ToDto).ToList(),
                KeyPoints = question.Answer.KeyPoints.ToList(),
                CircuitAnswer = ToDto(question.Answer.CircuitAnswer)
            },
            Explanation = question.Explanation,
            Media = question.Media.Select(ToDto).ToList(),
            Language = question.CodeQuestion?.Language,
            FunctionName = question.CodeQuestion?.FunctionName,
            StarterCode = question.CodeQuestion?.StarterCode,
            Tests = question.CodeQuestion?.Tests.Select(test => new CodeQuestionTestFileDto
            {
                Input = test.Input,
                Expected = test.Expected
            }).ToList(),
            CircuitQuestion = ToDto(question.CircuitQuestion)
        };
    }

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
                .ToList());
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
            "conceptlesson" => AssessmentType.ConceptLesson,
            "interactiveexploration" => AssessmentType.InteractiveExploration,
            _ => AssessmentType.Unknown
        };
    }

    private static RecallItemType ParseRecallItemType(string? value)
    {
        return Normalize(value) switch
        {
            "typed" => RecallItemType.Typed,
            "symbolic" => RecallItemType.Symbolic,
            "flashcard" => RecallItemType.Flashcard,
            "cloze" => RecallItemType.Cloze,
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
            _ => QuestionType.Unknown
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

    private static string ToWireValue(AssessmentMode mode)
    {
        return mode is AssessmentMode.Scored ? "scored" : "practice";
    }

    private static string ToWireValue(AssessmentType assessmentType)
    {
        return assessmentType switch
        {
            AssessmentType.Test => "test",
            AssessmentType.WorkedExample => "workedExample",
            AssessmentType.GuidedProject => "guidedProject",
            AssessmentType.RecallDrill => "recallDrill",
            AssessmentType.ConceptLesson => "conceptLesson",
            AssessmentType.InteractiveExploration => "interactiveExploration",
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

    private static CircuitAnnotationDefinition ToDomain(CircuitAnnotationFileDto dto)
    {
        return new CircuitAnnotationDefinition(
            dto.Id ?? string.Empty,
            dto.Type ?? string.Empty,
            dto.Text ?? string.Empty,
            dto.X,
            dto.Y
        );
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
}
