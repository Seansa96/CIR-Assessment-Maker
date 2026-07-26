using QuizApp.Core.Services;
using QuizApp.Infrastructure.Files;

namespace QuizApp.Tests;

public sealed class BinomialSeriesAuthoringContractTests
{
    [Theory]
    [InlineData("calc2-binomial-series-concept-lesson")]
    [InlineData("calc2-binomial-series-easy-quiz")]
    [InlineData("calc2-binomial-series-hard-test")]
    [InlineData("calc2-binomial-series-olympiad-quiz")]
    [InlineData("calc2-binomial-series-olympiad-test")]
    [InlineData("calc2-binomial-series-quiz")]
    [InlineData("calc2-binomial-series-worked-example")]
    [InlineData("calc2-binomial-series-worked-examples")]
    public async Task Published_content_has_no_blocking_authoring_contract_diagnostics(string assessmentId)
    {
        var dataRoot = FindRepositoryDataRoot();
        var files = new FileStorageOptions { DataRoot = dataRoot };
        var repository = new FileAssessmentRepository(files, new AssessmentValidator());
        var assessment = await repository.GetByIdAsync(assessmentId);
        var category = (await new FileCategoryRepository(files).ListAsync())
            .Single(item => item.Id == "calculus-2");

        Assert.NotNull(assessment);
        var diagnostics = new AssessmentAuthoringContractAudit().Evaluate(category, assessment, strict: true);

        Assert.DoesNotContain(diagnostics, diagnostic => diagnostic.IsBlocking);
    }

    private static string FindRepositoryDataRoot()
    {
        var directory = new DirectoryInfo(AppContext.BaseDirectory);
        while (directory is not null)
        {
            var dataRoot = Path.Combine(directory.FullName, "data");
            if (Directory.Exists(Path.Combine(dataRoot, "assessments"))) return dataRoot;
            directory = directory.Parent;
        }

        throw new DirectoryNotFoundException("Could not locate repository data directory.");
    }
}
