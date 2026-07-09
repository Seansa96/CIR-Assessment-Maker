using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public sealed class GraphingQuestionScorer : IGraphingQuestionScorer
{
    public Task<AnswerEvaluation> ScoreAsync(QuestionDefinition question, SubmittedAnswer submittedAnswer, AppSettings settings, CancellationToken cancellationToken = default)
    {
        var expectedAnswer = question.Answer.GraphingAnswer;
        var actualAnswer = submittedAnswer.GraphingAnswer;

        if (expectedAnswer is null)
        {
            return Task.FromResult(new AnswerEvaluation(question.Id, false, question.Explanation, null)
            {
                EarnedPoints = 0m,
                PossiblePoints = 1m
            });
        }

        var possiblePoints = expectedAnswer.Features.Sum(f => f.Weight);
        if (possiblePoints == 0m) possiblePoints = 1m; // safeguard

        var earnedPoints = 0m;
        var featureEvaluations = new List<GraphFeatureEvaluation>();

        if (actualAnswer is null)
        {
            return Task.FromResult(new AnswerEvaluation(question.Id, false, question.Explanation, null)
            {
                EarnedPoints = 0m,
                PossiblePoints = possiblePoints,
                GraphFeedback = new GraphFeedback(featureEvaluations)
            });
        }

        foreach (var feature in expectedAnswer.Features)
        {
            var (passed, message) = EvaluateFeature(feature, actualAnswer);
            featureEvaluations.Add(new GraphFeatureEvaluation(feature.Type, passed, message));
            if (passed)
            {
                earnedPoints += feature.Weight;
            }
        }

        var isCorrect = earnedPoints >= possiblePoints;

        return Task.FromResult(new AnswerEvaluation(question.Id, isCorrect, question.Explanation, null)
        {
            EarnedPoints = earnedPoints,
            PossiblePoints = possiblePoints,
            GraphFeedback = new GraphFeedback(featureEvaluations)
        });
    }

    private (bool passed, string message) EvaluateFeature(ExpectedGraphFeature feature, SubmittedGraphAnswer actualAnswer)
    {
        var type = feature.Type.ToLowerInvariant();
        var tol = feature.Tolerance;

        switch (type)
        {
            case "shapetype":
                if (feature.StringValue is null)
                {
                    return (false, "Configuration error: ShapeType requires a stringValue.");
                }
                var passedShape = string.Equals(actualAnswer.Shape, feature.StringValue, StringComparison.OrdinalIgnoreCase);
                return (passedShape, passedShape ? "Correct shape type." : $"Expected shape {feature.StringValue}, but got {actualAnswer.Shape}.");

            case "vertexat":
            case "passesthrough":
                if (feature.X is null || feature.Y is null)
                {
                    return (false, $"Configuration error: {feature.Type} requires X and Y.");
                }

                // If the user's curve is defined by control points, we must check if one of those points is exactly the vertex,
                // OR if the mathematical curve passes through X, Y.
                // For MVP: Check if the user placed ANY point near (X,Y).
                // Later, we can evaluate the actual curve expression `actualAnswer.Expression`.
                
                var passedPoint = actualAnswer.Points.Any(p => Math.Abs(p.X - feature.X.Value) <= tol && Math.Abs(p.Y - feature.Y.Value) <= tol);
                return (passedPoint, passedPoint ? $"Passes through ({feature.X}, {feature.Y})." : $"Does not pass through ({feature.X}, {feature.Y}).");

            default:
                return (false, $"Unknown feature type {feature.Type}.");
        }
    }
}
