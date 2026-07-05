using QuizApp.Core.Domain;
using QuizApp.Core.Services;

namespace QuizApp.Tests;

public sealed class AssessmentValidatorTests
{
    private readonly AssessmentValidator validator = new();

    [Fact]
    public void Validate_rejects_duplicate_question_ids()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.MultipleChoiceQuestion("q001"),
            TestData.MultipleChoiceQuestion("q001")
        });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "DUPLICATE_QUESTION_ID");
    }

    [Fact]
    public void Validate_rejects_multiple_choice_answer_that_is_not_a_choice()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.MultipleChoiceQuestion("q001") with
            {
                Answer = new AnswerDefinition("missing", Array.Empty<string>(), null, null, null, null, Array.Empty<MediaAsset>())
            }
        });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "MULTIPLE_CHOICE_ANSWER_NOT_FOUND");
    }

    [Fact]
    public void Validate_rejects_select_all_answer_ids_that_are_not_choices()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.SelectAllQuestion("q001") with
            {
                Answer = new AnswerDefinition(null, new[] { "a", "z" }, null, null, null, null, Array.Empty<MediaAsset>())
            }
        });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "SELECT_ALL_ANSWER_NOT_FOUND");
    }

    [Fact]
    public void Validate_rejects_quizzes_over_fifty_questions()
    {
        var questions = Enumerable.Range(1, 51)
            .Select(index => TestData.MultipleChoiceQuestion($"q{index:000}"))
            .ToList();

        var assessment = TestData.Assessment(AssessmentType.Quiz, questions);

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "QUIZ_TOO_LONG");
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    [InlineData(4)]
    public void Validate_rejects_invalid_attempt_question_count(int attemptQuestionCount)
    {
        var assessment = TestData.Assessment(AssessmentType.Test, new[]
        {
            TestData.MultipleChoiceQuestion("q001"),
            TestData.MultipleChoiceQuestion("q002"),
            TestData.MultipleChoiceQuestion("q003")
        }) with
        {
            AttemptQuestionCount = attemptQuestionCount
        };

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "INVALID_ATTEMPT_QUESTION_COUNT");
    }

    [Fact]
    public void Validate_rejects_numeric_response_without_non_negative_tolerance()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.NumericResponseQuestion("q001") with
            {
                Answer = new AnswerDefinition(null, Array.Empty<string>(), null, null, 8.5m, -0.1m, Array.Empty<MediaAsset>())
            }
        });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "INVALID_NUMERIC_TOLERANCE");
    }

    [Fact]
    public void Validate_rejects_image_media_without_alt_text()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.MultipleChoiceQuestion("q001") with
            {
                Media = new[] { new MediaAsset("image", "/samples/washer.svg", "", null) }
            }
        });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_MEDIA_ALT");
    }

    [Fact]
    public void Validate_accepts_valid_code_question()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.CodeQuestion("q001", "python") });

        var result = validator.Validate(assessment);

        Assert.True(result.IsValid);
    }

    [Fact]
    public void Validate_rejects_code_question_with_unsupported_language()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.CodeQuestion("q001", "javascript") });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "INVALID_CODE_LANGUAGE");
    }

    [Fact]
    public void Validate_rejects_code_question_without_tests()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.CodeQuestion("q001", "cpp") with
            {
                CodeQuestion = new CodeQuestionDefinition("cpp", "square", "int square(int n) { return n * n; }", Array.Empty<CodeQuestionTest>())
            }
        });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_CODE_TESTS");
    }

    [Fact]
    public void Validate_accepts_valid_symbolic_response()
    {
        var assessment = TestData.Assessment(questions: new[] { TestData.SymbolicResponseQuestion("q001") });

        var result = validator.Validate(assessment);

        Assert.True(result.IsValid);
    }

    [Fact]
    public void Validate_rejects_symbolic_response_without_expected_latex()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.SymbolicResponseQuestion("q001") with
            {
                Answer = TestData.SymbolicResponseQuestion("q001").Answer with { SymbolicExpectedLatex = null }
            }
        });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_SYMBOLIC_EXPECTED_LATEX");
    }

    [Fact]
    public void Validate_rejects_symbolic_response_with_invalid_equivalence_mode()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.SymbolicResponseQuestion("q001") with
            {
                Answer = TestData.SymbolicResponseQuestion("q001").Answer with { SymbolicEquivalenceMode = "rubric" }
            }
        });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "INVALID_SYMBOLIC_EQUIVALENCE_MODE");
    }

    [Fact]
    public void Validate_rejects_derivative_symbolic_response_without_variables()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.SymbolicResponseQuestion("q001", "derivative") with
            {
                Answer = TestData.SymbolicResponseQuestion("q001", "derivative").Answer with { SymbolicVariables = Array.Empty<string>() }
            }
        });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_SYMBOLIC_VARIABLE");
    }

    [Fact]
    public void Validate_rejects_symbolic_response_with_negative_tolerance()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.SymbolicResponseQuestion("q001") with
            {
                Answer = TestData.SymbolicResponseQuestion("q001").Answer with { SymbolicTolerance = -0.1m }
            }
        });

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "INVALID_SYMBOLIC_TOLERANCE");
    }

    [Fact]
    public void Validate_accepts_valid_worked_example()
    {
        var assessment = TestData.WorkedExampleAssessment();

        var result = validator.Validate(assessment);

        Assert.True(result.IsValid);
    }

    [Fact]
    public void Validate_rejects_worked_example_without_examples()
    {
        var assessment = TestData.WorkedExampleAssessment() with { WorkedExamples = Array.Empty<WorkedExampleDefinition>() };

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_WORKED_EXAMPLES");
    }

    [Fact]
    public void Validate_rejects_worked_example_without_steps()
    {
        var assessment = TestData.WorkedExampleAssessment() with
        {
            WorkedExamples = new[]
            {
                new WorkedExampleDefinition("we001", "Linear substitution", "Evaluate the integral.", Array.Empty<WorkedExampleStepDefinition>())
            }
        };

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_WORKED_EXAMPLE_STEPS");
    }

    [Fact]
    public void Validate_rejects_duplicate_worked_example_step_ids()
    {
        var step = TestData.WorkedExampleStep("s001");
        var assessment = TestData.WorkedExampleAssessment() with
        {
            WorkedExamples = new[]
            {
                new WorkedExampleDefinition("we001", "Linear substitution", "Evaluate the integral.", new[] { step, step })
            }
        };

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "DUPLICATE_WORKED_EXAMPLE_STEP_ID");
    }

    [Fact]
    public void Validate_reuses_question_validation_for_worked_example_steps()
    {
        var invalidStep = TestData.WorkedExampleStep("s001") with
        {
            Question = TestData.WorkedExampleStep("s001").Question with { Prompt = "" }
        };
        var assessment = TestData.WorkedExampleAssessment() with
        {
            WorkedExamples = new[]
            {
                new WorkedExampleDefinition("we001", "Linear substitution", "Evaluate the integral.", new[] { invalidStep })
            }
        };

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_PROMPT");
    }

    [Fact]
    public void Validate_accepts_valid_guided_project()
    {
        var assessment = TestData.GuidedProjectAssessment();

        var result = validator.Validate(assessment);

        Assert.True(result.IsValid);
    }

    [Fact]
    public void Validate_rejects_guided_project_without_required_checks()
    {
        var assessment = TestData.GuidedProjectAssessment() with
        {
            GuidedProject = TestData.GuidedProjectAssessment().GuidedProject! with
            {
                RequiredChecks = Array.Empty<GuidedProjectCheckDefinition>()
            }
        };

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_GUIDED_PROJECT_REQUIRED_CHECKS");
    }

    [Fact]
    public void Validate_accepts_valid_recall_drill()
    {
        var assessment = TestData.RecallDrillAssessment();

        var result = validator.Validate(assessment);

        Assert.True(result.IsValid);
    }

    [Fact]
    public void Validate_rejects_recall_drill_without_items()
    {
        var assessment = TestData.RecallDrillAssessment() with { Items = Array.Empty<RecallItemDefinition>() };

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_RECALL_ITEMS");
    }

    [Fact]
    public void Validate_rejects_symbolic_recall_item_without_expected_latex()
    {
        var item = TestData.RecallDrillAssessment().Items.First(candidate => candidate.Type is RecallItemType.Symbolic);
        var assessment = TestData.RecallDrillAssessment() with
        {
            Items = new[] { item with { Answer = item.Answer with { ExpectedLatex = null } } }
        };

        var result = validator.Validate(assessment);

        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_RECALL_EXPECTED_LATEX");
    }

    [Fact]
    public void Validate_rejects_concept_lesson_without_lesson()
    {
        var assessment = TestData.Assessment(AssessmentType.ConceptLesson, Array.Empty<QuestionDefinition>());
        var result = validator.Validate(assessment);
        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_CONCEPT_LESSON");
    }

    [Fact]
    public void Validate_rejects_worked_example_without_problem()
    {
        var assessment = TestData.WorkedExampleAssessment();
        var we = assessment.WorkedExamples[0] with { Problem = "" };
        var assessmentWithoutProblem = assessment with { WorkedExamples = new[] { we } };
        var result = validator.Validate(assessmentWithoutProblem);
        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_WORKED_EXAMPLE_PROBLEM");
    }

    [Fact]
    public void Validate_rejects_worked_example_step_without_title()
    {
        var assessment = TestData.WorkedExampleAssessment();
        var step = assessment.WorkedExamples[0].Steps[0] with { Title = "" };
        var we = assessment.WorkedExamples[0] with { Steps = new[] { step } };
        var assessmentWithoutTitle = assessment with { WorkedExamples = new[] { we } };
        var result = validator.Validate(assessmentWithoutTitle);
        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_WORKED_EXAMPLE_STEP_TITLE");
    }

    [Fact]
    public void Validate_rejects_multiple_choice_without_choices()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.MultipleChoiceQuestion("q001") with { Choices = Array.Empty<ChoiceOption>() }
        });
        var result = validator.Validate(assessment);
        Assert.Contains(result.Issues, issue => issue.Code == "MULTIPLE_CHOICE_WITHOUT_CHOICES");
    }

    [Fact]
    public void Validate_rejects_recall_drill_missing_expected()
    {
        var assessment = TestData.Assessment(AssessmentType.RecallDrill, Array.Empty<QuestionDefinition>()) with
        {
            Items = new[]
            {
                new RecallItemDefinition("i1", RecallItemType.Typed, "Prompt", new RecallItemAnswerDefinition("", null, Array.Empty<string>(), Array.Empty<MediaAsset>()), "", Array.Empty<string>())
            }
        };
        var result = validator.Validate(assessment);
        Assert.Contains(result.Issues, issue => issue.Code == "MISSING_RECALL_EXPECTED");
    }

    [Fact]
    public void Validate_rejects_recall_drill_invalid_item_type()
    {
        var assessment = TestData.Assessment(AssessmentType.RecallDrill, Array.Empty<QuestionDefinition>()) with
        {
            Items = new[]
            {
                new RecallItemDefinition("i1", RecallItemType.Unknown, "Prompt", new RecallItemAnswerDefinition("ans", null, Array.Empty<string>(), Array.Empty<MediaAsset>()), "", Array.Empty<string>())
            }
        };
        var result = validator.Validate(assessment);
        Assert.Contains(result.Issues, issue => issue.Code == "INVALID_RECALL_ITEM_TYPE");
    }

    [Fact]
    public void Validate_rejects_invalid_question_type()
    {
        var assessment = TestData.Assessment(questions: new[]
        {
            TestData.MultipleChoiceQuestion("q001") with { Type = QuestionType.Unknown }
        });
        var result = validator.Validate(assessment);
        Assert.Contains(result.Issues, issue => issue.Code == "INVALID_QUESTION_TYPE");
    }

    [Fact]
    public void Validate_rejects_invalid_navigation_activity_type()
    {
        var assessment = TestData.Assessment(AssessmentType.Quiz, Array.Empty<QuestionDefinition>()) with
        {
            Navigation = new NavigationMetadata("learn", "invalid-activity", Array.Empty<string>())
        };
        var result = validator.Validate(assessment);
        Assert.Contains(result.Issues, issue => issue.Code == "INVALID_ACTIVITY_TYPE");
    }
}
