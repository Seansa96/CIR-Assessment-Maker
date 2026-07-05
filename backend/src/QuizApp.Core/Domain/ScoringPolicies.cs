namespace QuizApp.Core.Domain;

public static class RecallScoringPolicy
{
    public static decimal GradeValue(RecallRating rating) => rating switch
    {
        RecallRating.Easy => 1.00m,
        RecallRating.Correct => 0.85m,
        RecallRating.NeedsReview => 0.40m,
        RecallRating.ForgotCompletely => 0.00m,
        _ => 0.00m
    };

    public static bool IsMastered(RecallRating rating) =>
        rating is RecallRating.Easy or RecallRating.Correct;

    public static bool IsWeak(RecallRating rating) =>
        rating is RecallRating.NeedsReview or RecallRating.ForgotCompletely;
}

public static class GradeContributionPolicy
{
    public static decimal WeightFor(AssessmentType type) => type switch
    {
        AssessmentType.Test => 1.00m,
        AssessmentType.Quiz => 0.75m,
        AssessmentType.RecallDrill => 0.40m,
        _ => 0.00m
    };
}
