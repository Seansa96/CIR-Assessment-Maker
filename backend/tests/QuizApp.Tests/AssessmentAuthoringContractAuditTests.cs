using QuizApp.Core.Domain;
using QuizApp.Core.Services;

namespace QuizApp.Tests;

public sealed class AssessmentAuthoringContractAuditTests
{
    private readonly AssessmentAuthoringContractAudit audit = new();
    private static readonly Category Stem = new(1, "physics-1", "Physics", []) { AuthoringProfile = AuthoringProfile.Stem };
    private static readonly Category NonStem = new(1, "python", "Python", []) { AuthoringProfile = AuthoringProfile.NonStem, DirectedProjectEligible = true };

    [Fact]
    public void Stem_easy_quiz_requires_standard_count_and_reports_mix_warning()
    {
        var assessment = TestData.Assessment(questions: Enumerable.Range(1, 10).Select(index => EasyQuestion($"q{index:000}")).ToList()) with
        {
            AttemptQuestionCount = 10,
            Authoring = new AssessmentAuthoringMetadata(VisualRequirement.NotApplicable, "Pure algebraic recognition.", AssessmentDifficultyTier.Easy)
        };

        var diagnostics = audit.Evaluate(Stem, assessment, strict: true);

        Assert.DoesNotContain(diagnostics, diagnostic => diagnostic.IsBlocking);
        Assert.DoesNotContain(diagnostics, diagnostic => diagnostic.Code == "EASY_QUIZ_MIX");
    }

    [Fact]
    public void Required_visual_without_media_blocks_new_content()
    {
        var assessment = TestData.Assessment(questions: Enumerable.Range(1, 10).Select(index => EasyQuestion($"q{index:000}")).ToList()) with
        {
            AttemptQuestionCount = 10,
            Authoring = new AssessmentAuthoringMetadata(VisualRequirement.Required, "Force diagram required.", AssessmentDifficultyTier.Easy)
        };

        var diagnostics = audit.Evaluate(Stem, assessment, strict: true);

        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "MISSING_REQUIRED_VISUAL" && diagnostic.IsBlocking);
    }

    [Fact]
    public void Missing_explanation_blocks_new_quiz_or_test_content()
    {
        var question = EasyQuestion("q001") with { Explanation = null };
        var assessment = TestData.Assessment(questions: Enumerable.Repeat(question, 10).ToList()) with
        {
            AttemptQuestionCount = 10,
            Authoring = new AssessmentAuthoringMetadata(VisualRequirement.NotApplicable, "Symbolic recognition.", AssessmentDifficultyTier.Easy)
        };

        var diagnostics = audit.Evaluate(Stem, assessment, strict: true);

        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "MISSING_EXPLANATION" && diagnostic.IsBlocking);
    }

    [Fact]
    public void Missing_structured_explanation_components_block_new_content()
    {
        var question = EasyQuestion("q001") with { Explanation = "TODO: explain." };
        var assessment = TestData.Assessment(questions: Enumerable.Repeat(question, 10).ToList()) with
        {
            AttemptQuestionCount = 10,
            Authoring = new AssessmentAuthoringMetadata(VisualRequirement.NotApplicable, "Symbolic recognition.", AssessmentDifficultyTier.Easy)
        };

        var diagnostics = audit.Evaluate(Stem, assessment, strict: true);

        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "PLACEHOLDER_EXPLANATION" && diagnostic.IsBlocking);
        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "MISSING_EXPLANATION_SOLUTION" && diagnostic.IsBlocking);
        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "MISSING_EXPLANATION_REASONING" && diagnostic.IsBlocking);
    }

    [Fact]
    public void Directed_project_is_allowed_for_non_stem_profile()
    {
        var assessment = TestData.Assessment(AssessmentType.DirectedProject, Array.Empty<QuestionDefinition>()) with
        {
            Authoring = new AssessmentAuthoringMetadata(VisualRequirement.NotApplicable, "Terminal-only drill.")
        };

        var diagnostics = audit.Evaluate(NonStem, assessment, strict: true);

        Assert.DoesNotContain(diagnostics, diagnostic => diagnostic.Code == "DIRECTED_PROJECT_NOT_ALLOWED");
    }

    [Fact]
    public void Hard_items_require_three_dimensions_and_a_transfer_objective()
    {
        var question = TestData.FreeResponseQuestion("q001") with
        {
            DifficultyDimensions = [DifficultyDimension.Simplification, DifficultyDimension.AuxiliaryTechnique],
            DifficultyEvidence = "Simplifies before applying an auxiliary technique."
        };
        var assessment = TestData.Assessment(questions: Enumerable.Repeat(question, 10).ToList()) with
        {
            AttemptQuestionCount = 10,
            Authoring = new AssessmentAuthoringMetadata(VisualRequirement.NotApplicable, "Symbolic analysis.", AssessmentDifficultyTier.Hard)
        };

        var diagnostics = audit.Evaluate(Stem, assessment, strict: true);

        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "INSUFFICIENT_DIFFICULTY_DIMENSIONS" && diagnostic.IsBlocking);
        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "MISSING_TRANSFER_OBJECTIVE" && diagnostic.IsBlocking);
    }

    [Fact]
    public void Olympiad_items_require_five_dimensions_and_an_extension_objective()
    {
        var question = TestData.MultipleChoiceQuestion("q001") with
        {
            DifficultyDimensions = [DifficultyDimension.Simplification, DifficultyDimension.AuxiliaryTechnique, DifficultyDimension.RepresentationTransfer, DifficultyDimension.ProofJustification, DifficultyDimension.ParameterThreshold],
            DifficultyEvidence = "Combines five distinct reasoning demands.",
            PrerequisiteObjectiveIds = ["linear-algebra"]
        };
        var assessment = TestData.Assessment(questions: Enumerable.Repeat(question, 5).ToList()) with
        {
            AttemptQuestionCount = 5,
            Authoring = new AssessmentAuthoringMetadata(VisualRequirement.NotApplicable, "No diagram is supplied by design.", AssessmentDifficultyTier.Olympiad)
        };

        var diagnostics = audit.Evaluate(Stem, assessment, strict: true);

        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "MISSING_EXTENSION_OBJECTIVE" && diagnostic.IsBlocking);
        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "MISSING_OLYMPIAD_PREREQUISITES" && diagnostic.IsBlocking);
        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "MISSING_OLYMPIAD_FURTHER_STUDY" && diagnostic.IsBlocking);
    }

    [Fact]
    public void Duplicate_or_unknown_dimensions_block_stem_item_saves()
    {
        var question = TestData.MultipleChoiceQuestion("q001") with
        {
            DifficultyDimensions = [DifficultyDimension.Simplification, DifficultyDimension.Simplification, DifficultyDimension.Unknown],
            DifficultyEvidence = "Claims several demands.",
            SubjectDifficultyTags = ["vseprAccounting"]
        };
        var assessment = TestData.Assessment(questions: Enumerable.Repeat(question, 10).ToList()) with
        {
            AttemptQuestionCount = 10,
            Authoring = new AssessmentAuthoringMetadata(VisualRequirement.NotApplicable, "Symbolic analysis.", AssessmentDifficultyTier.Easy)
        };

        var diagnostics = audit.Evaluate(Stem, assessment, strict: true);

        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "DUPLICATE_DIFFICULTY_DIMENSION" && diagnostic.IsBlocking);
        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "UNKNOWN_DIFFICULTY_DIMENSION" && diagnostic.IsBlocking);
    }

    [Fact]
    public void Dynamics_model_lesson_requires_physics_model_metadata_and_representations()
    {
        var assessment = TestData.Assessment(AssessmentType.ConceptLesson, Array.Empty<QuestionDefinition>()) with
        {
            CategoryId = "physics-1",
            TopicId = "physics-inclined-planes",
            Authoring = new AssessmentAuthoringMetadata(VisualRequirement.NotApplicable, "Metadata test.")
        };

        var diagnostics = audit.Evaluate(Stem, assessment, strict: true);

        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "MISSING_PHYSICS_MODEL" && diagnostic.IsBlocking);
    }

    [Fact]
    public void Inclined_plane_model_requires_axes_and_components()
    {
        var assessment = TestData.Assessment(AssessmentType.WorkedExample, Array.Empty<QuestionDefinition>()) with
        {
            CategoryId = "physics-1",
            TopicId = "physics-inclined-planes",
            Authoring = new AssessmentAuthoringMetadata(VisualRequirement.NotApplicable, "Metadata test.", PhysicsModel: new PhysicsModelAuthoringMetadata
            {
                ModelId = PhysicsAnalysisModel.InclinedPlane,
                ModelRole = PhysicsModelRole.Foundation,
                RequiredRepresentations = [PhysicsRepresentation.SystemBoundary, PhysicsRepresentation.FreeBodyDiagram]
            })
        };

        var diagnostics = audit.Evaluate(Stem, assessment, strict: true);

        Assert.Contains(diagnostics, diagnostic => diagnostic.Code == "INCLINED_PLANE_REPRESENTATIONS" && diagnostic.IsBlocking);
    }

    private static QuestionDefinition EasyQuestion(string id) => TestData.MultipleChoiceQuestion(id) with
    {
        Explanation = "Solution: Select the stated result after evaluating the given relationship.\n\nWhy it works: The governing rule maps the given representation to the correct conclusion.\n\nWhy the other choices fail: They apply a different rule or omit the stated condition.",
        DifficultyDimensions = [DifficultyDimension.Simplification, DifficultyDimension.RepresentationTransfer],
        DifficultyEvidence = "Rewrites the stated expression and transfers it into the target representation."
    };
}
