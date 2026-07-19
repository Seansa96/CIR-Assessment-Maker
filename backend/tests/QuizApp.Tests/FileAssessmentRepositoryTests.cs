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
            TopicId = "linear-equations"
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
    public async Task SaveAsync_round_trips_ordered_variant_question_selection_and_lists_slot_count()
    {
        var dataRoot = CreateDataRoot();
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());
        var assessment = TestData.Assessment(AssessmentType.Test, new[]
        {
            TestData.MultipleChoiceQuestion("q001a"),
            TestData.MultipleChoiceQuestion("q001b"),
            TestData.MultipleChoiceQuestion("q002a")
        }) with
        {
            Id = "ordered-variant-bank-test",
            QuestionSelection = new QuestionSelectionDefinition(
                QuestionSelectionMode.OrderedVariants,
                new[]
                {
                    new QuestionSelectionSlotDefinition("slot-001", "First", new[] { "q001a", "q001b" }),
                    new QuestionSelectionSlotDefinition("slot-002", "Second", new[] { "q002a" })
                })
        };

        await repository.SaveAsync(assessment);
        var loaded = await repository.GetByIdAsync("ordered-variant-bank-test");
        var summary = Assert.Single(await repository.ListByCategoryAsync(assessment.CategoryId));

        Assert.NotNull(loaded);
        Assert.Equal(QuestionSelectionMode.OrderedVariants, loaded.QuestionSelection?.Mode);
        Assert.Equal(2, loaded.QuestionSelection?.Slots.Count);
        Assert.Equal(new[] { "q001a", "q001b" }, loaded.QuestionSelection!.Slots[0].QuestionIds);
        Assert.Equal(2, summary.QuestionCount);
        Assert.Equal(3, summary.AuthoredQuestionCount);
        Assert.Equal(2, summary.AttemptQuestionCount);
    }

    [Fact]
    public async Task GetByIdAsync_defaults_question_selection_with_slots_to_ordered_variants()
    {
        var dataRoot = CreateDataRoot();
        await File.WriteAllTextAsync(Path.Combine(dataRoot, "assessments", "ordered-default-test.yaml"),
            """
            schemaVersion: 1
            id: ordered-default-test
            title: Ordered Default Test
            assessmentType: test
            categoryId: calculus-2
            topicId: integration-techniques
            modeDefault: practice
            randomizeQuestions: true
            questionSelection:
              slots:
                - id: slot-001
                  questionIds:
                    - q001a
                    - q001b
            questions:
              - id: q001a
                type: multipleChoice
                prompt: First variant A
                choices:
                  - id: a
                    text: A
                  - id: b
                    text: B
                answer:
                  choiceId: a
                explanation: A is correct.
              - id: q001b
                type: multipleChoice
                prompt: First variant B
                choices:
                  - id: a
                    text: A
                  - id: b
                    text: B
                answer:
                  choiceId: b
                explanation: B is correct.
            """);
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());

        var loaded = await repository.GetByIdAsync("ordered-default-test");
        var validation = await repository.ValidateFileAsync("ordered-default-test.yaml");

        Assert.NotNull(loaded);
        Assert.Equal(QuestionSelectionMode.OrderedVariants, loaded.QuestionSelection?.Mode);
        Assert.True(validation.IsValid, string.Join("; ", validation.Issues.Select(issue => issue.Message)));
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
    [InlineData("calc2-irreducible-quadratic-partial-fractions-worked-example")]
    [InlineData("calc2-irreducible-quadratic-partial-fractions-quiz")]
    [InlineData("calc2-improper-integrals-worked-example")]
    [InlineData("physics-tennis-ball-kinematics-free-response")]
    [InlineData("physics-relative-motion-basic-free-response")]
    [InlineData("physics-relative-motion-harder-free-response")]
    [InlineData("physics-forces-vectors-no-friction-worked-example")]
    [InlineData("chemistry-periodic-table-group-names-recall")]
    [InlineData("chemistry-periodic-table-elements-ions-recall")]
    [InlineData("chemistry-periodic-table-group-properties-recall")]
    [InlineData("chemistry-periodic-table-atomic-numbers-11-20-recall")]
    [InlineData("chemistry-periodic-table-atomic-numbers-21-30-recall")]
    [InlineData("chemistry-periodic-table-atomic-numbers-31-40-recall")]
    [InlineData("chemistry-mixture-separation-methods-concept-lesson")]
    [InlineData("chemistry-mixture-separation-methods-recall")]
    [InlineData("chemistry-binary-ionic-type-i-naming-quiz")]
    [InlineData("chemistry-binary-ionic-type-ii-naming-quiz")]
    [InlineData("dsa-hashmap-frequency-worked-example")]
    [InlineData("dsa-stack-parentheses-worked-example")]
    [InlineData("dsa-queue-bfs-worked-example")]
    [InlineData("dsa-binary-search-worked-example")]
    [InlineData("dsa-recursion-dp-worked-example")]
    [InlineData("dsa-pseudocode-recognition-recall")]
    [InlineData("dsa-foundations-complexity-concept-lesson")]
    [InlineData("dsa-arrays-strings-concept-lesson")]
    [InlineData("dsa-linked-structures-concept-lesson")]
    [InlineData("dsa-hashing-caches-concept-lesson")]
    [InlineData("dsa-stacks-queues-concept-lesson")]
    [InlineData("dsa-trees-indexes-concept-lesson")]
    [InlineData("dsa-heaps-priority-queues-concept-lesson")]
    [InlineData("dsa-graphs-dependencies-concept-lesson")]
    [InlineData("dsa-sorting-searching-concept-lesson")]
    [InlineData("dsa-recursion-backtracking-concept-lesson")]
    [InlineData("dsa-dynamic-greedy-concept-lesson")]
    [InlineData("dsa-range-resource-concept-lesson")]
    [InlineData("dsa-foundations-complexity-quiz")]
    [InlineData("dsa-arrays-strings-quiz")]
    [InlineData("dsa-linked-structures-quiz")]
    [InlineData("dsa-hashing-caches-quiz")]
    [InlineData("dsa-stacks-queues-quiz")]
    [InlineData("dsa-trees-indexes-quiz")]
    [InlineData("dsa-heaps-priority-queues-quiz")]
    [InlineData("dsa-graphs-dependencies-quiz")]
    [InlineData("dsa-sorting-searching-quiz")]
    [InlineData("dsa-recursion-backtracking-quiz")]
    [InlineData("dsa-dynamic-greedy-quiz")]
    [InlineData("dsa-range-resource-quiz")]
    [InlineData("dsa-foundations-through-hashing-test")]
    [InlineData("dsa-linear-trees-heaps-test")]
    [InlineData("dsa-graphs-searching-recursion-test")]
    [InlineData("dsa-practical-systems-capstone-test")]
    [InlineData("dsa-trie-route-matcher-directed-project")]
    [InlineData("dsa-priority-task-scheduler-directed-project")]
    [InlineData("dsa-dependency-resolver-directed-project")]
    [InlineData("dsa-fixed-telemetry-buffer-directed-project")]
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
    [InlineData("precalculus-binomial-theorem-concept-lesson")]
    [InlineData("precalculus-binomial-theorem-worked-example")]
    [InlineData("precalculus-binomial-theorem-recall")]
    [InlineData("precalculus-binomial-theorem-quiz")]
    [InlineData("caa-integer-representation-concept-lesson")]
    [InlineData("caa-bitwise-fundamentals-recall")]
    [InlineData("caa-rightmost-bit-worked-example")]
    [InlineData("caa-bitwise-fundamentals-easy-quiz")]
    [InlineData("caa-power-two-alignment-worked-example")]
    [InlineData("caa-power-two-alignment-quiz")]
    [InlineData("caa-bit-permutations-concept-lesson")]
    [InlineData("caa-bit-permutations-easy-quiz")]
    [InlineData("caa-bit-permutations-hard-quiz")]
    [InlineData("caa-bit-permutations-recall")]
    [InlineData("caa-bit-permutations-worked-example")]
    [InlineData("caa-bitwise-fundamentals-concept-lesson")]
    [InlineData("caa-bitwise-fundamentals-hard-quiz")]
    [InlineData("caa-bitwise-fundamentals-worked-example")]
    [InlineData("caa-encodings-error-correction-concept-lesson")]
    [InlineData("caa-encodings-error-correction-easy-quiz")]
    [InlineData("caa-encodings-error-correction-hard-quiz")]
    [InlineData("caa-encodings-error-correction-recall")]
    [InlineData("caa-encodings-error-correction-worked-example")]
    [InlineData("caa-floating-point-approximation-concept-lesson")]
    [InlineData("caa-floating-point-approximation-easy-quiz")]
    [InlineData("caa-floating-point-approximation-hard-quiz")]
    [InlineData("caa-floating-point-approximation-recall")]
    [InlineData("caa-floating-point-approximation-worked-example")]
    [InlineData("caa-integer-elementary-functions-concept-lesson")]
    [InlineData("caa-integer-elementary-functions-easy-quiz")]
    [InlineData("caa-integer-elementary-functions-hard-quiz")]
    [InlineData("caa-integer-elementary-functions-recall")]
    [InlineData("caa-integer-elementary-functions-worked-example")]
    [InlineData("caa-integer-multiply-divide-concept-lesson")]
    [InlineData("caa-integer-multiply-divide-easy-quiz")]
    [InlineData("caa-integer-multiply-divide-hard-quiz")]
    [InlineData("caa-integer-multiply-divide-recall")]
    [InlineData("caa-integer-multiply-divide-worked-example")]
    [InlineData("caa-integer-representation-easy-quiz")]
    [InlineData("caa-integer-representation-hard-quiz")]
    [InlineData("caa-integer-representation-recall")]
    [InlineData("caa-integer-representation-worked-example")]
    [InlineData("caa-overflow-safe-arithmetic-concept-lesson")]
    [InlineData("caa-overflow-safe-arithmetic-easy-quiz")]
    [InlineData("caa-overflow-safe-arithmetic-hard-quiz")]
    [InlineData("caa-overflow-safe-arithmetic-recall")]
    [InlineData("caa-overflow-safe-arithmetic-worked-example")]
    [InlineData("caa-packed-word-search-concept-lesson")]
    [InlineData("caa-packed-word-search-easy-quiz")]
    [InlineData("caa-packed-word-search-hard-quiz")]
    [InlineData("caa-packed-word-search-recall")]
    [InlineData("caa-packed-word-search-worked-example")]
    [InlineData("caa-popcount-bit-scans-concept-lesson")]
    [InlineData("caa-popcount-bit-scans-easy-quiz")]
    [InlineData("caa-popcount-bit-scans-hard-quiz")]
    [InlineData("caa-popcount-bit-scans-recall")]
    [InlineData("caa-popcount-bit-scans-worked-example")]
    [InlineData("caa-power-two-alignment-concept-lesson")]
    [InlineData("caa-power-two-alignment-easy-quiz")]
    [InlineData("caa-power-two-alignment-hard-quiz")]
    [InlineData("caa-power-two-alignment-recall")]
    [InlineData("precalculus-parametric-standard-forms-recall")]
    [InlineData("precalc-conic-sections-parabolas-quiz")]
    [InlineData("precalc-conic-sections-ellipses-hyperbolas-quiz")]
    [InlineData("precalc-conic-sections-cumulative-test")]
    [InlineData("precalc-conic-sections-parabola-worked-example")]
    [InlineData("precalc-conic-sections-ellipse-analysis-construction-worked-example")]
    [InlineData("precalc-conic-sections-hyperbola-worked-example")]
    [InlineData("precalc-conic-sections-classification-worked-example")]
    [InlineData("precalc-conic-sections-lunar-orbit-modeling-worked-example")]
    [InlineData("calc2-parametric-curves-basics-recall")]
    [InlineData("calc2-parametric-curves-worked-example")]
    [InlineData("calc2-parametric-derivatives-deep-concept-lesson")]
    [InlineData("calc2-parametric-derivatives-worked-example")]
    [InlineData("calc2-parametric-derivatives-deep-worked-example")]
    [InlineData("calc2-parametric-integrals-concept-lesson")]
    [InlineData("calc2-parametric-integrals-worked-example")]
    [InlineData("calc2-parametric-integrals-deep-worked-example")]
    [InlineData("calc2-parametric-cartesian-trig-identity-worked-example")]
    [InlineData("calc2-parametric-review-circle-start-orientation-worked-example")]
    [InlineData("calc2-parametric-review-horizontal-vertical-tangents-worked-example")]
    [InlineData("calc2-parametric-review-cycloid-arch-area-worked-example")]
    [InlineData("calc2-parametric-conic-orientation-recall")]
    [InlineData("calc2-parametric-conic-orientation-easy-quiz")]
    [InlineData("calc2-parametric-conic-orientation-hard-quiz")]
    [InlineData("calc2-polar-calculus-worked-example")]
    [InlineData("calc2-polar-cardioid-horizontal-vertical-tangents-worked-example")]
    [InlineData("calc2-polar-limacon-total-area-worked-example")]
    [InlineData("calc2-polar-rose-one-leaf-area-worked-example")]
    [InlineData("calc2-polar-tangent-slope-limacon-worked-example")]
    [InlineData("calc2-polar-cartesian-conversion-worked-example")]
    [InlineData("calc2-polar-graph-recognition-easy-quiz")]
    [InlineData("calc2-polar-graph-recognition-hard-quiz")]
    [InlineData("calc2-polar-tangent-theta-as-variable-concept-lesson")]
    [InlineData("calc2-polar-tangent-equation-solving-worked-example")]
    [InlineData("calc2-polar-review-limacon-inner-loop-area-worked-example")]
    [InlineData("calc2-polar-curve-graph-to-equation-review-worked-example")]
    [InlineData("calc2-polar-to-parametric-worked-example")]
    [InlineData("calc2-polar-curves-worked-example")]
    [InlineData("calc2-polar-curves-concept")]
    [InlineData("calc2-parametric-polar-conics-easy-practice-test")]
    [InlineData("calc2-parametric-polar-conics-hard-practice-test")]
    [InlineData("physics-two-vehicle-problems-worked-example")]
    [InlineData("physics-two-vehicle-problems-quiz")]
    [InlineData("calc2-improper-integrals-types-recall")]
    [InlineData("calc2-improper-integrals-p-test-recognition-quiz")]
    [InlineData("calc2-improper-integrals-convergence-quiz")]
    [InlineData("calc2-approximate-integration-worked-example")]
    [InlineData("physics-newtons-second-law-sprinter-worked-example")]
    [InlineData("physics-newtons-first-law-force-balance-worked-example")]
    [InlineData("physics-atwood-tension-acceleration-worked-example")]
    [InlineData("physics-atwood-friction-tension-acceleration-worked-example")]
    [InlineData("physics-propagation-of-errors-worked-example")]
    [InlineData("physics-propagation-of-errors-quiz")]
    [InlineData("physics-speed-displacement-basics-quiz")]
    [InlineData("geometry-angle-relationships-glossary")]
    [InlineData("geometry-triangles-basics-worked-example-1")]
    [InlineData("geometry-triangles-basics-worked-example-2")]
    [InlineData("geometry-triangle-congruence-worked-example-1")]
    [InlineData("geometry-triangle-congruence-worked-example-2")]
    [InlineData("geometry-triangle-similarity-worked-example-1")]
    [InlineData("geometry-triangle-similarity-worked-example-2")]
    [InlineData("geometry-right-triangles-worked-example-1")]
    [InlineData("geometry-right-triangles-worked-example-2")]
    [InlineData("geometry-triangle-centers-worked-example-1")]
    [InlineData("geometry-triangle-centers-worked-example-2")]
    [InlineData("geometry-triangle-area-worked-example-1")]
    [InlineData("geometry-triangle-area-worked-example-2")]
    [InlineData("geometry-oblique-triangles-worked-example-1")]
    [InlineData("geometry-oblique-triangles-worked-example-2")]
    [InlineData("calc2-polar-curves-glossary")]
    [InlineData("aops-symbolic-manipulation-worked-example")]
    [InlineData("calc2-integration-geometric-applications-transcribed-test")]
    [InlineData("calc2-practice-test-1-integrals")]
    [InlineData("circuit-basics-quiz")]
    [InlineData("circuit-builder-quiz")]
    [InlineData("python-loops-concept-lesson")]
    [InlineData("physics-centripetal-acceleration-concept-lesson")]
    [InlineData("physics-newtons-first-law-concept-lesson")]
    [InlineData("physics-newtons-second-law-concept-lesson")]
    [InlineData("physics-newtons-third-law-concept-lesson")]
    [InlineData("physics-static-kinetic-friction-concept-lesson")]
    [InlineData("cpp-oop-class-conventions-concept-lesson")]
    [InlineData("cpp-inheritance-concept-lesson")]
    [InlineData("cpp-polymorphism-concept-lesson")]
    [InlineData("python-oop-class-conventions-concept-lesson")]
    [InlineData("python-inheritance-concept-lesson")]
    [InlineData("python-polymorphism-concept-lesson")]
    [InlineData("calc2-trig-integrals-strategy-concept-lesson")]
    [InlineData("calc2-odd-secant-cosecant-concept-lesson")]
    [InlineData("calc2-trig-integrals-strategy-recall")]
    [InlineData("calc2-odd-secant-cosecant-worked-example")]
    [InlineData("calc2-common-antiderivatives-recall")]
    [InlineData("calc2-trig-substitution-reference-triangle-worked-example")]
    [InlineData("aops-identity-engineering-concept-lesson")]
    [InlineData("aops-identity-engineering-interactive-exploration")]
    [InlineData("aops-identity-engineering-worked-example")]
    [InlineData("aops-identity-engineering-quiz")]
    [InlineData("calc2-sequence-fundamentals-deep-concept-lesson")]
    [InlineData("calc2-geometric-telescoping-series-concept-lesson")]
    [InlineData("calc2-convergence-test-strategy-concept-lesson")]
    [InlineData("calc2-alternating-series-concept-lesson")]
    [InlineData("calc2-absolute-conditional-convergence-concept-lesson")]
    [InlineData("calc2-series-approximation-error-concept-lesson")]
    [InlineData("calc2-series-foundations-deep-worked-example")]
    [InlineData("calc2-convergence-tests-deep-worked-example")]
    [InlineData("calc2-power-taylor-error-deep-worked-example")]
    [InlineData("calc2-polar-coordinate-representation-worked-example")]
    [InlineData("calc2-polar-area-bounds-worked-example")]
    [InlineData("calc2-power-series-radius-endpoints-worked-example")]
    [InlineData("calc2-taylor-series-from-known-series-worked-example")]
    [InlineData("calc2-convergence-test-selection-worked-example")]
    [InlineData("calc2-intro-to-sequences-worked-example")]
    [InlineData("calc2-sequences-glossary")]
    [InlineData("calc2-sequence-fundamentals-convergence-easy-quiz")]
    [InlineData("calc2-sequence-fundamentals-convergence-hard-quiz")]
    [InlineData("calc2-sequence-limit-tools-medium-quiz")]
    [InlineData("calc2-sequence-limit-tools-worked-example")]
    [InlineData("calc2-series-fundamentals-convergence-easy-quiz")]
    [InlineData("calc2-series-fundamentals-convergence-hard-quiz")]
    [InlineData("calc2-series-limit-tools-medium-quiz")]
    [InlineData("calc2-series-limit-tools-worked-example")]
    [InlineData("os-introduction-system-calls-concept-lesson")]
    [InlineData("os-introduction-system-calls-glossary")]
    [InlineData("os-introduction-system-calls-recall")]
    [InlineData("os-introduction-system-calls-quiz")]
    [InlineData("os-introduction-system-calls-test")]
    [InlineData("os-structure-design-concept-lesson")]
    [InlineData("os-structure-design-glossary")]
    [InlineData("os-structure-design-recall")]
    [InlineData("os-structure-design-quiz")]
    [InlineData("os-structure-design-test")]
    [InlineData("os-processes-threads-concept-lesson")]
    [InlineData("os-processes-threads-glossary")]
    [InlineData("os-processes-threads-recall")]
    [InlineData("os-processes-threads-quiz")]
    [InlineData("os-processes-threads-test")]
    [InlineData("os-ipc-synchronization-concept-lesson")]
    [InlineData("os-ipc-synchronization-glossary")]
    [InlineData("os-ipc-synchronization-recall")]
    [InlineData("os-ipc-synchronization-quiz")]
    [InlineData("os-ipc-synchronization-test")]
    [InlineData("os-scheduling-concept-lesson")]
    [InlineData("os-scheduling-glossary")]
    [InlineData("os-scheduling-recall")]
    [InlineData("os-scheduling-quiz")]
    [InlineData("os-scheduling-test")]
    [InlineData("os-memory-management-concept-lesson")]
    [InlineData("os-memory-management-glossary")]
    [InlineData("os-memory-management-recall")]
    [InlineData("os-memory-management-quiz")]
    [InlineData("os-memory-management-test")]
    [InlineData("os-virtual-memory-concept-lesson")]
    [InlineData("os-virtual-memory-glossary")]
    [InlineData("os-virtual-memory-recall")]
    [InlineData("os-virtual-memory-quiz")]
    [InlineData("os-virtual-memory-test")]
    [InlineData("os-file-systems-concept-lesson")]
    [InlineData("os-file-systems-glossary")]
    [InlineData("os-file-systems-recall")]
    [InlineData("os-file-systems-quiz")]
    [InlineData("os-file-systems-test")]
    [InlineData("os-input-output-concept-lesson")]
    [InlineData("os-input-output-glossary")]
    [InlineData("os-input-output-recall")]
    [InlineData("os-input-output-quiz")]
    [InlineData("os-input-output-test")]
    [InlineData("os-deadlocks-concept-lesson")]
    [InlineData("os-deadlocks-glossary")]
    [InlineData("os-deadlocks-recall")]
    [InlineData("os-deadlocks-quiz")]
    [InlineData("os-deadlocks-test")]
    [InlineData("os-virtualization-cloud-concept-lesson")]
    [InlineData("os-virtualization-cloud-glossary")]
    [InlineData("os-virtualization-cloud-recall")]
    [InlineData("os-virtualization-cloud-quiz")]
    [InlineData("os-virtualization-cloud-test")]
    [InlineData("os-multiprocessor-systems-concept-lesson")]
    [InlineData("os-multiprocessor-systems-glossary")]
    [InlineData("os-multiprocessor-systems-recall")]
    [InlineData("os-multiprocessor-systems-quiz")]
    [InlineData("os-multiprocessor-systems-test")]
    [InlineData("os-security-concept-lesson")]
    [InlineData("os-security-glossary")]
    [InlineData("os-security-recall")]
    [InlineData("os-security-quiz")]
    [InlineData("os-security-test")]
    [InlineData("os-unix-linux-android-concept-lesson")]
    [InlineData("os-unix-linux-android-glossary")]
    [InlineData("os-unix-linux-android-recall")]
    [InlineData("os-unix-linux-android-quiz")]
    [InlineData("os-unix-linux-android-test")]
    [InlineData("os-windows-case-study-concept-lesson")]
    [InlineData("os-windows-case-study-glossary")]
    [InlineData("os-windows-case-study-recall")]
    [InlineData("os-windows-case-study-quiz")]
    [InlineData("os-windows-case-study-test")]
    [InlineData("os-operating-system-design-concept-lesson")]
    [InlineData("os-operating-system-design-glossary")]
    [InlineData("os-operating-system-design-recall")]
    [InlineData("os-operating-system-design-quiz")]
    [InlineData("os-operating-system-design-test")]
    [InlineData("operating-systems-cumulative-review-test")]
    [InlineData("os-introduction-system-calls-deep-concept-lesson")]
    [InlineData("os-introduction-system-calls-scenario-worked-example")]
    [InlineData("os-introduction-system-calls-hard-quiz")]
    [InlineData("os-structure-design-deep-concept-lesson")]
    [InlineData("os-structure-design-scenario-worked-example")]
    [InlineData("os-structure-design-hard-quiz")]
    [InlineData("os-processes-threads-deep-concept-lesson")]
    [InlineData("os-processes-threads-scenario-worked-example")]
    [InlineData("os-processes-threads-hard-quiz")]
    [InlineData("os-ipc-synchronization-deep-concept-lesson")]
    [InlineData("os-ipc-synchronization-scenario-worked-example")]
    [InlineData("os-ipc-synchronization-hard-quiz")]
    [InlineData("os-scheduling-deep-concept-lesson")]
    [InlineData("os-scheduling-scenario-worked-example")]
    [InlineData("os-scheduling-hard-quiz")]
    [InlineData("os-memory-management-deep-concept-lesson")]
    [InlineData("os-memory-management-scenario-worked-example")]
    [InlineData("os-memory-management-hard-quiz")]
    [InlineData("os-virtual-memory-deep-concept-lesson")]
    [InlineData("os-virtual-memory-scenario-worked-example")]
    [InlineData("os-virtual-memory-hard-quiz")]
    [InlineData("os-file-systems-deep-concept-lesson")]
    [InlineData("os-file-systems-scenario-worked-example")]
    [InlineData("os-file-systems-hard-quiz")]
    [InlineData("os-input-output-deep-concept-lesson")]
    [InlineData("os-input-output-scenario-worked-example")]
    [InlineData("os-input-output-hard-quiz")]
    [InlineData("os-deadlocks-deep-concept-lesson")]
    [InlineData("os-deadlocks-scenario-worked-example")]
    [InlineData("os-deadlocks-hard-quiz")]
    [InlineData("os-virtualization-cloud-deep-concept-lesson")]
    [InlineData("os-virtualization-cloud-scenario-worked-example")]
    [InlineData("os-virtualization-cloud-hard-quiz")]
    [InlineData("os-multiprocessor-systems-deep-concept-lesson")]
    [InlineData("os-multiprocessor-systems-scenario-worked-example")]
    [InlineData("os-multiprocessor-systems-hard-quiz")]
    [InlineData("os-security-deep-concept-lesson")]
    [InlineData("os-security-scenario-worked-example")]
    [InlineData("os-security-hard-quiz")]
    [InlineData("os-unix-linux-android-deep-concept-lesson")]
    [InlineData("os-unix-linux-android-scenario-worked-example")]
    [InlineData("os-unix-linux-android-hard-quiz")]
    [InlineData("os-windows-case-study-deep-concept-lesson")]
    [InlineData("os-windows-case-study-scenario-worked-example")]
    [InlineData("os-windows-case-study-hard-quiz")]
    [InlineData("os-operating-system-design-deep-concept-lesson")]
    [InlineData("os-operating-system-design-scenario-worked-example")]
    [InlineData("os-operating-system-design-hard-quiz")]
    [InlineData("operating-systems-foundations-interfaces-deep-test")]
    [InlineData("operating-systems-processes-concurrency-deep-test")]
    [InlineData("operating-systems-memory-storage-io-deep-test")]
    [InlineData("operating-systems-virtualization-parallel-security-deep-test")]
    [InlineData("operating-systems-case-studies-design-deep-test")]
    [InlineData("calc1-real-number-order-concept-lesson")]
    [InlineData("calc1-sets-functions-concept-lesson")]
    [InlineData("calc1-limits-continuity-concept-lesson")]
    [InlineData("calc1-derivative-theorems-concept-lesson")]
    [InlineData("calc1-lhopital-rule-concept-lesson")]
    [InlineData("calc1-indeterminate-forms-conversion-concept-lesson")]
    [InlineData("calc1-indeterminate-forms-lhopital-recall")]
    [InlineData("calc1-lhopital-quotient-worked-example")]
    [InlineData("calc1-lhopital-transformations-worked-example")]
    [InlineData("calc1-graph-integral-concept-lesson")]
    [InlineData("calc1-inequality-estimates-worked-example")]
    [InlineData("calc1-limits-continuity-worked-example")]
    [InlineData("calc1-derivative-mvt-worked-example")]
    [InlineData("calc1-graph-and-riemann-worked-example")]
    [InlineData("calc2-monotone-bounded-sequence-worked-example")]
    [InlineData("calc2-advanced-series-comparison-worked-example")]
    [InlineData("calc2-improper-integral-limit-comparison-worked-example")]
    [InlineData("calc2-taylor-remainder-decision-worked-example")]
    [InlineData("physics-moment-of-inertia-ke-quiz-easy")]
    [InlineData("physics-moment-of-inertia-ke-quiz-hard")]
    [InlineData("physics-moment-of-inertia-ke-test-easy")]
    [InlineData("physics-moment-of-inertia-ke-test-hard")]
    [InlineData("physics-calculating-moi-quiz-easy")]
    [InlineData("physics-calculating-moi-quiz-hard")]
    [InlineData("physics-calculating-moi-test-easy")]
    [InlineData("physics-calculating-moi-test-hard")]
    [InlineData("physics-constant-angular-acceleration-quiz-easy")]
    [InlineData("physics-constant-angular-acceleration-quiz-hard")]
    [InlineData("physics-constant-angular-acceleration-test-easy")]
    [InlineData("physics-constant-angular-acceleration-test-hard")]
    [InlineData("physics-torque-quiz-easy")]
    [InlineData("physics-torque-quiz-hard")]
    [InlineData("physics-torque-test-easy")]
    [InlineData("physics-torque-test-hard")]
    [InlineData("physics-rotational-work-power-quiz-easy")]
    [InlineData("physics-rotational-work-power-quiz-hard")]
    [InlineData("physics-rotational-work-power-test-easy")]
    [InlineData("physics-rotational-work-power-test-hard")]
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

    [Fact]
    public async Task Repository_loads_and_validates_cpp_files_strings_formatting_expansion()
    {
        string[] assessmentIds =
        [
            "cpp-word-capitalization-directed-project",
            "cpp-conditional-digit-rewriter-directed-project",
            "cpp-selective-character-reversal-directed-project",
            "cpp-length-based-word-transformer-directed-project",
            "cpp-repeated-substring-finder-directed-project",
            "cpp-text-file-writer-directed-project",
            "cpp-line-counter-directed-project",
            "cpp-binary-file-copier-directed-project",
            "cpp-append-only-journal-directed-project",
            "cpp-file-search-reporter-directed-project",
            "cpp-text-quality-analyzer-guided-project",
            "cpp-delimiter-toolkit-guided-project",
            "cpp-document-bundle-builder-guided-project",
            "cpp-log-archive-chunker-guided-project",
            "cpp-strings-formatting-worked-example",
            "cpp-working-with-files-worked-example",
            "cpp-strings-formatting-quiz",
            "cpp-strings-formatting-test",
            "cpp-working-with-files-quiz",
            "cpp-working-with-files-test"
        ];

        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = FindRepositoryDataRoot() },
            new AssessmentValidator());

        foreach (var assessmentId in assessmentIds)
        {
            var validation = await repository.ValidateFileAsync($"{assessmentId}.yaml");

            Assert.True(
                validation.IsValid,
                $"{assessmentId}: {string.Join("; ", validation.Issues.Select(issue => issue.Message))}");
        }
    }

    [Theory]
    [InlineData("calc2-sequence-fundamentals-convergence-easy-quiz")]
    [InlineData("calc2-sequence-fundamentals-convergence-hard-quiz")]
    [InlineData("calc2-sequence-limit-tools-medium-quiz")]
    [InlineData("calc2-sequence-limit-tools-worked-example")]
    [InlineData("calc2-series-fundamentals-convergence-easy-quiz")]
    [InlineData("calc2-series-fundamentals-convergence-hard-quiz")]
    [InlineData("calc2-series-limit-tools-medium-quiz")]
    [InlineData("calc2-series-limit-tools-worked-example")]
    public async Task Repository_loads_and_validates_sequence_and_series_limit_tool_content(string assessmentId)
    {
        var repositoryDataRoot = FindRepositoryDataRoot();
        var dataRoot = CreateDataRoot();
        File.Copy(
            Path.Combine(repositoryDataRoot, "assessments", $"{assessmentId}.yaml"),
            Path.Combine(dataRoot, "assessments", $"{assessmentId}.yaml"));

        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = dataRoot },
            new AssessmentValidator());

        var loaded = await repository.GetByIdAsync(assessmentId);
        var validation = await repository.ValidateFileAsync($"{assessmentId}.yaml");

        Assert.NotNull(loaded);
        Assert.True(validation.IsValid, string.Join("; ", validation.Issues.Select(issue => issue.Message)));
    }

    [Theory]
    [InlineData("physics-centripetal-acceleration-concept-lesson")]
    [InlineData("physics-newtons-first-law-concept-lesson")]
    [InlineData("physics-newtons-second-law-concept-lesson")]
    [InlineData("physics-newtons-third-law-concept-lesson")]
    [InlineData("physics-static-kinetic-friction-concept-lesson")]
    public async Task Repository_validates_physics_dynamics_concept_lessons(string assessmentId)
    {
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = FindRepositoryDataRoot() },
            new AssessmentValidator());

        var validation = await repository.ValidateFileAsync($"{assessmentId}.yaml");

        Assert.True(validation.IsValid, string.Join("; ", validation.Issues.Select(issue => issue.Message)));
    }

    [Theory]
    [InlineData("physics-moment-of-inertia-ke-quiz-easy")]
    [InlineData("physics-moment-of-inertia-ke-quiz-hard")]
    [InlineData("physics-moment-of-inertia-ke-test-easy")]
    [InlineData("physics-moment-of-inertia-ke-test-hard")]
    [InlineData("physics-calculating-moi-quiz-easy")]
    [InlineData("physics-calculating-moi-quiz-hard")]
    [InlineData("physics-calculating-moi-test-easy")]
    [InlineData("physics-calculating-moi-test-hard")]
    [InlineData("physics-constant-angular-acceleration-quiz-easy")]
    [InlineData("physics-constant-angular-acceleration-quiz-hard")]
    [InlineData("physics-constant-angular-acceleration-test-easy")]
    [InlineData("physics-constant-angular-acceleration-test-hard")]
    [InlineData("physics-torque-quiz-easy")]
    [InlineData("physics-torque-quiz-hard")]
    [InlineData("physics-torque-test-easy")]
    [InlineData("physics-torque-test-hard")]
    [InlineData("physics-rotational-work-power-quiz-easy")]
    [InlineData("physics-rotational-work-power-quiz-hard")]
    [InlineData("physics-rotational-work-power-test-easy")]
    [InlineData("physics-rotational-work-power-test-hard")]
    public async Task Repository_validates_rotational_quizzes_and_tests(string assessmentId)
    {
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = FindRepositoryDataRoot() },
            new AssessmentValidator());

        var validation = await repository.ValidateFileAsync($"{assessmentId}.yaml");

        Assert.True(validation.IsValid, string.Join("; ", validation.Issues.Select(issue => issue.Message)));
    }

    [Theory]
    [InlineData("cpp-oop-class-conventions-concept-lesson")]
    [InlineData("cpp-inheritance-concept-lesson")]
    [InlineData("cpp-polymorphism-concept-lesson")]
    [InlineData("python-oop-class-conventions-concept-lesson")]
    [InlineData("python-inheritance-concept-lesson")]
    [InlineData("python-polymorphism-concept-lesson")]
    public async Task Repository_validates_oop_concept_lessons(string assessmentId)
    {
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = FindRepositoryDataRoot() },
            new AssessmentValidator());

        var validation = await repository.ValidateFileAsync($"{assessmentId}.yaml");

        Assert.True(validation.IsValid, string.Join("; ", validation.Issues.Select(issue => issue.Message)));
    }

    [Theory]
    [InlineData("calc2-trig-integrals-strategy-concept-lesson")]
    [InlineData("calc2-odd-secant-cosecant-concept-lesson")]
    [InlineData("calc2-trig-integrals-strategy-recall")]
    [InlineData("calc2-odd-secant-cosecant-worked-example")]
    [InlineData("calc2-trig-integrals-identities-worked-example")]
    public async Task Repository_validates_trigonometric_integral_learning_modules(string assessmentId)
    {
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = FindRepositoryDataRoot() },
            new AssessmentValidator());

        var validation = await repository.ValidateFileAsync($"{assessmentId}.yaml");

        Assert.True(validation.IsValid, string.Join("; ", validation.Issues.Select(issue => issue.Message)));
    }

    [Theory]
    [InlineData("calc2-common-antiderivatives-recall")]
    [InlineData("calc2-trig-substitution-reference-triangle-worked-example")]
    public async Task Repository_validates_antiderivative_and_reference_triangle_modules(string assessmentId)
    {
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = FindRepositoryDataRoot() },
            new AssessmentValidator());

        var validation = await repository.ValidateFileAsync($"{assessmentId}.yaml");

        Assert.True(validation.IsValid, string.Join("; ", validation.Issues.Select(issue => issue.Message)));
    }

    [Theory]
    [InlineData("aops-identity-engineering-concept-lesson")]
    [InlineData("aops-identity-engineering-interactive-exploration")]
    [InlineData("aops-identity-engineering-worked-example")]
    [InlineData("aops-identity-engineering-quiz")]
    public async Task Repository_validates_identity_engineering_learning_path(string assessmentId)
    {
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = FindRepositoryDataRoot() },
            new AssessmentValidator());

        var validation = await repository.ValidateFileAsync($"{assessmentId}.yaml");

        Assert.True(validation.IsValid, string.Join("; ", validation.Issues.Select(issue => issue.Message)));
    }

    [Theory]
    [InlineData("csharp-async-concept-lesson")]
    [InlineData("csharp-async-quiz")]
    [InlineData("csharp-async-recall")]
    [InlineData("csharp-async-worked-example")]
    [InlineData("csharp-collections-concept-lesson")]
    [InlineData("csharp-collections-quiz")]
    [InlineData("csharp-collections-recall")]
    [InlineData("csharp-collections-worked-example")]
    [InlineData("csharp-combat-turn-guided-project")]
    [InlineData("csharp-control-flow-concept-lesson")]
    [InlineData("csharp-control-flow-quiz")]
    [InlineData("csharp-control-flow-recall")]
    [InlineData("csharp-control-flow-worked-example")]
    [InlineData("csharp-functions-concept-lesson")]
    [InlineData("csharp-functions-quiz")]
    [InlineData("csharp-functions-recall")]
    [InlineData("csharp-functions-worked-example")]
    [InlineData("csharp-game-score-tracker-guided-project")]
    [InlineData("csharp-leaderboard-guided-project")]
    [InlineData("csharp-oop-concept-lesson")]
    [InlineData("csharp-oop-quiz")]
    [InlineData("csharp-oop-recall")]
    [InlineData("csharp-oop-worked-example")]
    [InlineData("csharp-standard-library-concept-lesson")]
    [InlineData("csharp-standard-library-quiz")]
    [InlineData("csharp-standard-library-recall")]
    [InlineData("csharp-standard-library-worked-example")]
    [InlineData("csharp-types-variables-concept-lesson")]
    [InlineData("csharp-types-variables-quiz")]
    [InlineData("csharp-types-variables-recall")]
    [InlineData("csharp-types-variables-worked-example")]
    public async Task Repository_validates_csharp_gaming_assessments(string assessmentId)
    {
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = FindRepositoryDataRoot() },
            new AssessmentValidator());

        var validation = await repository.ValidateFileAsync($"{assessmentId}.yaml");

        Assert.True(validation.IsValid, string.Join("; ", validation.Issues.Select(issue => issue.Message)));
    }

    [Theory]
    [InlineData("python-basic-file-io-worked-example")]
    [InlineData("python-collections-concept-lesson")]
    [InlineData("python-collections-quiz")]
    [InlineData("python-collections-recall")]
    [InlineData("python-collections-worked-example")]
    [InlineData("python-control-flow-concept-lesson")]
    [InlineData("python-control-flow-quiz")]
    [InlineData("python-control-flow-recall")]
    [InlineData("python-control-flow-worked-example")]
    [InlineData("python-function-definition-conceptual-quiz")]
    [InlineData("python-function-definition-worked-example")]
    [InlineData("python-functions-concept-lesson")]
    [InlineData("python-functions-quiz")]
    [InlineData("python-functions-recall")]
    [InlineData("python-game-loop-guided-project")]
    [InlineData("python-inheritance-concept-lesson")]
    [InlineData("python-intro-loops-worked-example")]
    [InlineData("python-intro-threads-worked-example")]
    [InlineData("python-inventory-system-guided-project")]
    [InlineData("python-loops-concept-lesson")]
    [InlineData("python-loops-practice-quiz")]
    [InlineData("python-oop-class-conventions-concept-lesson")]
    [InlineData("python-oop-quiz")]
    [InlineData("python-oop-recall")]
    [InlineData("python-oop-worked-example")]
    [InlineData("python-polymorphism-concept-lesson")]
    [InlineData("python-sockets-basic-usage-worked-example")]
    [InlineData("python-sockets-conceptual-worked-example")]
    [InlineData("python-standard-library-concept-lesson")]
    [InlineData("python-standard-library-quiz")]
    [InlineData("python-standard-library-recall")]
    [InlineData("python-standard-library-worked-example")]
    [InlineData("python-text-rpg-battle-engine-guided-project")]
    [InlineData("python-types-variables-concept-lesson")]
    [InlineData("python-types-variables-quiz")]
    [InlineData("python-types-variables-recall")]
    [InlineData("python-types-variables-worked-example")]
    public async Task Repository_validates_python_gaming_assessments(string assessmentId)
    {
        var repository = new FileAssessmentRepository(
            new FileStorageOptions { DataRoot = FindRepositoryDataRoot() },
            new AssessmentValidator());

        var validation = await repository.ValidateFileAsync($"{assessmentId}.yaml");

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
