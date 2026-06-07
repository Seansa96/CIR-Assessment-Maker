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
            issues.Add(new ValidationIssue("INVALID_QUESTION_TYPE", "Question type must be multipleChoice, selectAll, or freeResponse.", question.Id));
            return;
        }

        var choiceIds = question.Choices.Select(choice => choice.Id).ToHashSet(StringComparer.OrdinalIgnoreCase);

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
    }

    private static void RequireText(string? value, string code, string message, List<ValidationIssue> issues, string? questionId = null)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            issues.Add(new ValidationIssue(code, message, questionId));
        }
    }
}
