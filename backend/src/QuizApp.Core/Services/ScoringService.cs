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
            correctCount,
            totalQuestions,
            percentScore,
            attempt.CompletedAt is not null,
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
            _ => null
        };
    }
}
