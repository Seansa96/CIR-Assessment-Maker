using QuizApp.Core.Domain;
using QuizApp.Core.Services;

namespace QuizApp.Tests;

public sealed class NavigationRecommendationServiceTests
{
    [Fact]
    public async Task Progression_uses_only_singular_topic_placement_and_surfaces_all_eligible_branches()
    {
        var start = TestData.Assessment(AssessmentType.ConceptLesson) with
        {
            Id = "start-lesson",
            CategoryId = "subject-one",
            TopicId = "start",
            Skills = ["branch-b"],
            Navigation = new NavigationMetadata("learn", "conceptLesson", ["branch-a", "branch-b", "other-area"])
        };
        var branchA = TestData.Assessment(AssessmentType.ConceptLesson) with { Id = "branch-a-lesson", CategoryId = "subject-one", TopicId = "branch-a" };
        var branchB = TestData.Assessment(AssessmentType.ConceptLesson) with { Id = "branch-b-lesson", CategoryId = "subject-one", TopicId = "branch-b" };
        var catalog = new NavigationCatalog(
            [new("subject-one", "Subject One")],
            [new("core", "Core", ["subject-one"], ["start"]), new("branches", "Branches", ["subject-one"], ["branch-a", "branch-b"])],
            [
                new("start", "Start", "subject-one", ProgressionIndex: 0),
                new("branch-a", "Branch A", "subject-one", PrerequisiteIds: ["start"], ProgressionIndex: 1),
                new("branch-b", "Branch B", "subject-one", PrerequisiteIds: ["start"], ProgressionIndex: 2)
            ],
            [],
            [Summary(start, "core"), Summary(branchA, "branches"), Summary(branchB, "branches")]);
        var attempts = new InMemoryAttemptRepository();
        await attempts.SaveAsync(new Attempt(
            "completed-start", start.Id, AssessmentMode.Practice, AttemptStatus.Completed, [], [],
            DateTimeOffset.UtcNow.AddMinutes(-1), null, DateTimeOffset.UtcNow, null));
        var service = new NavigationRecommendationService(
            new MultiAssessmentRepository([start, branchA, branchB]), attempts, new InMemoryAttemptSessionStore(),
            new InMemoryGradeLogRepository(), new StaticNavigationCatalogService(catalog),
            new ScoringService(null!, null!, null!, null!));

        var recommendations = await service.GetRecommendationsAsync();

        Assert.True(Assert.Single(recommendations, item => item.TopicId == "branch-a").IsNextRecommended);
        Assert.True(Assert.Single(recommendations, item => item.TopicId == "branch-b").IsNextRecommended);
        Assert.Equal("You have completion evidence for this topic.", Assert.Single(recommendations, item => item.TopicId == "start").ProgressionReason);
    }

    private static NavigationAssessmentSummary Summary(AssessmentDefinition assessment, string areaId) => new(
        assessment.Id, assessment.Title, assessment.AssessmentType, assessment.CategoryId, areaId, assessment.TopicId,
        "learn", "conceptLesson", assessment.Navigation?.Tags ?? [], 0, 0, null, false, assessment.Skills);
}
