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

    [Fact]
    public async Task SaveAsync_round_trips_numeric_response_and_image_media()
    {
        var dataRoot = CreateDataRoot();
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());
        var assessment = TestData.Assessment(questions: new[] { TestData.NumericResponseQuestion("q001") }) with
        {
            Id = "volume-numeric-quiz"
        };

        await repository.SaveAsync(assessment);
        var loaded = await repository.GetByIdAsync("volume-numeric-quiz");

        Assert.NotNull(loaded);
        var question = Assert.Single(loaded.Questions);
        Assert.Equal(QuestionType.NumericResponse, question.Type);
        Assert.Equal(8.38m, question.Answer.NumericValue);
        Assert.Equal(0.01m, question.Answer.NumericTolerance);
        Assert.Equal("/samples/volume-washer.svg", Assert.Single(question.Media).Src);
    }

    [Fact]
    public async Task SaveAsync_round_trips_code_question_fields()
    {
        var dataRoot = CreateDataRoot();
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());
        var assessment = TestData.Assessment(questions: new[] { TestData.CodeQuestion("q001", "cpp") }) with
        {
            Id = "code-question-quiz"
        };

        await repository.SaveAsync(assessment);
        var loaded = await repository.GetByIdAsync("code-question-quiz");

        Assert.NotNull(loaded);
        var question = Assert.Single(loaded.Questions);
        Assert.Equal(QuestionType.Code, question.Type);
        Assert.Equal("cpp", question.CodeQuestion?.Language);
        Assert.Equal("square", question.CodeQuestion?.FunctionName);
        Assert.Equal("9", Assert.Single(question.CodeQuestion!.Tests).Expected);
    }

    [Fact]
    public async Task SaveAsync_round_trips_symbolic_response_fields()
    {
        var dataRoot = CreateDataRoot();
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());
        var assessment = TestData.Assessment(questions: new[] { TestData.SymbolicResponseQuestion("q001", "derivative") }) with
        {
            Id = "symbolic-response-quiz"
        };

        await repository.SaveAsync(assessment);
        var loaded = await repository.GetByIdAsync("symbolic-response-quiz");

        Assert.NotNull(loaded);
        var question = Assert.Single(loaded.Questions);
        Assert.Equal(QuestionType.SymbolicResponse, question.Type);
        Assert.Equal("(x+1)^2", question.Answer.SymbolicExpectedLatex);
        Assert.Equal("derivative", question.Answer.SymbolicEquivalenceMode);
        Assert.Equal("x", Assert.Single(question.Answer.SymbolicVariables));
        Assert.Equal(0.000001m, question.Answer.SymbolicTolerance);
    }

    [Fact]
    public async Task SaveAsync_round_trips_free_response_key_points()
    {
        var dataRoot = CreateDataRoot();
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());
        var assessment = TestData.Assessment(questions: new[] { TestData.FreeResponseQuestion("q001") }) with
        {
            Id = "free-response-key-points"
        };

        await repository.SaveAsync(assessment);
        var loaded = await repository.GetByIdAsync("free-response-key-points");

        Assert.NotNull(loaded);
        var question = Assert.Single(loaded.Questions);
        Assert.Equal(new[] { "Mention the accumulated difference.", "Identify upper minus lower." }, question.Answer.KeyPoints);
    }

    [Fact]
    public async Task SaveAsync_round_trips_worked_examples()
    {
        var dataRoot = CreateDataRoot();
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());
        var assessment = TestData.WorkedExampleAssessment();

        await repository.SaveAsync(assessment);
        var loaded = await repository.GetByIdAsync(assessment.Id);
        var summaries = await repository.ListByCategoryAsync(assessment.CategoryId);

        Assert.NotNull(loaded);
        Assert.Equal(AssessmentType.WorkedExample, loaded.AssessmentType);
        var example = Assert.Single(loaded.WorkedExamples);
        Assert.Equal("Solving an integral with linear substitution", example.Title);
        Assert.Equal("s001", Assert.Single(example.Steps.Take(1)).Id);
        Assert.Contains(summaries, summary => summary.Id == assessment.Id && summary.QuestionCount == 2);
    }

    [Fact]
    public async Task SaveAsync_round_trips_guided_projects()
    {
        var dataRoot = CreateDataRoot();
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());
        var assessment = TestData.GuidedProjectAssessment();

        await repository.SaveAsync(assessment);
        var loaded = await repository.GetByIdAsync(assessment.Id);
        var summaries = await repository.ListByCategoryAsync(assessment.CategoryId);

        Assert.NotNull(loaded);
        Assert.Equal(AssessmentType.GuidedProject, loaded.AssessmentType);
        Assert.NotNull(loaded.GuidedProject);
        Assert.Equal("cpp", loaded.GuidedProject.Language);
        Assert.Equal("Runner.h", Assert.Single(loaded.GuidedProject.Files).Path);
        Assert.Equal("runner-check", Assert.Single(loaded.GuidedProject.RequiredChecks).Id);
        Assert.Contains(summaries, summary => summary.Id == assessment.Id && summary.QuestionCount == 1);
    }

    [Fact]
    public async Task Repository_loads_runner_guided_project_from_data_files()
    {
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = FindRepositoryDataRoot() },
            new AssessmentValidator());

        var loaded = await repository.GetByIdAsync("cpp-runner-race-control-guided-project");

        Assert.NotNull(loaded);
        Assert.Equal(AssessmentType.GuidedProject, loaded.AssessmentType);
        Assert.NotNull(loaded.GuidedProject);
        Assert.Equal("Runner.h", loaded.GuidedProject.Files[0].Path);
        Assert.Equal(2, loaded.GuidedProject.RequiredChecks.Count);
        Assert.Equal("coach-updates-distance", Assert.Single(loaded.GuidedProject.BonusChecks).Id);
    }

    private static string CreateDataRoot()
    {
        var dataRoot = Path.Combine(AppContext.BaseDirectory, "file-repository-tests", Guid.NewGuid().ToString("n"));
        Directory.CreateDirectory(Path.Combine(dataRoot, "assessments"));
        Directory.CreateDirectory(Path.Combine(dataRoot, "samples"));
        return dataRoot;
    }

    private static string FindRepositoryDataRoot()
    {
        var directory = new DirectoryInfo(AppContext.BaseDirectory);
        while (directory is not null)
        {
            var dataRoot = Path.Combine(directory.FullName, "data");
            if (Directory.Exists(Path.Combine(dataRoot, "assessments")))
            {
                return dataRoot;
            }

            directory = directory.Parent;
        }

        throw new DirectoryNotFoundException("Could not locate repository data directory.");
    }
}
