using QuizApp.Core.Domain;
using QuizApp.Core.Services;

namespace QuizApp.Tests;

public sealed class ScoringServiceTests
{
    private readonly ScoringService scoringService = new(null!, null!, null!, null!);

    [Fact]
    public async Task ScoreAnswer_scores_multiple_choice_by_choice_id()
    {
        var question = TestData.MultipleChoiceQuestion("q001");
        var submitted = new SubmittedAnswer("q001", "a", Array.Empty<string>(), null, null, null);

        var result = await scoringService.ScoreQuestionAsync(question, submitted, new AppSettings(1, AssessmentMode.Scored, QuestionOrderMode.Static, 10, 20, null, null, false));

        Assert.True(result.IsCorrect);
    }

    [Fact]
    public async Task ScoreAnswer_scores_select_all_as_exact_set()
    {
        var question = TestData.SelectAllQuestion("q001");
        var submitted = new SubmittedAnswer("q001", null, new[] { "c", "a", "b" }, null, null, null);

        var result = await scoringService.ScoreQuestionAsync(question, submitted, new AppSettings(1, AssessmentMode.Scored, QuestionOrderMode.Static, 10, 20, null, null, false));

        Assert.True(result.IsCorrect);
    }

    [Fact]
    public async Task ScoreAnswer_marks_select_all_wrong_when_extra_choice_is_selected()
    {
        var question = TestData.SelectAllQuestion("q001") with
        {
            Choices = new[]
            {
                new ChoiceOption("a", "Identify upper", Array.Empty<MediaAsset>()),
                new ChoiceOption("b", "Identify lower", Array.Empty<MediaAsset>()),
                new ChoiceOption("c", "Subtract lower from upper", Array.Empty<MediaAsset>()),
                new ChoiceOption("d", "Differentiate the upper function", Array.Empty<MediaAsset>())
            }
        };
        var submitted = new SubmittedAnswer("q001", null, new[] { "a", "b", "c", "d" }, null, null, null);

        var result = await scoringService.ScoreQuestionAsync(question, submitted, new AppSettings(1, AssessmentMode.Scored, QuestionOrderMode.Static, 10, 20, null, null, false));

        Assert.False(result.IsCorrect);
    }

    [Fact]
    public async Task ScoreAnswer_scores_numeric_response_within_tolerance()
    {
        var question = TestData.NumericResponseQuestion("q001");
        var submitted = new SubmittedAnswer("q001", null, Array.Empty<string>(), null, null, 8.371m);

        var result = await scoringService.ScoreQuestionAsync(question, submitted, new AppSettings(1, AssessmentMode.Scored, QuestionOrderMode.Static, 10, 20, null, null, false));

        Assert.True(result.IsCorrect);
    }

    [Fact]
    public async Task ScoreAnswer_marks_numeric_response_wrong_outside_tolerance()
    {
        var question = TestData.NumericResponseQuestion("q001");
        var submitted = new SubmittedAnswer("q001", null, Array.Empty<string>(), null, null, 8.2m);

        var result = await scoringService.ScoreQuestionAsync(question, submitted, new AppSettings(1, AssessmentMode.Scored, QuestionOrderMode.Static, 10, 20, null, null, false));

        Assert.False(result.IsCorrect);
    }
}
