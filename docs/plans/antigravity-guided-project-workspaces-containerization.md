# Antigravity Implementation Plan: Guided Project Workspaces and Containerization Labs

## Status

- **Audience:** Antigravity IDE agent
- **Project:** CIR Assessment Maker
- **Plan type:** Incremental implementation handoff
- **Primary objective:** Make Guided Projects operate as real, resumable, isolated project workspaces
- **Secondary objective:** Add a safe Containerization learning category centered on Docker fundamentals and small-scale orchestration
- **Current branch at review:** `main`

Before implementation, read:

- `AGENTS.md`
- `GEMINI.md`
- `docs/agent-coexistence.md`
- `planned-features.md`, especially **Guided Project Expansion** and **Container And Infrastructure Learning**
- `docs/plans/antigravity-code-editor-completion-guided-project-workspaces.md`
- `backend/src/QuizApp.Core/Services/GuidedProjectService.cs`
- `backend/src/QuizApp.Core/Domain/AssessmentModels.cs`
- `backend/src/QuizApp.Infrastructure/Files/FileGuidedProjectSessionRepository.cs`
- `backend/src/QuizApp.Infrastructure/CodeRunner/PistonCodeRunnerClient.cs`
- the Guided Project renderer in `frontend/src/pages/index.astro`
- `frontend/src/scripts/codeEditor.ts`
- existing C++ Guided Project YAML files

Check `git status --short` before editing. The reviewed worktree contains unrelated user and agent changes. Do not revert, normalize, stage, or claim those changes.

## Execution Constraints

- Prioritize a working vertical slice over a broad rewrite.
- Preserve all existing Guided Projects through the current runner.
- Do not rewrite existing assessment YAML automatically.
- Do not expose arbitrary shell commands, Docker commands, Docker sockets, host paths, or unrestricted networking to learners.
- Do not mount the repository root or user profile into execution containers.
- Do not use `docker system prune`, broad container deletion, or global network/volume cleanup.
- Do not add a raw browser terminal in the first version.
- Do not require persistent learner containers.
- Do not add cloud deployment, Kubernetes, Terraform, AWS labs, or multi-user permissions in this slice.
- Keep ordinary code questions on the current Piston adapter.
- Keep Guided Projects schema-authored. Do not add creator UI support.
- Add focused tests only. Run each build/test command once after implementation.
- Preserve the current app-owned Guided Project session files until a later retention migration is explicitly requested.

## Current-State Findings

### What Already Works

- `guidedProject` is a first-class instructional assessment type.
- A project can define multiple editable and read-only files.
- The frontend provides file tabs, a shared CodeMirror 6 editor, save progress, Run Checks, required/bonus check status, completion, pause/resume, and quit.
- CodeMirror already provides basic Python/C++ keyword, snippet, active-file, and cross-file completion.
- Project source state is stored in `data/project-sessions/{attemptId}.json`.
- Resuming a session restores project file contents.
- Completion requires all required checks and deletes the project-session file.
- Existing projects are unscored and excluded from grade-log commits.
- Piston supplies bounded compile/run execution for the current harness.

### What The Current Runner Actually Does

`GuidedProjectService` currently:

- accepts only `language: cpp`
- selects every `.h`, `.hpp`, and `.cpp`-like file
- strips `#pragma once` and project-local quoted includes
- concatenates all project content into one generated `main.cpp`
- appends one hidden `testCode` block
- sends that single file to Piston once per check
- passes a check by looking for configured strings in stdout

This is a compatibility harness, not a real project workspace.

### Material Gaps

The current implementation cannot reliably support:

- separate translation units
- real header/include resolution
- compilation and linking across files
- project directory structure
- fixture files
- generated output files
- stdin scenarios
- process lifecycle or terminal-like interactions
- socket client/listener scenarios
- memory diagnostics
- Python Guided Projects
- build profiles
- structured file, network, or diagnostic assertions
- Dockerfile or Compose labs

The existing `cpp-file-io-reader-guided-project` currently promises files such as `input/message.txt`, but the runner never materializes those files. Fix this mismatch as part of the first workspace slice.

## Target Architecture

Keep `GuidedProjectService` as the lifecycle coordinator, but move execution behind a runner abstraction.

```csharp
public interface IGuidedProjectRunner
{
    string Mode { get; }

    Task<GuidedProjectRunResult> RunAsync(
        GuidedProjectRunRequest request,
        CancellationToken cancellationToken);
}
```

Provide:

- `LegacyHarnessGuidedProjectRunner`
  - wraps the current C++ concatenation/Piston behavior
  - remains the default for old YAML
- `DockerWorkspaceGuidedProjectRunner`
  - materializes real files into a disposable workspace
  - uses allowlisted app-owned build/run profiles
  - returns structured build, run, file, network, and diagnostic results

Add a selector/resolver based on `guidedProject.runnerMode`.

Do not make `ICodeRunnerClient` responsible for project orchestration. Piston remains appropriate for code questions and the legacy harness, while the workspace runner owns filesystem and multi-process behavior.

## Additive Guided Project Schema

Add optional fields while preserving the current schema:

```yaml
guidedProject:
  language: cpp
  projectKind: code
  runnerMode: workspace

  instructions: |
    Build the requested project.

  workspace:
    buildProfile: cpp20
    entryPoint: app
    sourceGlobs:
      - src/*.cpp
    includePaths:
      - include
    writablePaths:
      - output

  files: []
  fixtures: []
  scenarios: []
  diagnostics: []
  requiredChecks: []
  bonusChecks: []
```

Defaults:

- missing `runnerMode` -> `legacyHarness`
- missing `projectKind` -> `code`
- old checks using `testCode` and `expectedOutputContains` remain valid for `legacyHarness`

Initial values:

- `runnerMode`: `legacyHarness`, `workspace`
- `projectKind`: `code`, `containerization`
- code workspace languages: `cpp`, then `python`
- build profiles: `cpp17`, `cpp20`, `python3`

Assessment YAML must never provide an arbitrary build or shell command. It selects an allowlisted profile and supplies declarative inputs/assertions.

## Workspace Domain Model

Add focused domain records for:

- workspace configuration
- fixture files
- build profile selection
- run scenarios
- stdin and arguments
- expected stdout/stderr/exit code
- expected generated files
- memory diagnostic profile
- network conversation events
- structured build/run/check results

Suggested result shape:

```csharp
GuidedProjectCheckResult
{
    string CheckId;
    bool Passed;
    BuildStageResult Build;
    ProcessStageResult? Run;
    IReadOnlyList<FileAssertionResult> Files;
    IReadOnlyList<NetworkEventResult> NetworkEvents;
    IReadOnlyList<DiagnosticFinding> Diagnostics;
    string? FailureReason;
}
```

Keep existing result properties available or map them for frontend compatibility during migration.

## Disposable Workspace Lifecycle

For each Run Checks request:

1. Generate a random run ID beneath an app-owned temporary execution root.
2. Validate and materialize the saved learner files.
3. Materialize read-only fixtures and hidden check files.
4. Generate build configuration from an allowlisted profile.
5. Start disposable, resource-limited Docker resources.
6. Compile/link or validate the project.
7. Run the declared scenario.
8. Capture bounded structured output and assertions.
9. Stop and remove only resources labeled for that run.
10. Delete the temporary run directory in `finally`.

Use labels such as:

```txt
cir.managed=true
cir.attempt=<attempt-id>
cir.run=<run-id>
```

Cleanup must target the exact run ID or those labels only.

The learner's durable state remains app-owned source/session data. Containers and build artifacts are disposable. On resume, the app rematerializes the saved files into a new workspace.

## Docker Adapter

Introduce an infrastructure boundary such as:

```csharp
public interface IDockerCommandRunner
{
    Task<DockerCommandResult> RunAsync(
        IReadOnlyList<string> arguments,
        TimeSpan timeout,
        CancellationToken cancellationToken);
}
```

V1 may invoke the installed Docker CLI with `ProcessStartInfo.ArgumentList` and `UseShellExecute = false`.

Rules:

- construct every command from backend-owned operations
- never concatenate learner/authored input into a shell command
- never invoke through `cmd /c`, PowerShell script text, Bash, or a shell
- validate resource names, image IDs, file paths, ports, and environment variable names
- capture bounded stdout/stderr
- enforce cancellation and hard timeouts
- make the adapter mockable for focused tests

A future Docker Engine SDK can replace this adapter without changing Core.

## Path And Resource Safety

Reject:

- absolute paths
- drive-qualified paths
- UNC paths
- `..` traversal
- null characters
- device paths
- symlinks/reparse points that leave the workspace
- duplicate normalized paths

Enforce:

- per-file size limits
- aggregate workspace size limits
- generated file count/size limits
- CPU, memory, PID, process, output, and wall-clock limits
- no privileged mode
- dropped capabilities where practical
- no host networking
- no repository/user-profile mounts
- no Docker socket mount
- no external internet by default

## Phase 1: Real C++ Workspace Vertical Slice

Implement this before containerization teaching content.

### Build Behavior

- preserve authored directories and filenames
- compile `.cpp` translation units separately
- preserve `.h/.hpp` includes
- apply only backend-owned compiler flags
- link one executable
- report diagnostics with original file and line information

Initial C++ profile:

```txt
g++ -std=c++20 -Wall -Wextra -pedantic
```

The exact command is generated by the runner, not YAML.

### First Migration Fixture

Create or migrate one small two-file C++ Guided Project to `runnerMode: workspace`.

It should prove:

- a header is included normally
- a `.cpp` implementation is compiled separately
- hidden checks link against learner code
- diagnostics name the real file
- an old legacy project still runs unchanged

Do not migrate all projects until this vertical slice passes.

## Phase 2: File I/O

Add read-only fixtures and output assertions:

```yaml
fixtures:
  - path: input/message.txt
    content: |
      This is a secret message.
      You have successfully read the file!
    readOnly: true

workspace:
  writablePaths:
    - output

requiredChecks:
  - id: reads-file
    run:
      arguments: []
      stdin: ''
    expect:
      stdoutContains:
        - This is a secret message.
      files:
        - path: output/summary.txt
          textContains:
            - complete
```

Implement:

- fixture materialization
- working-directory control
- bounded text-file previews
- exact/contains file assertions
- clear missing-file and permission feedback

Then correct `cpp-file-io-reader-guided-project` so its authored contract matches actual execution.

## Phase 3: Memory Diagnostics

Add allowlisted C++ diagnostic profiles:

- AddressSanitizer
- UndefinedBehaviorSanitizer
- LeakSanitizer where supported by the selected runner image

YAML selects a profile, not flags:

```yaml
diagnostics:
  - memorySafety
```

Return actionable categories:

- heap/stack out of bounds
- use after free
- double free
- memory leak
- undefined behavior
- clean run

Do not enable debugger attachment, `ptrace`, privileged mode, or raw host memory access.

## Phase 4: Deterministic Network Scenarios

Support instructional networking without unrestricted networking.

V1:

- TCP only
- one learner client or one learner listener
- line-oriented UTF-8 messages
- app-controlled peer
- internal Docker network
- no host-published ports
- no external internet
- deterministic connect/send/expect/disconnect events

Example:

```yaml
scenarios:
  - id: greeting-round-trip
    type: tcpConversation
    learnerRole: server
    events:
      - connect:
          peer: client-1
      - send:
          from: client-1
          text: "HELLO\n"
      - expect:
          from: learner
          text: "WELCOME\n"
      - disconnect:
          peer: client-1
```

Return a timestamped transcript and name the failed event. Do not expose raw network namespace controls to assessment YAML.

## Phase 5: Python Workspaces

After C++ workspace behavior is stable:

- preserve Python package directories
- use a declared entry module/script
- set the workspace as the import root
- support sibling imports
- reuse fixture, file assertion, stdin, and network scenario infrastructure

Do not permit package installation in V1. Runner images contain an approved standard-library environment.

## Guided Project Frontend Upgrade

Keep CodeMirror 6 and the current general layout.

Add:

- a compact file tree that preserves directories
- clear editable/read-only/fixture/generated distinctions
- stable per-file editor state across tab switches
- build/run status stages
- compiler diagnostics grouped by file
- clickable file/line navigation where practical
- bounded stdout and stderr panes
- generated-file preview pane
- network scenario transcript
- memory diagnostic summary
- runner capability/unavailable message

Do not add a raw terminal in V1.

For stdin-based exercises, use a bounded textarea or authored scenario. For networking, show the app-controlled transcript. The learner continues to press one Run Checks button while the app handles compilation, linking, process startup, and cleanup.

## Session And Lifecycle Behavior

Keep `IGuidedProjectSessionRepository` as the durable learner-source boundary for now.

Persist:

- editable file contents
- active file path if useful
- latest bounded check summary
- updated timestamp

Do not persist:

- containers
- networks
- build directories
- compiled binaries
- generated artifacts beyond bounded result previews

Behavior:

- Save and Quit preserves app-owned source state.
- Resume rematerializes a new execution workspace.
- Complete Project removes the project-session source state.
- Delete Attempt removes session state and any exact labeled runtime resources.
- Startup may run a targeted stale-resource cleanup for `cir.managed=true` resources older than a configured threshold.

Never perform global Docker cleanup.

## Containerization Category

Add:

```yaml
id: containerization
title: Containerization
description: Build, run, connect, persist, and coordinate small containerized applications safely.
```

Recommended subcategories:

- `containerization-foundations`
  - images, containers, layers, registries, isolation
- `docker-images-dockerfiles`
  - Dockerfile instructions, build context, caching, `.dockerignore`
- `docker-container-lifecycle`
  - create, run, stop, remove, inspect, logs, exit codes
- `docker-storage-volumes`
  - writable layers, named volumes, bind-mount concepts, persistence
- `docker-networking`
  - bridge networks, service names, ports, internal communication
- `docker-compose-orchestration`
  - services, dependencies, health checks, environment, volumes, networks
- `docker-security-troubleshooting`
  - non-root users, secrets concepts, least privilege, logs, common failures

Add an area:

```yaml
id: containerization-and-orchestration
title: Containerization and Orchestration
description: Packaging applications into isolated containers and coordinating small multi-service systems.
categoryIds:
  - containerization
subcategoryIds:
  - containerization-foundations
  - docker-images-dockerfiles
  - docker-container-lifecycle
  - docker-storage-volumes
  - docker-networking
  - docker-compose-orchestration
  - docker-security-troubleshooting
```

Use navigation metadata consistently:

- Concept Lessons and Worked Examples -> Learn
- Recall Drills -> Recall
- quizzes -> Practice or Evaluate
- Docker labs -> Apply / Guided Project

## Containerization Guided Project Model

Use `assessmentType: guidedProject`; do not create another assessment type.

Example:

```yaml
assessmentType: guidedProject
guidedProject:
  language: docker
  projectKind: containerization
  runnerMode: workspace
  workspace:
    labProfile: dockerCompose
    allowedBaseImages:
      - python:3.12-alpine
      - nginx:alpine
  files:
    - path: Dockerfile
      readOnly: false
      content: |
        # TODO
    - path: compose.yaml
      readOnly: false
      content: |
        services: {}
  requiredChecks: []
```

Treat learner Dockerfile and Compose YAML as data to validate and run through a constrained lab service. Do not give the learner a Docker CLI or shell.

## Container Lab Runner

Add a specialized backend service behind the Guided Project runner:

```csharp
public interface IContainerLabRunner
{
    Task<ContainerLabResult> RunAsync(
        ContainerLabRequest request,
        CancellationToken cancellationToken);
}
```

Allowed operations are backend-owned:

- validate Dockerfile
- validate Compose structure
- build an image from the isolated lab context
- create/start/stop/remove labeled containers
- inspect status and health
- read bounded logs
- create a labeled internal network
- create a labeled named volume
- run an app-owned probe/check container
- recreate a service to test volume persistence
- execute a bounded, predefined health probe

Forbidden:

- arbitrary Docker CLI input
- privileged containers
- host networking
- host PID/IPC namespaces
- Docker socket mounts
- arbitrary bind mounts
- arbitrary registry pulls
- arbitrary published host ports
- unrestricted Compose keys such as `privileged`, `devices`, `volumes` with host paths, or custom runtime controls

Parse Dockerfile and Compose content with structured parsers where practical. Reject unsupported instructions/options with clear learner feedback.

## Image Policy

V1 should use a small server-configured allowlist of pre-pulled, preferably digest-pinned images.

Suggested teaching images:

- `alpine`
- `busybox`
- `nginx:alpine`
- `python:3.12-alpine`

Do not permit arbitrary image names from assessment or learner input unless an administrator updates the server-side allowlist.

If an image is missing, return a clear setup error. Do not silently pull from the internet during a learner run.

## Small-Scale Orchestration Scope

Support Docker Compose concepts without attempting production orchestration.

V1 Compose support:

- two or three services
- one internal network
- named volumes
- environment variables from safe authored values
- service-to-service DNS
- health checks from an allowlisted form
- startup dependency concepts
- logs and exit status
- no replicas/scaling
- no Swarm/Kubernetes
- no external secrets manager

Generate a unique Compose project name from the attempt and run IDs. Apply a backend-generated override that enforces labels, resource limits, network isolation, and safe mounts.

## Initial Containerization Learning Path

Implement content only after the runner vertical slice works.

1. **Concept Lesson: Images, Containers, and Layers**
   - image versus running container
   - immutable image layers
   - writable container layer
   - build context and registry concepts
2. **Recall Drill: Docker Vocabulary and Lifecycle**
   - image, container, volume, network, build, run, stop, remove, logs, inspect
3. **Worked Example: Read and Improve a Dockerfile**
   - `FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD`
   - layer caching and `.dockerignore`
   - non-root user concept
4. **Guided Project: Dockerized Static Site**
   - learner edits Dockerfile
   - app supplies site files
   - checks build success, expected files, non-root/default process where applicable, and HTTP response through an internal probe
5. **Concept Lesson/Worked Example: Volumes and Persistence**
   - container writable layer versus named volume
6. **Guided Project: Persistent Counter or Log**
   - app recreates the container and verifies data persists in a labeled named volume
7. **Concept Lesson/Worked Example: Docker Networking**
   - bridge network, service DNS, container port versus published port
8. **Guided Project: Two-Service Greeting**
   - learner completes a Compose file for a client and server
   - internal probe verifies service-name communication
9. **Concept Lesson/Worked Example: Compose**
   - services, networks, volumes, health checks, dependency readiness
10. **Capstone Guided Project: Small Orchestrated Application**
    - two services, one named volume, health checks, internal communication, and logs

The first production vertical slice should be **Dockerized Static Site**. Add the two-service Compose lab only after single-container build/run/cleanup is reliable.

## Dockerized Static Site Acceptance Fixture

The app supplies read-only HTML/CSS content. The learner edits:

- `Dockerfile`
- optional `.dockerignore`

Required checks:

- Dockerfile parses within the supported subset.
- Image builds from an approved base image.
- Container starts under resource limits.
- Internal HTTP probe receives status `200`.
- Response contains a known page marker.
- Container logs remain bounded.
- Container and temporary image/resource labels are cleaned after the run.

This fixture proves the Containerization category without requiring Compose, external ports, or arbitrary commands.

## Shared/LAN Hosting Warning

Docker-backed learner execution is host-adjacent infrastructure.

If this feature is later enabled on the LAN/server branch:

- never expose the Docker API to the browser
- require server-side authorization for lab endpoints
- apply per-user/per-attempt concurrency and rate limits
- default container labs to disabled until explicitly enabled by the host
- do not treat one shared access token as sufficient protection for unrestricted container execution

The local-only build may enable labs through configuration after Docker availability is confirmed.

## Configuration And Health

Add settings such as:

```json
{
  "GuidedProjectWorkspace": {
    "Enabled": false,
    "DockerExecutable": "docker",
    "ExecutionRoot": "data/runtime/guided-project-runs",
    "MaxConcurrentRuns": 2,
    "BuildTimeoutSeconds": 60,
    "RunTimeoutSeconds": 15,
    "MemoryMb": 256,
    "CpuCount": 1,
    "PidsLimit": 64,
    "MaxOutputBytes": 65536
  },
  "ContainerLabs": {
    "Enabled": false,
    "AllowedImages": []
  }
}
```

Do not put machine-specific values into authored assessment YAML.

Add a lightweight capability endpoint or include capability state in settings:

- unavailable
- Docker command missing
- Docker daemon unavailable
- workspace runner ready
- container labs disabled
- container labs ready

Frontend should disable Run Checks with a useful setup message rather than crash.

## Validation

Extend assessment validation for:

- known runner mode/project kind
- runner-mode compatibility
- supported workspace language/profile
- normalized unique file and fixture paths
- no path traversal
- required entry point/profile fields
- unique check/scenario IDs
- valid writable paths
- valid assertions
- bounded scenario/event counts
- known network event types
- known diagnostic profiles
- containerization project requires the container lab profile
- Dockerfile/Compose files use expected paths
- allowed base images are server policy, not trusted from YAML alone

Legacy projects must continue validating under the existing rules.

## Focused Test Plan

### Unit Tests

- old Guided Project maps to `legacyHarness`
- workspace schema round-trips through YAML/JSON
- path validator rejects absolute, traversal, duplicate-normalized, and device paths
- runner selector preserves legacy behavior
- Docker argument builder does not use a shell
- cleanup targets only exact labeled resources
- unsupported Dockerfile/Compose fields are rejected

### Workspace Integration Tests

Run only when Docker is available; otherwise skip with a clear reason:

- two-file C++ project compiles and links
- diagnostics report the authored filename
- fixture file is readable
- expected generated file is inspected
- one intentional memory error is detected
- one TCP request/response scenario passes on an internal network
- timeout terminates a runaway process
- temporary workspace and labeled resources are removed

### Container Lab Integration Tests

- approved Dockerfile builds
- disallowed base image is rejected
- static-site internal HTTP check passes
- forbidden privileged/host-mount Compose options are rejected
- a named-volume persistence check survives container recreation
- two-service internal DNS check passes after Compose support is added

### Frontend Checks

- legacy project still displays and runs
- workspace build/run stages render
- compile error links to the correct file
- generated file preview is bounded
- network and memory feedback are readable
- unavailable Docker capability produces a setup message

## Minimal Verification

Run once after implementation:

```powershell
dotnet build backend\QuizApp.sln --no-restore
dotnet test backend\QuizApp.sln --no-build --filter "GuidedProjectWorkspace|ContainerLab|DockerWorkspace"
npm run build
```

Then perform one manual smoke path:

1. Run one existing legacy C++ Guided Project.
2. Run the new two-file C++ workspace fixture.
3. Save and Quit, resume, and rerun it.
4. Run the Dockerized Static Site lab if Docker is available.
5. Confirm no CIR-labeled containers/networks remain after completion.

Do not run the full backend suite, repeated browser automation, broad Docker experiments, or unrelated cleanup.

## Delivery Order

1. Extract current behavior into `LegacyHarnessGuidedProjectRunner`.
2. Add additive workspace schema and validation.
3. Add safe path/materialization utilities.
4. Add Docker CLI adapter and capability detection.
5. Implement real C++ multi-file build/link.
6. Upgrade frontend result rendering for structured stages.
7. Add fixtures, writable paths, and file assertions.
8. Fix/migrate the existing File I/O Guided Project.
9. Add memory diagnostic profile.
10. Add one deterministic TCP scenario.
11. Add Python workspace profile.
12. Add Containerization category, area, and introductory Learn/Recall content.
13. Add constrained Container Lab runner.
14. Add Dockerized Static Site Guided Project.
15. Add named-volume lab.
16. Add two-service Compose orchestration lab.
17. Update `README.md`, `planned-features.md`, and authoring documentation.

Do not begin with Compose orchestration. The single-project workspace and single-container lab must be reliable first.

## Acceptance Criteria

- Every existing Guided Project still loads and runs through `legacyHarness`.
- A workspace Guided Project preserves real paths and separate source files.
- C++ headers and translation units compile/link normally.
- File-I/O fixtures and generated output assertions work.
- Pause/resume restores app-owned source files without preserving a container.
- Run completion removes the disposable workspace and exact labeled Docker resources.
- Memory diagnostics return actionable feedback.
- A deterministic local TCP scenario works without external networking.
- The Containerization category, area, and metadata appear in navigation.
- A Dockerized Static Site lab builds and verifies through an internal probe.
- Learners never receive arbitrary shell or Docker command execution.
- Docker unavailable/disabled states fail clearly without crashing the app.
- Existing code questions remain on Piston and are unaffected.

## Completion Report

At the end, report:

- files changed
- schema additions
- legacy compatibility behavior
- Docker images/profiles required
- commands run
- checks passed/failed/skipped
- any CIR-labeled resources left after smoke testing
- manual checks still needed
- any existing Guided Projects not yet migrated to workspace mode

## Assumptions

- Docker Desktop or a compatible Docker Engine is installed and started by the host.
- Piston remains the ordinary code-question and legacy Guided Project runner.
- Workspace and Containerization runs are local, disposable, and app-orchestrated.
- Source/session persistence belongs to the app, not containers.
- Containerization labs are trusted authored content operating within server-side allowlists.
- A raw terminal is not necessary for the intended teaching flow.
- Docker Compose is sufficient for the requested small-scale orchestration curriculum.
- Kubernetes, cloud services, serverless, and IaC remain later roadmap items.
