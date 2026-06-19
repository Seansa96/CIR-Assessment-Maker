using System.Threading;
using System.Threading.Tasks;
using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public interface ICircuitQuestionScorer
{
    Task<AnswerEvaluation> ScoreAsync(
        QuestionDefinition question,
        SubmittedAnswer submittedAnswer,
        AppSettings settings,
        CancellationToken cancellationToken = default);
}
