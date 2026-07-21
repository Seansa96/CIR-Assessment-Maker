using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public sealed record AuthoringContractDiagnostic(string Code, string Message, bool IsBlocking);

/// <summary>Policy checks for newly authored content. Legacy content can be audited with strict=false.</summary>
public sealed class AssessmentAuthoringContractAudit
{
    public const int StandardQuizAttemptCount = 10;
    public const int StandardTestAttemptCount = 20;
    private const decimal PreferredRatio = 0.70m;

    public IReadOnlyList<AuthoringContractDiagnostic> Evaluate(Category? category, AssessmentDefinition assessment, bool strict)
    {
        var diagnostics = new List<AuthoringContractDiagnostic>();
        var profile = category?.AuthoringProfile ?? AuthoringProfile.Unknown;
        var metadata = assessment.Authoring;
        void Add(string code, string message, bool blocking) => diagnostics.Add(new(code, message, blocking && strict));

        if (profile is AuthoringProfile.Unknown)
            Add("MISSING_AUTHORING_PROFILE", "The assessment category must declare authoringProfile.", true);

        if (assessment.AssessmentType is AssessmentType.DirectedProject && category?.DirectedProjectEligible != true)
            Add("DIRECTED_PROJECT_NOT_ALLOWED", "Directed projects are restricted to non-STEM, Electrical Engineering, and Electronics/Circuits categories.", true);

        if (metadata is null)
        {
            Add("MISSING_AUTHORING_METADATA", "New or modified assessments need authoring metadata with visual requirement and, for quizzes/tests, difficulty tier.", true);
            return diagnostics;
        }

        if (metadata.VisualRequirement is VisualRequirement.Unspecified)
            Add("MISSING_VISUAL_REQUIREMENT", "Authoring metadata must declare visualRequirement.", true);
        if (metadata.VisualRequirement is VisualRequirement.NotApplicable && string.IsNullOrWhiteSpace(metadata.VisualRationale))
            Add("MISSING_VISUAL_RATIONALE", "visualRequirement: notApplicable requires a rationale.", true);
        if (metadata.VisualRequirement is VisualRequirement.Required && !HasMedia(assessment))
            Add("MISSING_REQUIRED_VISUAL", "This assessment requires at least one media asset.", true);

        if (category?.Id == "physics-1" && IsDynamicsModelTopic(assessment.TopicId) && assessment.AssessmentType is (AssessmentType.ConceptLesson or AssessmentType.WorkedExample))
            EvaluatePhysicsModelMetadata(assessment, metadata, diagnostics, strict);

        if (assessment.AssessmentType is AssessmentType.Quiz or AssessmentType.Test)
        {
            if (metadata.DifficultyTier is AssessmentDifficultyTier.Unspecified)
                Add("MISSING_DIFFICULTY_TIER", "Quizzes and tests must declare authoring.difficultyTier.", true);
            if (metadata.DifficultyTier is AssessmentDifficultyTier.Olympiad && profile is not AuthoringProfile.Stem)
                Add("OLYMPIAD_NON_STEM", "Olympiad quizzes and tests are supported only for STEM categories.", true);
            var expected = metadata.DifficultyTier is AssessmentDifficultyTier.Olympiad ? 5 : assessment.AssessmentType is AssessmentType.Quiz ? StandardQuizAttemptCount : StandardTestAttemptCount;
            var effective = assessment.AttemptQuestionCount ?? assessment.Questions.Count;
            if (effective != expected && string.IsNullOrWhiteSpace(metadata.ExceptionReason))
                Add("NONSTANDARD_ATTEMPT_COUNT", $"{assessment.AssessmentType} attempts must contain {expected} items unless authoring.exceptionReason is approved.", true);
            EvaluateQuestionMix(profile, metadata.DifficultyTier, assessment, diagnostics);
            EvaluateQuestionFeedback(assessment, diagnostics, strict);
            if (profile is AuthoringProfile.Stem)
                EvaluateDifficultyDimensions(metadata.DifficultyTier, assessment, diagnostics, strict);
        }

        if (assessment.AssessmentType is AssessmentType.ConceptLesson)
        {
            var sections = assessment.Lesson?.Sections ?? [];
            if (sections.Count < 7) Add("CONCEPT_LESSON_TOO_SHALLOW", "Concept lessons require at least seven sections.", true);
            if (sections.Any(section => section.Check is null)) Add("MISSING_LESSON_CHECK", "Every concept-lesson section requires an active check.", true);
            WarnRatio("CONCEPT_CHECK_MIX", sections.Where(section => section.Check is not null).Select(section => section.Check!.Type), [QuestionType.MultipleChoice], "Concept lessons should use at least 70% multiple-choice checks.", diagnostics);
        }

        if (assessment.AssessmentType is AssessmentType.WorkedExample)
        {
            var count = assessment.WorkedExamples.Count;
            if (count is < 2 or > 4) Add("WORKED_EXAMPLE_PROBLEM_COUNT", "Worked-example assessments require two to four distinct problems unless split with an approved exception.", true);
            var preferred = profile is AuthoringProfile.Stem ? new[] { QuestionType.SymbolicResponse, QuestionType.FreeResponse } : new[] { QuestionType.FreeResponse, QuestionType.Code };
            WarnRatio("WORKED_EXAMPLE_MIX", assessment.WorkedExamples.SelectMany(example => example.Steps).Select(step => step.Question.Type), preferred, "Worked-example steps should use the profile's preferred response types at least 70% of the time.", diagnostics);
        }

        if (assessment.AssessmentType is AssessmentType.RecallDrill)
            WarnRecallRatio(assessment, diagnostics);
        return diagnostics;
    }

    public static int MinimumDifficultyDimensions(AssessmentDifficultyTier tier) => tier switch
    {
        AssessmentDifficultyTier.Easy => 2,
        AssessmentDifficultyTier.Hard => 3,
        AssessmentDifficultyTier.Olympiad => 5,
        _ => 0
    };

    private static void EvaluateDifficultyDimensions(AssessmentDifficultyTier tier, AssessmentDefinition assessment, List<AuthoringContractDiagnostic> diagnostics, bool strict)
    {
        var minimum = MinimumDifficultyDimensions(tier);
        if (minimum == 0) return;
        var combinations = new Dictionary<string, int>(StringComparer.Ordinal);
        foreach (var question in assessment.Questions)
        {
            var dimensions = question.DifficultyDimensions;
            void Add(string code, string message) => diagnostics.Add(new AuthoringContractDiagnostic(code, $"Question '{question.Id}': {message}", strict));
            if (dimensions.Count == 0) Add("MISSING_DIFFICULTY_DIMENSIONS", "scored STEM items must declare difficulty dimensions.");
            if (dimensions.Any(dimension => dimension is DifficultyDimension.Unknown)) Add("UNKNOWN_DIFFICULTY_DIMENSION", "contains an unknown difficulty dimension.");
            if (dimensions.Distinct().Count() != dimensions.Count) Add("DUPLICATE_DIFFICULTY_DIMENSION", "cannot count the same difficulty dimension more than once.");
            if (dimensions.Where(dimension => dimension is not DifficultyDimension.Unknown).Distinct().Count() < minimum)
                Add("INSUFFICIENT_DIFFICULTY_DIMENSIONS", $"{tier} items require at least {minimum} distinct difficulty dimensions.");
            if (string.IsNullOrWhiteSpace(question.DifficultyEvidence)) Add("MISSING_DIFFICULTY_EVIDENCE", "must explain how its listed dimensions create difficulty.");
            var hasTransfer = question.PrerequisiteObjectiveIds.Count > 0 || question.ExtensionObjectiveIds.Count > 0;
            if (tier is AssessmentDifficultyTier.Hard && !hasTransfer) Add("MISSING_TRANSFER_OBJECTIVE", "hard items require a named prerequisite or extension objective.");
            if (tier is AssessmentDifficultyTier.Olympiad && question.ExtensionObjectiveIds.Count == 0) Add("MISSING_EXTENSION_OBJECTIVE", "Olympiad items require a named extension objective.");
            var signature = string.Join('|', dimensions.Where(dimension => dimension is not DifficultyDimension.Unknown).Distinct().Order());
            if (!string.IsNullOrWhiteSpace(signature)) combinations[signature] = combinations.GetValueOrDefault(signature) + 1;
        }
        if (combinations.Any(pair => pair.Value > 2))
            diagnostics.Add(new AuthoringContractDiagnostic("REPEATED_DIFFICULTY_COMBINATION", "More than two items use the same difficulty-dimension combination; vary the assessment's reasoning demands.", false));
    }

    private static void EvaluateQuestionMix(AuthoringProfile profile, AssessmentDifficultyTier tier, AssessmentDefinition assessment, List<AuthoringContractDiagnostic> diagnostics)
    {
        var types = assessment.Questions.Select(question => question.Type);
        if (tier is AssessmentDifficultyTier.Easy && assessment.AssessmentType is AssessmentType.Quiz)
            WarnRatio("EASY_QUIZ_MIX", types, [QuestionType.MultipleChoice], "Easy quizzes should be at least 70% multiple choice.", diagnostics);
        else if (tier is AssessmentDifficultyTier.Hard && assessment.AssessmentType is AssessmentType.Quiz)
            WarnRatio("HARD_QUIZ_MIX", types, profile is AuthoringProfile.Stem ? new[] { QuestionType.SymbolicResponse, QuestionType.FreeResponse } : new[] { QuestionType.Code, QuestionType.FreeResponse }, "Hard quizzes should use the profile's constructive response types at least 70% of the time.", diagnostics);
        else if (assessment.AssessmentType is AssessmentType.Test)
        {
            var allowed = profile is AuthoringProfile.Stem ? new[] { QuestionType.SymbolicResponse, QuestionType.FreeResponse } : new[] { QuestionType.Code, QuestionType.FreeResponse };
            if (types.Any(type => !allowed.Contains(type))) diagnostics.Add(new("TEST_UNSUPPORTED_QUESTION_TYPE", "Tests may only use the authoring profile's constructive response types.", true));
            WarnRatio("TEST_MIX", types, allowed, "Tests should use the profile's constructive response types for at least 70% of items.", diagnostics);
        }
        else if (tier is AssessmentDifficultyTier.Olympiad)
            WarnRatio("OLYMPIAD_QUIZ_MIX", types, new[] { QuestionType.MultipleChoice }, "Olympiad quizzes should use multiple choice to provide a constrained path through exceptionally difficult problems.", diagnostics);
    }

    private static void EvaluateQuestionFeedback(AssessmentDefinition assessment, List<AuthoringContractDiagnostic> diagnostics, bool strict)
    {
        foreach (var question in assessment.Questions)
        {
            if (string.IsNullOrWhiteSpace(question.Explanation))
            {
                diagnostics.Add(new("MISSING_EXPLANATION", $"Question '{question.Id}' must include an explanation of the answer and solution approach.", strict));
                continue;
            }

            var explanation = question.Explanation.Trim();
            if (IsPlaceholderExplanation(explanation))
                diagnostics.Add(new("PLACEHOLDER_EXPLANATION", $"Question '{question.Id}' has placeholder explanation text and needs author review.", false));
            if (explanation.Length < 80)
                diagnostics.Add(new("THIN_EXPLANATION", $"Question '{question.Id}' has a brief explanation; review it for the governing principle, decisive method step, and relevant trap or condition.", false));

            if (string.Equals(question.Answer.GradingMode, "selfCheck", StringComparison.OrdinalIgnoreCase) && explanation.Length < 80)
                diagnostics.Add(new("SELF_CHECK_SOLUTION_OUTLINE", $"Question '{question.Id}' is self-check and should provide a concise solution outline, not only a result.", false));
        }
    }

    private static bool IsDynamicsModelTopic(string topicId) => topicId is
        "physics-newton-laws" or "physics-free-body-diagrams" or "physics-inclined-planes" or
        "physics-connected-systems" or "physics-static-equilibrium-tension" or "physics-friction" or
        "physics-circular-motion";

    private static void EvaluatePhysicsModelMetadata(AssessmentDefinition assessment, AssessmentAuthoringMetadata metadata, List<AuthoringContractDiagnostic> diagnostics, bool strict)
    {
        var physics = metadata.PhysicsModel;
        void Add(string code, string message, bool blocking = true) => diagnostics.Add(new(code, message, blocking && strict));
        if (physics is null || physics.ModelId is PhysicsAnalysisModel.Unspecified)
        {
            Add("MISSING_PHYSICS_MODEL", "Dynamics concept lessons and worked examples require authoring.physicsModel.modelId.");
            return;
        }
        if (physics.ModelRole is PhysicsModelRole.Unspecified)
            Add("MISSING_PHYSICS_MODEL_ROLE", "Dynamics model content requires authoring.physicsModel.modelRole.");
        if (physics.RequiredRepresentations.Count == 0)
            Add("MISSING_PHYSICS_REPRESENTATIONS", "Dynamics model content must declare required representations.");
        if (!physics.RequiredRepresentations.Contains(PhysicsRepresentation.FreeBodyDiagram) || !physics.RequiredRepresentations.Contains(PhysicsRepresentation.SystemBoundary))
            Add("PHYSICS_MODEL_SETUP_INCOMPLETE", "Dynamics model content must require both a system boundary and a free-body diagram.");

        var representations = physics.RequiredRepresentations;
        if (physics.ModelId is PhysicsAnalysisModel.InclinedPlane && (!representations.Contains(PhysicsRepresentation.CoordinateAxes) || !representations.Contains(PhysicsRepresentation.ForceComponents)))
            Add("INCLINED_PLANE_REPRESENTATIONS", "Inclined-plane content requires coordinate axes and force components.");
        if ((physics.ModelId is PhysicsAnalysisModel.ConnectedSystem or PhysicsAnalysisModel.StaticEquilibrium) && !representations.Contains(PhysicsRepresentation.MotionConstraint))
            Add("MULTIBODY_CONSTRAINT_REPRESENTATION", "Connected-system and static-equilibrium content requires a constraint/equilibrium representation.");
        if (physics.ModelId is PhysicsAnalysisModel.Friction && !representations.Contains(PhysicsRepresentation.MotionConstraint))
            Add("FRICTION_DECISION_REPRESENTATION", "Friction content requires a static-versus-kinetic motion constraint.");
        if (physics.ModelId is PhysicsAnalysisModel.UniformCircularMotion && !representations.Contains(PhysicsRepresentation.RadialDirection))
            Add("CIRCULAR_RADIAL_REPRESENTATION", "Circular-motion content requires an inward radial-direction representation.");

        diagnostics.Add(new("PHYSICS_DIAGRAM_REVIEW", "Review that the original diagram visibly supports the declared system boundary, FBD, axes, and model-specific representations.", false));
    }

    private static bool IsPlaceholderExplanation(string explanation) =>
        explanation.Contains("todo", StringComparison.OrdinalIgnoreCase) ||
        explanation.Contains("placeholder", StringComparison.OrdinalIgnoreCase) ||
        explanation.Contains("explanation here", StringComparison.OrdinalIgnoreCase) ||
        explanation.Equals("n/a", StringComparison.OrdinalIgnoreCase) ||
        explanation.Equals("none", StringComparison.OrdinalIgnoreCase);

    private static void WarnRecallRatio(AssessmentDefinition assessment, List<AuthoringContractDiagnostic> diagnostics)
    {
        var items = assessment.Items;
        if (items.Count == 0) return;
        var preferred = items.Count(item => item.Type is RecallItemType.Cloze or RecallItemType.Typed);
        if ((decimal)preferred / items.Count < PreferredRatio)
            diagnostics.Add(new("RECALL_MIX", "Recall drills should use cloze and typed recall for at least 70% of items.", false));
    }

    private static void WarnRatio(string code, IEnumerable<QuestionType> types, IReadOnlyCollection<QuestionType> preferred, string message, List<AuthoringContractDiagnostic> diagnostics)
    {
        var list = types.ToList();
        if (list.Count > 0 && (decimal)list.Count(type => preferred.Contains(type)) / list.Count < PreferredRatio)
            diagnostics.Add(new(code, message, false));
    }

    private static bool HasMedia(AssessmentDefinition assessment) => assessment.AssessmentType switch
    {
        AssessmentType.ConceptLesson => assessment.Lesson?.Sections.Any(section => section.Media.Count > 0) == true,
        AssessmentType.WorkedExample => assessment.WorkedExamples.Any(example =>
            example.Problem.Contains("![", StringComparison.Ordinal) ||
            example.Steps.Any(step => step.Question.Media.Count > 0 || step.Question.Choices.Any(choice => choice.Media.Count > 0))),
        AssessmentType.RecallDrill => assessment.Items.Any(item => item.Answer.Media.Count > 0 || item.Choices.Any(choice => choice.Media.Count > 0)),
        _ => assessment.Questions.Any(question => question.Media.Count > 0 || question.Choices.Any(choice => choice.Media.Count > 0))
    };
}
