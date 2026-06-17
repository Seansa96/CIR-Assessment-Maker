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
            issues.Add(new ValidationIssue("INVALID_ASSESSMENT_TYPE", "Assessment type must be quiz, test, workedExample, guidedProject, or recallDrill."));
        }

        if (assessment.QuestionTimerSeconds is < 0)
        {
            issues.Add(new ValidationIssue("INVALID_QUESTION_TIMER", "Question timer must be null or a non-negative number of seconds."));
        }

        if (assessment.AssessmentTimerSeconds is < 0)
        {
            issues.Add(new ValidationIssue("INVALID_ASSESSMENT_TIMER", "Assessment timer must be null or a non-negative number of seconds."));
        }

        if (assessment.AssessmentType is AssessmentType.WorkedExample)
        {
            ValidateWorkedExamples(assessment, issues);
            return new AssessmentValidationResult(issues);
        }

        if (assessment.AssessmentType is AssessmentType.GuidedProject)
        {
            ValidateGuidedProject(assessment, issues);
            return new AssessmentValidationResult(issues);
        }

        if (assessment.AssessmentType is AssessmentType.RecallDrill)
        {
            ValidateRecallDrill(assessment, issues);
            return new AssessmentValidationResult(issues);
        }

        ValidateQuestions(assessment.Questions, issues);

        var questionCount = assessment.Questions.Count;
        if (assessment.AttemptQuestionCount is not null)
        {
            if (assessment.AssessmentType is not AssessmentType.Quiz and not AssessmentType.Test)
            {
                issues.Add(new ValidationIssue("INVALID_ATTEMPT_QUESTION_COUNT", "attemptQuestionCount is only supported for quiz and test assessments."));
            }
            else if (assessment.AttemptQuestionCount <= 0)
            {
                issues.Add(new ValidationIssue("INVALID_ATTEMPT_QUESTION_COUNT", "attemptQuestionCount must be greater than zero."));
            }
            else if (assessment.AttemptQuestionCount > questionCount)
            {
                issues.Add(new ValidationIssue("INVALID_ATTEMPT_QUESTION_COUNT", "attemptQuestionCount cannot exceed the number of authored questions."));
            }
        }

        if (assessment.AssessmentType is AssessmentType.Quiz && questionCount > QuizMaxQuestions)
        {
            issues.Add(new ValidationIssue("QUIZ_TOO_LONG", $"Quiz assessments cannot exceed {QuizMaxQuestions} questions."));
        }

        if (assessment.AssessmentType is AssessmentType.Test && questionCount > TestMaxQuestions)
        {
            issues.Add(new ValidationIssue("TEST_TOO_LONG", $"Test assessments cannot exceed {TestMaxQuestions} questions."));
        }

        return new AssessmentValidationResult(issues);
    }

    private static void ValidateRecallDrill(AssessmentDefinition assessment, List<ValidationIssue> issues)
    {
        if (assessment.Items.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_RECALL_ITEMS", "Recall drill assessments must include items."));
            return;
        }

        var duplicateItemIds = assessment.Items
            .Where(item => !string.IsNullOrWhiteSpace(item.Id))
            .GroupBy(item => item.Id, StringComparer.OrdinalIgnoreCase)
            .Where(group => group.Count() > 1)
            .Select(group => group.Key);

        foreach (var duplicateId in duplicateItemIds)
        {
            issues.Add(new ValidationIssue("DUPLICATE_RECALL_ITEM_ID", $"Recall item id '{duplicateId}' is duplicated.", duplicateId));
        }

        foreach (var item in assessment.Items)
        {
            RequireText(item.Id, "MISSING_RECALL_ITEM_ID", "Recall items must include an id.", issues);
            RequireText(item.Prompt, "MISSING_RECALL_PROMPT", "Recall items must include a prompt.", issues, item.Id);

            if (item.Type is RecallItemType.Unknown)
            {
                issues.Add(new ValidationIssue("INVALID_RECALL_ITEM_TYPE", "Recall item type must be typed, symbolic, flashcard, or cloze.", item.Id));
            }

            if (item.Type is RecallItemType.Symbolic)
            {
                RequireText(item.Answer.ExpectedLatex, "MISSING_RECALL_EXPECTED_LATEX", "Symbolic recall items must include answer.expectedLatex.", issues, item.Id);
            }
            else if (item.Type is not RecallItemType.Flashcard)
            {
                RequireText(item.Answer.Expected, "MISSING_RECALL_EXPECTED", "Recall items must include answer.expected.", issues, item.Id);
            }
            else if (string.IsNullOrWhiteSpace(item.Answer.Expected) && string.IsNullOrWhiteSpace(item.Answer.ExpectedLatex))
            {
                issues.Add(new ValidationIssue("MISSING_RECALL_EXPECTED", "Flashcard recall items must include answer.expected or answer.expectedLatex.", item.Id));
            }

            ValidateMedia(item.Answer.Media, issues, item.Id);
        }
    }

    private static void ValidateQuestions(IReadOnlyList<QuestionDefinition> questions, List<ValidationIssue> issues)
    {
        var duplicateQuestionIds = questions
            .Where(q => !string.IsNullOrWhiteSpace(q.Id))
            .GroupBy(q => q.Id, StringComparer.OrdinalIgnoreCase)
            .Where(group => group.Count() > 1)
            .Select(group => group.Key);

        foreach (var duplicateId in duplicateQuestionIds)
        {
            issues.Add(new ValidationIssue("DUPLICATE_QUESTION_ID", $"Question id '{duplicateId}' is duplicated.", duplicateId));
        }

        foreach (var question in questions)
        {
            ValidateQuestion(question, issues);
        }
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

    private static void ValidateWorkedExamples(AssessmentDefinition assessment, List<ValidationIssue> issues)
    {
        if (assessment.WorkedExamples.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_WORKED_EXAMPLES", "Worked example assessments must include workedExamples."));
            return;
        }

        var stepIds = new List<string>();
        foreach (var workedExample in assessment.WorkedExamples)
        {
            RequireText(workedExample.Id, "MISSING_WORKED_EXAMPLE_ID", "Worked examples must include an id.", issues);
            RequireText(workedExample.Title, "MISSING_WORKED_EXAMPLE_TITLE", "Worked examples must include a title.", issues);
            RequireText(workedExample.Problem, "MISSING_WORKED_EXAMPLE_PROBLEM", "Worked examples must include a problem.", issues);

            if (workedExample.Steps.Count == 0)
            {
                issues.Add(new ValidationIssue("MISSING_WORKED_EXAMPLE_STEPS", "Worked examples must include at least one step.", workedExample.Id));
            }

            foreach (var step in workedExample.Steps)
            {
                RequireText(step.Id, "MISSING_WORKED_EXAMPLE_STEP_ID", "Worked example steps must include an id.", issues, step.Id);
                RequireText(step.Title, "MISSING_WORKED_EXAMPLE_STEP_TITLE", "Worked example steps must include a title.", issues, step.Id);
                RequireText(step.Instruction, "MISSING_WORKED_EXAMPLE_STEP_INSTRUCTION", "Worked example steps must include instruction.", issues, step.Id);
                stepIds.Add(step.Id);
                ValidateQuestion(step.Question with { Id = step.Id }, issues);
            }
        }

        var duplicateStepIds = stepIds
            .Where(id => !string.IsNullOrWhiteSpace(id))
            .GroupBy(id => id, StringComparer.OrdinalIgnoreCase)
            .Where(group => group.Count() > 1)
            .Select(group => group.Key);

        foreach (var duplicateId in duplicateStepIds)
        {
            issues.Add(new ValidationIssue("DUPLICATE_WORKED_EXAMPLE_STEP_ID", $"Worked example step id '{duplicateId}' is duplicated.", duplicateId));
        }
    }

    private static void ValidateGuidedProject(AssessmentDefinition assessment, List<ValidationIssue> issues)
    {
        var project = assessment.GuidedProject;
        if (project is null)
        {
            issues.Add(new ValidationIssue("MISSING_GUIDED_PROJECT", "Guided project assessments must include guidedProject."));
            return;
        }

        if (!string.Equals(project.Language, "cpp", StringComparison.OrdinalIgnoreCase)
            && !string.Equals(project.Language, "python", StringComparison.OrdinalIgnoreCase))
        {
            issues.Add(new ValidationIssue("INVALID_GUIDED_PROJECT_LANGUAGE", "Guided project language must be cpp or python."));
        }

        RequireText(project.Instructions, "MISSING_GUIDED_PROJECT_INSTRUCTIONS", "Guided projects must include instructions.", issues);

        if (project.Files.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_GUIDED_PROJECT_FILES", "Guided projects must include at least one source file."));
        }

        if (!project.Files.Any(file => !file.ReadOnly))
        {
            issues.Add(new ValidationIssue("MISSING_EDITABLE_GUIDED_PROJECT_FILE", "Guided projects must include at least one editable source file."));
        }

        var duplicateFilePaths = project.Files
            .Where(file => !string.IsNullOrWhiteSpace(file.Path))
            .GroupBy(file => file.Path, StringComparer.OrdinalIgnoreCase)
            .Where(group => group.Count() > 1)
            .Select(group => group.Key);

        foreach (var duplicatePath in duplicateFilePaths)
        {
            issues.Add(new ValidationIssue("DUPLICATE_GUIDED_PROJECT_FILE", $"Guided project file path '{duplicatePath}' is duplicated."));
        }

        foreach (var file in project.Files)
        {
            RequireText(file.Path, "MISSING_GUIDED_PROJECT_FILE_PATH", "Guided project files must include path.", issues);
            if (!IsSafeRelativePath(file.Path))
            {
                issues.Add(new ValidationIssue("INVALID_GUIDED_PROJECT_FILE_PATH", $"Guided project file path '{file.Path}' must be a safe relative path."));
            }
        }

        if (project.RequiredChecks.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_GUIDED_PROJECT_REQUIRED_CHECKS", "Guided projects must include at least one required check."));
        }

        ValidateGuidedProjectChecks(project.RequiredChecks, issues, true);
        ValidateGuidedProjectChecks(project.BonusChecks, issues, false);
    }

    private static void ValidateGuidedProjectChecks(
        IReadOnlyList<GuidedProjectCheckDefinition> checks,
        List<ValidationIssue> issues,
        bool required)
    {
        var duplicateCheckIds = checks
            .Where(check => !string.IsNullOrWhiteSpace(check.Id))
            .GroupBy(check => check.Id, StringComparer.OrdinalIgnoreCase)
            .Where(group => group.Count() > 1)
            .Select(group => group.Key);

        foreach (var duplicateId in duplicateCheckIds)
        {
            issues.Add(new ValidationIssue("DUPLICATE_GUIDED_PROJECT_CHECK", $"Guided project check id '{duplicateId}' is duplicated.", duplicateId));
        }

        foreach (var check in checks)
        {
            RequireText(check.Id, "MISSING_GUIDED_PROJECT_CHECK_ID", "Guided project checks must include id.", issues);
            RequireText(check.Title, "MISSING_GUIDED_PROJECT_CHECK_TITLE", "Guided project checks must include title.", issues, check.Id);
            RequireText(check.Description, "MISSING_GUIDED_PROJECT_CHECK_DESCRIPTION", "Guided project checks must include description.", issues, check.Id);
            RequireText(check.TestCode, "MISSING_GUIDED_PROJECT_CHECK_TEST_CODE", "Guided project checks must include testCode.", issues, check.Id);

            if (required && check.ExpectedOutputContains.Count == 0)
            {
                issues.Add(new ValidationIssue("MISSING_GUIDED_PROJECT_EXPECTED_OUTPUT", "Required guided project checks must include expectedOutputContains.", check.Id));
            }
        }
    }

    private static bool IsSafeRelativePath(string path)
    {
        if (string.IsNullOrWhiteSpace(path)
            || Path.IsPathRooted(path)
            || path.Contains("..", StringComparison.Ordinal)
            || path.Contains('\\'))
        {
            return false;
        }

        return path.Split('/', StringSplitOptions.RemoveEmptyEntries)
            .All(part => part.Length > 0 && part.All(character => char.IsLetterOrDigit(character) || character is '-' or '_' or '.'));
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
