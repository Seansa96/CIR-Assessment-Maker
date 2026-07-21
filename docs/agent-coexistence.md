# Codex and Gemini Coexistence Report

**Repository:** CIR Assessment Maker  
**Prepared:** June 18, 2026  
**Purpose:** Make Codex and Gemini productive in the same repository with minimal duplicated context, accidental overwrites, runtime-state churn, or conflicting implementation assumptions.

## Executive Summary

The repository is well suited to multiple coding agents because its backend has explicit layers, assessment content is mostly isolated YAML, and regression commands are straightforward. The largest collaboration risks are not architectural complexity; they are context drift and file ownership:

1. `AGENTS.md` described the old MVP rather than the implemented system.
2. No Gemini-native root context file existed.
3. The assessment-authoring skill had a usable copy under `skills/` and an unfinished divergent copy under `.codex/skills/`.
4. Runtime state is partly tracked by Git, especially `.cir-processes.json` and `data/retention/quizapp.db`.
5. The launcher script contains an absolute machine path.
6. `README.md`, `planned-features.md`, and some examples lag behind the current schema.
7. The frontend is concentrated in one large Astro page, increasing merge-conflict risk when agents work concurrently.

The recommended operating model is:

- `AGENTS.md` is the concise shared contract and the primary Codex project instruction file.
- `GEMINI.md` is a thin Gemini entry point that imports `AGENTS.md`.
- This report is detailed reference material loaded only for architecture, agent infrastructure, broad refactors, or handoffs.
- `skills/assessment-question-pipeline/` is the cross-agent canonical assessment-authoring workflow.
- `.codex/skills/assessment-question-pipeline/` is a synchronized Codex discovery mirror, not an independently edited fork.
- Agents use file ownership, narrow commits, status checks, and explicit handoff notes.

## Current Project Snapshot

At the time of this report, the repository contains:

- 124 authored assessment files
- 13 category files
- 5 assessment types
- 6 question types
- 10 backend test source files
- 34 frontend public assets

Assessment distribution:

| Type | Count |
| --- | ---: |
| `quiz` | 55 |
| `test` | 1 |
| `workedExample` | 54 |
| `recallDrill` | 11 |
| `guidedProject` | 3 |

These counts are a snapshot, not a contract. Agents should inspect the repository rather than hard-code them.

## Architecture

### Backend

The backend is an ASP.NET Core .NET 8 solution:

```text
backend/
  src/
    QuizApp.Api/
    QuizApp.Core/
    QuizApp.Infrastructure/
  tests/
    QuizApp.Tests/
```

Responsibilities:

- **QuizApp.Core**
  - Domain records and enums
  - Assessment validation
  - Answer scoring
  - Attempt lifecycle
  - Grade analytics
  - Guided-project behavior
  - Interfaces for persistence and adapters

- **QuizApp.Infrastructure**
  - YAML/JSON DTOs and mapping
  - File-backed settings/categories/assessments/areas/project sessions
  - SQLite attempt and grade retention
  - Legacy JSON migration
  - Piston HTTP client
  - CortexJS Node-process adapter

- **QuizApp.Api**
  - Dependency injection
  - JSON enum/casing configuration
  - Local CORS
  - Minimal API endpoints
  - Request/response contracts

The repository-interface boundary is important. Agents should not bypass it by reading assessment YAML, writing SQLite, or modifying session files directly from controllers/services.

### Frontend

The frontend is Astro 2 with TypeScript. Most application behavior currently lives in:

- `frontend/src/pages/index.astro`
- `frontend/src/styles/global.css`

The app is a local SPA-style interface with views for:

- Loading assessments
- Quiz/test attempts
- Worked Examples
- Recall Drills
- Guided Projects
- Creation for supported creator types
- Settings
- Grade Log and analytics

Important frontend dependencies:

- MathLive for symbolic input
- KaTeX plus remark/rehype for rendered math
- CodeMirror 6 for code input
- CortexJS Compute Engine for symbolic comparison through the backend adapter

Because `index.astro` is large and central, concurrent frontend work should be serialized or split by carefully chosen line/function ownership. Two agents editing broad regions of this file at once will create avoidable conflicts.

## Assessment And Content Model

### Assessment Types

| Type | Storage Shape | Intended Experience |
| --- | --- | --- |
| `quiz` | `questions` | Short practice/check |
| `test` | `questions` | Longer scored or exam-like assessment |
| `workedExample` | `workedExamples[].steps` | Locked guided progression with hints |
| `guidedProject` | `guidedProject` | Multi-file code project with hidden checks |
| `recallDrill` | `items` | Reveal and self-rate recall loop |

Quiz/test assessments may use `attemptQuestionCount` to sample a fixed-size attempt from a larger authored bank.

### Question Types

| Type | Grading |
| --- | --- |
| `multipleChoice` | Exact choice ID |
| `selectAll` | Exact choice set |
| `freeResponse` | Human self-check |
| `numericResponse` | Numeric value within tolerance |
| `symbolicResponse` | Backend-authoritative symbolic equivalence |
| `code` | Piston execution through generated harness |
| `circuit` | Circuit-diagram response validation |
| `multipart` | Two or more independently validated parts (quiz/test only) |
| `graphingResponse` | Graph-based response validation |

### Content Sources Of Truth

For assessment schema behavior:

1. `backend/src/QuizApp.Core/Domain/AssessmentModels.cs`
2. `backend/src/QuizApp.Core/Services/AssessmentValidator.cs`
3. `backend/src/QuizApp.Infrastructure/Files/FileDtos.cs`
4. `backend/src/QuizApp.Infrastructure/Files/FileDtoMapper.cs`
5. Working assessment YAML of the same type
6. `docs/assessment-yaml-latex.md`

Do not infer current schema solely from `README.md` or old roadmap files.

## Persistence And Runtime Lifecycle

### Durable File Content

These are authored/configuration sources and normally belong in version control:

- `data/settings.yaml`
- `data/areas.yaml`
- `data/categories/`
- `data/assessments/`
- `data/samples/`
- `frontend/public/assessments/`

### Active Attempts

`InProgress` attempts live in `InMemoryAttemptSessionStore`.

Consequences:

- Active unsaved work is not restart durable.
- Save and Quit transitions an attempt to `Paused` and persists it.
- An agent restarting the backend can destroy active in-memory progress.
- Before stopping/restarting services, ask whether the user has an active attempt when that risk is plausible.

### SQLite Retention

SQLite stores:

- Paused attempts
- Completed attempts
- Abandoned attempts
- Committed grade-log entries
- Retention migration metadata

Default path:

```text
data/retention/quizapp.db
```

SQLite is embedded. It does not require a separately started database process.

Legacy JSON attempts and grades are imported once through `LegacyRetentionMigrationService`. They remain compatibility inputs rather than the current write target.

### Guided-Project Sessions

Guided-project files and check results are stored as JSON under:

```text
data/project-sessions/
```

These are user session state, not authored project definitions.

### Runtime Files Requiring Caution

| Path | Risk |
| --- | --- |
| `.cir-processes.json` | Machine-local PIDs; changes whenever launcher runs |
| `data/retention/quizapp.db` | User attempts and grades; binary merge conflicts/data loss |
| `data/project-sessions/` | In-progress guided-project work |
| `data/attempts/`, `data/grades/` | Legacy/local user data |
| `logs/` | Generated runtime output |
| `frontend/dist/` | Generated build output |

Agents should avoid these unless the request concerns retention, migration, sessions, or runtime debugging.

## External And Local Service Dependencies

### Symbolic Math

The backend starts Node and invokes:

```text
frontend/scripts/symbolic-engine.mjs
```

The adapter uses CortexJS Compute Engine and has a short timeout. Node and frontend dependencies must be available for symbolic scoring.

### Code Runner

Code questions and Guided Project checks require a Piston-compatible service. Default:

```text
http://localhost:2000/api/v2
```

The app does not start Piston automatically. An agent must not assume code-question failures are application bugs until it verifies:

- Docker/container runtime is available
- Piston is running
- Required Python/C++ runtimes are installed in Piston
- The configured base URL is reachable

### Development Servers

Expected local URLs:

- Backend: `http://localhost:5000`
- Frontend: `http://127.0.0.1:4321`

The frontend uses `PUBLIC_API_BASE` when set, otherwise `http://localhost:5000/api`.

## Instruction Hierarchy

### Codex

Codex should continue to use:

- System/developer instructions
- Root `AGENTS.md`
- Relevant local skill instructions
- Current user request

Do not replace `AGENTS.md` with a Gemini-specific document.

### Gemini

Gemini CLI recognizes `GEMINI.md` context files. The root `GEMINI.md` imports `AGENTS.md` with:

```text
@./AGENTS.md
```

This gives Gemini the same shared rules without duplicating them.

Gemini CLI officially supports hierarchical `GEMINI.md` files, just-in-time directory context, `/memory show`, `/memory reload`, and `@file.md` imports. Reference:

<https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md>

Do not configure Gemini to load both `AGENTS.md` and `GEMINI.md` independently when `GEMINI.md` already imports `AGENTS.md`; that would duplicate the shared instructions.

### Shared Versus Agent-Specific Context

Shared:

- Architecture and boundaries
- Storage safety
- Test commands
- Assessment schema rules
- Git/worktree behavior
- Handoff protocol

Codex-specific:

- `.codex/` discovery/configuration
- Codex skill mirrors
- Codex desktop/browser behavior

Gemini-specific:

- `GEMINI.md`
- Gemini memory/context diagnostics
- Gemini tool approval settings

## Skills Strategy

The repository currently has two assessment skill locations:

```text
skills/assessment-question-pipeline/
.codex/skills/assessment-question-pipeline/
```

The intended policy is:

- `skills/assessment-question-pipeline/` is canonical cross-agent content.
- `.codex/skills/assessment-question-pipeline/` is a Codex discovery mirror.
- Edit the canonical version first.
- Synchronize the Codex mirror in the same change.
- Gemini should read the canonical version only when the task concerns assessment content.

Do not allow the two copies to evolve independently. The previous `.codex` copy contained an unfinished skill template, which could cause Codex to receive lower-quality or contradictory guidance.

## Agent Work Allocation

### Safe Parallel Work

These tasks are usually easy to isolate:

- Separate assessment YAML files
- Separate category files
- Documentation files
- Backend tests in different classes
- New Infrastructure adapters in new files
- Media assets in separate directories

### Work That Should Be Serialized

- `frontend/src/pages/index.astro`
- `frontend/src/styles/global.css`
- `backend/src/QuizApp.Api/Program.cs`
- Core domain records used across serialization
- `FileDtos.cs` and `FileDtoMapper.cs`
- `AssessmentValidator.cs`
- `data/areas.yaml`
- `README.md`, `AGENTS.md`, `GEMINI.md`
- SQLite schema/migration code

### Suggested Ownership Labels

When coordinating agents, state ownership in the prompt or handoff:

```text
Owner: Codex
Files: backend/src/QuizApp.Core/Services/AttemptService.cs, related tests
Do not edit: frontend/src/pages/index.astro
```

or:

```text
Owner: Gemini
Files: data/assessments/new-topic-*.yaml
Shared file requiring coordination: backend/tests/QuizApp.Tests/FileAssessmentRepositoryTests.cs
```

## Handoff Protocol

Use this compact handoff format:

```markdown
## Agent Handoff

Goal:
- What the task is meant to achieve.

Changed:
- Exact files and behavior changed.

Validated:
- Commands/tests run and results.

Unverified:
- Browser checks, external services, or edge cases not tested.

Working tree:
- Relevant pre-existing changes that must not be reverted.

Next:
- Concrete remaining work with no hidden decisions.
```

For assessment content, also report:

- Assessment ID
- Category/subcategory IDs
- Question/item/step count
- Question types used
- Whether LaTeX scan passed
- Whether symbolic/numeric answers were independently verified

## Git And Change Isolation

### Before Work

Run:

```powershell
git -c safe.directory=C:/Users/SeanS/Downloads/cir_app status --short
```

The `safe.directory` override may be needed because the workspace ownership and execution user can differ.

### During Work

- Do not use `git reset --hard`, `git checkout --`, or broad clean commands.
- Do not normalize unrelated line endings.
- Do not include runtime database/PID changes in feature commits.
- Prefer narrow patches.
- Re-read files immediately before editing when another agent may be active.

### Before Handoff

Run status again and distinguish:

- Changes made by this task
- Pre-existing user/agent changes
- Generated runtime changes

Commit boundaries should separate:

1. Agent/documentation infrastructure
2. Backend schema/behavior
3. Frontend behavior
4. Assessment content/media

This makes cross-agent review and conflict resolution much easier.

## Validation Matrix

| Change | Required Checks |
| --- | --- |
| Assessment YAML only | Repository validation, IDs/counts, LaTeX scan |
| Category/area data | Load/list checks and affected analytics tests |
| Backend domain/schema | Focused tests plus full backend test suite |
| Attempt lifecycle/retention | Lifecycle and SQLite tests |
| API contract | Backend tests and frontend type/build check |
| Frontend TypeScript/UI | `npm run build` and browser smoke test |
| Symbolic scoring | Symbolic scorer/engine tests; Node dependencies present |
| Code runner | Mock/unit tests plus optional live Piston smoke test |
| Guided Project | Schema tests plus live runner check when available |
| Agent documentation | Link/path checks, Markdown review, status check |

Standard regression commands:

```powershell
dotnet test backend\QuizApp.sln --no-restore
```

```powershell
Set-Location frontend
npm run build
```

Known non-fatal frontend build observations:

- npm may report an `EPERM` warning while cleaning its log directory.
- Vite may report chunks larger than 500 kB.

Agents should report these warnings but not describe a successful build as failed.

## Documentation Findings

### AGENTS.md

Previous condition:

- Reflected the original MVP
- Omitted SQLite, Recall Drills, Guided Projects, symbolic/code systems, and analytics
- Contained a malformed encoded arrow

Remediation:

- Rewritten as the current shared contract
- Kept concise enough for routine agent context

### README.md

README is useful but has drift:

- It describes the project broadly as file-backed.
- It does not fully describe Recall Drills or Guided Projects.
- It previously said attempts and grade logs live as ordinary files.
- Some older examples use schema key names or YAML quoting styles that should be checked against current DTOs and the LaTeX guide.
- The limitations section still implies SQLite is future-only.

Recommendation:

- Keep README focused on users and assessment authors.
- Link to this report for agent/developer operations.
- Update feature/schema examples whenever public DTOs change.

### planned-features.md

The roadmap was refreshed on June 18, 2026 into explicit Implemented, Near-Term, Medium-Term, Long-Term, and Deliberately Deferred sections.

Maintenance guidance:

- Move completed capabilities into Implemented.
- Keep unfinished follow-up work in the appropriate future section.
- Continue treating current code and tests as the final implementation truth.

### newprojects.md

This is a content/project idea backlog. It contains encoding artifacts and should not override current Guided Project schema.

Recommendation:

- Treat as ideation only.
- Verify every proposed project against current runner constraints before implementation.

## Risk Register

### High: Tracked SQLite User Data

`data/retention/quizapp.db` is tracked and changes during normal application use.

Risks:

- Binary merge conflicts
- Accidental sharing of study history
- Data loss when switching branches
- No meaningful code review of binary diffs

Recommended follow-up:

1. Back up the current database.
2. Decide whether it is sample data or private user state.
3. If private state, remove it from tracking and add `data/retention/` to `.gitignore`.
4. Add a schema initializer/sample fixture instead of committing the live DB.

This report does not untrack or delete the database because that is a data-retention decision.

### High: Tracked PID File

`.cir-processes.json` is tracked but contains machine-local process IDs.

Recommended follow-up:

- Remove it from tracking.
- Add it to `.gitignore`.
- Recreate it only at runtime.

### Medium: File-Backed Guided Project State

`data/project-sessions/` contains user work but is not ignored.

Recommended follow-up:

- Ignore the directory.
- Add explicit export/import if project-session portability becomes necessary.

### Medium: Machine-Specific Launcher

`utility_user_scripts/start_cir.ps1` hard-codes:

```text
C:\Users\SeanS\Downloads\cir_app
```

Recommended follow-up:

- Resolve the repository root relative to `$PSScriptRoot`.
- Detect occupied ports.
- Validate saved PIDs before overwriting `.cir-processes.json`.
- Add a matching stop script.

### Medium: Monolithic Frontend

Most behavior is in one Astro page.

Risks:

- Merge conflicts
- Difficult ownership boundaries
- Larger agent context requirements
- Broad regressions from small changes

Recommended incremental extraction:

1. API client and shared types
2. Assessment renderers
3. Attempt lifecycle controls
4. Grade analytics
5. Creator/editor

Do not perform a wholesale frontend rewrite solely for agent convenience.

### Medium: Skill Duplication

The canonical and Codex skill copies can drift.

Recommended follow-up:

- Add a small verification script or test that compares the mirrored `SKILL.md`.
- Document canonical/mirror policy in both locations.

### Low: Roadmap And Encoding Drift

Some Markdown files contain mojibake and stale feature states.

Recommended follow-up:

- Normalize those documents during a dedicated documentation cleanup.
- Avoid broad encoding rewrites mixed with feature work.

## Recommended Agent Workflow

### Assessment Content Task

1. Read `AGENTS.md`.
2. Load the canonical assessment skill.
3. Read the LaTeX guide and nearby working assessment.
4. Inspect category/subcategory/area IDs.
5. Draft with stable IDs and explicit answer format.
6. Verify every answer.
7. Run parser/repository validation and LaTeX scan.
8. Report counts and verification.

### Backend Feature Task

1. Inspect domain, service, interface, Infrastructure implementation, API contract, and tests.
2. Choose additive schema changes when possible.
3. Update DTO mapping and TypeScript contracts together.
4. Add focused tests before or with implementation.
5. Run backend tests.
6. Run frontend build if wire contracts changed.

### Frontend Task

1. Inspect current state and relevant functions/styles.
2. Avoid unrelated formatting in `index.astro`.
3. Preserve existing interaction patterns and dev-only behavior.
4. Run build.
5. Smoke test localhost when browser tooling is available.

### Retention Or Session Task

1. Back up or avoid live state.
2. Use temporary test databases.
3. Test migration idempotency.
4. Verify active-memory versus durable-state transitions.
5. Do not manually edit the live SQLite database.

## Staged Improvement Roadmap

### Stage 1: Agent Context

- Maintain `AGENTS.md` as shared truth.
- Maintain thin `GEMINI.md`.
- Synchronize assessment skill mirror.
- Use handoff template.

### Stage 2: Repository Hygiene

- Decide policy for tracked SQLite/PID/project-session state.
- Make launcher path-relative.
- Refresh `.gitignore`.
- Add a stop/status helper.

### Stage 3: Documentation Accuracy

- Refresh README assessment types and persistence model.
- Reconcile roadmap with implemented features.
- Correct stale schema examples and encoding artifacts.

### Stage 4: Conflict Reduction

- Extract frontend types/API/renderers gradually.
- Split broad tests by subsystem only when it improves ownership.
- Add a script for content validation and skill-mirror verification.

## Definition Of Successful Coexistence

The Codex/Gemini setup is working when:

- Both agents receive the same architectural and safety rules.
- Gemini loads `GEMINI.md`, which imports `AGENTS.md`.
- Codex continues using `AGENTS.md` and its existing skill discovery.
- Neither agent edits the other agent's infrastructure casually.
- Runtime state does not enter ordinary feature commits.
- Handoffs clearly identify ownership, validation, and remaining work.
- Assessment content passes the same quality/LaTeX/schema checks regardless of which agent authored it.
- Backend/frontend contract changes are tested across both sides.
- Documentation describes implemented behavior rather than the original MVP.
