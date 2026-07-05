# Antigravity Implementation Plan: Assessment Error Remediation And Validation Tests

## Status

- **Audience:** Antigravity IDE agent
- **Project:** CIR Assessment Maker
- **Primary goal:** Fix the attached assessment validation errors and make `dotnet test` catch the same classes of errors before they reach runtime
- **Source report:** User-attached validation output from `C:\Users\SeanS\.codex\attachments\42a59ca2-4d25-4359-bf61-b108a7605856\pasted-text.txt`
- **Priority:** Deterministic content validity and loud test failures

Before editing, read:

- `AGENTS.md`
- `GEMINI.md`
- `docs/agent-coexistence.md`
- `docs/assessment-yaml-latex.md`
- `docs/plans/antigravity-assessment-taxonomy-validation-and-ingest.md`
- `.codex/skills/assessment-question-pipeline/SKILL.md`
- `backend/src/QuizApp.Core/Services/AssessmentValidator.cs`
- `backend/src/QuizApp.Core/Services/AssessmentTaxonomyValidator.cs`
- `backend/src/QuizApp.Infrastructure/Retention/SqliteAssessmentCatalogImporter.cs`
- `backend/tests/QuizApp.Tests/FileAssessmentRepositoryTests.cs`
- `backend/tests/QuizApp.Tests/AssessmentValidatorTests.cs`
- `backend/tests/QuizApp.Tests/TaxonomyValidationTests.cs`
- the affected assessment YAML files listed in the attached report

Check `git status --short` before editing. Do not alter runtime state, especially:

- `.cir-processes.json`
- `data/retention/quizapp.db`
- `data/project-sessions/`
- `data/attempts/`
- `data/grades/`
- `logs/`

## Execution Constraints

- Prioritize fixing the invalid authored assessment files and adding focused validation tests.
- Do not rewrite working assessment content unrelated to the attached report.
- Do not manually patch the live SQLite database.
- Do not run broad exploratory browser testing.
- Do not add a large new UI or unrelated schema feature.
- Keep changes reviewable by grouping them into content fixes and validation/test infrastructure.
- Prefer a reusable content-audit helper that can be called from tests over one-off test logic copied across files.
- At completion, report changed files, commands run, errors fixed by category, tests added, and any remaining failing files.

## Attached Report Summary

The attached report contains these issue counts:

| Severity | Code | Count | Meaning |
| --- | --- | ---: | --- |
| Error | `DUPLICATE_ID` | 18 | Duplicate assessment IDs exist across authored files. |
| Error | `INVALID_ACTIVITY_TYPE` | 3 | Navigation activity type is not in the accepted taxonomy. |
| Error | `INVALID_QUESTION_TYPE` | 54 | Worked-example or question entries use an unsupported/mis-shaped question type. |
| Error | `INVALID_RECALL_ITEM_TYPE` | 15 | Recall items use invalid item types. |
| Error | `INVALID_SYMBOLIC_EQUIVALENCE_MODE` | 99 | Symbolic response `equivalenceMode` is missing or invalid. |
| Error | `INVALID_SYMBOLIC_TOLERANCE` | 99 | Symbolic response `answer.tolerance` is missing or negative. |
| Error | `MISSING_CONCEPT_LESSON` | 9 | `assessmentType: conceptLesson` files do not include top-level `lesson`. |
| Error | `MISSING_PROMPT` | 54 | Question or step prompts are missing. |
| Error | `MISSING_RECALL_EXPECTED` | 15 | Recall item answer fields are missing required expected content. |
| Error | `MISSING_WORKED_EXAMPLE_PROBLEM` | 9 | Worked examples lack a `problem`. |
| Error | `MISSING_WORKED_EXAMPLE_STEP_TITLE` | 54 | Worked-example steps lack titles. |
| Error | `MULTIPLE_CHOICE_ANSWER_NOT_FOUND` | 78 | Multiple-choice answer IDs do not match available choices. |
| Error | `MULTIPLE_CHOICE_WITHOUT_CHOICES` | 78 | Multiple-choice questions lack `choices`. |
| Warning | `UNKNOWN_SUBCATEGORY_ID` | 18 | Assessment topic IDs do not exist in their category. |

High-volume affected groups include:

- `aops-olympiad-*`
- `calc2-parametric-*`
- `calc2-polar-*`
- `precalculus-conic-sections-*`
- several Chemistry quiz files
- several Physics momentum/impulse files
- `phys-n2-force-id-drill.yaml`

Treat the attached report as the authoritative starting list, but rerun validation after each batch because fixing one schema layer may expose deeper issues.

## Root-Cause Pattern

The failures look like generated content was written with an outline-like structure rather than the app's actual schema.

Common examples:

- Concept lessons likely have lesson text or sections in the wrong top-level field instead of:

  ```yaml
  assessmentType: conceptLesson
  lesson:
    introduction: |
      ...
    sections:
      - id: ...
        title: ...
        content: |
          ...
  ```

- Worked examples likely have steps that are missing required step fields or are not shaped like valid question interactions:

  ```yaml
  assessmentType: workedExample
  workedExamples:
    - id: we001
      title: ...
      problem: |
        ...
      steps:
        - id: s001
          title: ...
          instruction: |
            ...
          type: multipleChoice
          prompt: |
            ...
          choices:
            - id: a
              text: ...
          answer:
            choiceId: a
  ```

- Quizzes/tests likely have placeholder multiple-choice questions with no `choices`, or symbolic responses using old/incorrect answer metadata.

- Recall drills likely use non-supported item types or omit `answer.expected` / `answer.expectedLatex`.

- Some assessments use topic IDs not defined in the selected category, such as the reported `physics-momentum-collisions-collisions`.

## Phase 1: Reproduce And Preserve The Error Inventory

Create a temporary working report from the attached file or from a fresh validation run.

Recommended deliverable:

- `docs/agent-reports/assessment-validation-error-remediation.md`

The report should contain:

- current issue counts by code
- affected files grouped by category/topic family
- duplicate assessment ID pairs
- unknown subcategory IDs and suggested replacements
- a checklist for the remediation batches below

Do not copy the entire noisy pasted report verbatim. Summarize it into actionable tables.

## Phase 2: Add A Whole-Repository Content Audit Test

The current repository has focused content-validation theories, but new generated files can sit outside those lists. Add a test that validates every authored YAML assessment file.

Suggested location:

- `backend/tests/QuizApp.Tests/AssessmentContentAuditTests.cs`

Suggested tests:

1. `All_authored_assessment_files_deserialize_and_validate`
   - enumerate `data/assessments/*.yaml`
   - load each through the existing file DTO/repository path
   - call `AssessmentValidator.Validate`
   - fail with a compact grouped message:

     ```text
     data/assessments/foo.yaml
       MISSING_CONCEPT_LESSON: Concept lesson assessments must include lesson.
       INVALID_SYMBOLIC_TOLERANCE: Symbolic response questions must include a non-negative answer.tolerance.
     ```

2. `All_authored_assessment_ids_are_unique`
   - deserialize enough metadata to read `id`
   - fail with duplicate ID, first file, and duplicate file

3. `All_authored_assessments_have_valid_taxonomy`
   - load categories and areas from `data/categories/*.yaml` and `data/areas.yaml`
   - validate each assessment with `AssessmentTaxonomyValidator`
   - fail on unknown category, missing topic, unknown topic, or topic not mapped to an area

4. `All_authored_assessments_have_valid_navigation_metadata`
   - enforce known `navigation.learningGoal` and `navigation.activityType`
   - ensure top-level legacy `learningGoal` / `activityType` are not accepted silently if the existing source inspector already supports this

5. `Assessment_yaml_does_not_use_double_quoted_latex_backslashes`
   - run the existing rule from `docs/assessment-yaml-latex.md` against all changed or all authored YAML files
   - fail only when a double-quoted scalar appears to contain LaTeX backslashes

Mark these tests with a clear trait if the project uses xUnit traits:

```csharp
[Trait("Category", "ContentValidation")]
```

This allows a focused command:

```powershell
dotnet test backend\QuizApp.sln --no-build --filter "ContentValidation"
```

If the project does not currently use traits, add them only to the new audit tests.

## Phase 3: Add Focused Validator Regression Fixtures

Strengthen `AssessmentValidatorTests` with small in-memory fixtures for each error class from the report.

Add or confirm tests for:

- concept lesson without `lesson` returns `MISSING_CONCEPT_LESSON`
- concept lesson section check reuses question validation
- worked example without `problem` returns `MISSING_WORKED_EXAMPLE_PROBLEM`
- worked example step without `title` returns `MISSING_WORKED_EXAMPLE_STEP_TITLE`
- worked example step without prompt returns `MISSING_PROMPT`
- worked example step with bad type returns `INVALID_QUESTION_TYPE`
- multiple-choice question without choices returns `MULTIPLE_CHOICE_WITHOUT_CHOICES`
- multiple-choice answer not in choices returns `MULTIPLE_CHOICE_ANSWER_NOT_FOUND`
- symbolic response without valid `equivalenceMode` returns `INVALID_SYMBOLIC_EQUIVALENCE_MODE`
- symbolic response without non-negative `tolerance` returns `INVALID_SYMBOLIC_TOLERANCE`
- recall drill invalid item type returns `INVALID_RECALL_ITEM_TYPE`
- recall cloze/typed/flashcard item missing expected answer returns `MISSING_RECALL_EXPECTED`
- invalid navigation activity returns `INVALID_ACTIVITY_TYPE`

These tests should be tiny and deterministic. They protect the validator itself; the whole-repo audit protects actual content.

## Phase 4: Make The Audit Reusable

Avoid burying all scan logic inside one test method. Add a small helper/service in the test project or Core if appropriate.

Possible names:

- `AssessmentContentAudit`
- `AssessmentRepositoryAudit`
- `AuthoredContentValidator`

Responsibilities:

- enumerate assessment files
- deserialize and validate internal schema
- validate duplicate assessment IDs
- validate taxonomy relationships
- optionally scan source text for known YAML/LaTeX hazards
- return structured results

Keep it lightweight. A separate CLI tool is optional; the required deliverable is that `dotnet test` fails loudly.

If adding a CLI is cheap and helpful, prefer a small tool later:

```powershell
dotnet run --project backend\tools\QuizApp.ContentAudit -- data
```

Do not let the optional CLI delay the test coverage.

## Phase 5: Remediate Content In Batches

Fix content after the audit test exists, so each batch can be measured.

### Batch A: Duplicate IDs And Taxonomy Warnings

Fix first because they can make catalog behavior ambiguous.

Tasks:

- identify all duplicate assessment IDs
- preserve the intended canonical ID for the older/established file
- rename newer duplicates with stable, descriptive IDs
- ensure file names match renamed IDs when practical
- fix `physics-momentum-collisions-collisions` to the real category topic, likely `physics-momentum-collisions`, unless content indicates another topic
- add missing category subcategories or area mappings only when the content genuinely represents a new topic
- do not use `Other / Unmapped` as a normal solution

Expected errors addressed:

- `DUPLICATE_ID`
- `UNKNOWN_SUBCATEGORY_ID`

### Batch B: Concept Lessons

Affected examples include:

- `aops-olympiad-alg-concept-lesson.yaml`
- `aops-olympiad-geometry-concept-lesson.yaml`
- `aops-olympiad-trig-concept-lesson.yaml`
- `calc2-parametric-curves-basics-concept-lesson.yaml`
- `calc2-parametric-derivatives-concept-lesson.yaml`
- `calc2-parametric-integrals-concept-lesson.yaml`
- `calc2-polar-calculus-concept-lesson.yaml`
- `calc2-polar-curves-concept-lesson.yaml`
- `precalculus-conic-sections-concept-lesson.yaml`

Tasks:

- ensure each file has top-level `lesson`
- ensure `lesson.introduction` is non-empty
- ensure `lesson.sections` is non-empty
- ensure each section has `id`, `title`, and `content`
- ensure embedded checks, if present, use valid question shape
- preserve the learning intent; do not reduce concept lessons to bare stubs

Expected errors addressed:

- `MISSING_CONCEPT_LESSON`
- any nested check validation errors exposed afterward

### Batch C: Worked Examples

Affected examples include:

- `aops-olympiad-alg-worked-example.yaml`
- `aops-olympiad-geometry-worked-example.yaml`
- `aops-olympiad-trig-worked-example.yaml`
- `calc2-parametric-curves-basics-worked-example.yaml`
- `calc2-parametric-derivatives-worked-example.yaml`
- `calc2-parametric-integrals-worked-example.yaml`
- `calc2-polar-calculus-worked-example.yaml`
- `calc2-polar-curves-worked-example.yaml`
- `precalculus-conic-sections-worked-example.yaml`

Tasks:

- ensure top-level `workedExamples` is present
- ensure each worked example has `id`, `title`, `problem`, and `steps`
- ensure every step has `id`, `title`, `instruction`, `type`, `prompt`, `answer`, and any type-specific fields
- convert outline-only steps into real interactive steps
- use multiple-choice, select-all, free-response self-check, symbolic-response, or numeric-response according to the step's need
- make the final step ask the learner to solve or explain a complete path

Expected errors addressed:

- `MISSING_WORKED_EXAMPLE_PROBLEM`
- `MISSING_WORKED_EXAMPLE_STEP_TITLE`
- `MISSING_PROMPT`
- `INVALID_QUESTION_TYPE`
- nested multiple-choice/symbolic errors if present

### Batch D: Quizzes And Tests

Affected groups include:

- `aops-olympiad-*-easy-quiz.yaml`
- `aops-olympiad-*-hard-quiz.yaml`
- `calc2-parametric-*-easy-quiz.yaml`
- `calc2-parametric-*-hard-quiz.yaml`
- `calc2-parametric-*-easy-test.yaml`
- `calc2-parametric-*-hard-test.yaml`
- `calc2-polar-*-easy-quiz.yaml`
- `calc2-polar-*-hard-quiz.yaml`
- `calc2-polar-*-easy-test.yaml`
- `calc2-polar-*-hard-test.yaml`
- `precalculus-conic-sections-*-quiz.yaml`
- `precalculus-conic-sections-*-test.yaml`

Tasks:

- give every multiple-choice question a plausible `choices` list
- ensure `answer.choiceId` matches one authored choice ID
- ensure symbolic questions use:

  ```yaml
  answer:
    expectedLatex: '...'
    equivalenceMode: expression
    variables:
      - x
    tolerance: 0.000001
  ```

  or:

  ```yaml
  answer:
    expectedLatex: '...'
    equivalenceMode: derivative
    variables:
      - x
    tolerance: 0.000001
  ```

- use `expression` for ordinary expression equivalence
- use `derivative` for antiderivative-style answers
- include variables for derivative mode
- preserve quiz/test length requirements from the originating content plan
- keep easy/hard versions meaningfully different

Expected errors addressed:

- `MULTIPLE_CHOICE_WITHOUT_CHOICES`
- `MULTIPLE_CHOICE_ANSWER_NOT_FOUND`
- `INVALID_SYMBOLIC_EQUIVALENCE_MODE`
- `INVALID_SYMBOLIC_TOLERANCE`

### Batch E: Recall Drills

Affected examples include:

- `phys-fric-force-id-drill.yaml`
- `phys-m2d-frame-id-drill.yaml`
- `phys-n2-force-id-drill.yaml`
- any report-listed recall drill with invalid item types

Tasks:

- use only supported item types:
  - `typed`
  - `symbolic`
  - `flashcard`
  - `cloze`
- for `typed`, `flashcard`, and `cloze`, include `answer.expected`
- for `symbolic`, include `answer.expectedLatex`
- preserve explanations and tags where present
- verify ratings/reveal flow still makes sense for the item type

Expected errors addressed:

- `INVALID_RECALL_ITEM_TYPE`
- `MISSING_RECALL_EXPECTED`

### Batch F: Chemistry And Physics Legacy Files

The report includes several Chemistry files with small counts and Physics momentum/impulse files with duplicate/taxonomy issues.

Tasks:

- inspect each file directly rather than blind rewriting
- fix navigation metadata and activity types according to current taxonomy
- fix unknown topic IDs
- rename duplicate IDs where needed
- validate file by file after changes

## Phase 6: Validation Commands

Run focused checks after implementation.

Recommended sequence:

```powershell
dotnet build backend\QuizApp.sln --no-restore
dotnet test backend\QuizApp.sln --no-build --filter "AssessmentValidator|TaxonomyValidation|ContentValidation|FileAssessmentRepository"
```

If the new audit tests use a different trait/name, report the exact command.

Also run the LaTeX scan from `docs/assessment-yaml-latex.md` against changed assessment YAML.

If frontend files were not changed, do not run `npm run build`.

## Phase 7: Optional Temporary Catalog Smoke Check

Only after content validation passes, run one startup/import smoke check against a temporary SQLite database, not the live `data/retention/quizapp.db`.

Verify:

- catalog import does not reject the remediated files
- no remediated assessment lands in `Other / Unmapped`
- `/api/navigation/catalog` can include the remediated content

Do not manually edit SQLite.

## Acceptance Criteria

The work is complete when:

- all attached-report files either validate or are explicitly documented as intentionally deferred
- duplicate assessment IDs are resolved
- unknown subcategory IDs are resolved
- all concept lessons include valid `lesson` bodies
- all worked examples include valid `workedExamples` with real interactive steps
- all quizzes/tests have valid multiple-choice and symbolic-response metadata
- all recall drills use supported item types and required answer fields
- `dotnet test` includes a whole-repository content validation path that fails on these classes of errors
- taxonomy validation is part of the dotnet test path
- the LaTeX double-quote/backslash scan reports no unreviewed LaTeX hazards in changed files
- runtime state files are not intentionally modified

## Completion Report

Report:

- changed files
- fixed issue counts by code
- duplicate IDs renamed
- topic IDs corrected or areas/categories added
- new validation tests added
- commands run and results
- any files intentionally deferred
- any remaining warnings and why they are acceptable

## Assumptions

- The attached validation report is recent enough to drive the first remediation pass.
- Existing schema rules in `AssessmentValidator` are the source of truth.
- Category subcategories remain the canonical topics.
- Areas remain manually authored topic groupings.
- SQLite is derived runtime catalog state, not the place to fix authored content.

