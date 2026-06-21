using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public interface IGuidedProjectRunner
{
    string Mode { get; }

    Task<GuidedProjectRunResult> RunAsync(
        GuidedProjectRunRequest request,
        CancellationToken cancellationToken);
}
