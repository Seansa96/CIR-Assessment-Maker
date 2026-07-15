using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;
using Docker.DotNet;
using Docker.DotNet.Models;

namespace DockerApiTest
{
    class Program
    {
        static async Task Main(string[] args)
        {
            var attemptId = "test-" + Guid.NewGuid().ToString("N");
            var image = "mcr.microsoft.com/powershell:latest";
            var tempDir = Path.Combine(Path.GetTempPath(), "cir_sandbox", attemptId);
            Directory.CreateDirectory(tempDir);
            await File.WriteAllTextAsync(Path.Combine(tempDir, "test.txt"), "Hello from bind mount");

            using var dockerClient = new DockerClientConfiguration().CreateClient();
            var cts = new CancellationTokenSource(TimeSpan.FromSeconds(10));
            var ct = cts.Token;

            try
            {
                var hostConfig = new HostConfig
                {
                    ReadonlyRootfs = false,
                    AutoRemove = true,
                    Binds = new[] { $"{tempDir}:/workspace" }
                };

                // Split command exactly like SandboxService does
                var commandStr = "pwsh -NoExit -Command \"Write-Host 'Hello from inside'; Get-Content /workspace/test.txt; Start-Sleep -Seconds 2\"";
                var cmd = SplitCommand(commandStr);

                Console.WriteLine($"Starting container with command: {string.Join(" | ", cmd)}");

                var response = await dockerClient.Containers.CreateContainerAsync(new CreateContainerParameters
                {
                    Image = image,
                    Tty = true,
                    AttachStdin = true,
                    AttachStdout = true,
                    AttachStderr = true,
                    OpenStdin = true,
                    Cmd = cmd,
                    HostConfig = hostConfig
                }, ct);

                Console.WriteLine($"Container created: {response.ID}");
                await dockerClient.Containers.StartContainerAsync(response.ID, new ContainerStartParameters(), ct);
                Console.WriteLine("Container started successfully!");

                var outputLog = new System.Text.StringBuilder();
                using var stream = await dockerClient.Containers.AttachContainerAsync(
                    response.ID,
                    true,
                    new ContainerAttachParameters
                    {
                        Stream = true,
                        Stdin = true,
                        Stdout = true,
                        Stderr = true
                    }, ct);

                var buffer = new byte[4096];
                while (!ct.IsCancellationRequested)
                {
                    var result = await stream.ReadOutputAsync(buffer, 0, buffer.Length, ct);
                    if (result.EOF) break;
                    var str = System.Text.Encoding.UTF8.GetString(buffer, 0, result.Count);
                    Console.Write(str);
                }

                await dockerClient.Containers.StopContainerAsync(response.ID, new ContainerStopParameters { WaitBeforeKillSeconds = 1 }, CancellationToken.None);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\n--- EXCEPTION ---");
                Console.WriteLine(ex.ToString());
            }
            finally
            {
                if (Directory.Exists(tempDir)) Directory.Delete(tempDir, true);
            }
        }

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
    }
}
