namespace QuizApp.Core.Domain;

public sealed record AssessmentSearchRequest(
    string? Query,
    string? SubjectId,
    string? AreaId,
    string? TopicId,
    string? LearningGoal,
    string? ActivityType,
    string? AssessmentType,
    IReadOnlyList<string>? Tags,
    IReadOnlyList<string>? Skills,
    int Limit = 25);

public sealed record AssessmentSearchResult(
    string Id,
    string Title,
    AssessmentType AssessmentType,
    string SubjectId,
    string SubjectTitle,
    IReadOnlyList<string> AreaIds,
    IReadOnlyList<string> AreaTitles,
    IReadOnlyList<string> TopicIds,
    IReadOnlyList<string> TopicTitles,
    string LearningGoal,
    string ActivityType,
    IReadOnlyList<string> Tags,
    IReadOnlyList<string> Skills,
    int QuestionCount,
    int AuthoredQuestionCount,
    int? AttemptQuestionCount,
    decimal Score,
    IReadOnlyList<string> MatchedFields,
    string? Snippet);

public sealed record AssessmentSearchSuggestion(
    string Kind,      // assessment, topic, area, tag, skill
    string Id,
    string Label,
    string? SubjectId,
    int Count,
    decimal Score);
