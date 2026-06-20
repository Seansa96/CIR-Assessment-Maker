# Antigravity Implementation Plan: Attempt Cleanup, Free Response, and Adaptive Navigation

## Status

- **Audience:** Antigravity IDE agent
- **Project:** CIR Assessment Maker
- **Features:** Destructive Quit Early behavior, free-response progression fixes, and adaptive learning recommendations
- **Plan state:** Decision complete
- **Priority:** Implementation first; minimal verification only

Before implementation, read:

- `AGENTS.md`
- `GEMINI.md`
- `docs/agent-coexistence.md`
- Current attempt lifecycle, scoring, grade analytics, navigation catalog, and frontend assessment-session code

Check `git status --short` before editing. The worktree may already contain user, Codex, Gemini, circuit, assessment, SQLite, or runtime-state changes. Do not revert, overwrite, or clean unrelated work.

## Execution Constraints

- Prioritize a working vertical implementation over exhaustive testing.
- Do not run broad exploratory tests, repeated browser sessions, the full test suite, or unrelated refactors.
- Add only focused tests needed for the changed lifecycle, self-check, migration, and recommendation behavior.
- Run each required build or focused test command once after implementation.
- Preserve existing public endpoints where practical and keep migrations incremental and non-destructive except for the explicitly requested abandoned-attempt deletion.
- Do not add an external recommendation service, background worker, AI model, or new database provider.
- At completion, report changed files, commands run, checks passed or failed, and manual checks remaining for the user.

## Summary

Change unfinished-session behavior so `Quit Early` and starting another assessment permanently delete the active attempt after confirmation. `Save and Quit` remains the only way to retain unfinished progress.

Repair free-response self-check behavior so practice responses remain editable and a resolved `Needs Review` response can advance gated instructional assessments without being scored correct.

Replace the navigation's static first-item `Suggested` badge with topic-level recommendations based on completed learning activity and the two most recent eligible mastery attempts.

## Attempt Lifecycle

### Quit Early

- Replace frontend calls to the abandon endpoint with `DELETE /api/attempts/{attemptId}`.
- Show this confirmation immediately before deletion:

  > Quit this assessment early? This attempt and all unsaved progress will be permanently deleted.

- After successful deletion:
  - Clear `state.attempt`, `state.assessment`, `state.latestResults`, guided-project session state, and active editor/canvas state.
  - Reset the active-attempt chip and mode locks.
  - Show a concise deleted-attempt empty state.
  - Reload attempt history, grades, analytics, and recommendations.
- Do not create or display a replacement history row.

### Starting Another Assessment

- Apply the same behavior from both the classic picker and guided navigation.
- If the current attempt is `inProgress`:
  1. Warn that starting the selected assessment will permanently delete the current unsaved attempt.
  2. If declined, leave the current session and picker state unchanged.
  3. If confirmed, delete the current attempt and linked grade entry.
  4. Start the new assessment only after deletion succeeds.
- Do not warn when the previous attempt is paused, completed, deleted, or absent.
- Browsing categories, goals, activities, and assessments must not end the active session.

### Abandoned Compatibility And Cleanup

- Stop producing new `AttemptStatus.Abandoned` records.
- Remove `Abandoned` from frontend status labels, filters, chips, row actions, and review routing.
- Keep enum and deserialization compatibility temporarily so old files and rows can be read during migration.
- Change the existing abandon API endpoint to perform the same permanent deletion as the delete endpoint, preserving compatibility with stale clients without retaining an abandoned attempt.
- Add an idempotent SQLite startup migration:
  - delete grade entries linked to abandoned attempts
  - delete abandoned attempts
  - record completion in retention metadata
- Legacy JSON migration must skip attempts whose inferred or explicit status is abandoned.
- Do not remove the `abandoned_at` column or rewrite the full attempts table in this slice.

## Free-Response Self-Check

### Practice Mode Editing

- A submitted practice free response remains editable.
- Render the textarea populated with the saved response rather than the locked-response panel.
- If the learner edits and resubmits the text:
  - replace the saved response
  - set `selfCheckCorrect` back to `null`
  - require a new self-check decision
- Re-submitting identical text may also reset the self-check; use one consistent replacement path rather than comparing text.
- Continue showing expected answer, key points, explanation, and self-check controls after submission in practice mode.

### Scored Mode Locking

- During an active scored attempt, keep the submitted response locked.
- Do not reveal expected answers, explanations, key points, or self-check controls until completion.
- After completion, allow the existing self-check review flow.
- Continue blocking grade commit until every scored free response has a non-null self-check decision.

### Instructional Progression

Use two distinct concepts:

- **Correct:** `selfCheckCorrect == true`
- **Resolved:** a response exists and `selfCheckCorrect` is non-null

For Worked Examples, Concept Lesson checks, and any other correctness-gated instructional flow using self-check free response:

- Pending `null` blocks progression.
- `Mark Correct` resolves, advances, and counts correct.
- `Mark Needs Review` resolves, advances, and remains incorrect for results/analytics.
- Multiple-choice, select-all, numeric, symbolic, code, and circuit checks still require actual correctness.

Update all related logic consistently:

- backend section/step completion eligibility
- Worked Example automatic progression and completion
- current unlocked step calculation
- frontend `firstUnansweredIndex`
- Continue-button enabled state
- pause/resume and review rendering

Do not make `Needs Review` count as a correct answer or positive score.

## Adaptive Navigation Recommendations

### Public Contract

Add:

```http
GET /api/navigation/recommendations
```

Return one record per navigable topic:

```json
{
  "topicId": "u-sub-integration",
  "areaIds": ["integration"],
  "state": "review",
  "recommendedLearningGoal": "recall",
  "recommendedActivityTypes": ["mixedRecallSet", "clozeDrill"],
  "suggestedAssessmentIds": ["calc2-u-substitution-recall"],
  "completedLearnCount": 2,
  "completedRecallCount": 1,
  "eligibleMasteryAttemptCount": 2,
  "masteryPercent": 72.5,
  "provisionalMastery": false
}
```

Use string values:

- `learn`
- `recall`
- `practice`
- `review`
- `evaluate`

The endpoint must return an empty recommendation list, not fail, when no attempt data exists.

### Evidence Rules

Instructional completion counts:

- completed Concept Lessons
- completed Worked Examples
- completed Interactive Explorations

Recall completion counts:

- completed Recall Drills

Eligible mastery attempts:

- every completed scored quiz/test attempt, committed or uncommitted
- completed practice quiz/test attempts only when committed to the grade log

Exclude:

- uncommitted practice attempts
- instructional sessions
- recall drills
- paused/in-progress attempts
- abandoned/deleted attempts
- guided projects

Map an assessment result to every authored topic/subcategory ID on that assessment. Calculate recommendations independently for each topic.

### Recommendation State Machine

Apply these rules in order:

1. Fewer than two completed Learn sessions:
   - state `learn`
   - recommend Learn
2. Two or more Learn sessions and no completed Recall Drill:
   - state `recall`
   - recommend Recall
3. Recall completed and no eligible mastery evidence:
   - state `practice`
   - recommend Practice
4. Exactly one eligible mastery attempt:
   - below 80%: state `review`
   - at least 80%: state `practice` with `provisionalMastery: true`
5. Two or more eligible mastery attempts:
   - average only the two most recent eligible attempts
   - below 80%: state `review`
   - at least 80%: state `evaluate`

Review remediation:

- Find the most recent eligible attempt below 80%.
- If no Recall Drill was completed after that attempt, recommend Recall.
- If remedial Recall was completed after it, recommend Practice.
- Keep state `review` and show the Review badge until the latest-two eligible mastery average reaches 80%.

Area review state:

- An area receives a review count equal to the number of contained topics currently in `review`.
- Do not calculate a separate area mastery score in this slice.

### Availability Fallbacks

Recommendations must only reference activities and assessments available for that topic.

Fallback order:

- Learn: Concept Lesson → Guided Worked Example → Interactive Exploration
- Recall: Mixed Recall Set → Cloze Drill → Recognition Drill
- Practice: Focused Practice → Mixed Practice
- Review: Recall → Practice → Learn
- Evaluate: Mastery Check → Formal Test → Practice

If no assessment exists after applying the relevant fallback chain, return the recommendation state but leave suggested assessment IDs empty.

### Frontend Behavior

- Load recommendations independently from the navigation catalog.
- Recommendation failure must not break navigation; silently render without adaptive badges and retain normal tile behavior.
- Remove the current `index === 0` activity suggestion.
- Add badges:
  - `Suggested` on the recommended goal, activity, and assessment
  - `Review` on topics in review state
  - `Ready to Evaluate` on topics at 80% or higher using the latest-two rule
  - `Provisional` after one eligible result at 80% or higher
- Area tiles display a quiet `N topics need review` indicator when applicable.
- Recommendations guide only. Never disable other available goals, activities, or assessments.

## Focused Tests

Add narrowly scoped tests for:

### Attempt Lifecycle

- Quit Early permanently removes active memory state, SQLite state, guided-project files, and linked grade entries.
- Starting another assessment cancels cleanly when confirmation is declined.
- Confirmed replacement deletes the old attempt before creating the new attempt.
- Save and Quit still produces a resumable paused attempt.
- Startup cleanup removes abandoned attempts and linked grades idempotently.
- Legacy import skips abandoned attempts.

### Free Response

- Practice submission remains editable.
- Re-submission replaces text and resets self-check to pending.
- Scored response remains locked during the attempt.
- Needs Review resolves and advances a Worked Example step while remaining incorrect.
- Pending self-check continues blocking instructional progression.
- Pending scored self-check continues blocking grade commit.

### Recommendations

- Zero or one Learn completion suggests Learn.
- Two Learn completions suggest Recall.
- Recall completion with no mastery evidence suggests Practice.
- One score of at least 80% is provisional Practice.
- Latest-two average below 80% produces Review.
- Recall after the latest low score changes the Review recommendation from Recall to Practice.
- Latest-two average of at least 80% clears Review and suggests Evaluate.
- Uncommitted practice attempts do not affect mastery.
- Scored, uncommitted quiz/test attempts do affect mastery.
- Missing preferred activity follows the defined fallback order.

## Required Verification

Run only:

```powershell
dotnet build backend\QuizApp.sln --no-restore
dotnet test backend\QuizApp.sln --no-build --filter "AttemptDeletion|FreeResponse|Recommendation|AbandonedMigration"
npm run build
```

Perform one basic startup smoke check:

- start backend and frontend
- confirm recommendation endpoint returns
- confirm the frontend loads without crashing

Do not run:

- the full backend test suite
- broad browser automation
- repeated manual UI flows
- performance testing
- unrelated cleanup or refactoring

## Manual Checks For The User

Report these for user testing:

- Quit Early warning and permanent deletion
- replacing an active attempt from both navigation paths
- Save and Quit still resumes
- editable practice free response
- Needs Review progression in Worked Examples
- Learn → Recall → Practice recommendation progression
- Review and Ready to Evaluate badges
- recommendation behavior after two recent scores

## Assumptions

- Explicit Quit Early and replacement by a new assessment are destructive; browser/window closure is not changed.
- Existing abandoned attempts are permanently removed during migration.
- Latest-two eligible mastery attempts establish the 80% threshold.
- One score of at least 80% is provisional and does not recommend Evaluate yet.
- Recommendations are calculated locally on request with current SQLite/file-backed data.
- No authentication, external analytics service, AI recommendation engine, background worker, or SQLite replacement is added.
