using Docker.DotNet;
using Docker.DotNet.Models;
using QuizApp.Core.Services;

namespace QuizApp.Infrastructure.CodeRunner;

public sealed class SandboxService : ISandboxService
{
    private readonly DockerClient _dockerClient;

    public SandboxService()
    {
        _dockerClient = new DockerClientConfiguration().CreateClient();
    }

    public async Task<string> StartContainerAsync(string attemptId, QuizApp.Core.Domain.SandboxDefinition sandboxDef, string apiUrl, CancellationToken cancellationToken)
    {
        var image = sandboxDef.Image;
        // First check if image exists, pull if it doesn't
        try
        {
            await _dockerClient.Images.InspectImageAsync(image, cancellationToken);
        }
        catch (DockerApiException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
        {
            await _dockerClient.Images.CreateImageAsync(
                new ImagesCreateParameters { FromImage = image },
                null,
                new Progress<JSONMessage>(),
                cancellationToken);
        }

        var hostConfig = new HostConfig
        {
            ReadonlyRootfs = sandboxDef.ReadOnlyFileSystem,
            AutoRemove = true
        };

        if (sandboxDef.Files.Count > 0)
        {
            var tempDir = Path.Combine(Path.GetTempPath(), "cir_sandbox", attemptId);
            Directory.CreateDirectory(tempDir);
            foreach (var file in sandboxDef.Files)
            {
                var filePath = Path.Combine(tempDir, file.Path);
                var dir = Path.GetDirectoryName(filePath);
                if (!string.IsNullOrEmpty(dir))
                {
                    Directory.CreateDirectory(dir);
                }
                await File.WriteAllTextAsync(filePath, file.Content, cancellationToken);
            }
            // Bind the temp directory to /workspace
            hostConfig.Binds = new[] { $"{tempDir}:/workspace" };
        }

        var response = await _dockerClient.Containers.CreateContainerAsync(new CreateContainerParameters
        {
            Image = image,
            Tty = true,
            AttachStdin = true,
            AttachStdout = true,
            AttachStderr = true,
            OpenStdin = true,
            Cmd = string.IsNullOrEmpty(sandboxDef.InitialCommand) ? null : new[] { "sh", "-c", sandboxDef.InitialCommand },
            Env = new[] { $"CIR_ATTEMPT_ID={attemptId}", $"CIR_API_URL={apiUrl}" },
            HostConfig = hostConfig
        }, cancellationToken);

        await _dockerClient.Containers.StartContainerAsync(response.ID, new ContainerStartParameters(), cancellationToken);

        return response.ID;
    }

    public async Task AttachToContainerAsync(string containerId, Func<byte[], Task> onOutput, Func<Func<byte[], Task>, Task> configureInputProxy, CancellationToken cancellationToken)
    {
        using var stream = await _dockerClient.Containers.AttachContainerAsync(
            containerId,
            true,
            new ContainerAttachParameters
            {
                Stream = true,
                Stdin = true,
                Stdout = true,
                Stderr = true
            }, cancellationToken);

        // Handle sending input to container
        await configureInputProxy(async (bytes) =>
        {
            await stream.WriteAsync(bytes, 0, bytes.Length, cancellationToken);
        });

        // Read output from container
        var buffer = new byte[4096];
        while (!cancellationToken.IsCancellationRequested)
        {
            var result = await stream.ReadOutputAsync(buffer, 0, buffer.Length, cancellationToken);
            if (result.EOF) break;
            
            var chunk = new byte[result.Count];
            Array.Copy(buffer, chunk, result.Count);
            await onOutput(chunk);
        }
    }

    public async Task StopContainerAsync(string containerId, CancellationToken cancellationToken)
    {
        try
        {
            await _dockerClient.Containers.StopContainerAsync(
                containerId,
                new ContainerStopParameters { WaitBeforeKillSeconds = 1 },
                cancellationToken);
        }
        catch (DockerApiException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound || ex.StatusCode == System.Net.HttpStatusCode.NotModified)
        {
            // Already stopped or doesn't exist
        }
    }
}
