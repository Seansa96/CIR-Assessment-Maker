# Planned Features

This document tracks the current feature state and the most likely future work.

It is a roadmap, not the implementation source of truth. When this file conflicts with the code, tests, schemas, or `AGENTS.md`, follow the implementation.

## Implemented

### Application Foundation

- ASP.NET Core Web API on .NET 8
- Astro and TypeScript frontend
- Localhost-first development workflow
- YAML and JSON assessment loading
- File-backed settings, categories, assessments, areas, and media
- Repository interfaces separating Core from persistence details
- Assessment validation before active use
- Sample and authored STEM assessment library

### Assessment Types

- Quiz
- Test
- Worked Example
- Recall Drill
- Guided Project
- Fixed-size quiz/test attempts sampled from larger authored banks through `attemptQuestionCount`

### Question And Recall Types

- Multiple choice
- Select all
- Free response with delayed self-check grading
- Numeric response with tolerance
- Symbolic response
- Code questions for Python and C++
- Recall Drill typed items
- Recall Drill symbolic items
- Recall Drill flashcards
- Recall Drill cloze items
- Image media on questions, choices, answers, and recall content

### Assessment Experience

- Practice and scored modes
- Randomized or static question order
- Saved randomized/sampled question order per attempt
- Practice-mode immediate feedback
- Scored-mode delayed feedback
- Free-response key-point rubrics
- Symbolic math input with MathLive
- KaTeX rendering through the Markdown math pipeline
- Symbolic equivalence checks using CortexJS Compute Engine
- CodeMirror 6 editor for code questions and Guided Projects
- Piston-compatible code execution adapter
- Worked Example locked progression, hints, remediation, previous-step navigation, and review
- Recall Drill reveal/rate flow and weak-tag summary
- Guided Project editable files, required/bonus checks, and completion state
- Dev-only current-assessment refresh without ending the attempt
- Question-jump panel with answered-state indicators
- Locked mode display during active attempts

### Attempt And Grade Management

- In-memory active attempt sessions
- Save and Quit to durable paused state
- Resume paused attempts
- Quit early/abandon attempts
- Review completed and abandoned attempts
- Delete individual attempts and linked grades
- Bulk attempt deletion
- SQLite retention for paused, completed, and abandoned attempts
- SQLite retention for committed grades
- One-time migration from legacy attempt and grade JSON
- Grade commit blocking while free-response self-checks remain unresolved

### Analytics

- Overall committed average
- Category averages
- Subcategory statistics
- Manually managed area groupings
- Question-type performance
- Practice/scored and attempt-history filtering
- Sortable attempt and grade tables
- Weak-category, weak-area, and weak-question-type summaries
- Attempt history linked to review and management actions

### Frontend And Authoring

- Quiz/test creation scaffold
- Category and subcategory selection
- Basic question editors
- Add/remove questions
- Change supported question type
- Auto-generated question IDs
- Validation before save
- Assessment preview
- YAML/JSON preview support
- Responsive assessment layouts
- Selectable answer cards
- Segmented mode controls
- Code syntax highlighting, indentation, and bracket support

### Agent And Documentation Support

- Assessment YAML and LaTeX authoring guide
- Shared Codex/Gemini repository instructions
- Gemini-native `GEMINI.md`
- Codex/Gemini coexistence and handoff report
- Assessment-question authoring skill

## Near-Term Candidates

These features have been discussed and fit the current architecture without requiring a major redesign.

### Complete The Assessment Creator

The current creator is intentionally narrower than the schema.

Remaining work:

- More polished form editors for all currently supported quiz/test question types
- Media picker/path editor
- Better symbolic-answer authoring controls
- Code question test-case editor
- Reordering questions
- Draft persistence
- Templates and reusable question blocks
- Better YAML/JSON round-trip preview
- Duplicate assessment ID handling
- Creator support for sampled banks through `attemptQuestionCount`

Worked Examples, Recall Drills, and Guided Projects should remain schema-authored unless explicitly reconsidered.

### Matching Questions

Add a true `matching` question type:

- Left/right pair schema
- Shuffled right-side order saved in the attempt
- Validation and scoring
- Attempt submission shape
- Authoring and taking UI
- Practice/scored feedback
- Result review and analytics

### Timer Enforcement

Timer fields and settings already exist, but the app does not yet enforce a complete timed-attempt lifecycle.

Remaining work:

- Assessment-level countdown
- Question-level countdown
- Attempt start/pause/resume/expiration timestamps
- Explicit pause policy
- Expiration submission/completion behavior
- Practice versus scored behavior
- Browser refresh and backend restart handling
- Tests for expiration and saved checkpoints

The default remains untimed.

### Automatic Test Generation

Current support samples a fixed number of questions from one authored bank. It does not generate tests from multiple assessments.

Initial version:

- Select quizzes from one category
- Choose total question count
- Balance across selected subcategories
- Choose question-type distribution
- Start immediately
- Optionally save the generated test

Later:

- Multi-category generation
- Difficulty balancing
- Weak-topic weighting
- Avoid recently seen questions
- Preserve generated-source provenance

### Import And Export

- Export assessments to YAML or JSON
- Export attempt history and grade analytics
- Export/import Guided Project session files when useful
- Import assessment packs
- Validate packs before activation
- Detect ID collisions
- Media manifest and asset validation

### Repository And Runtime Hygiene

Discussed during the Codex/Gemini audit:

- Stop tracking the live SQLite retention database after backing it up
- Ignore `.cir-processes.json`
- Ignore or explicitly export `data/project-sessions/`
- Make the PowerShell launcher path-relative
- Add stop/status scripts
- Keep sample retention fixtures separate from personal study data

## Medium-Term Candidates

### Advanced Question Types

Potential additions, roughly in implementation order:

1. Ordering
2. Fill-in-the-blank as a graded quiz/test question
3. Multi-part questions
4. Equation or relationship entry beyond one symbolic expression
5. Diagram/image annotation or selection
6. Code-output and debugging questions
7. Proof or rubric-based responses

Every new type should include schema mapping, validation, attempt persistence, scoring or self-check behavior, review UI, analytics, tests, and sample content.

### Richer Symbolic Mathematics

Current symbolic response handles single-expression equivalence and derivative equivalence.

Discussed improvements:

- Tune MathLive navigation and templates further
- Better autocomplete and common-function entry
- More predictable cursor movement through powers, fractions, and grouped terms
- Multi-expression or equation-system answers
- Domain/assumption handling
- Better parse-error feedback
- Optional SymPy-backed service if CortexJS becomes insufficient
- Step-aware symbolic derivations without pretending to provide full proof grading

### Recall And Memory Training

Recall Drills exist, but scheduling does not.

Possible next version:

- Spaced-repetition scheduling
- Due dates and review queues
- Per-item history
- Confidence/ease tracking
- Formula-family and tag dashboards
- Missed-item retry sessions
- Optional SM-2-style scheduling only after the simpler history model is stable

### Grade Analytics Refinement

The light analytics dashboard exists.

Possible improvements:

- Trend charts over time
- Weighted category/subcategory policies
- Quiz versus test weighting
- Configurable minimum sample sizes
- Recent-versus-lifetime comparisons
- Links from weak topics to recommended Worked Examples or Recall Drills
- Better handling of sampled question banks
- Exportable analytics reports

An auxiliary analytics service is not currently necessary. Reconsider only if SQLite queries or dataset size become difficult to manage locally.

### Guided Project Expansion

The Guided Project assessment type and initial C++ projects exist.

Discussed next projects:

- Parallel Stat Calculator
- Thread-Safe Bank Ledger
- Combat Entity Simulator
- Event Bus/Achievement System
- Mini Task Scheduler

Runner improvements discussed:

- Stronger multi-file compilation model
- Clearer build and linker diagnostics
- Per-project compiler flags
- Temporary container workspaces
- Local volume/session restoration
- Explicit project cleanup after completion
- Optional stdin/terminal-style interactions
- File-I/O exercises inside isolated workspaces

The user should still press a single Run/Submit action; build-system and terminal commands should remain app-managed.

### Assessment Sections And Choice Rules

Sampled question banks are implemented, but richer exam structure is not.

Possible additions:

- Named sections
- Fixed questions plus sampled questions
- Sampling quotas by topic/type
- "Answer any three of four" sections
- Calculator-permitted section metadata
- Different instructions/timers per section
- Section-aware scoring and review

### Diagram And Graph Tooling

Current assessments can display images and already include generated graphs.

Discussed improvements:

- Reusable matplotlib templates for motion, vector, and integration diagrams
- Diagram metadata and source files beside exported images
- Consistent axes, labels, accessibility text, and sizing
- Media validation tooling
- Authoring workflow for hand-drawn or licensed external images

## Long-Term Candidates

### Broader SQLite Storage

SQLite currently stores attempts and grades. Authored content remains file-backed by design.

Possible future migrations:

- Settings
- Categories
- Areas
- Assessments
- Tags
- Templates
- Imported content packs

Any migration should preserve repository interfaces and support export back to portable files.

### CIR Study-System Integration

- CIR score fields by category/subcategory/result
- Friction and failure-mode tracking
- Remediation protocol links
- Recommended next assessment
- Weak-topic review queues
- Study-plan generation from local analytics
- Manual learner notes attached to attempts

### Local Semantic Free-Response Assistance

Free response currently uses reliable human self-check.

Discussed but intentionally postponed:

- Keyword or rubric assistance
- N-gram or embedding similarity
- Local retrieval-augmented reference material
- Small local model feedback

Any future implementation should assist review rather than silently assign authoritative grades until false-positive and false-negative behavior is well understood.

### Container And Infrastructure Learning

Potential extension of Guided Projects:

- Basic container orchestration exercises
- Serverless/IaC learning projects
- AWS-oriented labs
- Disposable cloud-simulation environments

These require stronger isolation, cost controls, credential handling, and cleanup guarantees before implementation.

### Frontend Decomposition And Polish

- Extract the monolithic Astro page into focused modules/components
- Shared API client and generated/shared contracts
- Dedicated assessment renderers
- Dedicated analytics and creator modules
- Dark mode
- More complete keyboard navigation
- Improved mobile layouts
- Accessibility audit
- Better loading, stale-data, and background-refresh states

Avoid a wholesale rewrite; extract incrementally along stable feature boundaries.

## Deliberately Deferred

These remain out of scope unless explicitly requested:

- Authentication
- Cloud synchronization
- Multi-user classrooms
- Public deployment
- Collaborative real-time authoring
- Payment features
- Mature role/permission systems
- LMS integrations
- Cloud-hosted code execution
- Fully automatic AI grading

## Maintenance Rule

When a planned feature is implemented:

1. Move it into the relevant Implemented section.
2. Leave any unfinished follow-up work under Near-Term, Medium-Term, or Long-Term.
3. Update `README.md` if the feature changes user-facing behavior.
4. Update `AGENTS.md` if it changes architecture, storage, validation, or agent workflow.
