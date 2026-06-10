using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public sealed class AssessmentValidator
{
    public const int QuizMaxQuestions = 50;
    public const int TestMaxQuestions = 200;

    public AssessmentValidationResult Validate(AssessmentDefinition assessment)
    {
        var issues = new List<ValidationIssue>();

        RequireText(assessment.Id, "MISSING_ID", "Assessment id is required.", issues);
        RequireText(assessment.Title, "MISSING_TITLE", "Assessment title is required.", issues);
        RequireText(assessment.CategoryId, "MISSING_CATEGORY_ID", "Category id is required.", issues);

        if (assessment.SchemaVersion <= 0)
        {
            issues.Add(new ValidationIssue("INVALID_SCHEMA_VERSION", "schemaVersion must be greater than zero."));
        }

        if (assessment.AssessmentType is AssessmentType.Unknown)
        {
            issues.Add(new ValidationIssue("INVALID_ASSESSMENT_TYPE", "Assessment type must be quiz or test."));
        }

        if (assessment.QuestionTimerSeconds is < 0)
        {
            issues.Add(new ValidationIssue("INVALID_QUESTION_TIMER", "Question timer must be null or a non-negative number of seconds."));
        }

        if (assessment.AssessmentTimerSeconds is < 0)
        {
            issues.Add(new ValidationIssue("INVALID_ASSESSMENT_TIMER", "Assessment timer must be null or a non-negative number of seconds."));
        }

        var questionCount = assessment.Questions.Count;
        if (assessment.AssessmentType is AssessmentType.Quiz && questionCount > QuizMaxQuestions)
        {
            issues.Add(new ValidationIssue("QUIZ_TOO_LONG", $"Quiz assessments cannot exceed {QuizMaxQuestions} questions."));
        }

        if (assessment.AssessmentType is AssessmentType.Test && questionCount > TestMaxQuestions)
        {
            issues.Add(new ValidationIssue("TEST_TOO_LONG", $"Test assessments cannot exceed {TestMaxQuestions} questions."));
        }

        var duplicateQuestionIds = assessment.Questions
            .Where(q => !string.IsNullOrWhiteSpace(q.Id))
            .GroupBy(q => q.Id, StringComparer.OrdinalIgnoreCase)
            .Where(group => group.Count() > 1)
            .Select(group => group.Key);

        foreach (var duplicateId in duplicateQuestionIds)
        {
            issues.Add(new ValidationIssue("DUPLICATE_QUESTION_ID", $"Question id '{duplicateId}' is duplicated.", duplicateId));
        }

        foreach (var question in assessment.Questions)
        {
            ValidateQuestion(question, issues);
        }

        return new AssessmentValidationResult(issues);
    }

    private static void ValidateQuestion(QuestionDefinition question, List<ValidationIssue> issues)
    {
        RequireText(question.Id, "MISSING_QUESTION_ID", "Question id is required.", issues);
        RequireText(question.Prompt, "MISSING_PROMPT", "Question prompt is required.", issues, question.Id);

        if (question.Type is QuestionType.Unknown)
        {
            issues.Add(new ValidationIssue("INVALID_QUESTION_TYPE", "Question type must be multipleChoice, selectAll, freeResponse, numericResponse, code, or symbolicResponse.", question.Id));
            return;
        }

        var choiceIds = question.Choices.Select(choice => choice.Id).ToHashSet(StringComparer.OrdinalIgnoreCase);
        ValidateMedia(question.Media, issues, question.Id);
        foreach (var choice in question.Choices)
        {
            ValidateMedia(choice.Media, issues, question.Id);
        }
        ValidateMedia(question.Answer.Media, issues, question.Id);

        if (question.Type is QuestionType.MultipleChoice)
        {
            if (question.Choices.Count == 0)
            {
                issues.Add(new ValidationIssue("MULTIPLE_CHOICE_WITHOUT_CHOICES", "Multiple choice questions must include choices.", question.Id));
            }

            if (string.IsNullOrWhiteSpace(question.Answer.ChoiceId) || !choiceIds.Contains(question.Answer.ChoiceId))
            {
                issues.Add(new ValidationIssue("MULTIPLE_CHOICE_ANSWER_NOT_FOUND", "Multiple choice answer choiceId must match a choice.", question.Id));
            }
        }

        if (question.Type is QuestionType.SelectAll)
        {
            if (question.Choices.Count == 0)
            {
                issues.Add(new ValidationIssue("SELECT_ALL_WITHOUT_CHOICES", "Select-all questions must include choices.", question.Id));
            }

            var missingChoiceIds = question.Answer.ChoiceIds.Where(choiceId => !choiceIds.Contains(choiceId)).ToList();
            if (question.Answer.ChoiceIds.Count == 0 || missingChoiceIds.Count > 0)
            {
                issues.Add(new ValidationIssue("SELECT_ALL_ANSWER_NOT_FOUND", "Select-all answer choiceIds must match choices.", question.Id));
            }
        }

        if (question.Type is QuestionType.FreeResponse)
        {
            if (!string.Equals(question.Answer.GradingMode, "selfCheck", StringComparison.OrdinalIgnoreCase))
            {
                issues.Add(new ValidationIssue("INVALID_FREE_RESPONSE_GRADING", "Free response questions must use selfCheck grading for the MVP.", question.Id));
            }
        }

        if (question.Type is QuestionType.NumericResponse)
        {
            if (question.Answer.NumericValue is null)
            {
                issues.Add(new ValidationIssue("MISSING_NUMERIC_ANSWER", "Numeric response questions must include answer.value.", question.Id));
            }

            if (question.Answer.NumericTolerance is null or < 0)
            {
                issues.Add(new ValidationIssue("INVALID_NUMERIC_TOLERANCE", "Numeric response questions must include a non-negative answer.tolerance.", question.Id));
            }
        }

        if (question.Type is QuestionType.Code)
        {
            ValidateCodeQuestion(question, issues);
        }

        if (question.Type is QuestionType.SymbolicResponse)
        {
            ValidateSymbolicQuestion(question, issues);
        }
    }

    private static void RequireText(string? value, string code, string message, List<ValidationIssue> issues, string? questionId = null)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            issues.Add(new ValidationIssue(code, message, questionId));
        }
    }

    private static void ValidateMedia(IReadOnlyList<MediaAsset> media, List<ValidationIssue> issues, string? questionId)
    {
        foreach (var item in media)
        {
            if (!string.Equals(item.Type, "image", StringComparison.OrdinalIgnoreCase))
            {
                issues.Add(new ValidationIssue("INVALID_MEDIA_TYPE", "Only image media is supported for now.", questionId));
            }

            if (string.IsNullOrWhiteSpace(item.Src))
            {
                issues.Add(new ValidationIssue("MISSING_MEDIA_SRC", "Image media must include src.", questionId));
            }

            if (string.IsNullOrWhiteSpace(item.Alt))
            {
                issues.Add(new ValidationIssue("MISSING_MEDIA_ALT", "Image media must include alt text.", questionId));
            }
        }
    }

    private static void ValidateCodeQuestion(QuestionDefinition question, List<ValidationIssue> issues)
    {
        var codeQuestion = question.CodeQuestion;
        if (codeQuestion is null)
        {
            issues.Add(new ValidationIssue("MISSING_CODE_DEFINITION", "Code questions must include language, functionName, starterCode, and tests.", question.Id));
            return;
        }

        if (!string.Equals(codeQuestion.Language, "python", StringComparison.OrdinalIgnoreCase)
            && !string.Equals(codeQuestion.Language, "cpp", StringComparison.OrdinalIgnoreCase))
        {
            issues.Add(new ValidationIssue("INVALID_CODE_LANGUAGE", "Code question language must be python or cpp.", question.Id));
        }

        RequireText(codeQuestion.FunctionName, "MISSING_CODE_FUNCTION_NAME", "Code questions must include functionName.", issues, question.Id);
        RequireText(codeQuestion.StarterCode, "MISSING_STARTER_CODE", "Code questions must include starterCode.", issues, question.Id);

        if (codeQuestion.Tests.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_CODE_TESTS", "Code questions must include at least one test.", question.Id));
        }

        foreach (var test in codeQuestion.Tests)
        {
            RequireText(test.Input, "MISSING_CODE_TEST_INPUT", "Code question tests must include input.", issues, question.Id);
            RequireText(test.Expected, "MISSING_CODE_TEST_EXPECTED", "Code question tests must include expected.", issues, question.Id);
        }
    }

    private static void ValidateSymbolicQuestion(QuestionDefinition question, List<ValidationIssue> issues)
    {
        var expectedLatex = question.Answer.SymbolicExpectedLatex ?? question.Answer.ExpectedLatex;
        var equivalenceMode = question.Answer.SymbolicEquivalenceMode ?? question.Answer.EquivalenceMode;
        var variables = question.Answer.SymbolicVariables.Count > 0 ? question.Answer.SymbolicVariables : question.Answer.Variables;
        var tolerance = question.Answer.SymbolicTolerance ?? question.Answer.Tolerance;

        RequireText(expectedLatex, "MISSING_SYMBOLIC_EXPECTED_LATEX", "Symbolic response questions must include answer.expectedLatex.", issues, question.Id);

        if (!string.Equals(equivalenceMode, "expression", StringComparison.OrdinalIgnoreCase)
            && !string.Equals(equivalenceMode, "derivative", StringComparison.OrdinalIgnoreCase))
        {
            issues.Add(new ValidationIssue("INVALID_SYMBOLIC_EQUIVALENCE_MODE", "Symbolic response equivalenceMode must be expression or derivative.", question.Id));
        }

        if (string.Equals(equivalenceMode, "derivative", StringComparison.OrdinalIgnoreCase)
            && variables.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_SYMBOLIC_VARIABLE", "Derivative equivalence requires at least one variable.", question.Id));
        }

        if (tolerance is null or < 0)
        {
            issues.Add(new ValidationIssue("INVALID_SYMBOLIC_TOLERANCE", "Symbolic response questions must include a non-negative answer.tolerance.", question.Id));
        }
    }
}
