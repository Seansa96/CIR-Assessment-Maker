namespace QuizApp.Core.Services;

public interface ISandboxService
{
    Task<SandboxContainerSession> CreateContainerAsync(string attemptId, QuizApp.Core.Domain.SandboxDefinition sandboxDef, string apiUrl, CancellationToken cancellationToken);
    Task StartContainerAsync(string containerId, CancellationToken cancellationToken);
    Task AttachToContainerAsync(string containerId, Func<byte[], Task> onOutput, Func<Func<byte[], Task>, Task> configureInputProxy, CancellationToken cancellationToken);
    Task StopContainerAsync(string containerId, CancellationToken cancellationToken);
    Task<bool> ResizeTerminalAsync(string containerId, int cols, int rows, CancellationToken cancellationToken);
}

public sealed record SandboxContainerSession(string ContainerId, string? WorkspacePath);
