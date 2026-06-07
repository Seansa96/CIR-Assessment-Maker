using QuizApp.Core.Domain;
using QuizApp.Core.Services;

namespace QuizApp.Tests;

public sealed class ScoringServiceTests
{
    private readonly ScoringService scoringService = new();

    [Fact]
    public void ScoreAnswer_scores_multiple_choice_by_choice_id()
    {
        var question = TestData.MultipleChoiceQuestion("q001");
        var submitted = new SubmittedAnswer("q001", "a", Array.Empty<string>(), null, null);

        var result = scoringService.ScoreAnswer(question, submitted);

        Assert.True(result.IsCorrect);
    }

    [Fact]
    public void ScoreAnswer_scores_select_all_as_exact_set()
    {
        var question = TestData.SelectAllQuestion("q001");
        var submitted = new SubmittedAnswer("q001", null, new[] { "c", "a", "b" }, null, null);

        var result = scoringService.ScoreAnswer(question, submitted);

        Assert.True(result.IsCorrect);
    }

    [Fact]
    public void ScoreAnswer_marks_select_all_wrong_when_extra_choice_is_selected()
    {
        var question = TestData.SelectAllQuestion("q001") with
        {
            Choices = new[]
            {
                new ChoiceOption("a", "Identify upper"),
                new ChoiceOption("b", "Identify lower"),
                new ChoiceOption("c", "Subtract lower from upper"),
                new ChoiceOption("d", "Differentiate the upper function")
            }
        };
        var submitted = new SubmittedAnswer("q001", null, new[] { "a", "b", "c", "d" }, null, null);

        var result = scoringService.ScoreAnswer(question, submitted);

        Assert.False(result.IsCorrect);
    }
}
