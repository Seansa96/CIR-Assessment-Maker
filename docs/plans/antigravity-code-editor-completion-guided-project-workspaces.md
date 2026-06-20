# Antigravity Implementation Plan: Code Editor Completion and Guided Project Workspaces

## Status

- **Audience:** Antigravity IDE agent
- **Project:** CIR Assessment Maker
- **Features:** CodeMirror completion/UX and expanded Guided Project execution
- **Plan state:** Decision complete
- **Priority:** Editor vertical slice first; runner expansion remains incremental

Before implementation, read:

- `AGENTS.md`
- `GEMINI.md`
- `docs/agent-coexistence.md`
- `planned-features.md`, especially **Guided Project Expansion**
- `newprojects.md`
- Current CodeMirror setup in `frontend/src/pages/index.astro`
- Current Guided Project schema, service, session repository, Piston adapter, and C++ project assessments

Check `git status --short` before editing. Do not revert or overwrite unrelated work in the dirty worktree.

## Execution Constraints

- Prioritize implementation over exhaustive testing.
- Implement the editor completion slice before changing runner architecture.
- Keep the existing Piston-backed code-question and Guided Project path working throughout migration.
- Do not add an always-running language server, terminal emulator, cloud runner, or browser-hosted compiler in the first slice.
- Do not expose arbitrary host commands, host paths, Docker sockets, or unrestricted outbound networking.
- Add only focused tests for completion extraction, workspace manifests, and runner adapters.
- Run each build/focused test once. Avoid broad exploratory testing and unrelated refactors.
- Report changed files, commands, results, and manual checks at completion.

## Summary

Upgrade the existing CodeMirror 6 editors with completion for language keywords, snippets, locally declared functions/classes/variables, and symbols declared in other editable Guided Project files.

Then lay the foundation for richer Guided Projects by replacing the current C++ source-concatenation assumption with an isolated workspace runner contract. The application should continue managing compilation, linking, fixtures, process orchestration, and cleanup while the learner edits source files and clicks one Run Checks action.

The expanded runner must eventually support:

- real multi-file builds
- controlled file-I/O fixtures and output inspection
- deterministic client/listener network simulations
- memory diagnostics through compiler/runtime tooling
- session restoration from app-owned local files
- automatic workspace destruction after completion/deletion

## Phase 1: CodeMirror Completion and UX

### Dependencies

Add:

- `@codemirror/autocomplete`
- `@codemirror/language` if it is not already available transitively as an explicit dependency
- `@codemirror/search` only if search/replace is not included reliably by the current setup

Do not add Monaco or replace CodeMirror 6.

### Shared Editor Factory

Extract the duplicated code-question and Guided Project editor setup from `index.astro` into a focused frontend module, for example:

```txt
frontend/src/scripts/codeEditor.ts
```

Expose a small API:

```ts
createCodeEditor({
  parent,
  document,
  language,
  readOnly,
  projectFiles,
  activeFilePath,
  onChange
})
```

The same factory should configure code questions and Guided Projects consistently.

### Completion Sources

Use `@codemirror/autocomplete` with:

- automatic completion while typing identifiers
- `Ctrl+Space` to explicitly open completion
- language keywords
- common Python and C++ snippets
- local symbols extracted from the active document
- project symbols extracted from all Guided Project source/header files

V1 symbol categories:

- functions and methods
- classes and structs
- variables, fields, parameters, and constants
- Python imports
- C++ namespaces, types, and included project headers

Use the CodeMirror/Lezer syntax tree where practical. A small language-specific extractor is acceptable for constructs the current grammar does not expose conveniently, but do not attempt to build a complete compiler.

Completion inserts the symbol name by default. Function/method completion should insert a call template such as:

```txt
calculateTotal(${parameters})
```

and place the cursor at the first argument. Class and constructor snippets may include named placeholders.

### Completion Scope

- Code questions: active-document symbols plus language keywords/snippets.
- Guided Projects: active-document symbols plus symbols from every project file.
- Read-only project files contribute symbols but cannot be edited.
- Recompute the project symbol index after a debounced file change and when switching files.
- Rank exact-prefix and same-file symbols above other project symbols.
- Do not send learner source code to an external service.

### Editing UX

Tune the editor with:

- visible active-line and matching-bracket highlighting
- close brackets and close quotes
- indentation on Enter
- Tab indentation when completion is closed
- Tab accepting the selected completion when completion is open
- Shift+Tab outdent
- signature/snippet placeholder navigation with Tab
- line numbers and fold gutters
- find/replace
- comment toggle
- undo/redo
- selection match highlighting
- persistent editor height with responsive minimum/maximum bounds
- horizontal scrolling for code instead of forced line wrapping by default
- optional line-wrap toggle stored in local settings
- clear read-only styling
- accessible completion labels and keyboard operation

Preserve editor state when switching Guided Project files:

- document text
- cursor/selection
- scroll position
- undo history where feasible

Destroy editor instances and listeners when changing assessment questions or leaving a project.

### Future Semantic Completion Hook

Define an internal completion-provider interface so a future local language-server adapter can replace or augment the V1 symbol extractor:

```ts
interface CodeCompletionProvider {
  complete(request: CompletionRequest): Promise<CompletionItem[]>;
}
```

Do not implement clangd, pylsp, or another persistent LSP in V1. Local/project completion is the intended first release.

## Phase 2: Guided Project Workspace Contract

### Current Limitation

The existing Guided Project service:

- supports C++ only
- concatenates source-like files into one generated `main.cpp`
- strips local includes
- runs each hidden check as an independent Piston request
- cannot model a real filesystem, separate compilation units, stdin sessions, sockets, or memory tooling

Keep this path as the compatibility runner while introducing a new workspace-capable adapter.

### Schema Additions

Extend `guidedProject` additively:

```yaml
guidedProject:
  language: cpp
  runnerMode: workspace
  build:
    system: generated
    standard: c++20
    sourceGlobs:
      - src/*.cpp
    includePaths:
      - include
    compilerFlags:
      - -Wall
      - -Wextra
  files: []
  fixtures: []
  scenarios: []
  requiredChecks: []
  bonusChecks: []
```

Supported runner modes:

- `legacyHarness`: current behavior and default for existing projects
- `workspace`: new isolated multi-file behavior

Do not rewrite existing project YAML automatically.

### Runner Interfaces

Add a runner abstraction separate from `ICodeRunnerClient`:

```csharp
public interface IGuidedProjectRunner
{
    Task<GuidedProjectWorkspaceResult> RunAsync(
        GuidedProjectWorkspaceRequest request,
        CancellationToken cancellationToken);
}
```

Use two implementations:

- legacy adapter wrapping the current Piston harness flow
- isolated workspace adapter for multi-file projects

The workspace request should contain structured data, not shell command strings supplied by assessment YAML:

- language/runtime
- files and read-only fixtures
- validated build profile
- check/scenario definition
- resource limits

The backend owns all actual build and run commands.

## Isolated Workspace Lifecycle

For each run:

1. Create a disposable workspace identified by attempt ID plus run ID.
2. Materialize learner files and read-only fixtures using validated relative paths.
3. Generate the build configuration from an allowlisted profile.
4. Build inside an isolated container.
5. Run one declared check/scenario with CPU, memory, process, file-size, and wall-clock limits.
6. Capture structured compile output, stdout, stderr, exit code, generated-file observations, and diagnostics.
7. Destroy the disposable container and temporary run directory.

Session persistence remains app-owned:

- Save editable project files in the existing Guided Project session repository.
- On resume, create a fresh disposable workspace and rematerialize those files.
- Do not preserve a running container between requests.
- Delete saved session files after project completion or deletion.

Never mount the repository root, user profile, Docker socket, or arbitrary host directories into a learner container.

## File-I/O Projects

Add declarative fixtures and file assertions:

```yaml
fixtures:
  - path: input/inventory.csv
    content: |
      id,name,count
      1,Bolt,12
    readOnly: true

checks:
  - id: writes-summary
    run:
      stdin: ''
      arguments: []
    expectedFiles:
      - path: output/summary.txt
        contains:
          - Total items: 12
```

Rules:

- All paths are normalized relative paths under the workspace.
- Reject absolute paths, drive prefixes, `..`, symlinks, device files, and path escapes.
- Allow writes only beneath configured writable directories.
- Limit generated file count and aggregate size.
- Return generated file previews only for allowlisted text formats and bounded sizes.

## Network Client/Listener Simulations

Do not grant unrestricted external networking.

Model network projects as deterministic scenarios managed by the runner:

- learner implements a client, listener, or protocol handler
- runner starts the learner process and an app-owned peer process in the same isolated network namespace
- runner assigns loopback/container-local ports
- scenario events define connection order, messages, delays, disconnects, and expected responses
- outbound internet access remains disabled

Example schema:

```yaml
scenarios:
  - id: greeting-round-trip
    type: tcpConversation
    learnerRole: server
    events:
      - connect: client-1
      - send:
          from: client-1
          text: "HELLO\n"
      - expect:
          from: learner
          text: "WELCOME\n"
      - disconnect: client-1
```

V1 network support:

- one TCP listener or one TCP client
- localhost/container-local connections only
- line-oriented UTF-8 messages
- deterministic timeout and event ordering
- captured transcript included in check feedback

Later additions may include multiple clients, UDP, partial packets, retry behavior, and concurrency. Do not include them in the first network slice.

## Memory Projects

For C++ workspace projects, add optional allowlisted diagnostics:

```yaml
diagnostics:
  memory:
    enabled: true
    tool: addressSanitizer
```

Initial tools:

- AddressSanitizer
- UndefinedBehaviorSanitizer
- LeakSanitizer where supported by the runner image

The backend selects compiler/linker flags. Assessment YAML selects only an allowlisted diagnostic profile.

Return structured results for:

- leak detected
- use after free
- out-of-bounds access
- double free
- undefined behavior
- clean run

Do not expose raw host memory, debugger attachment, `ptrace`, or privileged containers.

## Build Profiles

Start with:

- C++17/C++20 multi-file compilation
- Python 3 multi-file package/script execution

Generated C++ build behavior:

- preserve `.h/.hpp` and `.cpp` files
- compile translation units separately
- apply include paths
- link one executable
- report diagnostics by original filename and line

Generated Python behavior:

- preserve package directories
- choose a declared entry point
- set the workspace as the import root
- run with isolated mode where practical

Do not accept arbitrary Makefiles, CMake scripts, shell scripts, package installation, or learner-supplied compiler flags in the first workspace version. These can be considered later behind explicit allowlists.

## API and Persistence

Keep the existing Guided Project endpoints stable where possible:

- load session
- save files
- run checks
- complete project

Extend run results with:

- build stage and diagnostics
- run stage, stdout, stderr, and exit code
- scenario transcript
- file assertions
- memory diagnostics
- timeout/resource-limit reason

Persist project source/session state, not disposable containers or build artifacts.

Keep source files in the app-owned local project-session store for paused work. Consider SQLite metadata later, but do not migrate project file contents into SQLite as part of the editor slice.

## Delivery Order

1. Shared CodeMirror editor factory and tuned editing behavior.
2. Local active-file completion.
3. Cross-file Guided Project symbol completion.
4. Workspace schema and runner interface with legacy compatibility.
5. Real C++ multi-file compile/link workspace.
6. File-I/O fixtures and generated-file assertions.
7. Memory diagnostic profile.
8. Single-peer TCP scenario runner.
9. Python workspace execution.
10. Additional network/concurrency scenarios only after the first slices are stable.

## Focused Tests

### Editor

- Extract Python functions/classes/variables.
- Extract C++ functions/classes/methods/fields.
- Merge symbols from active and read-only project files.
- Rank active-file symbols first.
- Tab accepts completion when open and indents otherwise.
- Switching files preserves text and cursor position.
- Destroying an editor removes listeners.

### Workspace

- Legacy projects continue using the current runner.
- Path validation rejects traversal and absolute paths.
- A two-file C++ project compiles and links.
- A Python project imports a sibling module.
- File-I/O fixture is readable and expected output file is inspected.
- Memory check detects one intentional out-of-bounds write and passes a clean program.
- TCP scenario completes one request/response exchange with networking otherwise disabled.
- Timeout and output limits terminate runaway programs cleanly.
- Completion/deletion removes saved project-session state.

## Minimum Verification

Run once after each implemented slice:

```powershell
dotnet build backend\QuizApp.sln --no-restore
dotnet test backend\QuizApp.sln --no-build --filter "GuidedProjectWorkspace|CodeCompletion"
npm run build
```

Perform only these manual checks:

- Type a locally declared function name and accept its completion with Tab.
- Switch Guided Project files and complete a class/method declared in another file.
- Confirm Tab still indents when the completion popup is closed.
- Run one legacy Guided Project.
- After workspace support exists, run one two-file C++ fixture.

Do not run the complete test suite, repeated browser automation, or unrelated cleanup.

## Acceptance Criteria

- Code questions and Guided Projects share one CodeMirror configuration.
- Python and C++ editors complete locally declared symbols.
- Guided Projects complete symbols declared in sibling files.
- Function completion supports useful argument placeholders.
- Keyboard behavior is predictable and accessible.
- Existing Guided Projects still run unchanged.
- Workspace projects preserve real files and compile/link correctly.
- File-I/O projects use bounded workspace fixtures.
- Network exercises use deterministic isolated peer scenarios without internet access.
- Memory exercises return actionable sanitizer diagnostics.
- Containers remain disposable; session source state remains app-owned and resumable.

## Assumptions

- CodeMirror 6 remains the editor.
- V1 completion is local static extraction, not compiler-accurate IntelliSense.
- A future local LSP can plug into the completion-provider interface.
- Piston remains suitable for ordinary code questions and legacy projects.
- Rich workspace projects may require a dedicated local container-runner adapter because the current single-file Piston contract is insufficient.
- The app, not the learner, controls build commands, ports, fixtures, limits, and cleanup.
- No persistence is required inside containers.
