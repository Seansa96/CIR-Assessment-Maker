using Docker.DotNet;
using Docker.DotNet.Models;
using QuizApp.Core.Services;
using System.Diagnostics;
using System.Text;

namespace QuizApp.Infrastructure.CodeRunner;

public sealed class SandboxService : ISandboxService
{
    private readonly DockerClient _dockerClient;

    public SandboxService()
    {
        _dockerClient = new DockerClientConfiguration().CreateClient();
    }

    public async Task<SandboxContainerSession> CreateContainerAsync(string attemptId, QuizApp.Core.Domain.SandboxDefinition sandboxDef, string apiUrl, CancellationToken cancellationToken)
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

        var keepContainers = string.Equals(
            Environment.GetEnvironmentVariable("CIR_SANDBOX_KEEP_CONTAINERS"),
            "1",
            StringComparison.OrdinalIgnoreCase);

        var hostConfig = new HostConfig
        {
            ReadonlyRootfs = sandboxDef.ReadOnlyFileSystem,
            AutoRemove = !keepContainers
        };

        string? workspacePath = null;
        if (sandboxDef.Files.Count > 0)
        {
            var tempDir = Path.Combine(Path.GetTempPath(), "cir_sandbox", attemptId);
            workspacePath = tempDir;
            Directory.CreateDirectory(tempDir);
            foreach (var file in sandboxDef.Files)
            {
                var filePath = Path.Combine(tempDir, file.Path);
                var dir = Path.GetDirectoryName(filePath);
                if (!string.IsNullOrEmpty(dir))
                    Directory.CreateDirectory(dir);
                await File.WriteAllTextAsync(filePath, file.Content, cancellationToken);
            }

            // Bind the temp directory to /workspace
            // Docker Desktop on Windows accepts the Windows path format directly
            hostConfig.Binds = new[] { $"{tempDir}:/workspace" };
        }

        // Build the command array for Docker directly (no sh -c wrapper).
        // The InitialCommand in the YAML is a full shell invocation like:
        //   pwsh -NoExit -Command "& /workspace/.cir/setup.ps1; ..."
        // We split it into tokens ourselves so Docker exec's pwsh as PID 1.
        IList<string>? cmd = null;
        if (!string.IsNullOrWhiteSpace(sandboxDef.InitialCommand))
        {
            cmd = SplitCommand(sandboxDef.InitialCommand);
        }

        var createParameters = new CreateContainerParameters
        {
            Image = image,
            Tty = true,
            AttachStdin = true,
            AttachStdout = true,
            AttachStderr = true,
            OpenStdin = true,
            StdinOnce = false,
            Cmd = cmd,
            Env = new[]
            {
                $"CIR_ATTEMPT_ID={attemptId}",
                $"CIR_API_URL={apiUrl}",
                "TERM=xterm-256color",
                "COLORTERM=truecolor",
                "NO_COLOR=1"
            },
            HostConfig = hostConfig
        };

        var response = await CreateContainerWithMountFallbackAsync(createParameters, cancellationToken);
        return new SandboxContainerSession(response.ID, workspacePath);
    }

    public async Task StartContainerAsync(string containerId, CancellationToken cancellationToken)
    {
        if (UsesDockerCliStartAttach())
        {
            return;
        }

        var started = await _dockerClient.Containers.StartContainerAsync(containerId, new ContainerStartParameters(), cancellationToken);
        if (!started)
        {
            throw new InvalidOperationException($"Docker did not start sandbox container {containerId[..Math.Min(containerId.Length, 12)]}.");
        }
    }

    /// <summary>
    /// Splits a shell command string into tokens, respecting double-quoted segments.
    /// e.g. pwsh -NoExit -Command "foo bar" → ["pwsh", "-NoExit", "-Command", "foo bar"]
    /// </summary>
    private static IList<string> SplitCommand(string command)
    {
        var tokens = new List<string>();
        var current = new System.Text.StringBuilder();
        bool inDouble = false;
        bool inSingle = false;

        foreach (var ch in command)
        {
            if (ch == '"' && !inSingle)  { inDouble = !inDouble; continue; }
            if (ch == '\'' && !inDouble) { inSingle = !inSingle; continue; }

            if (ch == ' ' && !inDouble && !inSingle)
            {
                if (current.Length > 0)
                {
                    tokens.Add(current.ToString());
                    current.Clear();
                }
                continue;
            }
            current.Append(ch);
        }
        if (current.Length > 0)
            tokens.Add(current.ToString());

        return tokens;
    }

    private async Task<CreateContainerResponse> CreateContainerWithMountFallbackAsync(CreateContainerParameters createParameters, CancellationToken cancellationToken)
    {
        try
        {
            return await _dockerClient.Containers.CreateContainerAsync(createParameters, cancellationToken);
        }
        catch (DockerApiException ex) when (OperatingSystem.IsWindows() && createParameters.HostConfig?.Binds is { Count: > 0 } binds)
        {
            var fallbackBinds = binds.Select(ConvertWindowsBindToDockerDesktopPath).ToList();
            if (fallbackBinds.SequenceEqual(binds, StringComparer.OrdinalIgnoreCase))
            {
                throw;
            }

            createParameters.HostConfig.Binds = fallbackBinds;
            try
            {
                return await _dockerClient.Containers.CreateContainerAsync(createParameters, cancellationToken);
            }
            catch (DockerApiException fallbackEx)
            {
                throw new InvalidOperationException(
                    $"Docker failed to create sandbox container with both native and Docker Desktop mount paths. Native error: {ex.Message}; fallback error: {fallbackEx.Message}",
                    fallbackEx);
            }
        }
    }

    private static string ConvertWindowsBindToDockerDesktopPath(string bind)
    {
        var separatorIndex = bind.LastIndexOf(':');
        if (separatorIndex <= 1)
        {
            return bind;
        }

        var hostPath = bind[..separatorIndex];
        var containerPath = bind[(separatorIndex + 1)..];
        if (hostPath.Length < 3 || hostPath[1] != ':' || hostPath[2] != '\\')
        {
            return bind;
        }

        var drive = char.ToLowerInvariant(hostPath[0]);
        var rest = hostPath[2..].Replace('\\', '/');
        return $"/{drive}{rest}:{containerPath}";
    }

    public async Task AttachToContainerAsync(string containerId, Func<byte[], Task> onOutput, Func<Func<byte[], Task>, Task> configureInputProxy, CancellationToken cancellationToken)
    {
        if (UsesDockerCliStartAttach())
        {
            await AttachWithDockerCliAsync(containerId, onOutput, configureInputProxy, cancellationToken);
            return;
        }

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

        // Handle sending input to container — capture stream in a safe wrapper
        await configureInputProxy(async (bytes) =>
        {
            try
            {
                await stream.WriteAsync(bytes, 0, bytes.Length, cancellationToken);
            }
            catch (ObjectDisposedException)
            {
                throw new IOException("Sandbox input stream is closed; the container may have exited.");
            }
            catch (IOException)
            {
                throw;
            }
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

    private static bool UsesDockerCliStartAttach()
    {
        return !string.Equals(Environment.GetEnvironmentVariable("CIR_SANDBOX_ATTACH_TRANSPORT"), "docker-dotnet", StringComparison.OrdinalIgnoreCase);
    }

    private static async Task AttachWithDockerCliAsync(
        string containerId,
        Func<byte[], Task> onOutput,
        Func<Func<byte[], Task>, Task> configureInputProxy,
        CancellationToken cancellationToken)
    {
        var lastError = string.Empty;

        while (!cancellationToken.IsCancellationRequested)
        {
            using var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "docker",
                    Arguments = $"start --attach --interactive {containerId}",
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                },
                EnableRaisingEvents = true
            };

            try
            {
                if (!process.Start())
                {
                    throw new InvalidOperationException("Docker attach process did not start.");
                }
            }
            catch (Exception ex)
            {
                throw new InvalidOperationException($"Failed to start 'docker attach' for sandbox container {containerId[..Math.Min(containerId.Length, 12)]}: {ex.Message}", ex);
            }

            await configureInputProxy(async bytes =>
            {
                if (process.HasExited)
                {
                    throw new IOException($"Docker attach process exited with code {process.ExitCode}. Last error: {lastError}");
                }

                try
                {
                    await process.StandardInput.BaseStream.WriteAsync(bytes, 0, bytes.Length, cancellationToken);
                    await process.StandardInput.BaseStream.FlushAsync(cancellationToken);
                }
                catch (Exception ex) when (ex is IOException or ObjectDisposedException or InvalidOperationException)
                {
                    throw new IOException($"Failed to write to docker attach stdin: {ex.Message}", ex);
                }
            });

            await Task.Delay(300, cancellationToken);
            if (process.HasExited)
            {
                lastError = await process.StandardError.ReadToEndAsync(cancellationToken);
                if (string.IsNullOrWhiteSpace(lastError))
                {
                    lastError = $"docker start --attach --interactive exited with code {process.ExitCode}.";
                }

                await onOutput(Encoding.UTF8.GetBytes($"\r\n[sandbox attach retry] {lastError.Trim()}\r\n"));
                await Task.Delay(300, cancellationToken);
                continue;
            }

            var stdoutTask = PumpStreamAsync(process.StandardOutput.BaseStream, onOutput, cancellationToken);
            var stderrTask = PumpStreamAsync(process.StandardError.BaseStream, onOutput, cancellationToken);
            var exitTask = process.WaitForExitAsync(cancellationToken);

            try
            {
                await Task.WhenAny(Task.WhenAll(stdoutTask, stderrTask), exitTask);
                if (!process.HasExited)
                {
                    process.Kill(entireProcessTree: true);
                }

                await Task.WhenAll(stdoutTask, stderrTask).WaitAsync(TimeSpan.FromSeconds(2), cancellationToken);
                return;
            }
            catch (OperationCanceledException)
            {
                if (!process.HasExited)
                {
                    process.Kill(entireProcessTree: true);
                }

                throw;
            }
        }
    }

    private static async Task PumpStreamAsync(Stream stream, Func<byte[], Task> onOutput, CancellationToken cancellationToken)
    {
        var buffer = new byte[4096];
        while (!cancellationToken.IsCancellationRequested)
        {
            var count = await stream.ReadAsync(buffer, 0, buffer.Length, cancellationToken);
            if (count <= 0)
            {
                break;
            }

            var chunk = new byte[count];
            Array.Copy(buffer, chunk, count);
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

    public async Task ResizeTerminalAsync(string containerId, int cols, int rows, CancellationToken cancellationToken)
    {
        try
        {
            await _dockerClient.Containers.ResizeContainerTtyAsync(containerId, new ContainerResizeParameters
            {
                Width = (uint)cols,
                Height = (uint)rows
            }, cancellationToken);
        }
        catch
        {
            // Best effort — container may have already exited
        }
    }
}

