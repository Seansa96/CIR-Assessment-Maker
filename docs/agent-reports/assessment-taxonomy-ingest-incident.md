# Assessment Taxonomy And SQLite Ingest Incident Report

**Audience:** Gemini / Antigravity IDE agent  
**Status:** Active reference until the taxonomy migration and ingest hardening plan is implemented  
**Implementation plan:** `docs/plans/antigravity-assessment-taxonomy-validation-and-ingest.md`

## Read This Before Taxonomy Or Catalog Work

The current navigation hierarchy is:

```text
Category / Subject
  -> Area
  -> Subcategory / Topic
  -> Learning goal
  -> Activity type
  -> Assessment
```

There is no separate authored `topicId` field. A category's `subcategories` are the
navigation topics. Assessments link to topics through the plural field:

```yaml
subcategoryIds:
  - physics-circular-motion
```

Areas independently list the same topic IDs:

```yaml
categoryIds:
  - physics-1
subcategoryIds:
  - physics-circular-motion
```

An assessment is properly mapped only when:

1. `categoryId` identifies an existing category.
2. Every assessment `subcategoryIds` value exists in that category.
3. At least one matching area contains both that category and topic.

## Confirmed Root Cause

A large generated assessment batch uses a legacy or imagined schema:

```yaml
subcategoryId: physics-circular-motion
learningGoal: practice
activityType: mixedPractice
tags:
  - physics
```

The supported schema is:

```yaml
subcategoryIds:
  - physics-circular-motion
navigation:
  learningGoal: practice
  activityType: focusedPractice
  tags:
    - physics
```

`AssessmentFileDto` has `SubcategoryIds` but no singular `SubcategoryId`.
`FileFormat` uses YamlDotNet's `IgnoreUnmatchedProperties()`. The singular field and
top-level navigation fields are therefore discarded without an error.

The resulting `AssessmentDefinition.SubcategoryIds` is empty. The SQLite importer
cannot resolve an area and writes `other-unmapped`.

## Affected Content Snapshot

Singular-only assessment files:

| Category | Count |
| --- | ---: |
| Chemistry | 10 |
| Physics 1 | 16 |
| Calculus 2 | 22 |
| **Total** | **48** |

All declared category topics in these three subjects are already present in a
same-category area. `data/areas.yaml` is not the primary cause for this incident.

The repository contains many more occurrences of `subcategoryId`, including files
that may also contain the plural field. Do not perform a blind global replacement
without classifying each file.

## Secondary Schema Errors

Many of the same files use obsolete answer shapes:

```yaml
type: numericResponse
answer:
  expected: 2
```

Required:

```yaml
answer:
  value: 2
  tolerance: 0
```

Likewise, `symbolicResponse` requires `answer.expectedLatex`, not
`answer.expected`.

Consequences in the current SQLite database:

| Category | Active but `other-unmapped` | Rejected / absent because invalid |
| --- | ---: | ---: |
| Chemistry | 8 | 2 |
| Physics 1 | 1 | 15 |
| Calculus 2 | 5 | 17 |
| **Total** | **14** | **34** |

The active orphaned rows are the files whose assessment bodies otherwise validate.
The absent rows fail question validation and are skipped during import.

## Why The Failure Is Hard To Diagnose

1. Unknown YAML keys are silently ignored.
2. `AssessmentValidator` requires `categoryId` but does not require topic IDs.
3. It does not verify that topics exist in the selected category.
4. It does not verify that category/topic pairs map to an area.
5. Import failures are written only to stderr.
6. Invalid changed files preserve the last valid SQLite row, so YAML and runtime
   catalog state can differ.
7. Files with no previous valid row simply disappear from catalog navigation.
8. Navigation goal/activity inference can make ignored top-level metadata appear to
   work partially.
9. Category/area config changes trigger a full import, but parser/validation rule
   changes currently have no independent ingest-pipeline version.

## Important Implementation Warning

Do **not** fix this by globally removing `IgnoreUnmatchedProperties()`.

Existing assessment files contain tolerated legacy fields at several nested levels.
Making the shared deserializer strict immediately would reject a large portion of
the repository. Use an assessment-aware preflight linter with explicit diagnostics,
then migrate content in controlled batches.

## Current Files To Inspect

- `backend/src/QuizApp.Infrastructure/Files/FileDtos.cs`
- `backend/src/QuizApp.Infrastructure/Files/FileDtoMapper.cs`
- `backend/src/QuizApp.Infrastructure/Files/FileFormat.cs`
- `backend/src/QuizApp.Core/Services/AssessmentValidator.cs`
- `backend/src/QuizApp.Infrastructure/Retention/SqliteAssessmentCatalogImporter.cs`
- `backend/src/QuizApp.Infrastructure/Retention/SqliteNavigationCatalogService.cs`
- `backend/tests/QuizApp.Tests/AssessmentCatalogTests.cs`
- `data/categories/chemistry.yaml`
- `data/categories/physics-1.yaml`
- `data/categories/calculus-2.yaml`
- `data/areas.yaml`

## Required Outcome

After the implementation:

- legacy/wrong keys produce named diagnostics with suggested replacements
- invalid topic/category/area relationships are rejected before catalog activation
- import diagnostics are queryable rather than hidden in console output
- the last valid row is preserved explicitly and reported as stale
- parser or taxonomy rule changes force a deterministic re-ingest
- corrected Chemistry, Physics, and Calculus 2 assessments appear under their real
  areas and topics
- no affected assessment silently disappears or lands in `Other / Unmapped`

Do not edit the live `data/retention/quizapp.db` manually. Use a temporary database
for tests and let the importer rebuild catalog relationships from authored YAML.
