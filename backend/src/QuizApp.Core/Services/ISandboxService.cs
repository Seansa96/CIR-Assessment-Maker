namespace QuizApp.Core.Services;

public interface ISandboxService
{
    Task<string> StartContainerAsync(string attemptId, QuizApp.Core.Domain.SandboxDefinition sandboxDef, string apiUrl, CancellationToken cancellationToken);
    Task AttachToContainerAsync(string containerId, Func<byte[], Task> onOutput, Func<Func<byte[], Task>, Task> configureInputProxy, CancellationToken cancellationToken);
    Task StopContainerAsync(string containerId, CancellationToken cancellationToken);
}
