using Microsoft.Extensions.Logging.Abstractions;
using QuizApp.Core.Services;
using QuizApp.Infrastructure.CodeRunner;
using System.Net;
using System.Text;
using System.Text.Json;

namespace QuizApp.Tests;

public sealed class ManagedCodeRunnerServiceTests
{
    [Fact]
    public async Task Fresh_runner_creates_named_volume_and_mounts_it_at_piston()
    {
        var docker = new FakeDockerClient(new[]
        {
            Result(1, "No such container"), Result(0), Result(0), Result(0), Result(1, "No such container")
        });

        await CreateService(docker).PrepareAsync(new[] { "cpp" });

        Assert.Contains(docker.Commands, command => command.SequenceEqual(new[] { "volume", "create", "cir-code-runner-data" }));
        Assert.Contains(docker.Commands, command => command.Contains("-v") && command.Contains("cir-code-runner-data:/piston"));
        Assert.Contains(docker.Commands, command => command.Contains("ghcr.io/engineer-man/piston@sha256:test"));
    }

    [Fact]
    public async Task Healthy_managed_runner_is_reused_without_recreation()
    {
        var healthy = Inspection("running", 0, managed: true, compatible: true);
        var docker = new FakeDockerClient(new[] { Result(0, healthy), Result(0, healthy) });

        await CreateService(docker).PrepareAsync(new[] { "cpp" });

        Assert.DoesNotContain(docker.Commands, command => command[0] == "rm");
        Assert.DoesNotContain(docker.Commands, command => command[0] == "run");
        Assert.DoesNotContain(docker.Commands, command => command[0] == "pull");
    }

    [Fact]
    public async Task Exited_managed_runner_is_replaced_but_volume_is_retained()
    {
        var exited = Inspection("exited", 1, managed: true, compatible: false);
        var docker = new FakeDockerClient(new[]
        {
            Result(0, exited), Result(0), Result(0), Result(0), Result(0), Result(1, "No such container")
        });

        await CreateService(docker).PrepareAsync(new[] { "cpp" });

        Assert.Contains(docker.Commands, command => command.Take(2).SequenceEqual(new[] { "rm", "-f" }));
        Assert.Contains(docker.Commands, command => command.SequenceEqual(new[] { "volume", "create", "cir-code-runner-data" }));
        Assert.DoesNotContain(docker.Commands, command => command[0] == "volume" && command.Contains("rm"));
    }

    [Fact]
    public async Task Unmanaged_named_container_is_not_removed()
    {
        var docker = new FakeDockerClient(new[] { Result(0, Inspection("exited", 1, managed: false, compatible: false)) });

        var status = await CreateService(docker).PrepareAsync(new[] { "cpp" });

        Assert.Equal("failed", status.State);
        Assert.Contains("not managed by CIR", status.Message);
        Assert.DoesNotContain(docker.Commands, command => command[0] == "rm");
    }

    [Fact]
    public async Task Readiness_failure_retains_probe_error_exit_status_and_container_logs()
    {
        var healthy = Inspection("running", 0, managed: true, compatible: true);
        var exited = Inspection("exited", 1, managed: true, compatible: true);
        var docker = new FakeDockerClient(new[] { Result(0, healthy), Result(0, exited), Result(0, "chown: cannot access '/piston': No such file or directory") });

        var status = await CreateService(docker).PrepareAsync(new[] { "cpp" });

        Assert.Equal("unavailable", status.State);
        Assert.Equal("exited", status.Diagnostics?.ContainerState);
        Assert.Equal(1, status.Diagnostics?.ContainerExitCode);
        Assert.NotNull(status.Diagnostics?.LastProbeError);
        Assert.Contains("cannot access '/piston'", status.Diagnostics?.RecentContainerLogs);
    }

    [Fact]
    public async Task Cpp_provisioning_uses_gcc_catalog_package_and_reports_ready_alias()
    {
        var healthy = Inspection("running", 0, managed: true, compatible: true);
        var docker = new FakeDockerClient(new[] { Result(0, healthy), Result(0, healthy) });
        var handler = new QueueHttpHandler(new[]
        {
            Json("[]"),
            Json("[{\"language\":\"gcc\",\"languageVersion\":\"10.2.0\",\"installed\":false}]"),
            Json("{\"language\":\"gcc\",\"version\":\"10.2.0\"}"),
            Json("[{\"language\":\"c++\",\"version\":\"10.2.0\",\"aliases\":[\"cpp\"]}]")
        });

        var status = await CreateService(docker, new HttpClient(handler)).PrepareAsync(new[] { "cpp" });

        Assert.Equal("ready", status.State);
        Assert.Contains("cpp", status.Languages);
        Assert.Contains(handler.RequestBodies, body => body.Contains("\"language\":\"gcc\"") && body.Contains("\"version\":\"10.2.0\""));
    }

    private static ManagedCodeRunnerService CreateService(FakeDockerClient docker, HttpClient? httpClient = null)
    {
        var options = new ManagedCodeRunnerOptions
        {
            Image = "ghcr.io/engineer-man/piston@sha256:test",
            ReadinessTimeoutSeconds = 0,
            ProbeRetryMilliseconds = 1,
            DockerLogTailLines = 5
        };
        return new ManagedCodeRunnerService(
            docker,
            options,
            NullLogger<ManagedCodeRunnerService>.Instance,
            httpClient ?? new HttpClient(new QueueHttpHandler(Array.Empty<HttpResponseMessage>())));
    }

    private static CodeRunnerDockerResult Result(int exitCode, string output = "") => new(exitCode, output);

    private static string Inspection(string state, int exitCode, bool managed, bool compatible)
    {
        var image = compatible ? "ghcr.io/engineer-man/piston@sha256:test" : "old-image";
        return JsonSerializer.Serialize(new
        {
            State = new { Status = state, ExitCode = exitCode, StartedAt = "2026-01-01T00:00:00Z", FinishedAt = "2026-01-01T00:01:00Z" },
            Config = new { Image = image, Labels = managed ? new Dictionary<string, string> { ["cir.managed-code-runner"] = "true" } : new Dictionary<string, string> { ["other"] = "true" } },
            Mounts = new[] { new { Type = "volume", Name = "cir-code-runner-data", Destination = "/piston" } },
            NetworkSettings = new { Ports = new Dictionary<string, object> { ["2000/tcp"] = new[] { new { HostPort = "2000" } } } }
        });
    }

    private sealed class FakeDockerClient(IEnumerable<CodeRunnerDockerResult> results) : ICodeRunnerDockerClient
    {
        private readonly Queue<CodeRunnerDockerResult> results = new(results);
        public List<IReadOnlyList<string>> Commands { get; } = new();

        public Task<CodeRunnerDockerResult> RunAsync(IReadOnlyList<string> arguments, CancellationToken cancellationToken = default)
        {
            Commands.Add(arguments);
            return Task.FromResult(results.Count > 0 ? results.Dequeue() : Result(1, "Unexpected docker command"));
        }
    }

    private sealed class QueueHttpHandler(IEnumerable<HttpResponseMessage> responses) : HttpMessageHandler
    {
        private readonly Queue<HttpResponseMessage> responses = new(responses);
        public List<string> RequestBodies { get; } = new();

        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            if (request.Content is not null) RequestBodies.Add(await request.Content.ReadAsStringAsync(cancellationToken));
            return responses.Count > 0 ? responses.Dequeue() : new HttpResponseMessage(HttpStatusCode.InternalServerError);
        }
    }

    private static HttpResponseMessage Json(string content) => new(HttpStatusCode.OK) { Content = new StringContent(content, Encoding.UTF8, "application/json") };
}
