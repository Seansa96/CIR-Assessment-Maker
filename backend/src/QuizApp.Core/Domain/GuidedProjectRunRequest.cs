namespace QuizApp.Core.Domain;

public sealed record GuidedProjectRunRequest(
    GuidedProjectSession Session,
    AssessmentDefinition Assessment,
    AppSettings Settings);
