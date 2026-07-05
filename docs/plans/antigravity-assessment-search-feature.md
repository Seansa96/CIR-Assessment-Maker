# Antigravity Implementation Plan: Assessment Search And Filter

## Status

- **Audience:** Antigravity IDE agent
- **Project:** CIR Assessment Maker
- **Primary goal:** Add a lightweight, responsive assessment search feature for the growing SQLite assessment catalog
- **Priority:** Working vertical slice, fast local search, useful filters, and clean integration with the existing segmented navigator

Before editing, read:

- `AGENTS.md`
- `GEMINI.md`
- `docs/agent-coexistence.md`
- `backend/src/QuizApp.Core/Domain/NavigationModels.cs`
- `backend/src/QuizApp.Infrastructure/Retention/SqliteRetentionInitializer.cs`
- `backend/src/QuizApp.Infrastructure/Retention/SqliteAssessmentCatalogImporter.cs`
- `backend/src/QuizApp.Infrastructure/Retention/SqliteNavigationCatalogService.cs`
- `backend/src/QuizApp.Api/Program.cs`
- `frontend/src/pages/index.astro`
- `frontend/src/styles/global.css`

Check `git status --short` before editing. The worktree may contain active Codex or user changes. Do not revert or rewrite unrelated work.

Do not alter runtime state intentionally, especially:

- `.cir-processes.json`
- `data/retention/quizapp.db`
- `data/project-sessions/`
- `data/attempts/`
- `data/grades/`
- `logs/`

## Execution Constraints

- Prioritize a working vertical slice over a large search platform.
- Use the existing SQLite assessment catalog as the search source.
- Keep YAML/JSON as the authored source of truth.
- Do not add a remote search service, vector database, embeddings, AI search, or cloud dependency.
- Do not load and parse all assessment YAML on every keystroke.
- Do not block existing guided navigation or classic picker if search fails.
- Keep all SQL parameterized.
- Keep results deterministic and explainable enough to debug.
- Add focused backend tests and run minimum build checks.
- Avoid broad exploratory browser testing.

## User Experience Goal

A user should be able to narrow to a subject, type a partial idea, and immediately see likely targets.

Example:

1. User filters to `Physics 1 w/ Calculus`.
2. User types `wor`.
3. Before pressing Enter, the UI shows likely matches:
   - Work and energy topics
   - Work-energy theorem assessments
   - Work-related tags/skills
   - matching quizzes, worked examples, recall drills, concept lessons, and tests
4. As the query becomes `work energy`, title and topic matches remain strongest, but tags/skills help break close ties.

## Search Scope

Search should cover:

- assessment title
- assessment ID
- assessment type
- subject/category title
- area title and description
- topic/subcategory title and description
- `navigation.learningGoal`
- `navigation.activityType`
- `navigation.tags`
- `assessment_skills`

Optional v1.1 search fields:

- question prompts
- worked-example titles/problems/step titles
- recall item prompts
- concept lesson section titles

Do not include full explanation bodies in the first implementation unless it is cheap and measured, because long explanation text can drown title/topic/tag intent.

## Filters

Support these filters in v1:

- subject/category
- area
- topic/subcategory
- learning goal
- activity type
- assessment type
- tag
- skill

Optional v1.1 filters:

- item/question count range
- has media
- has code questions
- has symbolic responses
- recently attempted
- weak/review recommended

Do not implement full saved searches or recommendation logic in this slice.

## Backend Design

### Contracts

Add request/response models in Core or API contracts.

Recommended query:

```csharp
public sealed record AssessmentSearchRequest(
    string? Query,
    string? SubjectId,
    string? AreaId,
    string? TopicId,
    string? LearningGoal,
    string? ActivityType,
    string? AssessmentType,
    IReadOnlyList<string>? Tags,
    IReadOnlyList<string>? Skills,
    int Limit = 25);
```

Recommended result:

```csharp
public sealed record AssessmentSearchResult(
    string Id,
    string Title,
    AssessmentType AssessmentType,
    string SubjectId,
    string SubjectTitle,
    IReadOnlyList<string> AreaIds,
    IReadOnlyList<string> AreaTitles,
    IReadOnlyList<string> TopicIds,
    IReadOnlyList<string> TopicTitles,
    string LearningGoal,
    string ActivityType,
    IReadOnlyList<string> Tags,
    IReadOnlyList<string> Skills,
    int QuestionCount,
    int AuthoredQuestionCount,
    int? AttemptQuestionCount,
    decimal Score,
    IReadOnlyList<string> MatchedFields,
    string? Snippet);
```

Recommended suggestion result:

```csharp
public sealed record AssessmentSearchSuggestion(
    string Kind,      // assessment, topic, area, tag, skill
    string Id,
    string Label,
    string? SubjectId,
    int Count,
    decimal Score);
```

### Endpoints

Add endpoints:

```http
GET /api/search/assessments?q=&subjectId=&areaId=&topicId=&learningGoal=&activityType=&assessmentType=&tag=&skill=&limit=25
GET /api/search/suggestions?q=&subjectId=&areaId=&topicId=&limit=12
```

Use `GET` query parameters for easy browser/debug use. If the query grows unwieldy later, add a `POST` endpoint additively.

Failure behavior:

- If the SQLite catalog is unavailable, return `503 SEARCH_UNAVAILABLE` with a clear message.
- The frontend should fall back to normal navigation/classic picker.
- Do not silently return empty results on infrastructure errors.

## SQLite Search Index

Use SQLite FTS5 when available. It is the best fit for local-first, in-process, lightweight catalog search.

Add search tables in `SqliteRetentionInitializer`.

Recommended schema:

```sql
CREATE VIRTUAL TABLE IF NOT EXISTS assessment_search_fts
USING fts5(
    assessment_id UNINDEXED,
    title,
    normalized_title,
    assessment_type,
    subject_title,
    area_titles,
    topic_titles,
    learning_goal,
    activity_type,
    tags,
    skills,
    prompt_terms,
    tokenize = 'unicode61 remove_diacritics 2'
);
```

Add a small non-FTS term table for fast suggestions and fuzzy correction:

```sql
CREATE TABLE IF NOT EXISTS assessment_search_terms (
    term TEXT NOT NULL,
    normalized_term TEXT NOT NULL,
    kind TEXT NOT NULL,
    source_id TEXT NOT NULL,
    subject_id TEXT NULL,
    weight INTEGER NOT NULL,
    PRIMARY KEY (normalized_term, kind, source_id)
);
```

Indexes:

```sql
CREATE INDEX IF NOT EXISTS idx_assessment_search_terms_prefix
ON assessment_search_terms(normalized_term);

CREATE INDEX IF NOT EXISTS idx_assessment_search_terms_subject
ON assessment_search_terms(subject_id);
```

If FTS5 is not available in the bundled SQLite provider, fall back to:

- normalized columns
- `LIKE @prefix || '%'`
- `LIKE '%' || @query || '%'`
- C# re-ranking over the top 200 candidate rows

Do not fail the application solely because FTS5 is unavailable.

## Index Population

Populate search rows during assessment catalog import/upsert.

For every active assessment, index:

- title
- ID split into readable tokens
- assessment type label
- subject title
- area titles/descriptions
- topic titles/descriptions
- learning goal and activity type labels
- navigation tags
- assessment skills
- optional prompt terms from questions/items/sections

When an assessment becomes inactive, remove or ignore its search rows.

When an assessment is upserted, delete old search rows for that assessment and insert the fresh version in the same transaction as the catalog relationship rows if practical.

Do not index invalid/rejected source files.

## Normalization

Add a small normalizer used by both indexer and search:

- lowercase
- trim
- collapse whitespace
- remove common punctuation
- split kebab-case and snake_case
- normalize plural-ish surface forms only lightly, if at all
- preserve math terms like `u-sub`, `p-test`, `work-energy`, and `dy/dx` as searchable tokens where possible

Do not use aggressive stemming in v1. STEM content has terms where small changes matter.

## Ranking Model

Use a simple weighted model that is easy to tune.

Recommended ranking order:

1. exact assessment title match
2. title prefix match
3. title token prefix match
4. topic title match
5. area title match
6. tag/skill exact or prefix match
7. subject title match
8. prompt-term match
9. fuzzy term match

For FTS results:

- use SQLite FTS/BM25 for initial candidate scoring
- apply a C# boost/re-rank for title/topic/tag/skill matches
- limit the candidate set before re-ranking, for example top 200

For fuzzy suggestions:

- implement a bounded Levenshtein distance helper in C#
- run it only against the small `assessment_search_terms` table candidate set
- avoid running Levenshtein across full assessment bodies
- for short queries like `wor`, prioritize prefix matches over fuzzy matches
- for longer queries, allow edit distance 1 or 2 depending on length

Tie-breakers:

- exact/prefix title beats tags
- tags/skills beat prompt-term matches
- selected subject/area/topic filters boost in-domain matches
- lower edit distance wins
- shorter matched term wins for suggestions
- stable final tie-break by title

## Frontend Design

Add a compact search section to the segmented navigation area, above or near the subject/area/topic flow.

UI elements:

- search input with placeholder like `Search assessments, topics, tags, skills...`
- clear button
- compact filter chips for subject, area, topic, learning goal, activity type, assessment type, tags, and skills
- suggestions dropdown while typing
- result list when query or filters are active
- empty state with useful wording
- error state that keeps normal navigator usable

Behavior:

- debounce input by about 150 to 250 ms
- minimum query length of 1 for prefix suggestions
- show suggestions before Enter
- pressing Enter should run/focus the full results list
- selecting a suggestion should either apply a filter or set the query, depending on kind
- selecting an assessment should reuse the existing `selectNavigationStage` and `startNavigationAttempt` flow
- browsing search results must not terminate or overwrite an active attempt
- if an attempt is active, keep the compact active-session navigation behavior

Result card content:

- title
- assessment type
- subject / area / topic breadcrumb
- learning goal and activity type
- item count
- matching tags/skills
- optional snippet or matched fields

Keep cards scan-friendly. This should feel like finding a known item quickly, not like a full search-engine page.

## Filter Interaction

Filters should compose with the existing navigation selection.

Rules:

- If a subject is selected in guided navigation, default search filter to that subject.
- If user explicitly clears the subject filter, search all subjects.
- If area is selected, topic options should only include topics in that area.
- If query is empty but filters are active, show filtered results.
- If query and filters are empty, show normal segmented navigation rather than a giant all-assessments list.

Preserve future hooks for saved search and recommendations, but do not build them now.

## Performance Requirements

Target behavior:

- suggestion response under 100 ms for the current local catalog on a typical desktop
- full search response under 200 ms for the current local catalog
- no YAML parsing during search
- no full `definition_json` parse during every keypress unless prompt-term indexing was deferred and the result set is already small
- query is capped by `limit`, default 25, max 100

Implementation notes:

- precompute indexed text during catalog import
- use SQLite indexes and FTS
- re-rank only bounded candidate sets
- debounce frontend calls
- abort stale frontend requests with `AbortController`
- cache the latest query/filter result in memory only if simple

## Tests

Add focused tests only.

Backend tests:

- search normalizer splits title, tags, skills, and kebab-case IDs predictably
- Levenshtein helper returns expected distances and respects max distance cutoff
- search ranks exact title above tag-only matches
- search ranks title prefix above fuzzy title match
- search can find by tag
- search can find by skill
- search can filter by subject
- search can filter by area
- search can filter by topic
- search can filter by learning goal/activity type
- search can filter by assessment type
- suggestions return prefix topic/tag/title matches for `wor`
- inactive assessments are not returned
- catalog unavailable returns a controlled unavailable result/error

SQLite tests:

- FTS index is created or fallback mode is detected cleanly
- importer/upsert populates search rows
- importer removes/replaces stale search rows on update
- missing/inactive assessment does not appear in search

Frontend checks:

- `npm run build`
- manual smoke test:
  - load app
  - filter to Physics
  - type `wor`
  - confirm work-related suggestions/results appear
  - select a result
  - start the assessment through the existing attempt flow
  - clear search and return to normal navigation

Do not add broad browser automation in this slice.

## Implementation Order

1. Add Core search contracts and search service interface.
2. Add SQLite search schema and fallback detection.
3. Add search index population to catalog import/upsert.
4. Add normalizer and bounded Levenshtein helper.
5. Add SQLite search service with filters and ranking.
6. Add `/api/search/assessments` and `/api/search/suggestions`.
7. Add focused backend tests.
8. Add frontend search state, input, suggestions, filters, and results.
9. Wire result selection into the existing assessment loading/starting flow.
10. Add CSS for compact, tactile search controls consistent with the current navigation UI.
11. Run focused checks and one manual smoke test.

## Minimum Verification

Run:

```powershell
dotnet build backend\QuizApp.sln --no-restore
dotnet test backend\QuizApp.sln --no-build --filter "Search|AssessmentCatalog"
```

If frontend changed:

```powershell
Set-Location frontend
npm run build
```

Do not run long exploratory suites unless a focused failure requires it.

## Acceptance Criteria

The feature is complete when:

- users can search assessments by title
- users can search by topic, area, tag, and skill
- partial queries produce useful suggestions before Enter
- subject, area, topic, goal, activity, assessment type, tag, and skill filters work
- ranking prioritizes closest literal title/topic matches, then tag/skill matches
- fuzzy suggestions catch near-misses without overwhelming exact prefix results
- search uses SQLite catalog/index data rather than reparsing YAML at query time
- inactive or invalid catalog rows are not returned
- current guided navigation and classic picker still work
- active assessment sessions are not disrupted by browsing search
- focused backend tests pass
- frontend build passes

## Completion Report

Report:

- files changed
- schema/tables added
- endpoints added
- ranking rules implemented
- filters implemented
- commands run and results
- whether SQLite FTS5 is active or fallback mode is used
- manual checks performed
- limitations deferred to later work

## Deferred Work

Leave these out of v1:

- semantic/vector search
- AI-generated query expansion
- saved searches
- search analytics
- cross-user popularity ranking
- cloud search services
- deep full-text search over every explanation paragraph
- typo correction beyond bounded Levenshtein suggestions
- recommendation logic changes

