using QuizApp.Core.Domain;

namespace QuizApp.Infrastructure.Files;

internal static class FileDtoMapper
{
    public static Category ToDomain(this CategoryFileDto dto)
    {
        return new Category(
            dto.SchemaVersion,
            dto.Id ?? string.Empty,
            dto.Title ?? string.Empty,
            (dto.Subcategories ?? new List<SubCategoryFileDto>())
                .Select(subcategory => new SubCategory(subcategory.Id ?? string.Empty, subcategory.Title ?? string.Empty))
                .ToList());
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
            dto.QuestionTimerSeconds,
            dto.AssessmentTimerSeconds,
            (dto.Questions ?? new List<QuestionFileDto>()).Select(ToDomain).ToList())
        {
            WorkedExamples = (dto.WorkedExamples ?? new List<WorkedExampleFileDto>()).Select(ToDomain).ToList(),
            GuidedProject = dto.GuidedProject is null ? null : ToDomain(dto.GuidedProject)
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
            QuestionTimerSeconds = assessment.QuestionTimerSeconds,
            AssessmentTimerSeconds = assessment.AssessmentTimerSeconds,
            Questions = assessment.Questions.Select(ToDto).ToList(),
            WorkedExamples = assessment.WorkedExamples.Select(ToDto).ToList(),
            GuidedProject = assessment.GuidedProject is null ? null : ToDto(assessment.GuidedProject)
        };
    }

    private static GuidedProjectDefinition ToDomain(GuidedProjectFileDto dto)
    {
        return new GuidedProjectDefinition(
            dto.Language ?? string.Empty,
            dto.Instructions ?? string.Empty,
            (dto.Files ?? new List<GuidedProjectSourceFileDto>())
                .Select(file => new GuidedProjectFileDefinition(
                    file.Path ?? string.Empty,
                    file.Content ?? string.Empty,
                    file.ReadOnly))
                .ToList(),
            (dto.RequiredChecks ?? new List<GuidedProjectCheckFileDto>()).Select(ToDomain).ToList(),
            (dto.BonusChecks ?? new List<GuidedProjectCheckFileDto>()).Select(ToDomain).ToList());
    }

    private static GuidedProjectFileDto ToDto(GuidedProjectDefinition project)
    {
        return new GuidedProjectFileDto
        {
            Language = project.Language,
            Instructions = project.Instructions,
            Files = project.Files.Select(file => new GuidedProjectSourceFileDto
            {
                Path = file.Path,
                Content = file.Content,
                ReadOnly = file.ReadOnly
            }).ToList(),
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
            dto.TestCode ?? string.Empty,
            dto.ExpectedOutputContains ?? new List<string>());
    }

    private static GuidedProjectCheckFileDto ToDto(GuidedProjectCheckDefinition check)
    {
        return new GuidedProjectCheckFileDto
        {
            Id = check.Id,
            Title = check.Title,
            Description = check.Description,
            TestCode = check.TestCode,
            ExpectedOutputContains = check.ExpectedOutputContains.ToList()
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
        return new QuestionDefinition(
            dto.Id ?? string.Empty,
            ParseQuestionType(dto.Type),
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
                KeyPoints = dto.Answer?.KeyPoints ?? new List<string>()
            },
            dto.Explanation,
            (dto.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList())
        {
            CodeQuestion = ToCodeQuestion(dto)
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
                KeyPoints = question.Answer.KeyPoints.ToList()
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
            }).ToList()
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
            _ => AssessmentType.Unknown
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
            _ => "quiz"
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
            _ => "multipleChoice"
        };
    }

    private static string Normalize(string? value)
    {
        return string.Concat((value ?? string.Empty).Where(char.IsLetterOrDigit)).ToLowerInvariant();
    }
}
