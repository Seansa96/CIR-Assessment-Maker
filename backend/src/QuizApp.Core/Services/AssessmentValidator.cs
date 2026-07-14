using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public sealed class AssessmentValidator
{
    public const int QuizMaxQuestions = 50;
    public const int TestMaxQuestions = 200;

    public AssessmentValidationResult Validate(AssessmentDefinition assessment)
    {
        var issues = new List<ValidationIssue>();

        RequireText(assessment.Id, "MISSING_ID", "Assessment id is required.", issues);
        RequireText(assessment.Title, "MISSING_TITLE", "Assessment title is required.", issues);
        RequireText(assessment.CategoryId, "MISSING_CATEGORY_ID", "Category id is required.", issues);
        ValidateNavigation(assessment.Navigation, issues);

        if (assessment.SchemaVersion <= 0)
        {
            issues.Add(new ValidationIssue("INVALID_SCHEMA_VERSION", "schemaVersion must be greater than zero."));
        }

        if (assessment.AssessmentType is AssessmentType.Unknown)
        {
            issues.Add(new ValidationIssue("INVALID_ASSESSMENT_TYPE", "Assessment type must be quiz, test, workedExample, guidedProject, recallDrill, glossary, conceptLesson, interactiveExploration, or directedProject."));
        }

        if (assessment.QuestionTimerSeconds is < 0)
        {
            issues.Add(new ValidationIssue("INVALID_QUESTION_TIMER", "Question timer must be null or a non-negative number of seconds."));
        }

        if (assessment.AssessmentTimerSeconds is < 0)
        {
            issues.Add(new ValidationIssue("INVALID_ASSESSMENT_TIMER", "Assessment timer must be null or a non-negative number of seconds."));
        }

        ValidateQuestionSelection(assessment, issues);

        if (assessment.AssessmentType is AssessmentType.WorkedExample)
        {
            ValidateWorkedExamples(assessment, issues);
            return new AssessmentValidationResult(issues);
        }

        if (assessment.AssessmentType is AssessmentType.GuidedProject)
        {
            ValidateGuidedProject(assessment, issues);
            return new AssessmentValidationResult(issues);
        }

        if (assessment.AssessmentType is AssessmentType.RecallDrill)
        {
            ValidateRecallDrill(assessment, issues);
            return new AssessmentValidationResult(issues);
        }

        if (assessment.AssessmentType is AssessmentType.Glossary)
        {
            ValidateGlossary(assessment, issues);
            return new AssessmentValidationResult(issues);
        }

        if (assessment.AssessmentType is AssessmentType.ConceptLesson)
        {
            ValidateConceptLesson(assessment, issues);
            return new AssessmentValidationResult(issues);
        }

        if (assessment.AssessmentType is AssessmentType.InteractiveExploration)
        {
            ValidateInteractiveExploration(assessment, issues);
            return new AssessmentValidationResult(issues);
        }

        if (assessment.AssessmentType is AssessmentType.DirectedProject)
        {
            ValidateDirectedProject(assessment, issues);
            return new AssessmentValidationResult(issues);
        }

        ValidateQuestions(assessment.Questions, assessment.AssessmentType, issues);

        var questionCount = assessment.Questions.Count;
        if (assessment.AttemptQuestionCount is not null)
        {
            if (assessment.AssessmentType is not AssessmentType.Quiz and not AssessmentType.Test)
            {
                issues.Add(new ValidationIssue("INVALID_ATTEMPT_QUESTION_COUNT", "attemptQuestionCount is only supported for quiz and test assessments."));
            }
            else if (assessment.AttemptQuestionCount <= 0)
            {
                issues.Add(new ValidationIssue("INVALID_ATTEMPT_QUESTION_COUNT", "attemptQuestionCount must be greater than zero."));
            }
            else if (assessment.AttemptQuestionCount > questionCount)
            {
                issues.Add(new ValidationIssue("INVALID_ATTEMPT_QUESTION_COUNT", "attemptQuestionCount cannot exceed the number of authored questions."));
            }
        }

        if (assessment.AssessmentType is AssessmentType.Quiz && questionCount > QuizMaxQuestions)
        {
            issues.Add(new ValidationIssue("QUIZ_TOO_LONG", $"Quiz assessments cannot exceed {QuizMaxQuestions} questions."));
        }

        if (assessment.AssessmentType is AssessmentType.Test && questionCount > TestMaxQuestions)
        {
            issues.Add(new ValidationIssue("TEST_TOO_LONG", $"Test assessments cannot exceed {TestMaxQuestions} questions."));
        }

        return new AssessmentValidationResult(issues);
    }

    private static void ValidateQuestionSelection(AssessmentDefinition assessment, List<ValidationIssue> issues)
    {
        var selection = assessment.QuestionSelection;
        if (selection is null)
        {
            return;
        }

        if (assessment.AssessmentType is not AssessmentType.Quiz and not AssessmentType.Test)
        {
            issues.Add(new ValidationIssue("INVALID_QUESTION_SELECTION", "questionSelection is only supported for quiz and test assessments."));
        }

        if (selection.Mode is not QuestionSelectionMode.OrderedVariants)
        {
            issues.Add(new ValidationIssue("INVALID_QUESTION_SELECTION_MODE", "questionSelection.mode must be orderedVariants."));
        }

        if (selection.Slots.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_QUESTION_SELECTION_SLOTS", "Ordered variant questionSelection must include at least one slot."));
        }

        if (assessment.AttemptQuestionCount is not null && assessment.AttemptQuestionCount != selection.Slots.Count)
        {
            issues.Add(new ValidationIssue("INVALID_ATTEMPT_QUESTION_COUNT", "attemptQuestionCount must match the number of ordered variant slots when questionSelection is used."));
        }

        var authoredQuestionIds = assessment.Questions
            .Select(question => question.Id)
            .ToHashSet(StringComparer.OrdinalIgnoreCase);
        var usedSlotIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var usedQuestionIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        foreach (var slot in selection.Slots)
        {
            if (string.IsNullOrWhiteSpace(slot.Id))
            {
                issues.Add(new ValidationIssue("MISSING_QUESTION_SELECTION_SLOT_ID", "Ordered variant slots must include an id."));
            }
            else if (!usedSlotIds.Add(slot.Id))
            {
                issues.Add(new ValidationIssue("DUPLICATE_QUESTION_SELECTION_SLOT_ID", "Ordered variant slot ids must be unique.", slot.Id));
            }

            if (slot.QuestionIds.Count == 0)
            {
                issues.Add(new ValidationIssue("MISSING_QUESTION_SELECTION_SLOT_QUESTIONS", "Ordered variant slots must include at least one questionId.", slot.Id));
                continue;
            }

            var slotQuestionIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            foreach (var questionId in slot.QuestionIds)
            {
                if (string.IsNullOrWhiteSpace(questionId))
                {
                    issues.Add(new ValidationIssue("MISSING_QUESTION_SELECTION_QUESTION_ID", "Ordered variant slot questionIds cannot be blank.", slot.Id));
                    continue;
                }

                if (!slotQuestionIds.Add(questionId))
                {
                    issues.Add(new ValidationIssue("DUPLICATE_QUESTION_SELECTION_QUESTION_ID", "A questionId cannot be repeated inside the same ordered variant slot.", questionId));
                }

                if (!authoredQuestionIds.Contains(questionId))
                {
                    issues.Add(new ValidationIssue("UNKNOWN_QUESTION_SELECTION_QUESTION_ID", "Ordered variant slot references a question id that does not exist in questions.", questionId));
                }

                if (!usedQuestionIds.Add(questionId))
                {
                    issues.Add(new ValidationIssue("DUPLICATE_QUESTION_SELECTION_BANK_USE", "A questionId can only appear in one ordered variant slot.", questionId));
                }
            }
        }
    }

    private static void ValidateConceptLesson(AssessmentDefinition assessment, List<ValidationIssue> issues)
    {
        var lesson = assessment.Lesson;
        if (lesson is null)
        {
            issues.Add(new ValidationIssue("MISSING_CONCEPT_LESSON", "Concept lesson assessments must include lesson."));
            return;
        }

        RequireText(lesson.Introduction, "MISSING_LESSON_INTRODUCTION", "Concept lessons must include an introduction.", issues);
        ValidateLearningSections(
            lesson.Sections.Select(section => (
                section.Id,
                section.Title,
                section.Content,
                section.Media,
                section.Check)).ToList(),
            "lesson",
            assessment.AssessmentType,
            issues);
    }

    private static void ValidateGlossary(AssessmentDefinition assessment, List<ValidationIssue> issues)
    {
        var glossary = assessment.Glossary;
        if (glossary is null)
        {
            issues.Add(new ValidationIssue("MISSING_GLOSSARY", "Glossary assessments must include glossary."));
            return;
        }

        if (assessment.ModeDefault is AssessmentMode.Scored)
        {
            issues.Add(new ValidationIssue("INVALID_GLOSSARY_MODE", "Glossary assessments must use practice mode."));
        }

        if (assessment.QuestionTimerSeconds is not null || assessment.AssessmentTimerSeconds is not null)
        {
            issues.Add(new ValidationIssue("INVALID_GLOSSARY_TIMER", "Glossary assessments do not support timers."));
        }
        if (assessment.AttemptQuestionCount is not null)
        {
            issues.Add(new ValidationIssue("INVALID_GLOSSARY_QUESTION_COUNT", "Glossary assessments do not support attemptQuestionCount."));
        }

        RequireText(glossary.Introduction, "MISSING_GLOSSARY_INTRODUCTION", "Glossaries must include an introduction.", issues);
        if (glossary.Sections.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_GLOSSARY_SECTIONS", "Glossaries must include at least one section."));
            return;
        }

        AddDuplicateIssues(
            glossary.Sections.Select(section => section.Id),
            "DUPLICATE_GLOSSARY_SECTION_ID",
            "Glossary section id",
            issues);
        AddDuplicateIssues(
            glossary.Sections.SelectMany(section => section.Entries).Select(entry => entry.Id),
            "DUPLICATE_GLOSSARY_ENTRY_ID",
            "Glossary entry id",
            issues);
        AddDuplicateIssues(
            glossary.Sections.SelectMany(section => section.Entries).SelectMany(entry => entry.Drills).Select(drill => drill.Id),
            "DUPLICATE_GLOSSARY_DRILL_ID",
            "Glossary drill id",
            issues);

        foreach (var section in glossary.Sections)
        {
            RequireText(section.Id, "MISSING_GLOSSARY_SECTION_ID", "Glossary sections must include an id.", issues);
            RequireText(section.Title, "MISSING_GLOSSARY_SECTION_TITLE", "Glossary sections must include a title.", issues, section.Id);
            if (section.Entries.Count == 0)
            {
                issues.Add(new ValidationIssue("MISSING_GLOSSARY_ENTRIES", "Glossary sections must include at least one entry.", section.Id));
            }

            foreach (var entry in section.Entries)
            {
                RequireText(entry.Id, "MISSING_GLOSSARY_ENTRY_ID", "Glossary entries must include an id.", issues);
                RequireText(entry.Term, "MISSING_GLOSSARY_TERM", "Glossary entries must include a term.", issues, entry.Id);
                RequireText(entry.Definition, "MISSING_GLOSSARY_DEFINITION", "Glossary entries must include a definition.", issues, entry.Id);
                ValidateMedia(entry.Media, issues, entry.Id);
                if (entry.Drills.Count == 0)
                {
                    issues.Add(new ValidationIssue("MISSING_GLOSSARY_DRILLS", "Each glossary entry must include at least one drill.", entry.Id));
                }

                foreach (var drill in entry.Drills)
                {
                    ValidateRecallItem(drill, issues, "Glossary drill");
                }
            }
        }
    }

    private static void ValidateInteractiveExploration(AssessmentDefinition assessment, List<ValidationIssue> issues)
    {
        var exploration = assessment.Exploration;
        if (exploration is null)
        {
            issues.Add(new ValidationIssue("MISSING_INTERACTIVE_EXPLORATION", "Interactive exploration assessments must include exploration."));
            return;
        }

        RequireText(exploration.Introduction, "MISSING_EXPLORATION_INTRODUCTION", "Interactive explorations must include an introduction.", issues);
        ValidateLearningSections(
            exploration.Sections.Select(section => (
                section.Id,
                section.Title,
                section.Instruction,
                (IReadOnlyList<MediaAsset>)Array.Empty<MediaAsset>(),
                section.Check)).ToList(),
            "exploration",
            assessment.AssessmentType,
            issues);

        foreach (var section in exploration.Sections)
        {
            if (section.Controls.Count == 0)
            {
                issues.Add(new ValidationIssue("MISSING_EXPLORATION_CONTROLS", "Exploration sections must include at least one control.", section.Id));
            }

            var controlIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            foreach (var control in section.Controls)
            {
                RequireText(control.Id, "MISSING_EXPLORATION_CONTROL_ID", "Exploration controls must include an id.", issues, section.Id);
                RequireText(control.Label, "MISSING_EXPLORATION_CONTROL_LABEL", "Exploration controls must include a label.", issues, section.Id);
                if (!controlIds.Add(control.Id))
                {
                    issues.Add(new ValidationIssue("DUPLICATE_EXPLORATION_CONTROL_ID", $"Exploration control id '{control.Id}' is duplicated.", section.Id));
                }

                var type = control.Type.Trim().ToLowerInvariant();
                if (type is not ("slider" or "number" or "select" or "toggle"))
                {
                    issues.Add(new ValidationIssue("INVALID_EXPLORATION_CONTROL_TYPE", "Exploration control type must be slider, number, select, or toggle.", section.Id));
                }
                if (type is "slider" or "number")
                {
                    if (control.Min is null || control.Max is null || control.Min > control.Max)
                    {
                        issues.Add(new ValidationIssue("INVALID_EXPLORATION_CONTROL_RANGE", $"Control '{control.Id}' must define min <= max.", section.Id));
                    }
                    if (control.Step is null or <= 0)
                    {
                        issues.Add(new ValidationIssue("INVALID_EXPLORATION_CONTROL_STEP", $"Control '{control.Id}' must define a positive step.", section.Id));
                    }
                }
                if (type is "select" && (control.Options is null || control.Options.Count == 0))
                {
                    issues.Add(new ValidationIssue("MISSING_EXPLORATION_OPTIONS", $"Select control '{control.Id}' must define options.", section.Id));
                }
            }

            var viewIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            foreach (var view in section.Views)
            {
                RequireText(view.Id, "MISSING_EXPLORATION_VIEW_ID", "Exploration views must include an id.", issues, section.Id);
                RequireText(view.Label, "MISSING_EXPLORATION_VIEW_LABEL", "Exploration views must include a label.", issues, section.Id);
                if (!viewIds.Add(view.Id))
                {
                    issues.Add(new ValidationIssue("DUPLICATE_EXPLORATION_VIEW_ID", $"Exploration view id '{view.Id}' is duplicated.", section.Id));
                }

                var type = view.Type.Trim().ToLowerInvariant();
                if (type is not ("readout" or "conditionaltext" or "table" or "plot"))
                {
                    issues.Add(new ValidationIssue("INVALID_EXPLORATION_VIEW_TYPE", "Exploration view type must be readout, conditionalText, table, or plot.", section.Id));
                }
                if (type is "readout" or "table" or "plot")
                {
                    RequireText(view.Expression, "MISSING_EXPLORATION_EXPRESSION", $"View '{view.Id}' must include an expression.", issues, section.Id);
                }
                if (type is "conditionaltext")
                {
                    RequireText(view.Condition, "MISSING_EXPLORATION_CONDITION", $"View '{view.Id}' must include a condition.", issues, section.Id);
                    RequireText(view.Content, "MISSING_EXPLORATION_CONTENT", $"View '{view.Id}' must include content.", issues, section.Id);
                }
                if (type is "table" or "plot")
                {
                    if (string.IsNullOrWhiteSpace(view.InputControlId) || !controlIds.Contains(view.InputControlId))
                    {
                        issues.Add(new ValidationIssue("INVALID_EXPLORATION_INPUT_CONTROL", $"View '{view.Id}' must reference a control in its section.", section.Id));
                    }
                    if (view.Start is null || view.End is null || view.Start > view.End || view.Step is null or <= 0)
                    {
                        issues.Add(new ValidationIssue("INVALID_EXPLORATION_VIEW_RANGE", $"View '{view.Id}' must define start <= end and a positive step.", section.Id));
                    }
                }
            }
        }
    }

    private static void ValidateLearningSections(
        IReadOnlyList<(string Id, string Title, string Content, IReadOnlyList<MediaAsset> Media, QuestionDefinition? Check)> sections,
        string kind,
        AssessmentType assessmentType,
        List<ValidationIssue> issues)
    {
        if (sections.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_LEARNING_SECTIONS", $"{kind} assessments must include at least one section."));
            return;
        }

        var sectionIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var checkIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var section in sections)
        {
            RequireText(section.Id, "MISSING_LEARNING_SECTION_ID", "Learning sections must include an id.", issues);
            RequireText(section.Title, "MISSING_LEARNING_SECTION_TITLE", "Learning sections must include a title.", issues, section.Id);
            RequireText(section.Content, "MISSING_LEARNING_SECTION_CONTENT", "Learning sections must include content or instruction.", issues, section.Id);
            if (!sectionIds.Add(section.Id))
            {
                issues.Add(new ValidationIssue("DUPLICATE_LEARNING_SECTION_ID", $"Learning section id '{section.Id}' is duplicated.", section.Id));
            }
            ValidateMedia(section.Media, issues, section.Id);
            if (section.Check is not null)
            {
                if (!checkIds.Add(section.Check.Id))
                {
                    issues.Add(new ValidationIssue("DUPLICATE_LEARNING_CHECK_ID", $"Learning check id '{section.Check.Id}' is duplicated.", section.Id));
                }
                ValidateQuestion(section.Check, assessmentType, issues);
            }
        }
    }

    private static void ValidateNavigation(NavigationMetadata? navigation, List<ValidationIssue> issues)
    {
        if (navigation is null)
        {
            return;
        }

        var goal = navigation.LearningGoal?.Trim();
        var activity = navigation.ActivityType?.Trim();
        if (string.IsNullOrWhiteSpace(goal) && string.IsNullOrWhiteSpace(activity))
        {
            return;
        }

        if (string.IsNullOrWhiteSpace(goal) || string.IsNullOrWhiteSpace(activity))
        {
            issues.Add(new ValidationIssue(
                "INVALID_NAVIGATION_METADATA",
                "navigation.learningGoal and navigation.activityType must either both be set or both be omitted."));
            return;
        }

        var knownGoal = LearningGoals.All.FirstOrDefault(candidate =>
            string.Equals(candidate.Id, goal, StringComparison.OrdinalIgnoreCase));
        if (string.IsNullOrWhiteSpace(knownGoal.Id))
        {
            issues.Add(new ValidationIssue("INVALID_LEARNING_GOAL", $"Unknown navigation learning goal '{goal}'."));
            return;
        }

        if (!knownGoal.ActivityTypes.Contains(activity, StringComparer.OrdinalIgnoreCase))
        {
            issues.Add(new ValidationIssue(
                "INVALID_ACTIVITY_TYPE",
                $"Activity type '{activity}' is not valid for learning goal '{goal}'."));
        }
    }

    private static void ValidateRecallDrill(AssessmentDefinition assessment, List<ValidationIssue> issues)
    {
        if (assessment.Items.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_RECALL_ITEMS", "Recall drill assessments must include items."));
            return;
        }

        var duplicateItemIds = assessment.Items
            .Where(item => !string.IsNullOrWhiteSpace(item.Id))
            .GroupBy(item => item.Id, StringComparer.OrdinalIgnoreCase)
            .Where(group => group.Count() > 1)
            .Select(group => group.Key);

        foreach (var duplicateId in duplicateItemIds)
        {
            issues.Add(new ValidationIssue("DUPLICATE_RECALL_ITEM_ID", $"Recall item id '{duplicateId}' is duplicated.", duplicateId));
        }

        foreach (var item in assessment.Items)
        {
            ValidateRecallItem(item, issues, "Recall item");
        }
    }

    private static void ValidateRecallItem(RecallItemDefinition item, List<ValidationIssue> issues, string label)
    {
        RequireText(item.Id, "MISSING_RECALL_ITEM_ID", $"{label}s must include an id.", issues);
        RequireText(item.Prompt, "MISSING_RECALL_PROMPT", $"{label}s must include a prompt.", issues, item.Id);

        if (item.Type is RecallItemType.Unknown)
        {
            issues.Add(new ValidationIssue("INVALID_RECALL_ITEM_TYPE", "Recall item type must be typed, symbolic, flashcard, cloze, or recognition.", item.Id));
        }

        if (item.Type is RecallItemType.Symbolic)
        {
            RequireText(item.Answer.ExpectedLatex, "MISSING_RECALL_EXPECTED_LATEX", "Symbolic recall items must include answer.expectedLatex.", issues, item.Id);
        }
        else if (item.Type is RecallItemType.Recognition)
        {
            if (item.Choices.Count < 2)
            {
                issues.Add(new ValidationIssue("MISSING_RECOGNITION_CHOICES", "Recognition items must include at least two choices.", item.Id));
            }
            RequireText(item.ChoiceId, "MISSING_RECOGNITION_ANSWER", "Recognition items must include answer.choiceId.", issues, item.Id);
            if (!string.IsNullOrWhiteSpace(item.ChoiceId)
                && !item.Choices.Any(choice => string.Equals(choice.Id, item.ChoiceId, StringComparison.OrdinalIgnoreCase)))
            {
                issues.Add(new ValidationIssue("RECOGNITION_ANSWER_NOT_FOUND", "Recognition answer.choiceId must match a choice id.", item.Id));
            }
        }
        else if (item.Type is not RecallItemType.Flashcard)
        {
            RequireText(item.Answer.Expected, "MISSING_RECALL_EXPECTED", "Recall items must include answer.expected.", issues, item.Id);
        }
        else if (string.IsNullOrWhiteSpace(item.Answer.Expected) && string.IsNullOrWhiteSpace(item.Answer.ExpectedLatex))
        {
            issues.Add(new ValidationIssue("MISSING_RECALL_EXPECTED", "Flashcard recall items must include answer.expected or answer.expectedLatex.", item.Id));
        }

        ValidateMedia(item.Answer.Media, issues, item.Id);
        foreach (var choice in item.Choices)
        {
            RequireText(choice.Id, "MISSING_CHOICE_ID", "Recognition choices must include an id.", issues, item.Id);
            RequireText(choice.Text, "MISSING_CHOICE_TEXT", "Recognition choices must include text.", issues, item.Id);
            ValidateMedia(choice.Media, issues, item.Id);
        }
        foreach (var duplicateChoiceId in item.Choices
            .Where(choice => !string.IsNullOrWhiteSpace(choice.Id))
            .GroupBy(choice => choice.Id, StringComparer.OrdinalIgnoreCase)
            .Where(group => group.Count() > 1)
            .Select(group => group.Key))
        {
            issues.Add(new ValidationIssue("DUPLICATE_RECOGNITION_CHOICE_ID", $"Recognition choice id '{duplicateChoiceId}' is duplicated.", item.Id));
        }
    }

    private static void AddDuplicateIssues(
        IEnumerable<string> ids,
        string code,
        string label,
        List<ValidationIssue> issues)
    {
        foreach (var duplicateId in ids
            .Where(id => !string.IsNullOrWhiteSpace(id))
            .GroupBy(id => id, StringComparer.OrdinalIgnoreCase)
            .Where(group => group.Count() > 1)
            .Select(group => group.Key))
        {
            issues.Add(new ValidationIssue(code, $"{label} '{duplicateId}' is duplicated.", duplicateId));
        }
    }

    private static void ValidateQuestions(IReadOnlyList<QuestionDefinition> questions, AssessmentType assessmentType, List<ValidationIssue> issues)
    {
        var duplicateQuestionIds = questions
            .Where(q => !string.IsNullOrWhiteSpace(q.Id))
            .GroupBy(q => q.Id, StringComparer.OrdinalIgnoreCase)
            .Where(group => group.Count() > 1)
            .Select(group => group.Key);

        foreach (var duplicateId in duplicateQuestionIds)
        {
            issues.Add(new ValidationIssue("DUPLICATE_QUESTION_ID", $"Question id '{duplicateId}' is duplicated.", duplicateId));
        }

        foreach (var question in questions)
        {
            ValidateQuestion(question, assessmentType, issues);
        }
    }

    private static void ValidateQuestion(QuestionDefinition question, AssessmentType assessmentType, List<ValidationIssue> issues)
    {
        RequireText(question.Id, "MISSING_QUESTION_ID", "Question id is required.", issues);
        RequireText(question.Prompt, "MISSING_PROMPT", "Question prompt is required.", issues, question.Id);

        if (question.Type is QuestionType.Unknown)
        {
            issues.Add(new ValidationIssue("INVALID_QUESTION_TYPE", "Question type must be multipleChoice, selectAll, freeResponse, numericResponse, code, symbolicResponse, circuit, multipart, or graphingResponse.", question.Id));
            return;
        }

        if (question.Type is QuestionType.Multipart)
        {
            if (assessmentType is not AssessmentType.Quiz && assessmentType is not AssessmentType.Test)
            {
                issues.Add(new ValidationIssue("INVALID_MULTIPART_ASSESSMENT", "Multipart questions are only supported in quiz and test assessments.", question.Id));
            }
            ValidateMultipartQuestion(question, issues);
            return;
        }

        var choiceIds = question.Choices.Select(choice => choice.Id).ToHashSet(StringComparer.OrdinalIgnoreCase);
        ValidateMedia(question.Media, issues, question.Id);
        foreach (var choice in question.Choices)
        {
            ValidateMedia(choice.Media, issues, question.Id);
        }
        ValidateMedia(question.Answer.Media, issues, question.Id);

        if (question.Type is QuestionType.MultipleChoice)
        {
            if (question.Choices.Count == 0)
            {
                issues.Add(new ValidationIssue("MULTIPLE_CHOICE_WITHOUT_CHOICES", "Multiple choice questions must include choices.", question.Id));
            }

            if (string.IsNullOrWhiteSpace(question.Answer.ChoiceId) || !choiceIds.Contains(question.Answer.ChoiceId))
            {
                issues.Add(new ValidationIssue("MULTIPLE_CHOICE_ANSWER_NOT_FOUND", "Multiple choice answer choiceId must match a choice.", question.Id));
            }
        }

        if (question.Type is QuestionType.SelectAll)
        {
            if (question.Choices.Count == 0)
            {
                issues.Add(new ValidationIssue("SELECT_ALL_WITHOUT_CHOICES", "Select-all questions must include choices.", question.Id));
            }

            var missingChoiceIds = question.Answer.ChoiceIds.Where(choiceId => !choiceIds.Contains(choiceId)).ToList();
            if (question.Answer.ChoiceIds.Count == 0 || missingChoiceIds.Count > 0)
            {
                issues.Add(new ValidationIssue("SELECT_ALL_ANSWER_NOT_FOUND", "Select-all answer choiceIds must match choices.", question.Id));
            }
        }

        if (question.Type is QuestionType.FreeResponse)
        {
            if (!string.Equals(question.Answer.GradingMode, "selfCheck", StringComparison.OrdinalIgnoreCase))
            {
                issues.Add(new ValidationIssue("INVALID_FREE_RESPONSE_GRADING", "Free response questions must use selfCheck grading for the MVP.", question.Id));
            }
        }

        if (question.Type is QuestionType.NumericResponse)
        {
            if (question.Answer.NumericValue is null)
            {
                issues.Add(new ValidationIssue("MISSING_NUMERIC_ANSWER", "Numeric response questions must include answer.value.", question.Id));
            }

            if (question.Answer.NumericTolerance is null or < 0)
            {
                issues.Add(new ValidationIssue("INVALID_NUMERIC_TOLERANCE", "Numeric response questions must include a non-negative answer.tolerance.", question.Id));
            }
        }

        if (question.Type is QuestionType.Code)
        {
            ValidateCodeQuestion(question, issues);
        }

        if (question.Type is QuestionType.SymbolicResponse)
        {
            ValidateSymbolicQuestion(question, issues);
        }

        if (question.Type is QuestionType.Circuit)
        {
            ValidateCircuitQuestion(question, issues);
        }

        if (question.Type is QuestionType.GraphingResponse)
        {
            ValidateGraphingQuestion(question, issues);
        }
    }

    private static void ValidateMultipartQuestion(QuestionDefinition question, List<ValidationIssue> issues)
    {
        if (question.Parts.Count < 2)
        {
            issues.Add(new ValidationIssue("INVALID_MULTIPART_PARTS", "Multipart questions must include at least two parts.", question.Id));
        }

        var partIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var part in question.Parts)
        {
            if (string.IsNullOrWhiteSpace(part.Id))
            {
                issues.Add(new ValidationIssue("MISSING_PART_ID", "Multipart parts must include an id.", question.Id));
            }
            else if (!partIds.Add(part.Id))
            {
                issues.Add(new ValidationIssue("DUPLICATE_PART_ID", $"Multipart part id '{part.Id}' is duplicated.", question.Id));
            }

            if (part.Type is QuestionType.Multipart)
            {
                issues.Add(new ValidationIssue("NESTED_MULTIPART", "Multipart parts cannot be nested.", question.Id));
                continue;
            }

            var partDef = new QuestionDefinition(
                Id: part.Id,
                Type: part.Type,
                Prompt: part.Prompt,
                Choices: part.Choices,
                Answer: part.Answer,
                Explanation: part.Explanation,
                Media: part.Media)
            {
                CodeQuestion = part.CodeQuestion,
                CircuitQuestion = part.CircuitQuestion
            };
            
            ValidateQuestion(partDef, AssessmentType.Quiz, issues);
        }
    }

    private static void ValidateWorkedExamples(AssessmentDefinition assessment, List<ValidationIssue> issues)
    {
        if (assessment.WorkedExamples.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_WORKED_EXAMPLES", "Worked example assessments must include workedExamples."));
            return;
        }

        var stepIds = new List<string>();
        foreach (var workedExample in assessment.WorkedExamples)
        {
            RequireText(workedExample.Id, "MISSING_WORKED_EXAMPLE_ID", "Worked examples must include an id.", issues);
            RequireText(workedExample.Title, "MISSING_WORKED_EXAMPLE_TITLE", "Worked examples must include a title.", issues);
            RequireText(workedExample.Problem, "MISSING_WORKED_EXAMPLE_PROBLEM", "Worked examples must include a problem.", issues);

            if (workedExample.Steps.Count == 0)
            {
                issues.Add(new ValidationIssue("MISSING_WORKED_EXAMPLE_STEPS", "Worked examples must include at least one step.", workedExample.Id));
            }

            foreach (var step in workedExample.Steps)
            {
                RequireText(step.Id, "MISSING_WORKED_EXAMPLE_STEP_ID", "Worked example steps must include an id.", issues, step.Id);
                RequireText(step.Title, "MISSING_WORKED_EXAMPLE_STEP_TITLE", "Worked example steps must include a title.", issues, step.Id);
                RequireText(step.Instruction, "MISSING_WORKED_EXAMPLE_STEP_INSTRUCTION", "Worked example steps must include instruction.", issues, step.Id);
                stepIds.Add(step.Id);
                ValidateQuestion(step.Question with { Id = step.Id }, assessment.AssessmentType, issues);
            }
        }

        var duplicateStepIds = stepIds
            .Where(id => !string.IsNullOrWhiteSpace(id))
            .GroupBy(id => id, StringComparer.OrdinalIgnoreCase)
            .Where(group => group.Count() > 1)
            .Select(group => group.Key);

        foreach (var duplicateId in duplicateStepIds)
        {
            issues.Add(new ValidationIssue("DUPLICATE_WORKED_EXAMPLE_STEP_ID", $"Worked example step id '{duplicateId}' is duplicated.", duplicateId));
        }
    }

    private static void ValidateGuidedProject(AssessmentDefinition assessment, List<ValidationIssue> issues)
    {
        var project = assessment.GuidedProject;
        if (project is null)
        {
            issues.Add(new ValidationIssue("MISSING_GUIDED_PROJECT", "Guided project assessments must include guidedProject."));
            return;
        }

        if (!string.Equals(project.Language, "cpp", StringComparison.OrdinalIgnoreCase)
            && !string.Equals(project.Language, "python", StringComparison.OrdinalIgnoreCase)
            && !string.Equals(project.Language, "bash", StringComparison.OrdinalIgnoreCase)
            && !string.Equals(project.Language, "pwsh", StringComparison.OrdinalIgnoreCase))
        {
            issues.Add(new ValidationIssue("INVALID_GUIDED_PROJECT_LANGUAGE", "Guided project language must be cpp, python, bash, or pwsh."));
        }

        RequireText(project.Instructions, "MISSING_GUIDED_PROJECT_INSTRUCTIONS", "Guided projects must include instructions.", issues);

        if (project.Files.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_GUIDED_PROJECT_FILES", "Guided projects must include at least one source file."));
        }

        if (!project.Files.Any(file => !file.ReadOnly))
        {
            issues.Add(new ValidationIssue("MISSING_EDITABLE_GUIDED_PROJECT_FILE", "Guided projects must include at least one editable source file."));
        }

        var duplicateFilePaths = project.Files
            .Where(file => !string.IsNullOrWhiteSpace(file.Path))
            .GroupBy(file => file.Path, StringComparer.OrdinalIgnoreCase)
            .Where(group => group.Count() > 1)
            .Select(group => group.Key);

        foreach (var duplicatePath in duplicateFilePaths)
        {
            issues.Add(new ValidationIssue("DUPLICATE_GUIDED_PROJECT_FILE", $"Guided project file path '{duplicatePath}' is duplicated."));
        }

        foreach (var file in project.Files)
        {
            RequireText(file.Path, "MISSING_GUIDED_PROJECT_FILE_PATH", "Guided project files must include path.", issues);
            if (!IsSafeRelativePath(file.Path))
            {
                issues.Add(new ValidationIssue("INVALID_GUIDED_PROJECT_FILE_PATH", $"Guided project file path '{file.Path}' must be a safe relative path."));
            }
        }

        if (project.RequiredChecks.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_GUIDED_PROJECT_REQUIRED_CHECKS", "Guided projects must include at least one required check."));
        }

        ValidateGuidedProjectChecks(project.RequiredChecks, issues, true);
        ValidateGuidedProjectChecks(project.BonusChecks, issues, false);
    }

    private static void ValidateGuidedProjectChecks(
        IReadOnlyList<GuidedProjectCheckDefinition> checks,
        List<ValidationIssue> issues,
        bool required)
    {
        var duplicateCheckIds = checks
            .Where(check => !string.IsNullOrWhiteSpace(check.Id))
            .GroupBy(check => check.Id, StringComparer.OrdinalIgnoreCase)
            .Where(group => group.Count() > 1)
            .Select(group => group.Key);

        foreach (var duplicateId in duplicateCheckIds)
        {
            issues.Add(new ValidationIssue("DUPLICATE_GUIDED_PROJECT_CHECK", $"Guided project check id '{duplicateId}' is duplicated.", duplicateId));
        }

        foreach (var check in checks)
        {
            RequireText(check.Id, "MISSING_GUIDED_PROJECT_CHECK_ID", "Guided project checks must include id.", issues);
            RequireText(check.Title, "MISSING_GUIDED_PROJECT_CHECK_TITLE", "Guided project checks must include title.", issues, check.Id);
            RequireText(check.Description, "MISSING_GUIDED_PROJECT_CHECK_DESCRIPTION", "Guided project checks must include description.", issues, check.Id);

            var hasTestCode = !string.IsNullOrWhiteSpace(check.TestCode);
            var hasExpectedOutput = check.ExpectedOutputContains?.Count > 0;
            var hasRun = check.Run is not null;
            var hasExpect = check.Expect is not null;

            if (required && !hasExpectedOutput && !hasExpect)
            {
                issues.Add(new ValidationIssue("MISSING_GUIDED_PROJECT_EXPECTED_OUTPUT", "Required guided project checks must include expectedOutputContains or expect.", check.Id));
            }
        }
    }

    private static bool IsSafeRelativePath(string path)
    {
        if (string.IsNullOrWhiteSpace(path)
            || Path.IsPathRooted(path)
            || path.Contains("..", StringComparison.Ordinal)
            || path.Contains('\\'))
        {
            return false;
        }

        return path.Split('/', StringSplitOptions.RemoveEmptyEntries)
            .All(part => part.Length > 0 && part.All(character => char.IsLetterOrDigit(character) || character is '-' or '_' or '.'));
    }

    private static void RequireText(string? value, string code, string message, List<ValidationIssue> issues, string? questionId = null)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            issues.Add(new ValidationIssue(code, message, questionId));
        }
    }

    private static void ValidateMedia(IReadOnlyList<MediaAsset> media, List<ValidationIssue> issues, string? questionId)
    {
        foreach (var item in media)
        {
            if (!string.Equals(item.Type, "image", StringComparison.OrdinalIgnoreCase))
            {
                issues.Add(new ValidationIssue("INVALID_MEDIA_TYPE", "Only image media is supported for now.", questionId));
            }

            if (string.IsNullOrWhiteSpace(item.Src))
            {
                issues.Add(new ValidationIssue("MISSING_MEDIA_SRC", "Image media must include src.", questionId));
            }

            if (string.IsNullOrWhiteSpace(item.Alt))
            {
                issues.Add(new ValidationIssue("MISSING_MEDIA_ALT", "Image media must include alt text.", questionId));
            }
        }
    }

    private static void ValidateCodeQuestion(QuestionDefinition question, List<ValidationIssue> issues)
    {
        var codeQuestion = question.CodeQuestion;
        if (codeQuestion is null)
        {
            issues.Add(new ValidationIssue("MISSING_CODE_DEFINITION", "Code questions must include language, functionName, starterCode, and tests.", question.Id));
            return;
        }

        if (!string.Equals(codeQuestion.Language, "python", StringComparison.OrdinalIgnoreCase)
            && !string.Equals(codeQuestion.Language, "cpp", StringComparison.OrdinalIgnoreCase))
        {
            issues.Add(new ValidationIssue("INVALID_CODE_LANGUAGE", "Code question language must be python or cpp.", question.Id));
        }

        RequireText(codeQuestion.FunctionName, "MISSING_CODE_FUNCTION_NAME", "Code questions must include functionName.", issues, question.Id);
        RequireText(codeQuestion.StarterCode, "MISSING_STARTER_CODE", "Code questions must include starterCode.", issues, question.Id);

        if (codeQuestion.Tests.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_CODE_TESTS", "Code questions must include at least one test.", question.Id));
        }

        foreach (var test in codeQuestion.Tests)
        {
            RequireText(test.Input, "MISSING_CODE_TEST_INPUT", "Code question tests must include input.", issues, question.Id);
            RequireText(test.Expected, "MISSING_CODE_TEST_EXPECTED", "Code question tests must include expected.", issues, question.Id);
        }
    }

    private static void ValidateSymbolicQuestion(QuestionDefinition question, List<ValidationIssue> issues)
    {
        var expectedLatex = question.Answer.SymbolicExpectedLatex ?? question.Answer.ExpectedLatex;
        var equivalenceMode = question.Answer.SymbolicEquivalenceMode ?? question.Answer.EquivalenceMode;
        var variables = question.Answer.SymbolicVariables.Count > 0 ? question.Answer.SymbolicVariables : question.Answer.Variables;
        var tolerance = question.Answer.SymbolicTolerance ?? question.Answer.Tolerance;

        RequireText(expectedLatex, "MISSING_SYMBOLIC_EXPECTED_LATEX", "Symbolic response questions must include answer.expectedLatex.", issues, question.Id);

        if (!string.Equals(equivalenceMode, "expression", StringComparison.OrdinalIgnoreCase)
            && !string.Equals(equivalenceMode, "derivative", StringComparison.OrdinalIgnoreCase))
        {
            issues.Add(new ValidationIssue("INVALID_SYMBOLIC_EQUIVALENCE_MODE", "Symbolic response equivalenceMode must be expression or derivative.", question.Id));
        }

        if (string.Equals(equivalenceMode, "derivative", StringComparison.OrdinalIgnoreCase)
            && variables.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_SYMBOLIC_VARIABLE", "Derivative equivalence requires at least one variable.", question.Id));
        }

        if (tolerance is null or < 0)
        {
            issues.Add(new ValidationIssue("INVALID_SYMBOLIC_TOLERANCE", "Symbolic response questions must include a non-negative answer.tolerance.", question.Id));
        }
    }

    private static void ValidateCircuitQuestion(QuestionDefinition question, List<ValidationIssue> issues)
    {
        var circ = question.CircuitQuestion;
        if (circ is null)
        {
            issues.Add(new ValidationIssue("MISSING_CIRCUIT_DEFINITION", "Circuit questions must include circuit question definitions.", question.Id));
            return;
        }

        if (circ.SchemaVersion <= 0)
        {
            issues.Add(new ValidationIssue("INVALID_CIRCUIT_SCHEMA_VERSION", "Circuit schemaVersion must be greater than zero.", question.Id));
        }

        var allowedModes = new[] { "select", "meterPlacement", "valueEntry", "build" };
        if (string.IsNullOrWhiteSpace(circ.InteractionMode) || !allowedModes.Contains(circ.InteractionMode))
        {
            issues.Add(new ValidationIssue("INVALID_CIRCUIT_INTERACTION_MODE", "Circuit interactionMode must be select, meterPlacement, valueEntry, or build.", question.Id));
        }

        var diagram = circ.Diagram;
        if (diagram is null)
        {
            issues.Add(new ValidationIssue("MISSING_CIRCUIT_DIAGRAM", "Circuit questions must include diagram definitions.", question.Id));
            return;
        }

        if (diagram.Components.Count > 100)
        {
            issues.Add(new ValidationIssue("CIRCUIT_TOO_MANY_COMPONENTS", "Circuit diagram cannot exceed 100 components.", question.Id));
        }
        if (diagram.Wires.Count > 250)
        {
            issues.Add(new ValidationIssue("CIRCUIT_TOO_MANY_WIRES", "Circuit diagram cannot exceed 250 wires.", question.Id));
        }
        if (diagram.Nodes.Count > 200)
        {
            issues.Add(new ValidationIssue("CIRCUIT_TOO_MANY_NODES", "Circuit diagram cannot exceed 200 nodes.", question.Id));
        }

        var compIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var comp in diagram.Components)
        {
            if (string.IsNullOrWhiteSpace(comp.Id))
            {
                issues.Add(new ValidationIssue("MISSING_COMPONENT_ID", "Component must have a stable id.", question.Id));
            }
            else if (!compIds.Add(comp.Id))
            {
                issues.Add(new ValidationIssue("DUPLICATE_COMPONENT_ID", $"Duplicate component id '{comp.Id}'.", question.Id));
            }

            if (string.IsNullOrWhiteSpace(comp.SymbolId))
            {
                issues.Add(new ValidationIssue("MISSING_COMPONENT_SYMBOL_ID", $"Component '{comp.Id}' must have a symbol id.", question.Id));
            }
        }

        var nodeIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var node in diagram.Nodes)
        {
            if (string.IsNullOrWhiteSpace(node.Id))
            {
                issues.Add(new ValidationIssue("MISSING_NODE_ID", "Node must have a stable id.", question.Id));
            }
            else if (!nodeIds.Add(node.Id))
            {
                issues.Add(new ValidationIssue("DUPLICATE_NODE_ID", $"Duplicate node id '{node.Id}'.", question.Id));
            }
        }

        var wireIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var wire in diagram.Wires)
        {
            if (string.IsNullOrWhiteSpace(wire.Id))
            {
                issues.Add(new ValidationIssue("MISSING_WIRE_ID", "Wire must have a stable id.", question.Id));
            }
            else if (!wireIds.Add(wire.Id))
            {
                issues.Add(new ValidationIssue("DUPLICATE_WIRE_ID", $"Duplicate wire id '{wire.Id}'.", question.Id));
            }

            if (string.IsNullOrWhiteSpace(wire.SourceId) || string.IsNullOrWhiteSpace(wire.TargetId))
            {
                issues.Add(new ValidationIssue("INVALID_WIRE_ENDPOINT", $"Wire '{wire.Id}' must have sourceId and targetId.", question.Id));
            }
            else if (string.Equals(wire.SourceId, wire.TargetId, StringComparison.OrdinalIgnoreCase))
            {
                issues.Add(new ValidationIssue("ILLEGAL_SELF_LOOP_WIRE", $"Wire '{wire.Id}' cannot connect a terminal to itself.", question.Id));
            }
        }

        var ans = question.Answer?.CircuitAnswer;
        if (ans is null)
        {
            issues.Add(new ValidationIssue("MISSING_CIRCUIT_ANSWER", "Circuit questions must define answer.circuit properties.", question.Id));
            return;
        }

        if (string.Equals(circ.InteractionMode, "select", StringComparison.OrdinalIgnoreCase))
        {
            if (ans.SelectedTargetIds is null || ans.SelectedTargetIds.Count == 0)
            {
                issues.Add(new ValidationIssue("MISSING_CIRCUIT_EXPECTED_TARGETS", "Select interaction mode requires answer.circuit.selectedTargetIds.", question.Id));
            }
        }
        else if (string.Equals(circ.InteractionMode, "meterPlacement", StringComparison.OrdinalIgnoreCase))
        {
            var mp = ans.MeterPlacement;
            if (mp is null)
            {
                issues.Add(new ValidationIssue("MISSING_CIRCUIT_METER_PLACEMENT", "meterPlacement interaction mode requires answer.circuit.meterPlacement.", question.Id));
            }
            else
            {
                if (string.IsNullOrWhiteSpace(mp.MeterType) || (!string.Equals(mp.MeterType, "ammeter", StringComparison.OrdinalIgnoreCase) && !string.Equals(mp.MeterType, "voltmeter", StringComparison.OrdinalIgnoreCase)))
                {
                    issues.Add(new ValidationIssue("INVALID_METER_TYPE", "Meter placement type must be ammeter or voltmeter.", question.Id));
                }

                if (string.Equals(mp.MeterType, "ammeter", StringComparison.OrdinalIgnoreCase) && string.IsNullOrWhiteSpace(mp.TargetBranchId))
                {
                    issues.Add(new ValidationIssue("MISSING_METER_TARGET_BRANCH", "Ammeter requires a target branch/wire ID.", question.Id));
                }

                if (string.Equals(mp.MeterType, "voltmeter", StringComparison.OrdinalIgnoreCase) && (mp.TargetNodeIds is null || mp.TargetNodeIds.Count != 2))
                {
                    issues.Add(new ValidationIssue("INVALID_METER_TARGET_NODES", "Voltmeter requires exactly two target node IDs.", question.Id));
                }
            }
        }
        else if (string.Equals(circ.InteractionMode, "valueEntry", StringComparison.OrdinalIgnoreCase))
        {
            if (ans.ExpectedValues is null || ans.ExpectedValues.Count == 0)
            {
                issues.Add(new ValidationIssue("MISSING_CIRCUIT_EXPECTED_VALUES", "valueEntry interaction mode requires answer.circuit.expectedValues.", question.Id));
            }
            else
            {
                foreach (var kv in ans.ExpectedValues)
                {
                    var ev = kv.Value;
                    if (string.IsNullOrWhiteSpace(ev.Mode) || (!string.Equals(ev.Mode, "text", StringComparison.OrdinalIgnoreCase) &&
                        !string.Equals(ev.Mode, "numeric", StringComparison.OrdinalIgnoreCase) &&
                        !string.Equals(ev.Mode, "symbolic", StringComparison.OrdinalIgnoreCase)))
                    {
                        issues.Add(new ValidationIssue("INVALID_VALUE_MODE", $"Value entry '{kv.Key}' has invalid mode. Must be text, numeric, or symbolic.", question.Id));
                    }

                    if (string.Equals(ev.Mode, "numeric", StringComparison.OrdinalIgnoreCase))
                    {
                        if (ev.NumericValue is null)
                        {
                            issues.Add(new ValidationIssue("MISSING_NUMERIC_VALUE", $"Value entry '{kv.Key}' requires numericValue.", question.Id));
                        }
                        if (ev.NumericTolerance is null or < 0)
                        {
                            issues.Add(new ValidationIssue("INVALID_NUMERIC_TOLERANCE", $"Value entry '{kv.Key}' requires a non-negative numericTolerance.", question.Id));
                        }
                    }

                    if (string.Equals(ev.Mode, "symbolic", StringComparison.OrdinalIgnoreCase))
                    {
                        if (string.IsNullOrWhiteSpace(ev.SymbolicExpectedLatex))
                        {
                            issues.Add(new ValidationIssue("MISSING_SYMBOLIC_EXPECTED", $"Value entry '{kv.Key}' requires symbolicExpectedLatex.", question.Id));
                        }
                        if (ev.SymbolicTolerance is null or < 0)
                        {
                            issues.Add(new ValidationIssue("INVALID_SYMBOLIC_TOLERANCE", $"Value entry '{kv.Key}' requires a non-negative symbolicTolerance.", question.Id));
                        }
                    }
                }
            }
        }
        else if (string.Equals(circ.InteractionMode, "build", StringComparison.OrdinalIgnoreCase))
        {
            var topo = ans.Topology;
            if (topo is null)
            {
                issues.Add(new ValidationIssue("MISSING_CIRCUIT_TOPOLOGY", "build interaction mode requires answer.circuit.topology.", question.Id));
            }
            else
            {
                if (topo.RequiredComponents is null || topo.RequiredComponents.Count == 0)
                {
                    issues.Add(new ValidationIssue("MISSING_REQUIRED_COMPONENTS", "Topology must specify requiredComponents.", question.Id));
                }
                else
                {
                    foreach (var rc in topo.RequiredComponents)
                    {
                        if (string.IsNullOrWhiteSpace(rc.SymbolId))
                        {
                            issues.Add(new ValidationIssue("MISSING_REQUIRED_COMPONENT_SYMBOL", "Required component must specify symbolId.", question.Id));
                        }
                        if (rc.Count <= 0)
                        {
                            issues.Add(new ValidationIssue("INVALID_REQUIRED_COMPONENT_COUNT", "Required component count must be greater than zero.", question.Id));
                        }
                    }
                }
            }
        }
    }

    private static void ValidateDirectedProject(AssessmentDefinition assessment, List<ValidationIssue> issues)
    {
        if (assessment.AttemptQuestionCount is not null)
        {
            issues.Add(new ValidationIssue("INVALID_ATTEMPT_QUESTION_COUNT", "attemptQuestionCount is not supported for directedProject assessments."));
        }

        var project = assessment.DirectedProject;
        if (project is null)
        {
            issues.Add(new ValidationIssue("MISSING_DIRECTED_PROJECT", "Directed projects must define the 'directedProject' field."));
            return;
        }

        RequireText(project.Summary, "MISSING_SUMMARY", "Directed project summary is required.", issues);

        if (project.EstimatedTimeMinutes.HasValue && project.EstimatedTimeMinutes.Value <= 0)
        {
            issues.Add(new ValidationIssue("INVALID_ESTIMATED_TIME", "Estimated time minutes must be greater than zero."));
        }

        if (project.Phases.Count == 0)
        {
            issues.Add(new ValidationIssue("DIRECTED_PROJECT_NO_PHASES", "Directed project must contain at least one phase."));
            return;
        }

        var phaseIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var stepIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);

        foreach (var phase in project.Phases)
        {
            RequireText(phase.Id, "MISSING_PHASE_ID", "Directed project phases must have an id.", issues);
            RequireText(phase.Title, "MISSING_PHASE_TITLE", $"Phase '{phase.Id}' must have a title.", issues);

            if (!phaseIds.Add(phase.Id))
            {
                issues.Add(new ValidationIssue("DUPLICATE_PHASE_ID", $"Phase id '{phase.Id}' must be unique across the project."));
            }

            if (phase.Steps.Count == 0)
            {
                issues.Add(new ValidationIssue("PHASE_NO_STEPS", $"Phase '{phase.Id}' must contain at least one step."));
            }

            foreach (var step in phase.Steps)
            {
                RequireText(step.Id, "MISSING_STEP_ID", $"Step in phase '{phase.Id}' must have an id.", issues);
                RequireText(step.Title, "MISSING_STEP_TITLE", $"Step '{step.Id}' must have a title.", issues);
                RequireText(step.Instruction, "MISSING_STEP_INSTRUCTION", $"Step '{step.Id}' must have an instruction.", issues);

                if (!stepIds.Add(step.Id))
                {
                    issues.Add(new ValidationIssue("DUPLICATE_STEP_ID", $"Step id '{step.Id}' must be unique across the project."));
                }

                ValidateMedia(step.Media, issues, step.Id);

                var checklistIds = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
                foreach (var item in step.Checklist)
                {
                    RequireText(item.Id, "MISSING_CHECKLIST_ID", $"Checklist item in step '{step.Id}' must have an id.", issues);
                    RequireText(item.Text, "MISSING_CHECKLIST_TEXT", $"Checklist item '{item.Id}' must have text.", issues);

                    if (!checklistIds.Add(item.Id))
                    {
                        issues.Add(new ValidationIssue("DUPLICATE_CHECKLIST_ID", $"Checklist id '{item.Id}' must be unique within step '{step.Id}'."));
                    }
                }

                ValidateDirectedProjectResources(step.Resources, issues);
            }
        }

        ValidateDirectedProjectResources(project.Resources, issues);
        if (project.Environment is not null)
        {
            ValidateDirectedProjectResources(project.Environment.InstallLinks, issues);
        }
    }

    private static void ValidateDirectedProjectResources(IReadOnlyList<DirectedProjectResourceDefinition> resources, List<ValidationIssue> issues)
    {
        foreach (var resource in resources)
        {
            RequireText(resource.Label, "MISSING_RESOURCE_LABEL", "Directed project resource must have a label.", issues);
            
            if (string.Equals(resource.Kind, "internal", StringComparison.OrdinalIgnoreCase))
            {
                RequireText(resource.Target, "MISSING_RESOURCE_TARGET", $"Internal resource '{resource.Label}' must have a target.", issues);
            }
            else
            {
                RequireText(resource.Url, "MISSING_RESOURCE_URL", $"External resource '{resource.Label}' must have a url.", issues);
            }
        }
    }

    private static void ValidateGraphingQuestion(QuestionDefinition question, List<ValidationIssue> issues)
    {
        if (question.Answer.GraphingAnswer is null)
        {
            issues.Add(new ValidationIssue("MISSING_GRAPHING_ANSWER", "Graphing questions must include answer.graphingAnswer.", question.Id));
            return;
        }

        if (question.Answer.GraphingAnswer.Features.Count == 0)
        {
            issues.Add(new ValidationIssue("MISSING_GRAPHING_FEATURES", "Graphing questions must include at least one expected feature.", question.Id));
        }

        foreach (var feature in question.Answer.GraphingAnswer.Features)
        {
            if (string.IsNullOrWhiteSpace(feature.Type))
            {
                issues.Add(new ValidationIssue("MISSING_GRAPHING_FEATURE_TYPE", "Graphing features must have a type.", question.Id));
            }
            if (feature.Weight <= 0)
            {
                issues.Add(new ValidationIssue("INVALID_GRAPHING_FEATURE_WEIGHT", "Graphing features must have a positive weight.", question.Id));
            }
        }
    }
}
