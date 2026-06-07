using QuizApp.Core.Domain;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Tests;

public sealed class FileAssessmentRepositoryTests
{
    [Fact]
    public async Task SaveAsync_writes_assessment_and_lists_it_by_category()
    {
        var dataRoot = CreateDataRoot();
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());
        var assessment = TestData.Assessment(questions: Array.Empty<QuestionDefinition>()) with
        {
            Id = "new-algebra-quiz",
            Title = "New Algebra Quiz",
            CategoryId = "algebra",
            SubcategoryIds = new[] { "linear-equations" }
        };

        await repository.SaveAsync(assessment);
        var summaries = await repository.ListByCategoryAsync("algebra");
        var loaded = await repository.GetByIdAsync("new-algebra-quiz");

        Assert.Contains(summaries, summary => summary.Id == "new-algebra-quiz" && summary.QuestionCount == 0);
        Assert.NotNull(loaded);
        Assert.Equal("New Algebra Quiz", loaded.Title);
    }

    [Fact]
    public async Task SaveAsync_rejects_invalid_assessment()
    {
        var dataRoot = CreateDataRoot();
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());
        var assessment = TestData.Assessment() with { Id = "", Title = "Invalid Quiz" };

        var exception = await Assert.ThrowsAsync<InvalidOperationException>(() => repository.SaveAsync(assessment));

        Assert.Contains("Assessment id is required", exception.Message);
    }

    private static string CreateDataRoot()
    {
        var dataRoot = Path.Combine(AppContext.BaseDirectory, "file-repository-tests", Guid.NewGuid().ToString("n"));
        Directory.CreateDirectory(Path.Combine(dataRoot, "assessments"));
        Directory.CreateDirectory(Path.Combine(dataRoot, "samples"));
        return dataRoot;
    }
}
