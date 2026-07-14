using Microsoft.AspNetCore.SignalR;
using QuizApp.Core.Services;

namespace QuizApp.Api.Hubs;

public class SandboxHub : Hub
{
    private readonly ISandboxService _sandboxService;
    private readonly ILogger<SandboxHub> _logger;
    private static readonly Dictionary<string, string> _connectionContainers = new();

    private readonly AttemptService _attemptService;
    private readonly QuizApp.Core.Repositories.IAssessmentRepository _assessmentRepository;

    public SandboxHub(ISandboxService sandboxService, ILogger<SandboxHub> logger, AttemptService attemptService, QuizApp.Core.Repositories.IAssessmentRepository assessmentRepository)
    {
        _sandboxService = sandboxService;
        _logger = logger;
        _attemptService = attemptService;
        _assessmentRepository = assessmentRepository;
    }

    public async Task StartSandbox(string attemptId)
    {
        try
        {
            var attempt = await _attemptService.GetAsync(attemptId, CancellationToken.None);
            var assessment = await _assessmentRepository.GetByIdAsync(attempt.AssessmentId, CancellationToken.None);
            
            if (assessment?.Sandbox is null)
            {
                throw new InvalidOperationException("Assessment does not have a sandbox definition.");
            }

            // Set timeout for sandbox duration (e.g. 1 hour)
            var cts = new CancellationTokenSource(TimeSpan.FromHours(1));
            
            var apiUrl = "http://host.docker.internal:5000"; // Assuming local dev
            var containerId = await _sandboxService.StartContainerAsync(attemptId, assessment.Sandbox, apiUrl, cts.Token);
            _connectionContainers[Context.ConnectionId] = containerId;

            // Start background task to pipe data
            _ = Task.Run(async () =>
            {
                try
                {
                    await _sandboxService.AttachToContainerAsync(
                        containerId,
                        async (bytes) =>
                        {
                            var base64 = Convert.ToBase64String(bytes);
                            await Clients.Caller.SendAsync("ReceiveOutput", base64);
                        },
                        (writeFunc) =>
                        {
                            // Store the write function in connection context so Input method can use it
                            Context.Items["WriteInput"] = writeFunc;
                            return Task.CompletedTask;
                        },
                        cts.Token);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error while streaming container output.");
                }
            });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to start sandbox.");
            await Clients.Caller.SendAsync("Error", ex.Message);
        }
    }

    public async Task SendInput(string base64Data)
    {
        if (Context.Items.TryGetValue("WriteInput", out var writeObj) && writeObj is Func<byte[], Task> writeFunc)
        {
            var bytes = Convert.FromBase64String(base64Data);
            await writeFunc(bytes);
        }
    }

    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        if (_connectionContainers.TryGetValue(Context.ConnectionId, out var containerId))
        {
            _connectionContainers.Remove(Context.ConnectionId);
            await _sandboxService.StopContainerAsync(containerId, CancellationToken.None);
        }
        await base.OnDisconnectedAsync(exception);
    }
}
