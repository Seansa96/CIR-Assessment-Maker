using QuizApp.Core.Services;

namespace QuizApp.Tests;

public sealed class AssessmentItemCounterTests
{
    [Theory]
    [MemberData(nameof(AssessmentsAndExpectedCounts))]
    public void Count_returns_the_learner_facing_item_total_for_every_assessment_shape(
        QuizApp.Core.Domain.AssessmentDefinition assessment,
        int expectedCount)
    {
        Assert.Equal(expectedCount, AssessmentItemCounter.Count(assessment));
    }

    public static IEnumerable<object[]> AssessmentsAndExpectedCounts()
    {
        yield return [TestData.Assessment(), 1];
        yield return [TestData.WorkedExampleAssessment(), 2];
        yield return [TestData.GuidedProjectAssessment(), 1];
        yield return [TestData.RecallDrillAssessment(), 4];
        yield return [TestData.GlossaryAssessment(), 2];
        yield return [TestData.ConceptLessonAssessment(), 2];
        yield return [TestData.InteractiveExplorationAssessment(), 1];
        yield return [TestData.DirectedProjectAssessment(), 1];
    }
}
