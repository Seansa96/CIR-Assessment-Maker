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
    public async Task SaveAsync_round_trips_attempt_question_count_and_lists_effective_count()
    {
        var dataRoot = CreateDataRoot();
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());
        var assessment = TestData.Assessment(AssessmentType.Test, new[]
        {
            TestData.MultipleChoiceQuestion("q001"),
            TestData.MultipleChoiceQuestion("q002"),
            TestData.MultipleChoiceQuestion("q003")
        }) with
        {
            Id = "sample-bank-test",
            AttemptQuestionCount = 2
        };

        await repository.SaveAsync(assessment);
        var loaded = await repository.GetByIdAsync("sample-bank-test");
        var summary = Assert.Single(await repository.ListByCategoryAsync(assessment.CategoryId));

        Assert.NotNull(loaded);
        Assert.Equal(2, loaded.AttemptQuestionCount);
        Assert.Equal(2, summary.QuestionCount);
        Assert.Equal(3, summary.AuthoredQuestionCount);
        Assert.Equal(2, summary.AttemptQuestionCount);
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
    public async Task SaveAsync_round_trips_circuit_node_coordinates()
    {
        var dataRoot = CreateDataRoot();
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());
        var question = TestData.MultipleChoiceQuestion("q001") with
        {
            Type = QuestionType.Circuit,
            Answer = TestData.MultipleChoiceQuestion("q001").Answer with
            {
                CircuitAnswer = new CircuitAnswerDefinition(
                    new CircuitTopologyDefinition(
                        new[] { new RequiredComponentDefinition("resistor", 1) },
                        "graphIsomorphism"))
            },
            CircuitQuestion = new CircuitQuestionDefinition(
                1,
                1,
                "build",
                Array.Empty<string>(),
                Array.Empty<string>(),
                new CircuitDiagramDefinition(
                    900,
                    520,
                    Array.Empty<CircuitComponentInstance>(),
                    new[] { new CircuitNodeDefinition("node-1", "Junction", 245.5m, 180.25m) },
                    Array.Empty<CircuitWireDefinition>(),
                    Array.Empty<CircuitAnnotationDefinition>()))
        };
        var assessment = TestData.Assessment(questions: new[] { question }) with
        {
            Id = "circuit-node-coordinate-quiz"
        };

        await repository.SaveAsync(assessment);
        var loaded = await repository.GetByIdAsync(assessment.Id);

        Assert.NotNull(loaded);
        var node = Assert.Single(Assert.Single(loaded.Questions).CircuitQuestion!.Diagram.Nodes);
        Assert.Equal(245.5m, node.X);
        Assert.Equal(180.25m, node.Y);
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
    public async Task SaveAsync_round_trips_recall_drills()
    {
        var dataRoot = CreateDataRoot();
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());
        var assessment = TestData.RecallDrillAssessment();

        await repository.SaveAsync(assessment);
        var loaded = await repository.GetByIdAsync(assessment.Id);
        var summaries = await repository.ListByCategoryAsync(assessment.CategoryId);

        Assert.NotNull(loaded);
        Assert.Equal(AssessmentType.RecallDrill, loaded.AssessmentType);
        Assert.Equal(4, loaded.Items.Count);
        Assert.Equal(RecallItemType.Symbolic, loaded.Items[1].Type);
        Assert.Equal("\\sin^2(x)+\\cos^2(x)=1", loaded.Items[1].Answer.ExpectedLatex);
        Assert.Contains(summaries, summary => summary.Id == assessment.Id && summary.QuestionCount == 4);
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

    [Theory]
    [InlineData("calc2-rational-integration-quiz")]
    [InlineData("calc2-improper-integrals-worked-example")]
    [InlineData("physics-tennis-ball-kinematics-free-response")]
    [InlineData("physics-relative-motion-basic-free-response")]
    [InlineData("physics-relative-motion-harder-free-response")]
    [InlineData("physics-forces-vectors-no-friction-worked-example")]
    [InlineData("chemistry-periodic-table-group-names-recall")]
    [InlineData("chemistry-periodic-table-elements-ions-recall")]
    [InlineData("chemistry-periodic-table-group-properties-recall")]
    [InlineData("chemistry-binary-ionic-type-i-naming-quiz")]
    [InlineData("chemistry-binary-ionic-type-ii-naming-quiz")]
    [InlineData("dsa-hashmap-frequency-worked-example")]
    [InlineData("dsa-stack-parentheses-worked-example")]
    [InlineData("dsa-queue-bfs-worked-example")]
    [InlineData("dsa-binary-search-worked-example")]
    [InlineData("dsa-recursion-dp-worked-example")]
    [InlineData("dsa-pseudocode-recognition-recall")]
    [InlineData("cpp-pointer-vs-reference-worked-example")]
    [InlineData("cpp-pointer-array-traversal-worked-example")]
    [InlineData("cpp-pointer-basics-quiz")]
    [InlineData("cpp-find-first-even-code-question")]
    [InlineData("cpp-inventory-pointer-scanner-guided-project")]
    [InlineData("cpp-new-delete-array-worked-example")]
    [InlineData("cpp-dynamic-array-resize-worked-example")]
    [InlineData("cpp-memory-management-basics-quiz")]
    [InlineData("cpp-resize-array-code-question")]
    [InlineData("cpp-int-buffer-guided-project")]
    [InlineData("precalculus-polynomial-division-worked-example")]
    [InlineData("precalculus-polynomial-division-quiz")]
    [InlineData("precalculus-partial-fractions-deep-worked-example")]
    [InlineData("precalculus-binomial-theorem-worked-example")]
    [InlineData("precalculus-binomial-theorem-recall")]
    [InlineData("precalculus-binomial-theorem-quiz")]
    [InlineData("physics-two-vehicle-problems-worked-example")]
    [InlineData("physics-two-vehicle-problems-quiz")]
    [InlineData("calc2-improper-integrals-types-recall")]
    [InlineData("calc2-improper-integrals-p-test-recognition-quiz")]
    [InlineData("calc2-improper-integrals-convergence-quiz")]
    [InlineData("calc2-approximate-integration-worked-example")]
    [InlineData("physics-newtons-second-law-sprinter-worked-example")]
    [InlineData("physics-newtons-first-law-force-balance-worked-example")]
    [InlineData("physics-propagation-of-errors-worked-example")]
    [InlineData("physics-propagation-of-errors-quiz")]
    [InlineData("physics-speed-displacement-basics-quiz")]
    [InlineData("aops-symbolic-manipulation-worked-example")]
    [InlineData("calc2-practice-test-1-integrals")]
    [InlineData("circuit-basics-quiz")]
    [InlineData("circuit-builder-quiz")]
    public async Task Repository_loads_and_validates_new_assessment_content(string assessmentId)
    {
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = FindRepositoryDataRoot() },
            new AssessmentValidator());

        var loaded = await repository.GetByIdAsync(assessmentId);
        var validation = await repository.ValidateFileAsync($"{assessmentId}.yaml");

        Assert.NotNull(loaded);
        Assert.True(validation.IsValid, string.Join("; ", validation.Issues.Select(issue => issue.Message)));
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
