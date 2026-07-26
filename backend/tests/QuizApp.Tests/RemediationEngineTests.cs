using QuizApp.Core.Domain;
using Xunit;

namespace QuizApp.Tests;

public class RemediationEngineTests
{
    [Fact]
    public void MasteryTier_DefinesExpectedLevels()
    {
        Assert.Equal(0, (int)MasteryTier.Unknown);
        Assert.Equal(1, (int)MasteryTier.Novice);
        Assert.Equal(2, (int)MasteryTier.Developing);
        Assert.Equal(3, (int)MasteryTier.Proficient);
        Assert.Equal(4, (int)MasteryTier.Mastered);
    }

    [Fact]
    public void IssueSignal_Record_HoldsIdAndDomains()
    {
        var signal = new IssueSignal("sign-error", new[] { "algebra", "arithmetic" });
        Assert.Equal("sign-error", signal.Id);
        Assert.Equal(2, signal.Domains.Count);
        Assert.Contains("algebra", signal.Domains);
        Assert.Contains("arithmetic", signal.Domains);
    }

    [Fact]
    public void ChoiceOption_Initializes_IssueSignals()
    {
        var choice = new ChoiceOption("A", "x = 5", Array.Empty<MediaAsset>());
        Assert.NotNull(choice.IssueSignals);
        Assert.Empty(choice.IssueSignals);

        var choiceWithSignal = choice with { IssueSignals = new[] { new IssueSignal("algebra-error", Array.Empty<string>()) } };
        Assert.Single(choiceWithSignal.IssueSignals);
        Assert.Equal("algebra-error", choiceWithSignal.IssueSignals[0].Id);
    }

    [Fact]
    public void QuestionResult_Initializes_IssueSignalIds()
    {
        var result = new QuestionResult(
            "q1",
            "Solve for x",
            QuestionType.MultipleChoice,
            Array.Empty<MediaAsset>(),
            null,
            false,
            null,
            null,
            null,
            null)
        {
            IssueSignalIds = new[] { "algebra-error" }
        };

        Assert.Single(result.IssueSignalIds);
        Assert.Equal("algebra-error", result.IssueSignalIds[0]);
    }
}
