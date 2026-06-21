using System.Threading.Tasks;
using Xunit;
using QuizApp.Core.Services;
using QuizApp.Core.Domain;
using System.Collections.Generic;
using System.Threading;
using System.IO;
using System;

namespace QuizApp.Tests;

public class DockerWorkspaceGuidedProjectRunnerTests
{
    private sealed class RealDockerRunner : IDockerCommandRunner
    {
        public async Task<DockerCommandResult> RunAsync(
            string image,
            string command,
            IReadOnlyList<string> arguments,
            IReadOnlyDictionary<string, string>? environment = null,
            IReadOnlyDictionary<string, string>? volumeMounts = null,
            string? workingDirectory = null,
            string? standardInput = null,
            bool privileged = false,
            int timeoutSeconds = 30,
            CancellationToken cancellationToken = default)
        {
            var process = new System.Diagnostics.Process();
            process.StartInfo.FileName = "docker";
            process.StartInfo.ArgumentList.Add("run");
            process.StartInfo.ArgumentList.Add("--rm");
            
            if (privileged)
            {
                process.StartInfo.ArgumentList.Add("--privileged");
            }

            if (volumeMounts != null)
            {
                foreach (var mount in volumeMounts)
                {
                    process.StartInfo.ArgumentList.Add("-v");
                    process.StartInfo.ArgumentList.Add($"{mount.Key}:{mount.Value}");
                }
            }
            if (workingDirectory != null)
            {
                process.StartInfo.ArgumentList.Add("-w");
                process.StartInfo.ArgumentList.Add(workingDirectory);
            }
            
            process.StartInfo.ArgumentList.Add(image);
            process.StartInfo.ArgumentList.Add(command);
            foreach (var arg in arguments)
            {
                process.StartInfo.ArgumentList.Add(arg);
            }

            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.RedirectStandardError = true;
            
            process.Start();
            
            var stdoutTask = process.StandardOutput.ReadToEndAsync(cancellationToken);
            var stderrTask = process.StandardError.ReadToEndAsync(cancellationToken);
            
            await process.WaitForExitAsync(cancellationToken);
            
            var stdout = await stdoutTask;
            var stderr = await stderrTask;

            return new DockerCommandResult(process.ExitCode == 0, process.ExitCode, stdout, stderr);
        }
    }

    [Fact]
    public async Task CanRunTcpConversationScenario()
    {
        // Require docker in PATH
        try { System.Diagnostics.Process.Start(new System.Diagnostics.ProcessStartInfo { FileName = "docker", Arguments = "version", RedirectStandardOutput = true }).WaitForExit(); }
        catch { return; } // skip if no docker

        var runner = new DockerWorkspaceGuidedProjectRunner(new RealDockerRunner());

        var project = new GuidedProjectDefinition(
            "cpp",
            "console",
            "workspace",
            "Build a server",
            new GuidedProjectWorkspaceDefinition("cpp20", null, null, new[] { "server.cpp" }, Array.Empty<string>(), Array.Empty<string>(), new[] { "gcc:13.2" }),
            new List<GuidedProjectFileDefinition>(),
            new List<GuidedProjectFixtureDefinition>(),
            new List<GuidedProjectScenarioDefinition>
            {
                new GuidedProjectScenarioDefinition(
                    "greeting-round-trip",
                    "tcpConversation",
                    "server",
                    new List<GuidedProjectNetworkEventDefinition>
                    {
                        new GuidedProjectNetworkEventDefinition("connect", "client-1", null, null),
                        new GuidedProjectNetworkEventDefinition("expect", null, "learner", "HELLO\n"),
                        new GuidedProjectNetworkEventDefinition("send", null, "client-1", "WELCOME\n"),
                        new GuidedProjectNetworkEventDefinition("disconnect", "client-1", null, null)
                    })
            },
            new List<string>(),
            new List<GuidedProjectCheckDefinition>
            {
                new GuidedProjectCheckDefinition(
                    "reads-file",
                    "Network test",
                    "",
                    null,
                    null,
                    new GuidedProjectCheckRunDefinition(new List<string>(), null, "greeting-round-trip"),
                    null)
            },
            new List<GuidedProjectCheckDefinition>()
        );

        // A simple C++ server that listens on 8080, sends HELLO\n, and waits for WELCOME\n
        var serverCpp = @"
#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <cstring>

int main() {
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt));
    
    struct sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(8080);
    
    bind(server_fd, (struct sockaddr*)&address, sizeof(address));
    listen(server_fd, 3);
    
    int new_socket = accept(server_fd, nullptr, nullptr);
    const char* hello = ""HELLO\n"";
    send(new_socket, hello, strlen(hello), 0);
    
    char buffer[1024] = {0};
    read(new_socket, buffer, 1024);
    
    close(new_socket);
    close(server_fd);
    return 0;
}
";
        var session = new GuidedProjectSession("attempt-1", "assessment-1", new List<GuidedProjectFileState>
        {
            new GuidedProjectFileState("server.cpp", serverCpp, false)
        }, new List<GuidedProjectCheckResult>(), DateTimeOffset.UtcNow);

        var assessment = new AssessmentDefinition(
            1,
            "assessment-1",
            "Test",
            AssessmentType.GuidedProject,
            "cat-1",
            new List<string>(),
            AssessmentMode.Practice,
            false,
            null,
            null,
            null,
            new List<QuestionDefinition>())
        {
            GuidedProject = project
        };
        var settings = new AppSettings(1, AssessmentMode.Practice, QuestionOrderMode.Static, 10, 20, null, null, false);
        var request = new GuidedProjectRunRequest(session, assessment, settings);
        var result = await runner.RunAsync(request, CancellationToken.None);

        Assert.True(result.AllRequiredPassed);
        Assert.Single(result.Session.CheckResults);
        var checkResult = result.Session.CheckResults[0];
        Assert.True(checkResult.Passed);
        Assert.NotNull(checkResult.NetworkEvents);
        Assert.Equal(4, checkResult.NetworkEvents.Count);
        Assert.True(checkResult.NetworkEvents[0].Passed);
        Assert.True(checkResult.NetworkEvents[1].Passed);
        Assert.True(checkResult.NetworkEvents[2].Passed);
        Assert.True(checkResult.NetworkEvents[3].Passed);
    }
}
