using QuizApp.Core.Domain;
using QuizApp.Core.Services;

namespace QuizApp.Tests;

public sealed class AssessmentValidatorTests
{
    private readonly AssessmentValidator validator = new();

    [Fact]
    public void Validate_rejects_duplicate_question_ids()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.MultipleChoiceQuestion("q001"),
            TestData.MultipleChoiceQuestion("q001")
        });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "DUPLICATE_QUESTION_ID");
    }

    [Fact]
    public void Validate_rejects_multiple_choice_answer_that_is_not_a_choice()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.MultipleChoiceQuestion("q001") with
            {
                Answer = new AnswerDefinition("missing", Array.Empty<string>(), null, null)
            }
        });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "MULTIPLE_CHOICE_ANSWER_NOT_FOUND");
    }

    [Fact]
    public void Validate_rejects_select_all_answer_ids_that_are_not_choices()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.SelectAllQuestion("q001") with
            {
                Answer = new AnswerDefinition(null, new[] { "a", "z" }, null, null)
            }
        });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "SELECT_ALL_ANSWER_NOT_FOUND");
    }

    [Fact]
    public void Validate_rejects_quizzes_over_fifty_questions()
    {
        var questions = Enumerable.Range(1, 51)
            .Select(index => TestData.MultipleChoiceQuestion($"q{index:000}"))
            .ToList();

        var assessment = TestData.Assessment(AssessmentType.Quiz, questions);

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "QUIZ_TOO_LONG");
    }
}
