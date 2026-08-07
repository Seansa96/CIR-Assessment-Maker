namespace QuizApp.Infrastructure.CodeRunner;

public sealed class ManagedCodeRunnerOptions
{
    public const string SectionName = "ManagedCodeRunner";

    // The upstream image is pinned so a new pull cannot silently change the local runner contract.
    public string Image { get; init; } = "ghcr.io/engineer-man/piston@sha256:2f66b7456189c4d713aa986d98eccd0b6ee16d26c7ec5f21b30e942756fd127a";
    public string ContainerName { get; init; } = "cir-code-runner";
    public string VolumeName { get; init; } = "cir-code-runner-data";
    public int ReadinessTimeoutSeconds { get; init; } = 30;
    public int ProbeRetryMilliseconds { get; init; } = 1000;
    public int DockerLogTailLines { get; init; } = 80;
}
