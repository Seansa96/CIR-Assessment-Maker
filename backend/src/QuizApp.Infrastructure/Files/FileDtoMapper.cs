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
            (dto.Questions ?? new List<QuestionFileDto>()).Select(ToDomain).ToList());
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
            Questions = assessment.Questions.Select(ToDto).ToList()
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
                (dto.Answer?.Media ?? new List<MediaFileDto>()).Select(ToDomain).ToList()),
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
                Value = question.Answer.NumericValue,
                Tolerance = question.Answer.NumericTolerance,
                Media = question.Answer.Media.Select(ToDto).ToList()
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
        return assessmentType is AssessmentType.Test ? "test" : "quiz";
    }

    private static string ToWireValue(QuestionType questionType)
    {
        return questionType switch
        {
            QuestionType.SelectAll => "selectAll",
            QuestionType.FreeResponse => "freeResponse",
            QuestionType.NumericResponse => "numericResponse",
            QuestionType.Code => "code",
            _ => "multipleChoice"
        };
    }

    private static string Normalize(string? value)
    {
        return string.Concat((value ?? string.Empty).Where(char.IsLetterOrDigit)).ToLowerInvariant();
    }
}
