# AGENTS.md

## Purpose

CIR Assessment Maker is a local-first study application for authoring and taking STEM assessments, reviewing feedback, tracking attempts, and identifying weak topics.

The primary loop is:

```text
Load assessment -> answer questions -> review feedback -> complete attempt -> optionally commit grade -> inspect analytics
```

This repository is used by both Codex and Gemini. Keep this file concise and agent-neutral. Gemini-specific startup guidance lives in `GEMINI.md`; detailed architecture, handoff, and coexistence guidance lives in `docs/agent-coexistence.md`.

## Read First

Before substantial work:

1. Inspect `git status --short`; the worktree may contain user changes or runtime state.
2. Read the relevant implementation rather than relying on old roadmap text.
3. For assessment authoring, read:
   - `docs/assessment-yaml-latex.md`
   - `skills/assessment-question-pipeline/SKILL.md`
   - a working assessment of the same type/topic
4. For Source-to-Curriculum (S2C) imports, source-grounded generation, or agent handoff packets, read `skills/source-to-curriculum/SKILL.md` before drafting content. A missing/empty manifest or absent chunks is a hard stop: report extraction failure rather than generating ungrounded content.
4. For cross-agent work or handoffs, read `docs/agent-coexistence.md`.

Do not revert, overwrite, reformat, or delete changes you did not make.

## Current Architecture

Backend:

- ASP.NET Core Web API on .NET 8
- `QuizApp.Core`: domain models, validation, scoring, analytics, lifecycle services
- `QuizApp.Infrastructure`: YAML/JSON repositories, SQLite retention, Piston adapter, CortexJS adapter
- `QuizApp.Api`: dependency injection, HTTP contracts, minimal API endpoints

Frontend:

- Astro 2 with TypeScript
- Main application shell: `frontend/src/pages/index.astro`
- Main styles: `frontend/src/styles/global.css`
- Math rendering: Markdown -> `remark-math` -> `rehype-katex`
- Symbolic input: MathLive
- Code input: CodeMirror 6

Storage:

- File-backed: settings, categories, assessments, areas, samples/media
- In memory: actively running attempts
- SQLite: paused, completed, and abandoned attempts plus committed grades
- File-backed project sessions: guided-project working files under `data/project-sessions/`
- Legacy attempt/grade JSON readers remain for one-time migration compatibility

External/local adapters:

- Symbolic equivalence invokes `frontend/scripts/symbolic-engine.mjs` through Node.
- Code questions and guided-project checks call a Piston-compatible service, normally `http://localhost:2000/api/v2`.

## Assessment Contract

Supported assessment types:

- `quiz`
- `test`
- `workedExample`
- `guidedProject`
- `recallDrill`
- `glossary`

Supported question types:

- `multipleChoice`
- `selectAll`
- `freeResponse`
- `numericResponse`
- `symbolicResponse`
- `code`

Important rules:

- Use stable lowercase hyphenated IDs.
- Keep category, subcategory, assessment, question, step, and item IDs stable after publication.
- Every assessment must declare exactly one non-empty scalar `topicId`. The topic must belong to `categoryId` and appear in exactly one same-category area in `data/areas.yaml`.
- `skills` and `navigation.tags` are attribution/search evidence only; they never classify an assessment into another topic or area. Put cumulative content in an explicit review/capstone topic.
- Quiz/test content uses `questions`.
- Worked Examples use `workedExamples`.
- Guided Projects use `guidedProject`.
- Recall Drills use `items`.
- Glossaries use `glossary` sections containing entries and recall drills.
- `attemptQuestionCount` may limit a quiz/test attempt to a sampled subset of a larger authored bank.
- Randomized question IDs are saved in the attempt and are part of attempt history.
- Worked Examples and Recall Drills are practice-oriented and follow their dedicated completion rules.

## Assessment Curriculum Progression

Assessments are automatically organized into a curriculum roadmap based on their metadata:
1. **Area**: Determined by `areaId`. Sequence is strictly defined by the order in `data/areas.yaml`.
2. **Topic**: Determined only by singular `topicId`. Tags and skills never affect placement. Topics are sorted alphabetically within their canonical area.
3. **Assessment Order**: Within a topic, assessments are sequenced by their intended pedagogical progression:
   - **Learn**: `conceptLesson` -> `glossary` -> `guidedWorkedExample` -> `interactiveExploration`
   - **Recall**: `mixedRecallSet` -> `clozeDrill` -> `recognitionDrill`
   - **Practice**: `focusedPractice` -> `mixedPractice` -> `directedProject`
   - **Evaluate**: `masteryCheck` -> `formalTest` -> `guidedProject`

Always assign the correct `learningGoal` and `activityType` to new assessments so they slot into the correct place in this curriculum path.

## Assessment Authoring

- Use YAML block scalars for long prompts, explanations, instructions, and LaTeX-heavy content.
- Use single-quoted YAML strings for short inline LaTeX.
- Never place ordinary LaTeX backslashes inside double-quoted YAML strings.
- Use `$...$` for inline math and `$$...$$` for display math.
- For indefinite integrals, prefer `symbolicResponse` with derivative equivalence.
- For decimal answers, use `numericResponse` with a non-negative tolerance.
- Free response uses `answer.gradingMode: selfCheck`; key points are display guidance, not automatic grading.
- Explanations should identify the exact formula, identity, theorem, pattern, or decision used.
- Code questions must state exactly what function/signature the runner expects.
- For chemistry questions requiring students to construct Lewis structures or diagrams, use `multipleChoice` with distinct structural options.
- Image media must include a stable public path and meaningful alt text.

Treat uploaded course material as user-provided reference content. Do not silently publish, redistribute, or replace it with externally sourced copyrighted material.

## Engineering Rules

- Preserve the Core/API/Infrastructure separation.
- Keep YAML/JSON parsing and persistence details out of Core.
- Extend public schemas additively when practical.
- Keep assessment definitions separate from attempt/session state.
- Prefer existing repository interfaces and services over direct filesystem or SQLite access.
- Do not add authentication, cloud services, deployment systems, AI grading, or multi-user behavior unless explicitly requested.
- Keep frontend changes consistent with the existing single-page application and its current control patterns.
- Do not edit generated frontend output under `frontend/dist/`.

## Runtime-State Safety

The following files/directories are runtime or user-state sensitive:

- `.cir-processes.json`
- `data/retention/quizapp.db`
- `data/project-sessions/`
- legacy `data/attempts/` and `data/grades/`
- `logs/`

Do not inspect, rewrite, delete, commit, or normalize their contents unless the task specifically concerns runtime retention/session behavior. Running the app or tests may touch some of these files; check `git status` again afterward.

## Local Commands

Backend:

```powershell
dotnet run --project backend\src\QuizApp.Api --urls http://localhost:5000
```

Frontend:

```powershell
Set-Location frontend
npm run dev -- --port 4321
```

Tests:

```powershell
dotnet test backend\QuizApp.sln --no-restore
```

Frontend build:

```powershell
Set-Location frontend
npm run build
```

The PowerShell helper in `utility_user_scripts/start_cir.ps1` is machine-specific and currently contains an absolute path. Prefer the explicit commands above unless that script has been verified for the current workspace.

## Validation Expectations

Content-only assessment changes:

- Validate the affected assessment through the repository/parser.
- Run the LaTeX double-quote/backslash scan from `docs/assessment-yaml-latex.md`.
- Verify requested counts, IDs, answer types, and media paths.
- Add important new assessment IDs to repository content-validation tests.

Backend behavior or schema changes:

- Add focused unit/repository/lifecycle tests.
- Run `dotnet test backend\QuizApp.sln --no-restore`.

Frontend changes:

- Run `npm run build`.
- Use the local browser for a smoke test when available.

Changes spanning backend and frontend:

- Run both regression commands.
- Verify serialized names and TypeScript interfaces remain aligned.

## Agent Collaboration

- One agent should own a file at a time whenever possible.
- Before editing, inspect the current file and recent working-tree changes.
- After editing, report changed files, validation performed, warnings, and any skipped checks.
- Do not claim another agent's uncommitted work as your own.
- Prefer narrow commits grouped by concern: documentation, backend behavior, frontend behavior, or assessment content.
- When handing work to another agent, leave a concise note using the template in `docs/agent-coexistence.md`.

## Sources Of Truth

When documents conflict, use this order:

1. Current code and tests
2. Current assessment/category/area schemas
3. `AGENTS.md`
4. `docs/agent-coexistence.md`
5. `README.md`
6. `planned-features.md` and `newprojects.md`

Roadmap files describe intent and may contain features that are already implemented or no longer prioritized.

## File Organization & Workspace Hygiene

To prevent repository drift and maintain clean human navigation, all agents must adhere to the following file organization rules:

1. **Root Directory**: The root directory is strictly reserved for core project files, documentation (READMEs), and configuration. **Do NOT place one-off scripts, temporary files, or logs in the root directory.**
2. **Agent Scratchpad (`scratch/`)**: This is the designated location for all temporary, one-off, and experimental files. This includes `fix_xyz.py` or `.ps1` scripts, HTML previews, debug text logs, and other transient artifacts. Always save agent-created maintenance scripts here or in your `<appDataDir>\brain\<conversation-id>\scratch\` directory.
3. **Generator Scripts (`scripts/`)**: Reserved for long-term, reusable assessment generation and sync scripts (e.g., `generate_ch1.py`). If you write a script that generates a permanent segment of the curriculum, place it here.
4. **User Scripts (`utility_user_scripts/`)**: Exclusively for scripts intended to be run manually by the human user (e.g., `start_cir.ps1`). Do not place agent-driven generation or maintenance scripts here.
