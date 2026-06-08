using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public sealed class ScoringService
{
    public AnswerEvaluation ScoreAnswer(QuestionDefinition question, SubmittedAnswer submittedAnswer)
    {
        var isCorrect = question.Type switch
        {
            QuestionType.MultipleChoice => string.Equals(question.Answer.ChoiceId, submittedAnswer.ChoiceId, StringComparison.OrdinalIgnoreCase),
            QuestionType.SelectAll => SameChoiceSet(question.Answer.ChoiceIds, submittedAnswer.ChoiceIds),
            QuestionType.FreeResponse => submittedAnswer.SelfCheckCorrect == true,
            QuestionType.NumericResponse => IsNumericCorrect(question.Answer.NumericValue, submittedAnswer.NumericValue, question.Answer.NumericTolerance),
            _ => false
        };

        return new AnswerEvaluation(
            question.Id,
            isCorrect,
            question.Explanation,
            DescribeExpectedAnswer(question));
    }

    public AttemptResults BuildResults(AssessmentDefinition assessment, Attempt attempt)
    {
        var answersByQuestion = attempt.Answers.ToDictionary(answer => answer.QuestionId, StringComparer.OrdinalIgnoreCase);
        var orderedQuestions = attempt.QuestionOrder
            .Select(questionId => assessment.Questions.First(question => string.Equals(question.Id, questionId, StringComparison.OrdinalIgnoreCase)))
            .ToList();

        var questionResults = orderedQuestions.Select(question =>
        {
            answersByQuestion.TryGetValue(question.Id, out var answer);
            var showFeedback = attempt.CompletedAt is not null || attempt.Mode is AssessmentMode.Practice;

            return new QuestionResult(
                question.Id,
                question.Prompt,
                question.Type,
                question.Media,
                answer?.Answer,
                showFeedback ? answer?.Evaluation?.IsCorrect : null,
                showFeedback ? question.Explanation : null,
                showFeedback ? DescribeExpectedAnswer(question) : null);
        }).ToList();

        var correctCount = attempt.Answers.Count(answer => answer.Evaluation?.IsCorrect == true);
        var totalQuestions = attempt.QuestionOrder.Count;
        var percentScore = totalQuestions == 0 ? 0 : Math.Round(correctCount * 100m / totalQuestions, 2);

        return new AttemptResults(
            attempt.Id,
            assessment.Id,
            assessment.Title,
            attempt.Mode,
            attempt.Status,
            correctCount,
            totalQuestions,
            percentScore,
            attempt.Status is AttemptStatus.Completed,
            questionResults);
    }

    private static bool SameChoiceSet(IReadOnlyList<string> expected, IReadOnlyList<string> actual)
    {
        return expected.ToHashSet(StringComparer.OrdinalIgnoreCase)
            .SetEquals(actual.ToHashSet(StringComparer.OrdinalIgnoreCase));
    }

    private static string? DescribeExpectedAnswer(QuestionDefinition question)
    {
        return question.Type switch
        {
            QuestionType.MultipleChoice => question.Answer.ChoiceId,
            QuestionType.SelectAll => string.Join(", ", question.Answer.ChoiceIds),
            QuestionType.FreeResponse => question.Answer.Expected,
            QuestionType.NumericResponse => question.Answer.NumericValue?.ToString(),
            _ => null
        };
    }

    private static bool IsNumericCorrect(decimal? expected, decimal? actual, decimal? tolerance)
    {
        if (expected is null || actual is null || tolerance is null)
        {
            return false;
        }

        return Math.Abs(expected.Value - actual.Value) <= tolerance.Value;
    }
}
