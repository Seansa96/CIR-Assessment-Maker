# Antigravity Implementation Plan: Multipart Questions and Compact Active Navigation

## Status

- **Audience:** Antigravity IDE agent
- **Project:** CIR Assessment Maker
- **Features:** Multipart evaluation questions and compact navigation during active assessments
- **Plan state:** Decision complete
- **Priority:** Working vertical slice with focused verification

Before implementation, read:

- `AGENTS.md`
- `GEMINI.md`
- `docs/agent-coexistence.md`
- `docs/assessment-yaml-latex.md`
- The current question schema, validator, attempt service, scoring service, SQLite retention, and frontend question-rendering code
- `docs/plans/antigravity-attempt-cleanup-free-response-adaptive-navigation.md`

Check `git status --short` before editing. Do not revert or overwrite unrelated work in the dirty worktree.

## Execution Constraints

- Prioritize implementation over broad testing or unrelated refactoring.
- Add only focused multipart validation, scoring, persistence, and UI tests.
- Do not run the complete test suite or repeated exploratory browser testing.
- Preserve existing assessment files and API behavior additively.
- Do not add multipart authoring to the frontend creator in this slice.
- At completion, report changed files, commands run, results, and remaining manual checks.

## Summary

Add `type: multipart` for quiz and test assessments. A multipart question contains an authored, fixed-order list of parts, and each part reuses an existing question type.

The parent multipart question contributes exactly one point to the assessment. Each required part contributes an equal fraction of that point, providing proportional credit.

Multiple-choice cards inside each part use the existing deterministic per-attempt randomizer. Part order remains authored and static.

When an assessment session is active, replace the large navigation-selection flow with a compact Subject -> Area -> Topic breadcrumb and a `Change Assessment` action so the assessment viewport begins near the active content.

## Multipart Schema

Add `QuestionType.Multipart` with YAML/JSON wire value:

```yaml
type: multipart
```

Example:

```yaml
- id: q004
  type: multipart
  prompt: |
    Analyze the particle's motion over the interval.
  parts:
    - id: a
      type: multipleChoice
      prompt: Which expression gives the velocity?
      choices:
        - id: derivative
          text: '$v(t)=s''(t)$'
        - id: integral
          text: '$v(t)=\int s(t)\,dt$'
      answer:
        choiceId: derivative
      explanation: |
        Velocity is the derivative of position.

    - id: b
      type: symbolicResponse
      prompt: Find the velocity function.
      answer:
        expectedLatex: '3t^2-4t'
        equivalenceMode: expression
        variables:
          - t
        tolerance: 0.000001
      explanation: |
        Differentiate each term of the position function.

    - id: c
      type: numericResponse
      prompt: Find the velocity at $t=2$.
      answer:
        value: 4
        tolerance: 0.001
      explanation: |
        Substitute $t=2$ into the velocity function.
  explanation: |
    The parts connect interpretation, symbolic differentiation, and evaluation.
```

### Domain Types

- Add `QuestionDefinition.Parts`, defaulting to an empty list.
- Add `MultipartPartDefinition` with:
  - stable part ID
  - question type
  - prompt
  - choices
  - answer
  - explanation
  - media
  - code and circuit definitions where applicable
- Reuse the same shape and validation behavior as `QuestionDefinition`, but do not permit nested `multipart` parts in V1.
- Parent multipart questions require:
  - ID
  - prompt
  - at least two parts
  - unique part IDs within the parent
  - optional parent explanation/media
- Parent `choices` and `answer` remain empty/default because scoring belongs to the parts.

### Supported Parts

Allow all currently implemented answer-bearing question types:

- `multipleChoice`
- `selectAll`
- `freeResponse`
- `numericResponse`
- `symbolicResponse`
- `code`
- `circuit`

Reject:

- `multipart` nested inside multipart
- unknown question types
- instructional-only structures such as Worked Example containers or Recall Drill items

Restrict top-level multipart questions to `assessmentType: quiz` and `assessmentType: test`. Validation must reject multipart questions in Worked Examples, Concept Lessons, Interactive Explorations, Recall Drills, and other assessment types.

## Submission, Evaluation, and Persistence

### Submitted Answer

Extend `SubmittedAnswer` additively:

```csharp
IReadOnlyList<SubmittedAnswer> PartAnswers
```

- The parent submission uses the parent question ID.
- Each nested submission uses its part ID as `QuestionId`.
- Require exactly one submission per authored part ID.
- Reject duplicate, missing, or unknown part IDs.
- Preserve compatibility by defaulting `PartAnswers` to an empty list for existing JSON and SQLite records.

### Evaluation

Extend `AnswerEvaluation` with:

```csharp
decimal EarnedPoints
decimal PossiblePoints
IReadOnlyList<AnswerEvaluation> PartEvaluations
```

Defaults for existing question types:

- correct: `1 / 1`
- incorrect or unresolved: `0 / 1`

Multipart evaluation:

- Parent `PossiblePoints` is always `1`.
- Each required part has equal weight: `1 / partCount`.
- Parent `EarnedPoints` is the sum of earned part fractions.
- Parent `IsCorrect` is true only when every part is correct.
- Each part retains its normal correctness, feedback, expected answer, code feedback, symbolic feedback, and circuit feedback.

Example with three parts:

- three correct: `1.0`
- two correct: `0.6667`
- one correct: `0.3333`
- none correct: `0`

Use full decimal precision internally and round only percentages for display.

### Asynchronous Scoring

Move single-question evaluation behind one reusable asynchronous scoring method so multipart parts can invoke the same backend-authoritative pipelines as top-level questions:

- regular scoring
- code runner
- symbolic engine
- circuit scorer

Do not duplicate code/symbolic/circuit scoring logic inside the multipart branch.

### Free-Response Parts

- Follow the free-response behavior defined in the attempt-cleanup/free-response plan.
- A pending self-check part contributes zero points and marks the parent as pending review.
- Recalculating a part's self-check recalculates the parent earned points.
- Grade commit remains blocked while any multipart free-response part is pending.

### Results and Grade Log

Extend `QuestionResult` with nested `PartResults`.

Extend attempt and grade results with:

```csharp
decimal EarnedPoints
decimal PossiblePoints
```

- `PercentScore` must use total earned points divided by total possible points.
- Every ordinary top-level question contributes one possible point.
- Every multipart parent contributes one possible point regardless of part count.
- Retain existing integer `CorrectCount` and `TotalQuestions` for compatibility:
  - `CorrectCount` counts fully correct top-level questions.
  - `TotalQuestions` counts top-level questions.
- Add decimal earned/possible columns to grade-log persistence through an additive SQLite migration.
- Backfill legacy grade rows using `correct_count` and `total_questions`.
- Existing JSON/SQLite attempts without part data must continue loading.

## Choice Randomization

- Keep multipart part order exactly as authored.
- For a multiple-choice part, use the existing seeded Fisher-Yates helper.
- Seed with:

```txt
{attemptId}:{parentQuestionId}:{partId}
```

- Preserve stable authored choice IDs for scoring.
- Display letters and keyboard shortcuts follow the randomized visual positions.
- The order must remain stable through:
  - submission
  - practice feedback
  - scored navigation
  - previous/next navigation
  - dev refresh
  - Save and Quit / resume
  - result review
- Do not randomize select-all choices or multipart part order in V1.

## API and Attempt Flow

- Keep the existing answer-submission endpoint:

```http
POST /api/attempts/{attemptId}/answers
```

- Accept nested `partAnswers` in the request contract.
- Validate the complete multipart submission before mutating attempt state.
- Store one parent `AttemptAnswer` containing the nested submissions and nested evaluation.
- Re-submission replaces the complete parent answer.
- Quiz/test completion and grade commit use parent-level possible points, not raw part count.
- Assessment summaries and `attemptQuestionCount` continue counting the multipart parent as one authored question.
- Question-type analytics should include `multipart` as a top-level type and may additionally expose contained part types when building diagnostic filters. Do not count parts as separate assessment-history rows.

## Frontend Multipart Experience

- Render the parent prompt and media once.
- Render parts in authored order with clear labels:
  - `Part A`
  - `Part B`
  - `Part C`
- Reuse existing controls for each part, scoped to that part's container.
- Avoid duplicate DOM IDs by generating part-qualified IDs for:
  - forms and inputs
  - CodeMirror mounts
  - MathLive fields
  - circuit mounts
  - self-check controls
- Submit the parent multipart question with one `Submit Answer` action.
- Validate required client input and focus the first incomplete part before sending.
- Practice mode:
  - show per-part correctness and explanation after submission
  - show earned credit such as `2 of 3 parts correct - 0.67 / 1 point`
- Scored mode:
  - hide correctness, expected answers, and explanations until completion
- Result review:
  - show parent earned points
  - show every part's submitted answer and feedback

Keyboard answer shortcuts must apply to the currently focused or active part only. Clicking a part makes it the active shortcut scope.

## Compact Active Navigation

### Active Session State

When `state.attempt.status` is `inProgress`:

- Hide the Subject, Area, Topic, Learning Goal, Activity Type, and Assessment tile stages.
- Hide the classic picker.
- Replace them with a compact bar containing:
  - Subject
  - Area
  - Topic
  - assessment title
  - current mode
  - `Change Assessment` button
- Keep the assessment workspace immediately below the compact bar.
- After starting or resuming an attempt, scroll the assessment workspace into view using `scrollIntoView({ block: "start", behavior: "smooth" })`.
- Do not repeatedly auto-scroll during ordinary question navigation or answer submission.

### Change Assessment

- `Change Assessment` expands/restores the complete navigation flow without ending the current attempt.
- Browsing does not delete, pause, or replace the attempt.
- Starting another assessment delegates to the destructive replacement confirmation defined in `antigravity-attempt-cleanup-free-response-adaptive-navigation.md`.
- Cancelling that confirmation keeps the existing session and returns to its compact active-navigation state.

### Other Attempt States

- Paused, completed, deleted, or absent attempts show the normal full navigator.
- Reviewing a completed attempt uses a compact breadcrumb but labels the mode as `Review`; it does not expose a destructive replacement warning.
- Mobile layout wraps breadcrumb segments and keeps `Change Assessment` visible without increasing the page width.

## Focused Tests

### Backend

- YAML and JSON round-trip preserve multipart parts.
- Validation accepts quiz/test multipart questions.
- Validation rejects duplicate part IDs, fewer than two parts, unknown part types, nested multipart, and multipart in unsupported assessment types.
- A three-part parent earns `0`, `1/3`, `2/3`, or `1` point correctly.
- Parent `IsCorrect` is true only when all parts are correct.
- Code, symbolic, numeric, multiple-choice, and self-check parts reuse their authoritative scorers.
- Pending multipart self-check blocks grade commit.
- Attempt and SQLite round-trip preserve nested submissions and evaluations.
- Legacy attempts and grades load with point fields derived from integer counts.
- A multipart parent counts as one question for sampling and assessment summaries.

### Frontend

- All part controls render without duplicate IDs.
- Multiple-choice choices vary across attempts and remain stable within one attempt.
- Part order never changes.
- Keyboard shortcuts affect only the active part.
- Practice feedback displays per-part and parent credit.
- Scored mode hides multipart feedback until completion.
- Save/resume restores all part responses.
- Starting or resuming collapses navigation to the compact breadcrumb.
- Change Assessment restores navigation without ending the session.

## Required Verification

Run only:

```powershell
dotnet build backend\QuizApp.sln --no-restore
dotnet test backend\QuizApp.sln --no-build --filter "Multipart|PointScoring|CompactNavigation"
npm run build
```

Perform one smoke flow:

- load a quiz containing one multipart question
- answer some but not all parts correctly
- confirm proportional credit
- navigate away and back
- Save and Quit, resume, and confirm stable choices/responses
- confirm compact navigation and Change Assessment behavior

Do not run broad exploratory testing, the complete backend suite, repeated browser automation, or unrelated cleanup.

## Example Content

Add one small schema-authored quiz fixture or production sample containing:

- one ordinary multiple-choice question
- one multipart question with:
  - multiple-choice part
  - symbolic or numeric part
  - free-response self-check part

Use it for focused validation and smoke testing. Do not add multipart support to the frontend assessment creator.

## Assumptions

- Multipart is evaluation-only in V1 and supported only by quizzes and tests.
- Every multipart parent is worth exactly one point.
- Parts have equal weight and provide proportional credit.
- Part order is fixed.
- Only multiple-choice card order is randomized.
- Nested multipart questions are not supported.
- Existing integer correct/question counts remain available for compatibility, while decimal earned/possible points become authoritative for percentages.
- The full navigation flow remains accessible through `Change Assessment`.
