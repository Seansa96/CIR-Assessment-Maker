# Antigravity Implementation Plan: Recall Drill Grade Weighting And Category Recommendations

## Status

- **Audience:** Antigravity IDE agent
- **Project:** CIR Assessment Maker
- **Primary goal:** Make recall drills contribute meaningfully to grade analytics and recommended next steps, while fixing category-level recommendation display
- **Priority:** Coherent analytics semantics, clear UI, and focused tests

Before editing, read:

- `AGENTS.md`
- `GEMINI.md`
- `docs/agent-coexistence.md`
- `backend/src/QuizApp.Core/Domain/AnalyticsModels.cs`
- `backend/src/QuizApp.Core/Domain/AttemptModels.cs`
- `backend/src/QuizApp.Core/Services/GradeAnalyticsService.cs`
- `backend/src/QuizApp.Core/Services/GradeLogService.cs`
- `backend/src/QuizApp.Core/Services/ScoringService.cs`
- `backend/src/QuizApp.Core/Services/NavigationRecommendationService.cs`
- `frontend/src/pages/index.astro`
- relevant tests in `backend/tests/QuizApp.Tests`

Check `git status --short` before editing. The worktree may contain active user or agent changes. Do not revert unrelated work.

Do not intentionally alter runtime state:

- `.cir-processes.json`
- `data/retention/quizapp.db`
- `data/project-sessions/`
- `data/attempts/`
- `data/grades/`
- `logs/`

## Current Problems

### 1. Recommended next steps are overview-only

`GradeAnalyticsSummary.ActionableNextSteps` is a single top-level list. It does not include category, area, topic, or source-skill metadata beyond `SkillId`.

The frontend renders `analytics.actionableNextSteps` only in the overview branch of `renderAnalyticsDashboard`. The category-specific branch renders category metrics, area table, and committed entries, but no next steps.

There is also a likely category-tab bug: the category branch uses `analytics.areas.filter(a => a.categoryId === state.activeAnalyticsCategory)`, but `AreaGradeAnalytics` does not currently define `categoryId`.

### 2. Recall drills do not affect official grades

`GradeLogService.CommitAttemptAsync` rejects `AssessmentType.RecallDrill` as an instructional session. The frontend also hides the commit action for recall drills.

Recall drill attempts still produce:

- recall rating analytics
- weak recall tags
- recall category/subcategory analytics
- attempt-history rows
- navigation recommendation evidence

But they currently have **zero official committed-grade weighting**.

### 3. Recall scoring semantics are split

Recall results currently treat `Easy` and `Correct` as correct, and `NeedsReview` / `ForgotCompletely` as not correct for percent scoring. Recall analytics separately use a 4/3/2/1 diagnostic scale.

This creates two meanings for the same rating set.

## Design Decision

Introduce one canonical recall scoring policy and use it consistently.

Recommended recall rating weights:

| Rating | Grade value | Meaning |
| --- | ---: | --- |
| `Easy` | `1.00` | Automatic recall; strong evidence of mastery. |
| `Correct` | `0.85` | Recalled correctly, but with some effort; solid but less fluent. |
| `NeedsReview` | `0.40` | Partial or fragile recall; useful evidence, but not mastery. |
| `ForgotCompletely` | `0.00` | No usable recall evidence. |
| `Unknown` | `0.00` | Unrated; should block completion/commit where applicable. |

Rationale:

- `Easy` deserves full credit because it represents fluent recall.
- `Correct` should be high but not identical to `Easy`; the learner got it, but it is not yet automatic.
- `NeedsReview` should receive partial credit because it often means recognition or partial reconstruction happened.
- `ForgotCompletely` should contribute no grade credit.

Use the same policy for:

- recall result percent
- recall grade-log commit percent
- recall analytics averages where a percentage is needed
- recommendation weakness thresholds

Keep the existing 4/3/2/1 scale only if the UI explicitly labels it as a diagnostic rating scale. Do not mix it with grade percent.

## Grade Weighting Policy

Recall drills should contribute to grades, but they should not overpower quizzes/tests.

Implement type-aware grade contribution in analytics:

| Assessment type | Recommended analytics weight |
| --- | ---: |
| `test` | `1.00` |
| `quiz` | `0.75` |
| `recallDrill` | `0.40` |
| other instructional types | `0.00` for official grade averages |

This means:

- recall drills can be committed or included as grade evidence
- recall drill scores count less than quiz/test performance
- official averages become weighted averages, not simple average of entries

Use `GradeLogEntry.EarnedPoints` and `PossiblePoints` where possible, but add an explicit analytics contribution weight if needed. Avoid silently pretending a 40-item recall drill is equivalent to a 40-question formal test.

## Backend Changes

### 1. Add canonical recall scoring helper

Add a small helper in Core, for example:

```csharp
public static class RecallScoringPolicy
{
    public static decimal GradeValue(RecallRating rating) => rating switch
    {
        RecallRating.Easy => 1.00m,
        RecallRating.Correct => 0.85m,
        RecallRating.NeedsReview => 0.40m,
        RecallRating.ForgotCompletely => 0.00m,
        _ => 0.00m
    };

    public static bool IsMastered(RecallRating rating) =>
        rating is RecallRating.Easy or RecallRating.Correct;

    public static bool IsWeak(RecallRating rating) =>
        rating is RecallRating.NeedsReview or RecallRating.ForgotCompletely;
}
```

Use this helper instead of duplicating switches.

### 2. Update recall result scoring

In `ScoringService.BuildRecallResults`:

- `earnedPoints` should sum `RecallScoringPolicy.GradeValue(item.Rating)` for rated items.
- `possiblePoints` should remain total authored items.
- `percentScore` should use weighted earned / possible.
- `correctCount` can remain `Easy + Correct` for display, but the percent must be weighted.
- `RecallDrillSummary` can keep counts unchanged.

### 3. Allow recall drills to be grade-log eligible

In `GradeLogService.CommitAttemptAsync`:

- remove `AssessmentType.RecallDrill` from the rejected instructional session list
- keep `workedExample`, `guidedProject`, `conceptLesson`, and `interactiveExploration` non-committable
- ensure recall drills must be complete before commit
- ensure unrated items block completion or commit

If recall drills already auto-complete only when all items are rated, document that in tests. If not, add the guard.

### 4. Add grade contribution weighting

Add a central grade contribution policy, for example:

```csharp
public static class GradeContributionPolicy
{
    public static decimal WeightFor(AssessmentType type) => type switch
    {
        AssessmentType.Test => 1.00m,
        AssessmentType.Quiz => 0.75m,
        AssessmentType.RecallDrill => 0.40m,
        _ => 0.00m
    };
}
```

Use it when computing:

- overall committed average
- category averages
- subcategory averages
- area averages

Recommended weighted formula:

```text
weighted average =
  sum(percentScore * contributionWeight)
  / sum(contributionWeight)
```

If the app should also account for item count, use:

```text
effectiveWeight = contributionWeight * max(1, possiblePoints)
```

Choose one policy and apply it consistently. Recommended v1: use `contributionWeight * max(1, possiblePoints)` so larger quizzes/tests matter more, while recall drills remain dampened.

### 5. Extend `ActionableNextStep`

Add category/topic context so the frontend can render category-specific next steps without guessing.

Recommended shape:

```csharp
public sealed record ActionableNextStep(
    string SkillId,
    string Message,
    string RecommendedAssessmentId,
    string RecommendedAssessmentTitle,
    string? CategoryId,
    string? CategoryTitle,
    IReadOnlyList<string> AreaIds,
    IReadOnlyList<string> AreaTitles,
    IReadOnlyList<string> TopicIds,
    IReadOnlyList<string> TopicTitles,
    string Source,
    decimal? EvidencePercent);
```

`Source` examples:

- `skillPerformance`
- `recallWeakTag`
- `lowCategoryAverage`
- `lowTopicAverage`

Keep JSON property names camelCase through existing serializer behavior.

### 6. Include recall weakness in actionable next steps

Update `GradeAnalyticsService.BuildActionableNextSteps` so it considers:

- weak skill performance from quiz/test/worked-example checks
- weak recall tags
- weak recall category/subcategory groups
- low category/subcategory/area committed averages

For recall-specific recommendations:

- `ForgotCompletely` or heavy `NeedsReview` should prioritize recall drills if available
- if no recall drill exists, fall back to concept lesson or worked example
- if recall is decent but quiz/test score is weak, prioritize practice/worked example

Suggested rule:

```text
if recall tag weak count is high and average recall grade < 70:
  recommend recall activity for that topic/tag
else if skill/question performance < 60:
  recommend concept lesson
else if skill/question performance < 80:
  recommend worked example or focused practice
```

Avoid producing duplicate recommendations for the same recommended assessment.

### 7. Make category-level next steps available

Either:

- return one enriched `ActionableNextSteps` list with category/topic metadata and let the frontend filter it, or
- add grouped fields:

```csharp
IReadOnlyList<CategoryActionableNextSteps> CategoryActionableNextSteps
```

Recommended v1: enrich the existing list and filter on the frontend. This is additive and simpler.

### 8. Fix category-area filtering

`AreaGradeAnalytics` should include category context, or the frontend should derive it from assessment rows.

Recommended backend change:

```csharp
public sealed record AreaGradeAnalytics(
    string AreaId,
    string AreaTitle,
    IReadOnlyList<string> CategoryIds,
    int AttemptCount,
    decimal AveragePercent,
    string? WeakestSubcategoryId,
    string? WeakestSubcategoryTitle);
```

Then update frontend TypeScript and filtering.

## Frontend Changes

### 1. Show next steps in category tabs

In the category branch of `renderAnalyticsDashboard`:

- filter `analytics.actionableNextSteps` by `categoryId`
- render the same card/list UI as overview
- if no category-specific recommendations exist, show a compact empty state

Example:

```text
Recommended Next Steps for Physics 1 w/ Calculus
- Recall Work-Energy theorem definitions
- Practice Work-Energy theorem applications
```

### 2. Show recall contribution clearly

Update grade-log wording so users understand recall drills affect grades differently.

Possible UI labels:

- `Recall score: 82% weighted`
- `Recall Drill · 40% grade weight`
- `Easy=100%, Correct=85%, Needs Review=40%, Forgot=0%`

Do not make the UI feel punitive. Frame recall weighting as memory evidence.

### 3. Allow recall drill commit action

In attempt history:

- allow `Commit` for completed recall drills
- keep commit disabled if any recall item is unrated
- preserve non-committable behavior for worked examples, guided projects, concept lessons, and interactive explorations

In results:

- recall drills should show a commit button when completed and not already committed
- results should show weighted percent and rating counts

### 4. Update overview tables

If official averages now include recall:

- add a note or chip near overall average: `Includes weighted recall drills`
- keep separate recall analytics tables, because they answer a different question than grades

## Tests

Add focused tests only.

### Backend scoring tests

- recall drill with `Easy`, `Correct`, `NeedsReview`, `ForgotCompletely` scores weighted percent correctly
- `Correct` is less than `Easy`
- `NeedsReview` contributes partial credit
- `ForgotCompletely` contributes zero
- unrated recall item does not count as earned

### Grade-log commit tests

- completed recall drill can be committed
- incomplete/unrated recall drill cannot be committed
- worked example/guided project/concept lesson/interactive exploration still cannot be committed
- committed recall drill stores weighted earned/possible points

### Analytics tests

- overall committed average includes recall drills using recall contribution weight
- category average includes recall drills in the correct category
- area/subcategory averages include recall drills in the correct mapping
- recall drill does not count as full test-equivalent weight
- category-specific actionable next steps include matching category recommendations
- recall weak tags can generate a recommended next step
- duplicate recommendation targets are collapsed

### Navigation recommendation tests

- completed recall drills still count as recall progress evidence
- low recall rating after weak quiz/test can recommend recall
- decent recall plus low quiz/test can recommend practice

### Frontend build/manual checks

Run:

```powershell
Set-Location frontend
npm run build
```

Manual smoke checks:

- complete a recall drill with mixed ratings
- verify weighted recall percent appears
- commit recall drill
- verify overall and category analytics change
- open that category tab and verify recommended next steps appear
- verify non-recall instructional sessions still cannot be committed

## Minimum Verification

Run:

```powershell
dotnet build backend\QuizApp.sln --no-restore
dotnet test backend\QuizApp.sln --no-build --filter "Recall|GradeAnalytics|GradeLog|NavigationRecommendation"
```

If frontend changed:

```powershell
Set-Location frontend
npm run build
```

Do not run broad exploratory browser automation unless a focused failure requires it.

## Acceptance Criteria

The work is complete when:

- recall drills have one canonical weighted scoring policy
- recall drill results use weighted percent
- completed recall drills can be committed
- unrated/incomplete recall drills cannot be committed
- recall drills contribute to overall, category, subcategory, and area grade analytics with dampened assessment-type weight
- category tabs display relevant recommended next steps
- recommendation generation considers weak recall tags/ratings
- grade-log UI communicates recall weighting clearly
- existing non-recall instructional sessions remain non-committable
- focused backend tests pass
- frontend build passes

## Completion Report

Report:

- files changed
- recall rating weights implemented
- grade contribution weights implemented
- analytics fields added or changed
- recommendation rules changed
- commands run and results
- manual checks performed
- any remaining limitations or follow-up recommendations

## Deferred Work

Do not implement in this slice:

- spaced repetition scheduling
- SM-2 or Anki-style due dates
- AI grading
- user-specific profiles
- long-term memory decay modeling
- search/recommendation personalization beyond current local attempt history

