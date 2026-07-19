using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

/// <summary>Counts the learner-facing items for every assessment type.</summary>
public static class AssessmentItemCounter
{
    public static int Count(AssessmentDefinition assessment) => assessment.AssessmentType switch
    {
        AssessmentType.WorkedExample => assessment.WorkedExamples.Sum(example => example.Steps.Count),
        AssessmentType.GuidedProject => assessment.GuidedProject?.RequiredChecks.Count ?? 0,
        AssessmentType.RecallDrill => assessment.Items.Count,
        AssessmentType.Glossary => assessment.Glossary?.Sections
            .SelectMany(section => section.Entries)
            .Sum(entry => entry.Drills.Count) ?? 0,
        AssessmentType.ConceptLesson => assessment.Lesson?.Sections.Count ?? 0,
        AssessmentType.InteractiveExploration => assessment.Exploration?.Sections.Count ?? 0,
        AssessmentType.DirectedProject => assessment.DirectedProject?.Phases.Sum(phase => phase.Steps.Count) ?? 0,
        _ => assessment.Questions.Count
    };

    public static int? EffectiveAttemptCount(AssessmentDefinition assessment)
    {
        if (assessment.AssessmentType is AssessmentType.Quiz or AssessmentType.Test
            && assessment.QuestionSelection?.Mode is QuestionSelectionMode.OrderedVariants)
        {
            return assessment.QuestionSelection.Slots.Count;
        }

        return assessment.AttemptQuestionCount;
    }
}
