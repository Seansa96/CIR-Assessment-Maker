# Antigravity Implementation Plan: Assessment Taxonomy Validation And SQLite Ingest Diagnostics

## Status

- **Audience:** Antigravity IDE agent
- **Project:** CIR Assessment Maker
- **Priority:** Correct authored taxonomy first, then make future failures loud
- **Scope:** Assessment/category/area validation, SQLite catalog ingest, diagnostics,
  and targeted Chemistry/Physics/Calculus 2 migration
- **Incident reference:** `docs/agent-reports/assessment-taxonomy-ingest-incident.md`

Before editing, read:

- `AGENTS.md`
- `GEMINI.md`
- `docs/agent-coexistence.md`
- `docs/agent-reports/assessment-taxonomy-ingest-incident.md`
- `skills/assessment-question-pipeline/SKILL.md`
- current category, area, assessment DTO, validator, importer, and catalog service
  implementations

Check `git status --short`. Do not alter runtime state, especially
`data/retention/quizapp.db`.

## Execution Constraints

- Prioritize implementation and deterministic diagnostics over broad refactoring.
- Keep YAML/JSON as the authored source of truth.
- Keep SQLite as the runtime catalog after successful validation/import.
- Preserve the last valid SQLite version when a changed source becomes invalid.
- Never silently activate invalid or ambiguously mapped assessment content.
- Do not manually patch the live SQLite database.
- Do not globally make the shared YAML deserializer strict in the first slice.
- Do not silently auto-correct authored files during normal startup.
- Keep migration incremental and reviewable.
- Avoid unrelated question-content rewrites.
- Run focused tests with temporary databases, then one build.

## Current Contract

### Category

```yaml
schemaVersion: 1
id: physics-1
title: Physics 1 w/ Calculus
subcategories:
  - id: physics-circular-motion
    title: Circular Motion and Centripetal Acceleration
```

The category's subcategories are navigation topics.

### Area

```yaml
schemaVersion: 1
areas:
  - id: physics-dynamics
    categoryIds:
      - physics-1
    subcategoryIds:
      - physics-circular-motion
```

### Assessment

```yaml
categoryId: physics-1
subcategoryIds:
  - physics-circular-motion
navigation:
  learningGoal: practice
  activityType: focusedPractice
  tags:
    - circular-motion
```

## Confirmed Defects

1. `subcategoryId` singular is ignored because the DTO supports only
   `subcategoryIds`.
2. Top-level `learningGoal`, `activityType`, and `tags` are ignored because they
   belong under `navigation`.
3. Numeric answers use obsolete `answer.expected` instead of `answer.value`.
4. Symbolic answers use obsolete `answer.expected` instead of
   `answer.expectedLatex`.
5. Schema validation does not validate taxonomy relationships.
6. Import diagnostics exist only as console messages.
7. New invalid files disappear; changed invalid files retain a stale row without a
   queryable stale/error state.
8. Import invalidation considers content and category/area hashes but not an
   explicit parser/validation pipeline version.

## Phase 1: Assessment Preflight Diagnostics

Add an assessment-specific source preflight step before DTO deserialization.

Do not alter `FileFormat` globally. Introduce a focused service, for example:

```csharp
public interface IAssessmentSourceInspector
{
    AssessmentSourceInspection Inspect(string content, string extension);
}
```

Return structured diagnostics:

```csharp
AssessmentSourceDiagnostic
{
    Severity;
    Code;
    Message;
    Path;
    Line;
    Column;
    ActualKey;
    SuggestedKey;
}
```

Required legacy-key diagnostics:

| Code | Detection | Suggested fix |
| --- | --- | --- |
| `LEGACY_SUBCATEGORY_ID` | top-level `subcategoryId` | `subcategoryIds: [value]` |
| `MISPLACED_LEARNING_GOAL` | top-level `learningGoal` | `navigation.learningGoal` |
| `MISPLACED_ACTIVITY_TYPE` | top-level `activityType` | `navigation.activityType` |
| `MISPLACED_NAVIGATION_TAGS` | top-level `tags` | `navigation.tags` |
| `LEGACY_NUMERIC_EXPECTED` | numeric answer has `expected`, no `value` | `answer.value` |
| `LEGACY_SYMBOLIC_EXPECTED` | symbolic answer has `expected`, no `expectedLatex` | `answer.expectedLatex` |

Requirements:

- inspect YAML and JSON
- preserve source locations where parser APIs expose them
- inspect nested quiz questions, multipart parts, Worked Example steps, and Concept
  Lesson checks
- emit all diagnostics in one pass
- distinguish warnings from activation-blocking errors
- include the assessment ID and source path when discoverable

For these known legacy keys, use activation-blocking errors after the migration is
complete. During the migration branch, a compatibility mode may report them before
blocking, but no production path should silently accept them.

## Phase 2: Taxonomy Relationship Validator

Keep `AssessmentValidator` focused on assessment-internal domain rules. Add a
taxonomy-aware validator that receives current categories and areas:

```csharp
public interface IAssessmentTaxonomyValidator
{
    AssessmentTaxonomyValidationResult Validate(
        AssessmentDefinition assessment,
        IReadOnlyList<Category> categories,
        IReadOnlyList<AreaDefinition> areas);
}
```

Required errors:

- `UNKNOWN_CATEGORY_ID`
- `MISSING_SUBCATEGORY_IDS`
- `UNKNOWN_SUBCATEGORY_ID`
- `SUBCATEGORY_NOT_IN_CATEGORY`
- `SUBCATEGORY_NOT_MAPPED_TO_AREA`
- `AREA_CATEGORY_TOPIC_MISMATCH`

Rules:

1. `categoryId` must identify exactly one category.
2. At least one `subcategoryIds` value is required for active authored
   assessments.
3. Every topic must exist under the selected category.
4. Every topic must belong to at least one area that also contains the category.
5. Duplicate topic IDs should be normalized or rejected consistently.
6. Area definitions must not reference unknown categories or unknown topics.
7. An area topic must belong to at least one of the area's categories.

Do not use a global topic dictionary without category qualification. Even though
topic IDs are currently unique, relationship checks should use
`(categoryId, subcategoryId)` to prevent future cross-category collisions.

## Phase 3: Category And Area Validation

Add startup/catalog validation for category and area sources.

Validate:

- category IDs are unique
- subcategory IDs are unique within a category
- optionally enforce repository-wide unique topic IDs, or explicitly document that
  topics are category-qualified
- area IDs are unique
- every area category exists
- every area topic exists
- every area topic belongs to an area category
- every category topic is mapped to at least one same-category area

Return a report rather than silently dropping unknown area topics in
`SqliteNavigationCatalogService`.

Current behavior:

```csharp
a.SubcategoryIds.Where(knownTopics.ContainsKey)
```

This silently removes invalid area references. Replace it with validated input and
diagnostics. The navigation service should consume already validated taxonomy.

## Phase 4: SQLite Import Diagnostics

Add durable catalog-import reporting using new SQLite tables.

Suggested tables:

```sql
catalog_import_runs
  id
  started_at
  completed_at
  status
  source_count
  imported_count
  unchanged_count
  invalid_count
  stale_count
  inactive_count
  pipeline_version
  global_config_hash

catalog_import_diagnostics
  id
  run_id
  source_path
  assessment_id
  severity
  code
  message
  field_path
  line
  column
  suggested_fix
  retained_previous_version
  created_at
```

Importer behavior per file:

1. Read source.
2. Run source preflight inspection.
3. Deserialize only if preflight permits it.
4. Run internal assessment validation.
5. Run taxonomy relationship validation.
6. Infer/validate navigation metadata.
7. Upsert only when every activation-blocking validation passes.
8. Store all diagnostics for that import run.

Outcomes:

- `Imported`: active row updated.
- `Unchanged`: active row retained.
- `StalePreviousVersion`: current source invalid; previous active row explicitly
  retained and reported.
- `RejectedNewSource`: invalid and no previous row; no active catalog entry.
- `InactiveMissingSource`: source genuinely removed.

Do not describe `StalePreviousVersion` as successfully imported.

## Phase 5: Import Pipeline Versioning

Add a constant or configuration value such as:

```csharp
const int CatalogPipelineVersion = 2;
```

Store it in retention metadata/import runs. Force a full assessment re-ingest when
any of these change:

- category/area global hash
- pipeline version
- assessment source content hash

Increment the version whenever DTO compatibility, source inspection, navigation
inference, or taxonomy resolution changes in a way that affects catalog output.

This prevents a corrected parser or validator from leaving unchanged files with
stale SQLite relations.

## Phase 6: Diagnostics API And Startup Reporting

Add endpoints:

```http
GET /api/navigation/catalog/diagnostics
GET /api/navigation/catalog/diagnostics?severity=error
GET /api/navigation/catalog/diagnostics/{assessmentId}
POST /api/navigation/catalog/reimport
```

The reimport endpoint should be development/admin-local only unless the server
branch later supplies appropriate authorization.

Return:

- latest import summary
- file/assessment diagnostics
- whether a previous valid row is being served
- actionable suggested fixes
- orphan counts grouped by category

Startup logging should include one concise summary:

```text
Catalog import: 510 sources, 476 imported/unchanged, 14 stale, 20 rejected.
Run GET /api/navigation/catalog/diagnostics for details.
```

Do not print hundreds of full stack traces for content errors.

## Phase 7: Navigation Failure Presentation

Keep `Other / Unmapped` only as an explicit diagnostic fallback, not a normal
destination for authored content.

Recommended behavior:

- production catalog omits newly rejected invalid assessments
- stale previous versions remain navigable but carry a diagnostic/stale marker in
  admin/development responses
- development UI shows a compact catalog-health warning when errors exist
- classic assessment fallback continues to work when the SQLite catalog itself is
  unavailable
- do not expose raw source paths to ordinary LAN users

The normal learner navigation should not present invalid content as though
`Other / Unmapped` were a legitimate curriculum area.

## Phase 8: Targeted Content Migration

Migrate the 48 confirmed singular-only files in three reviewable batches:

1. Chemistry: 10
2. Physics 1: 16
3. Calculus 2: 22

For each file:

- replace `subcategoryId: value` with:

  ```yaml
  subcategoryIds:
    - value
  ```

- move top-level learning metadata beneath `navigation`
- map legacy activity names to the current taxonomy
- convert numeric `expected` to `value`
- convert symbolic `expected` to `expectedLatex`
- preserve answer meaning and tolerance
- add missing `modeDefault` and `randomizeQuestions` only when current defaults are
  not the intended behavior
- validate question counts against `attemptQuestionCount`
- preserve attribution/provenance text
- follow `docs/assessment-yaml-latex.md`

Do not use blind search-and-replace for answer fields. `expected` is still correct
for several other schemas, including free response and recall items.

Suggested legacy activity mapping:

| Legacy value | Current goal/activity |
| --- | --- |
| `practice` / `mixedPractice` | `practice` / `mixedPractice` if supported, otherwise `practice` / `focusedPractice` |
| `learn` / `guidedWorkedExample` | `learn` / `guidedWorkedExample` |
| formula recall drill | infer or explicitly use `recall` / appropriate recall activity |
| section test | `evaluate` / `formalTest` or `masteryCheck` based on intent |

Use the current `LearningGoals.All` contract rather than inventing activity names.

## Phase 9: Repository Audit Command

Add a deterministic developer command or test utility that scans all authored
content and outputs:

- unknown YAML keys covered by preflight rules
- missing/unknown category IDs
- missing/unknown topic IDs
- category-topic-area mismatches
- assessments assigned to no area
- duplicate assessment/category/topic/area IDs
- invalid navigation goal/activity pairs
- obsolete numeric/symbolic answer shapes
- SQLite rows whose source file is invalid, missing, or hash-stale

Preferred invocation:

```powershell
dotnet run --project backend\tools\QuizApp.ContentAudit -- data
```

If a new tool project is excessive, expose the same service through a focused test
or API diagnostic endpoint. The output should support JSON and readable text.

Exit codes:

- `0`: no errors
- `1`: content errors
- `2`: infrastructure/parser failure

## Focused Tests

### Source Inspection

- singular `subcategoryId` reports `LEGACY_SUBCATEGORY_ID`
- top-level navigation fields report their exact nested replacements
- numeric and symbolic obsolete answer keys are found at every supported nesting
  level
- valid current YAML produces no preflight diagnostics

### Taxonomy Validation

- valid category/topic/area relationship passes
- missing topics fail
- unknown topic fails
- topic from another category fails
- topic absent from all same-category areas fails
- invalid area references are reported

### Import Lifecycle

- valid new file imports
- unchanged valid file remains unchanged
- changed valid file updates
- new invalid file is rejected and diagnosed
- changed invalid file retains the last valid row and is marked stale
- missing source becomes inactive
- pipeline version bump forces relationship rebuild
- diagnostics survive application restart

### Targeted Content

- all 48 migrated files deserialize with non-empty `SubcategoryIds`
- each topic exists in its category
- each topic resolves to the expected area
- no migrated file uses the six known legacy key patterns
- repository validation passes for all migrated files

## Minimum Verification

Run once after implementation:

```powershell
dotnet build backend\QuizApp.sln --no-restore
dotnet test backend\QuizApp.sln --no-build --filter "AssessmentSource|Taxonomy|AssessmentCatalog"
```

Then run one audit against the repository and one startup with a temporary SQLite
database.

Verify:

- diagnostics identify a deliberately malformed fixture
- Chemistry, Physics 1, and Calculus 2 report zero orphaned active assessments
- the live `data/retention/quizapp.db` was not modified during testing

Do not run repeated browser automation or broad unrelated tests.

## Delivery Order

1. Add source diagnostic models and assessment preflight inspector.
2. Add taxonomy relationship validator.
3. Add category/area validation.
4. Add focused tests for all three validators.
5. Add SQLite import-run and diagnostic tables.
6. Refactor importer into explicit per-file outcomes.
7. Add pipeline version invalidation.
8. Add diagnostics API and concise startup summary.
9. Add repository content-audit command.
10. Migrate Chemistry batch.
11. Migrate Physics 1 batch.
12. Migrate Calculus 2 batch.
13. Re-import into a temporary catalog and verify zero target orphans.
14. Update assessment-authoring documentation with the canonical hierarchy.

## Acceptance Criteria

- Unsupported singular and misplaced navigation keys cannot fail silently.
- Validation names the exact file, field, invalid value, and suggested correction.
- Assessments cannot activate without a valid category/topic/area relationship.
- Invalid area definitions are reported rather than filtered away.
- Import diagnostics are queryable through an API and retained per run.
- Changed invalid sources explicitly report that a stale previous version is served.
- New invalid sources explicitly report that they were rejected.
- A pipeline-version bump deterministically reprocesses unchanged sources.
- All 48 targeted assessments use the current schema.
- Chemistry, Physics 1, and Calculus 2 have no active orphan assessments.
- Existing valid assessments remain compatible.
- Tests use temporary databases and leave live runtime state untouched.

## Completion Report

Report:

- files changed
- migration counts by category
- diagnostics introduced
- taxonomy validation rules introduced
- catalog rows imported, stale, rejected, and inactive
- any remaining `Other / Unmapped` assessments with reasons
- commands run and results
- live runtime files intentionally not touched
- any legacy patterns still present outside the targeted categories

## Assumptions

- Category subcategories remain the canonical navigation topics.
- Areas remain manually authored groupings of category/topic IDs.
- Every active assessment should have at least one topic and area.
- `Other / Unmapped` is a diagnostic fallback, not a curriculum destination.
- YAML/JSON remains authoritative; SQLite relationships are derived.
- Existing valid catalog rows should remain available when a temporary source edit is
  invalid, but that stale state must be visible.
