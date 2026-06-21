using System.Text.RegularExpressions;
using QuizApp.Core.Domain;

namespace QuizApp.Core.Services;

public sealed class DockerWorkspaceGuidedProjectRunner : IGuidedProjectRunner
{
    private readonly IDockerCommandRunner _dockerRunner;

    public string Mode => "workspace";

    public DockerWorkspaceGuidedProjectRunner(IDockerCommandRunner dockerRunner)
    {
        _dockerRunner = dockerRunner;
    }

    public async Task<GuidedProjectRunResult> RunAsync(
        GuidedProjectRunRequest request,
        CancellationToken cancellationToken)
    {
        var project = request.Assessment.GuidedProject!;
        var session = request.Session;
        var checkResults = new List<GuidedProjectCheckResult>();

        using var workspaceDir = new TemporaryDirectory();

        try
        {
            await MaterializeFilesAsync(workspaceDir.Path, project, session.Files, cancellationToken);

            var buildResult = await RunBuildStageAsync(workspaceDir.Path, project, cancellationToken);
            
            if (!buildResult.Succeeded)
            {
                foreach (var check in project.RequiredChecks.Concat(project.BonusChecks))
                {
                    checkResults.Add(new GuidedProjectCheckResult(
                        check.Id,
                        check.Title,
                        project.RequiredChecks.Contains(check),
                        false,
                        null,
                        buildResult.Output,
                        null,
                        DateTimeOffset.UtcNow)
                    {
                        Build = buildResult,
                        FailureReason = "Build failed"
                    });
                }
                
                var sessionUpdatedFailed = session with
                {
                    CheckResults = checkResults,
                    UpdatedAt = DateTimeOffset.UtcNow
                };

                return new GuidedProjectRunResult(sessionUpdatedFailed, false);
            }

            foreach (var check in project.RequiredChecks)
            {
                checkResults.Add(await RunCheckAsync(workspaceDir.Path, project, session.Files, check, true, cancellationToken));
            }

            foreach (var check in project.BonusChecks)
            {
                checkResults.Add(await RunCheckAsync(workspaceDir.Path, project, session.Files, check, false, cancellationToken));
            }
        }
        catch (Exception ex)
        {
            return new GuidedProjectRunResult(session with
            {
                CheckResults = project.RequiredChecks.Concat(project.BonusChecks).Select(check => new GuidedProjectCheckResult(
                    check.Id,
                    check.Title,
                    project.RequiredChecks.Contains(check),
                    false,
                    null,
                    null,
                    ex.Message,
                    DateTimeOffset.UtcNow)).ToList(),
                UpdatedAt = DateTimeOffset.UtcNow
            }, false);
        }

        var allRequiredPassed = project.RequiredChecks.All(check => checkResults.Any(result =>
            result.Required && string.Equals(result.CheckId, check.Id, StringComparison.OrdinalIgnoreCase) && result.Passed));

        var updated = session with
        {
            CheckResults = checkResults,
            UpdatedAt = DateTimeOffset.UtcNow
        };

        return new GuidedProjectRunResult(updated, allRequiredPassed);
    }

    private async Task MaterializeFilesAsync(
        string rootPath,
        GuidedProjectDefinition project,
        IReadOnlyList<GuidedProjectFileState> files,
        CancellationToken cancellationToken)
    {
        var allFiles = project.Fixtures.Select(f => new { f.Path, f.Content })
            .Concat(files.Select(f => new { f.Path, f.Content }));

        foreach (var file in allFiles)
        {
            if (!IsSafeRelativePath(file.Path))
            {
                throw new InvalidOperationException($"Path '{file.Path}' is not safe.");
            }

            var fullPath = Path.GetFullPath(Path.Combine(rootPath, file.Path));
            if (!fullPath.StartsWith(rootPath, StringComparison.OrdinalIgnoreCase))
            {
                throw new InvalidOperationException($"Path escapes workspace root.");
            }

            var dir = Path.GetDirectoryName(fullPath);
            if (!string.IsNullOrEmpty(dir))
            {
                Directory.CreateDirectory(dir);
            }

            await File.WriteAllTextAsync(fullPath, file.Content, cancellationToken);
        }

        if (project.Workspace?.WritablePaths is not null)
        {
            foreach (var writablePath in project.Workspace.WritablePaths)
            {
                if (!IsSafeRelativePath(writablePath))
                {
                    throw new InvalidOperationException($"Writable path '{writablePath}' is not safe.");
                }

                var fullPath = Path.GetFullPath(Path.Combine(rootPath, writablePath));
                if (!fullPath.StartsWith(rootPath, StringComparison.OrdinalIgnoreCase))
                {
                    throw new InvalidOperationException($"Writable path escapes workspace root.");
                }

                Directory.CreateDirectory(fullPath);
            }
        }
    }

    private async Task<GuidedProjectBuildStageResult> RunBuildStageAsync(
        string workspaceDir,
        GuidedProjectDefinition project,
        CancellationToken cancellationToken)
    {
        if (project.Language == "python" || project.Language == "bash")
        {
            return new GuidedProjectBuildStageResult(true, $"{project.Language} projects do not require compilation.");
        }

        if (project.Workspace?.BuildProfile is null || project.Workspace.BuildProfile == "cpp20")
        {
            var files = Directory.GetFiles(workspaceDir, "*.cpp", SearchOption.AllDirectories)
                .Select(f => Path.GetRelativePath(workspaceDir, f).Replace('\\', '/'))
                .ToList();
            
            var args = new List<string> { "-std=c++20", "-Wall" };
            
            if (project.Diagnostics.Contains("memorySafety", StringComparer.OrdinalIgnoreCase))
            {
                args.Add("-fsanitize=address,undefined");
                args.Add("-fno-omit-frame-pointer");
                args.Add("-g");
            }
            
            args.AddRange(files);
            args.Add("-o");
            args.Add("program");

            var result = await _dockerRunner.RunAsync(
                image: "gcc:13.2",
                command: "g++",
                arguments: args,
                volumeMounts: new Dictionary<string, string> { { workspaceDir, "/workspace" } },
                workingDirectory: "/workspace",
                timeoutSeconds: 30,
                cancellationToken: cancellationToken);

            return new GuidedProjectBuildStageResult(result.Succeeded, result.Stdout + result.Stderr);
        }

        throw new NotSupportedException($"Build profile '{project.Workspace.BuildProfile}' not supported.");
    }

    private async Task<GuidedProjectCheckResult> RunCheckAsync(
        string workspaceDir,
        GuidedProjectDefinition project,
        IReadOnlyList<GuidedProjectFileState> submittedFiles,
        GuidedProjectCheckDefinition check,
        bool required,
        CancellationToken cancellationToken)
    {
        GuidedProjectProcessStageResult? processResult = null;
        List<GuidedProjectFileAssertionResult>? fileResults = null;
        List<GuidedProjectNetworkEventResult>? networkResults = null;
        bool runPassed = true;
        bool filesPassed = true;
        var isPython = project.Language == "python";
        var isBash = project.Language == "bash";
        var entryPoint = project.Workspace?.EntryPoint ?? (isPython ? "main.py" : (isBash ? "run.sh" : "main"));
        
        var command = isPython ? "python3" : (isBash ? "sh" : "./program");
        var arguments = check.Run?.Arguments?.ToList() ?? new List<string>();
        
        if (isPython || isBash)
        {
            arguments.Insert(0, entryPoint);
        }

        var runCommandStr = isPython ? $"python3 {entryPoint}" : (isBash ? $"sh {entryPoint}" : "./program");

        if (check.Run?.Scenario is not null)
        {
            var scenario = project.Scenarios.FirstOrDefault(s => string.Equals(s.Id, check.Run.Scenario, StringComparison.OrdinalIgnoreCase));
            if (scenario is not null && scenario.Type == "tcpConversation")
            {
                var scriptPath = Path.Combine(workspaceDir, "__scenario.py");
                var scriptContent = GenerateScenarioScript(scenario);
                await File.WriteAllTextAsync(scriptPath, scriptContent, cancellationToken);
                
                command = "/bin/bash";
                arguments = new List<string> { "-c" };
                
                if (string.Equals(scenario.LearnerRole, "server", StringComparison.OrdinalIgnoreCase))
                {
                    arguments.Add($"{runCommandStr} & sleep 1 && python3 __scenario.py");
                }
                else
                {
                    arguments.Add($"python3 __scenario.py & sleep 1 && {runCommandStr}");
                }
            }
        }

        var runImage = project.Workspace?.AllowedBaseImages?.FirstOrDefault() ?? (isPython ? "python:3.11" : (isBash ? "docker:dind" : "gcc:13.2"));
        var privileged = isBash && runImage.Contains("dind");

        if (privileged)
        {
            var finalCommand = "";
            if ((command == "sh" || command == "/bin/bash") && arguments.Count > 0 && arguments[0] == "-c")
            {
                finalCommand = arguments.Last();
            }
            else if (arguments.Count > 0)
            {
                finalCommand = $"{command} {string.Join(" ", arguments)}";
            }
            else
            {
                finalCommand = runCommandStr;
            }
                
            command = "sh";
            arguments = new List<string> { "-c", $"DOCKER_HOST=unix:///var/run/docker.sock dockerd-entrypoint.sh dockerd > /dev/null 2>&1 & i=0; until DOCKER_HOST=unix:///var/run/docker.sock docker info > /dev/null 2>&1; do i=$((i+1)); if [ $i -ge 30 ]; then echo 'dockerd did not start in time'; exit 1; fi; sleep 1; done && DOCKER_HOST=unix:///var/run/docker.sock {finalCommand}" };
        }

        var dindEnvironment = privileged
            ? new Dictionary<string, string> { { "DOCKER_HOST", "unix:///var/run/docker.sock" } }
            : null;
        var runTimeoutSeconds = privileged ? 60 : 15;

        if (check.Run is not null)
        {
            var dockerResult = await _dockerRunner.RunAsync(
                image: runImage,
                command: command,
                arguments: arguments,
                environment: dindEnvironment,
                standardInput: check.Run.Stdin,
                privileged: privileged,
                volumeMounts: new Dictionary<string, string> { { workspaceDir, "/workspace" } },
                workingDirectory: "/workspace",
                timeoutSeconds: runTimeoutSeconds,
                cancellationToken: cancellationToken);

            processResult = new GuidedProjectProcessStageResult(
                dockerResult.Succeeded,
                dockerResult.Stdout,
                dockerResult.Stderr,
                dockerResult.ExitCode);

            if (check.Run.Scenario is not null)
            {
                var scenarioJsonPath = Path.Combine(workspaceDir, "__scenario.json");
                if (File.Exists(scenarioJsonPath))
                {
                    try
                    {
                        var json = await File.ReadAllTextAsync(scenarioJsonPath, cancellationToken);
                        var events = System.Text.Json.JsonSerializer.Deserialize<List<Dictionary<string, object>>>(json);
                        if (events is not null)
                        {
                            networkResults = new List<GuidedProjectNetworkEventResult>();
                            foreach (var evt in events)
                            {
                                var type = evt.TryGetValue("type", out var t) ? t.ToString() : "unknown";
                                var evtPassed = evt.TryGetValue("passed", out var p) && p is System.Text.Json.JsonElement je && je.GetBoolean();
                                var expected = evt.TryGetValue("expected", out var exp) ? exp.ToString() : null;
                                var actual = evt.TryGetValue("actual", out var act) ? act.ToString() : null;
                                var error = evt.TryGetValue("error", out var err) ? err.ToString() : null;
                                networkResults.Add(new GuidedProjectNetworkEventResult(type!, evtPassed, expected, actual, error));
                                if (!evtPassed)
                                {
                                    runPassed = false;
                                }
                            }
                            // Store network events, but we need a property for it
                            // We will add it to the final result
                            // Note: C# 9+ allows assigning to init-only properties during object creation.
                        }
                    }
                    catch
                    {
                        runPassed = false;
                    }
                }
                else
                {
                    runPassed = false;
                }
            }

            if (check.Expect?.StdoutContains is not null)
            {
                foreach (var expected in check.Expect.StdoutContains)
                {
                    if (!dockerResult.Stdout.Contains(expected, StringComparison.Ordinal))
                    {
                        runPassed = false;
                        break;
                    }
                }
            }
            if (!dockerResult.Succeeded)
            {
                runPassed = false;
            }
        }

        if (check.Expect?.Files is not null)
        {
            fileResults = new List<GuidedProjectFileAssertionResult>();
            foreach (var fileExpect in check.Expect.Files)
            {
                var fullPath = Path.Combine(workspaceDir, fileExpect.Path);
                if (File.Exists(fullPath))
                {
                    var fileInfo = new FileInfo(fullPath);
                    string content;
                    if (fileInfo.Length > 1024 * 1024) // 1 MB limit
                    {
                        var buffer = new char[1024 * 1024];
                        using var reader = new StreamReader(fullPath);
                        await reader.ReadBlockAsync(buffer, 0, buffer.Length);
                        content = new string(buffer) + "\n...[truncated]";
                    }
                    else
                    {
                        content = await File.ReadAllTextAsync(fullPath, cancellationToken);
                    }
                    
                    var filePassed = true;
                    foreach (var contains in fileExpect.TextContains)
                    {
                        if (!content.Contains(contains, StringComparison.Ordinal))
                        {
                            filePassed = false;
                            break;
                        }
                    }
                    fileResults.Add(new GuidedProjectFileAssertionResult(fileExpect.Path, filePassed, content, null));
                    if (!filePassed) filesPassed = false;
                }
                else
                {
                    fileResults.Add(new GuidedProjectFileAssertionResult(fileExpect.Path, false, null, "File not found."));
                    filesPassed = false;
                }
            }
        }

        var passed = runPassed && filesPassed;
        var failureReason = !passed ? (runPassed ? "File expectations failed" : "Run expectations failed") : null;

        List<GuidedProjectDiagnosticFinding>? diagnosticFindings = null;
        if (project.Diagnostics.Contains("memorySafety", StringComparer.OrdinalIgnoreCase) && processResult?.Stderr is not null)
        {
            diagnosticFindings = new List<GuidedProjectDiagnosticFinding>();
            var stderr = processResult.Stderr;
            
            bool hasDiagnostics = false;

            if (stderr.Contains("heap-buffer-overflow", StringComparison.OrdinalIgnoreCase) || 
                stderr.Contains("stack-buffer-overflow", StringComparison.OrdinalIgnoreCase) ||
                stderr.Contains("global-buffer-overflow", StringComparison.OrdinalIgnoreCase))
            {
                diagnosticFindings.Add(new GuidedProjectDiagnosticFinding("memorySafety", "heap/stack out of bounds", null, null));
                hasDiagnostics = true;
            }
            if (stderr.Contains("heap-use-after-free", StringComparison.OrdinalIgnoreCase))
            {
                diagnosticFindings.Add(new GuidedProjectDiagnosticFinding("memorySafety", "use after free", null, null));
                hasDiagnostics = true;
            }
            if (stderr.Contains("double-free", StringComparison.OrdinalIgnoreCase) || stderr.Contains("attempting double-free", StringComparison.OrdinalIgnoreCase))
            {
                diagnosticFindings.Add(new GuidedProjectDiagnosticFinding("memorySafety", "double free", null, null));
                hasDiagnostics = true;
            }
            if (stderr.Contains("detected memory leaks", StringComparison.OrdinalIgnoreCase))
            {
                diagnosticFindings.Add(new GuidedProjectDiagnosticFinding("memorySafety", "memory leak", null, null));
                hasDiagnostics = true;
            }
            if (stderr.Contains("runtime error:", StringComparison.OrdinalIgnoreCase) || stderr.Contains("UndefinedBehaviorSanitizer", StringComparison.OrdinalIgnoreCase))
            {
                diagnosticFindings.Add(new GuidedProjectDiagnosticFinding("memorySafety", "undefined behavior", null, null));
                hasDiagnostics = true;
            }

            if (!hasDiagnostics && passed)
            {
                diagnosticFindings.Add(new GuidedProjectDiagnosticFinding("memorySafety", "clean run", null, null));
            }
        }

        return new GuidedProjectCheckResult(
            check.Id,
            check.Title,
            required,
            passed,
            processResult?.Stdout,
            null,
            processResult?.Stderr,
            DateTimeOffset.UtcNow)
        {
            Run = processResult,
            Files = fileResults,
            NetworkEvents = networkResults,
            Diagnostics = diagnosticFindings,
            FailureReason = failureReason
        };
    }

    private static bool IsSafeRelativePath(string path)
    {
        if (string.IsNullOrWhiteSpace(path)
            || Path.IsPathRooted(path)
            || path.Contains("..", StringComparison.Ordinal)
            || path.Contains('\\'))
        {
            return false;
        }

        return path.Split('/', StringSplitOptions.RemoveEmptyEntries)
            .All(part => part.Length > 0 && part.All(character => char.IsLetterOrDigit(character) || character is '-' or '_' or '.'));
    }

    private static string GenerateScenarioScript(GuidedProjectScenarioDefinition scenario)
    {
        var sb = new System.Text.StringBuilder();
        sb.AppendLine("import socket");
        sb.AppendLine("import time");
        sb.AppendLine("import sys");
        sb.AppendLine("import json");
        sb.AppendLine("results = []");
        sb.AppendLine("try:");
        sb.AppendLine("    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)");
        sb.AppendLine("    s.settimeout(5)");
        
        if (string.Equals(scenario.LearnerRole, "server", StringComparison.OrdinalIgnoreCase))
        {
            sb.AppendLine("    time.sleep(1) # wait for learner server to start");
            sb.AppendLine("    s.connect(('127.0.0.1', 8080))");
        }
        else
        {
            sb.AppendLine("    s.bind(('127.0.0.1', 8080))");
            sb.AppendLine("    s.listen(1)");
            sb.AppendLine("    conn, addr = s.accept()");
            sb.AppendLine("    conn.settimeout(5)");
            sb.AppendLine("    s = conn # use the accepted connection");
        }

        foreach (var evt in scenario.Events)
        {
            if (evt.Type == "connect")
            {
                sb.AppendLine("    results.append({\"type\": \"connect\", \"passed\": True})");
            }
            else if (evt.Type == "send" && evt.Text != null)
            {
                var text = evt.Text.Replace("\n", "\\n").Replace("\"", "\\\"");
                sb.AppendLine($"    s.sendall(b\"{text}\")");
                sb.AppendLine("    results.append({\"type\": \"send\", \"passed\": True})");
            }
            else if (evt.Type == "expect" && evt.Text != null)
            {
                var text = evt.Text.Replace("\n", "\\n").Replace("\"", "\\\"");
                sb.AppendLine("    data = s.recv(1024).decode('utf-8')");
                sb.AppendLine($"    if \"{text}\" in data:");
                sb.AppendLine($"        results.append({{\"type\": \"expect\", \"passed\": True, \"expected\": \"{text}\", \"actual\": data}})");
                sb.AppendLine("    else:");
                sb.AppendLine($"        results.append({{\"type\": \"expect\", \"passed\": False, \"expected\": \"{text}\", \"actual\": data}})");
            }
            else if (evt.Type == "disconnect")
            {
                sb.AppendLine("    s.close()");
                sb.AppendLine("    results.append({\"type\": \"disconnect\", \"passed\": True})");
            }
        }
        sb.AppendLine("except Exception as e:");
        sb.AppendLine("    results.append({\"type\": \"error\", \"passed\": False, \"error\": str(e)})");
        sb.AppendLine("finally:");
        sb.AppendLine("    with open('__scenario.json', 'w') as f:");
        sb.AppendLine("        json.dump(results, f)");
        
        return sb.ToString();
    }
}

public sealed class TemporaryDirectory : IDisposable
{
    public string Path { get; }

    public TemporaryDirectory()
    {
        Path = System.IO.Path.Combine(System.IO.Path.GetTempPath(), Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(Path);
    }

    public void Dispose()
    {
        try
        {
            if (Directory.Exists(Path))
            {
                Directory.Delete(Path, true);
            }
        }
        catch
        {
            // Ignore cleanup errors
        }
    }
}
