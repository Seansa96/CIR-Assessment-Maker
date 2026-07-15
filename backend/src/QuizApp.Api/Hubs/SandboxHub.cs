using Microsoft.AspNetCore.SignalR;
using QuizApp.Core.Services;
using System.Collections.Concurrent;
using System.Text;

namespace QuizApp.Api.Hubs;

public class SandboxHub : Hub
{
    private readonly ISandboxService _sandboxService;
    private readonly ILogger<SandboxHub> _logger;
    private static readonly ConcurrentDictionary<string, string> _connectionContainers = new();
    private static readonly ConcurrentDictionary<string, Func<byte[], Task>> _connectionInputWriters = new();
    private static readonly ConcurrentDictionary<string, CancellationTokenSource> _connectionCancellation = new();

    private readonly AttemptService _attemptService;
    private readonly QuizApp.Core.Repositories.IAssessmentRepository _assessmentRepository;

    public SandboxHub(ISandboxService sandboxService, ILogger<SandboxHub> logger, AttemptService attemptService, QuizApp.Core.Repositories.IAssessmentRepository assessmentRepository)
    {
        _sandboxService = sandboxService;
        _logger = logger;
        _attemptService = attemptService;
        _assessmentRepository = assessmentRepository;
    }

    public async Task StartSandbox(string attemptId, int cols = 120, int rows = 30)
    {
        var connectionId = Context.ConnectionId;
        await CleanupConnectionAsync(connectionId, stopContainer: true);

        try
        {
            await SendStatusAsync(connectionId, "starting", $"Starting sandbox for attempt {attemptId}.");
            var attempt = await _attemptService.GetAsync(attemptId, CancellationToken.None);
            var assessment = await _assessmentRepository.GetByIdAsync(attempt.AssessmentId, CancellationToken.None);
            
            if (assessment?.Sandbox is null)
            {
                throw new InvalidOperationException("Assessment does not have a sandbox definition.");
            }

            var cts = new CancellationTokenSource(TimeSpan.FromHours(1));
            _connectionCancellation[connectionId] = cts;
            
            var apiUrl = "http://host.docker.internal:5000"; // Assuming local dev
            await SendStatusAsync(connectionId, "creating", $"Creating Docker container from image '{assessment.Sandbox.Image}'.");
            var session = await _sandboxService.CreateContainerAsync(attemptId, assessment.Sandbox, apiUrl, cts.Token);
            var containerId = session.ContainerId;
            _connectionContainers[connectionId] = containerId;
            await SendStatusAsync(connectionId, "created", $"Created container {ShortId(containerId)}{(session.WorkspacePath is null ? "." : $" with workspace {session.WorkspacePath}.")}");

            var inputReady = new TaskCompletionSource<Func<byte[], Task>>(TaskCreationOptions.RunContinuationsAsynchronously);
            var client = Clients.Client(connectionId);

            await SendStatusAsync(connectionId, "container-starting", $"Starting container {ShortId(containerId)}.");
            await _sandboxService.StartContainerAsync(containerId, cts.Token);
            await SendStatusAsync(connectionId, "container-started", $"Container {ShortId(containerId)} is running.");

            if (await _sandboxService.ResizeTerminalAsync(containerId, cols, rows, cts.Token))
            {
                await SendStatusAsync(connectionId, "resized", $"Terminal size set to {cols}x{rows}.");
            }
            else
            {
                await SendStatusAsync(connectionId, "resize-pending", $"Terminal resize to {cols}x{rows} will retry after the terminal stream attaches.");
            }

            await SendStatusAsync(connectionId, "attaching", "Attaching terminal stream.");
            _ = Task.Run(async () =>
            {
                try
                {
                    await _sandboxService.AttachToContainerAsync(
                        containerId,
                        async (bytes) =>
                        {
                            var base64 = Convert.ToBase64String(bytes);
                            await client.SendAsync("ReceiveOutput", base64);
                        },
                        (writeFunc) =>
                        {
                            _connectionInputWriters[connectionId] = writeFunc;
                            inputReady.TrySetResult(writeFunc);
                            _logger.LogInformation("Sandbox input-ready for {ConnectionId}: Terminal input stream is ready.", connectionId);
                            _ = client.SendAsync("SandboxStatus", "input-ready", "Terminal input stream is ready.");
                            return Task.CompletedTask;
                        },
                        cts.Token);

                    _logger.LogInformation("Sandbox stream-ended for {ConnectionId}: Sandbox terminal stream ended.", connectionId);
                    await client.SendAsync("SandboxStatus", "stream-ended", "Sandbox terminal stream ended.");
                }
                catch (OperationCanceledException)
                {
                    _logger.LogInformation("Sandbox stream canceled for {ConnectionId}.", connectionId);
                    await client.SendAsync("SandboxStatus", "stream-canceled", "Sandbox terminal stream was closed.");
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error while streaming container output.");
                    inputReady.TrySetException(ex);
                    await client.SendAsync("SandboxFailed", "stream", ex.Message);
                    await client.SendAsync("Error", ex.Message);
                }
            }, cts.Token);

            var readyTask = await Task.WhenAny(inputReady.Task, Task.Delay(TimeSpan.FromSeconds(5), cts.Token));
            if (readyTask == inputReady.Task)
            {
                var writeInput = await inputReady.Task;
                var resized = await ResizeTerminalWithRetriesAsync(connectionId, containerId, cols, rows, cts.Token);
                await ConfigureInteractiveShellAsync(connectionId, assessment.Sandbox, writeInput, resized, cts.Token);
                await Clients.Client(connectionId).SendAsync("SandboxReady");
                await SendStatusAsync(connectionId, "ready", "Sandbox is ready for input.");
            }
            else
            {
                await SendStatusAsync(connectionId, "waiting-for-input", "Container is running, but the input stream has not reported ready yet.");
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to start sandbox.");
            await Clients.Caller.SendAsync("SandboxFailed", "startup", ex.Message);
            await Clients.Caller.SendAsync("Error", ex.Message);
        }
    }


    public async Task SendInput(string base64Data)
    {
        if (_connectionInputWriters.TryGetValue(Context.ConnectionId, out var writeFunc))
        {
            var bytes = Convert.FromBase64String(base64Data);
            try
            {
                await writeFunc(bytes);
                _logger.LogDebug("Wrote {ByteCount} sandbox input bytes for connection {ConnectionId}.", bytes.Length, Context.ConnectionId);
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "Failed to write sandbox input for connection {ConnectionId}.", Context.ConnectionId);
                await Clients.Caller.SendAsync("SandboxFailed", "input-write", ex.Message);
                await Clients.Caller.SendAsync("Error", $"Sandbox input write failed: {ex.Message}");
            }
            return;
        }

        await Clients.Caller.SendAsync("SandboxStatus", "input-waiting", "Sandbox input is not ready yet.");
        await Clients.Caller.SendAsync("Error", "Sandbox input is not ready yet. Try again in a moment.");
    }

    public async Task ResizeTerminal(int cols, int rows)
    {
        if (_connectionContainers.TryGetValue(Context.ConnectionId, out var containerId))
        {
            if (!await _sandboxService.ResizeTerminalAsync(containerId, cols, rows, CancellationToken.None))
            {
                await Clients.Caller.SendAsync("SandboxStatus", "resize-skipped", $"Terminal resize to {cols}x{rows} was not applied.");
            }
        }
    }

    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        await CleanupConnectionAsync(Context.ConnectionId, stopContainer: true);
        await base.OnDisconnectedAsync(exception);
    }

    private async Task CleanupConnectionAsync(string connectionId, bool stopContainer)
    {
        _connectionInputWriters.TryRemove(connectionId, out _);
        if (_connectionCancellation.TryRemove(connectionId, out var cts))
        {
            await cts.CancelAsync();
            cts.Dispose();
        }

        if (stopContainer && _connectionContainers.TryRemove(connectionId, out var containerId))
        {
            await _sandboxService.StopContainerAsync(containerId, CancellationToken.None);
        }
    }

    private Task SendStatusAsync(string connectionId, string phase, string message)
    {
        _logger.LogInformation("Sandbox {Phase} for {ConnectionId}: {Message}", phase, connectionId, message);
        return Clients.Client(connectionId).SendAsync("SandboxStatus", phase, message);
    }

    private async Task<bool> ResizeTerminalWithRetriesAsync(string connectionId, string containerId, int cols, int rows, CancellationToken cancellationToken)
    {
        for (var attempt = 1; attempt <= 5; attempt++)
        {
            if (await _sandboxService.ResizeTerminalAsync(containerId, cols, rows, cancellationToken))
            {
                await SendStatusAsync(connectionId, "resized", $"Terminal size confirmed at {cols}x{rows}.");
                return true;
            }

            if (attempt < 5)
            {
                await SendStatusAsync(connectionId, "resize-retry", $"Terminal resize attempt {attempt} did not apply yet; retrying.");
                await Task.Delay(250, cancellationToken);
            }
        }

        await SendStatusAsync(connectionId, "resize-warning", $"Terminal resize to {cols}x{rows} could not be confirmed. Input is enabled, but some shells may behave poorly.");
        return false;
    }

    private async Task ConfigureInteractiveShellAsync(
        string connectionId,
        QuizApp.Core.Domain.SandboxDefinition sandbox,
        Func<byte[], Task> writeInput,
        bool terminalResizeConfirmed,
        CancellationToken cancellationToken)
    {
        if (!IsPowerShellSandbox(sandbox))
        {
            return;
        }

        if (!terminalResizeConfirmed)
        {
            await SendStatusAsync(connectionId, "shell-basic", "PowerShell line editing stayed in basic mode because terminal resize was not confirmed.");
            return;
        }

        await SendStatusAsync(connectionId, "shell-enhancing", "Enabling PowerShell tab completion and line-editing keybinds.");
        var script =
            "try { " +
            "Import-Module PSReadLine -ErrorAction Stop; " +
            "Set-PSReadLineOption -PredictionSource None -EditMode Emacs -BellStyle None -ErrorAction SilentlyContinue; " +
            "Set-PSReadLineKeyHandler -Key Tab -Function Complete -ErrorAction SilentlyContinue; " +
            "Set-PSReadLineKeyHandler -Key Ctrl+a -Function BeginningOfLine -ErrorAction SilentlyContinue; " +
            "Set-PSReadLineKeyHandler -Key Ctrl+e -Function EndOfLine -ErrorAction SilentlyContinue; " +
            "Set-PSReadLineKeyHandler -Key Ctrl+l -Function ClearScreen -ErrorAction SilentlyContinue; " +
            "Set-PSReadLineKeyHandler -Key Backspace -Function BackwardDeleteChar -ErrorAction SilentlyContinue; " +
            "Set-PSReadLineKeyHandler -Key Delete -Function DeleteChar -ErrorAction SilentlyContinue " +
            "} catch { }";

        try
        {
            await writeInput(Encoding.UTF8.GetBytes(script + "\r"));
            await Task.Delay(150, cancellationToken);
            await SendStatusAsync(connectionId, "shell-enhanced", "PowerShell line editing is enabled.");
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Failed to enable PowerShell line editing for sandbox connection {ConnectionId}.", connectionId);
            await SendStatusAsync(connectionId, "shell-basic", $"PowerShell line editing could not be enabled: {ex.Message}");
        }
    }

    private static bool IsPowerShellSandbox(QuizApp.Core.Domain.SandboxDefinition sandbox)
    {
        if (sandbox.Language.Equals("pwsh", StringComparison.OrdinalIgnoreCase) ||
            sandbox.Language.Equals("powershell", StringComparison.OrdinalIgnoreCase))
        {
            return true;
        }

        return sandbox.InitialCommand.TrimStart().StartsWith("pwsh", StringComparison.OrdinalIgnoreCase) ||
            sandbox.InitialCommand.TrimStart().StartsWith("powershell", StringComparison.OrdinalIgnoreCase);
    }

    private static string ShortId(string containerId)
    {
        return containerId[..Math.Min(containerId.Length, 12)];
    }
}
