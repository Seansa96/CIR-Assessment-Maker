---
name: assessment-question-pipeline
description: Create, refine, validate, or review CIR Assessment Maker quiz/test content, especially YAML/JSON assessments with symbolicResponse, multipleChoice, selectAll, freeResponse, numericResponse, or code questions. Use when Codex is asked to generate STEM assessment questions, improve answers/explanations, verify question difficulty, cite or refresh educational source context, or decide whether a question-building task needs web research, OER sources, or a larger local knowledge corpus.
---

# Assessment Question Pipeline

## Core Workflow

1. Inspect the local assessment schema first:
   - `data/assessments/*.yaml`
   - `backend/src/QuizApp.Core/Domain/AssessmentModels.cs`
   - `backend/src/QuizApp.Core/Services/AssessmentValidator.cs`
   - relevant existing quizzes in the same category.

2. Decide the source mode:
   - Use local context only for routine formatting, schema repair, and content already present in the repo.
   - Browse current web sources when asked to research, refresh, cite, benchmark difficulty, or generate from external curriculum standards.
   - Prefer open educational resources and primary references over answer-farm or scraped homework sites.
   - Do not bulk scrape by default. Recommend a corpus pipeline only when repeated refresh, large coverage, provenance tracking, or offline retrieval is required.

3. Draft content against the app contract:
   - Shared top level: `schemaVersion`, `id`, `title`, `assessmentType`, `categoryId`, singular `topicId`, `modeDefault`, `randomizeQuestions`, and optional timers.
   - Classification is authoritative and singular: `topicId` places the assessment in exactly one topic, and that topic has exactly one canonical area in `data/areas.yaml`.
   - `skills` and `navigation.tags` describe searchable capabilities and evidence only. Never use them as additional topic or area assignments, even when a skill/tag happens to equal another topic or area ID.
   - A genuinely cumulative assessment belongs to a declared review/capstone topic; do not list several content topics or choose one narrow supporting topic merely to satisfy the schema.
   - Quiz/test: `questions`; optional `attemptQuestionCount` can sample an attempt from a larger authored bank.
   - Worked Example: `workedExamples`.
   - Guided Project: `guidedProject`.
   - Recall Drill: `items`.
   - Stable IDs: `q001`, `q002`, etc.; no duplicates.
   - Use Markdown math delimiters for rendered text: `$...$` and `$$...$$`, not `\(...\)` or `\[...\]`.
   - For `symbolicResponse`, use `answer.expectedLatex`, `equivalenceMode`, `tolerance`, and `variables`.
   - Keep explanations short but instructional: method, key identity/substitution, final check, and optional related topic.

4. Verify every answer:
   - Differentiate indefinite-integral answers mentally or with a CAS-style check when possible.
   - For symbolic answers, prefer derivative equivalence for antiderivatives.
   - For numeric answers, include a tolerance and ensure the explanation reaches the same value.
   - For multiple choice/select-all, ensure correct choices exist and distractors are plausible but unambiguous.

5. Validate before finishing:
   - Parse changed YAML/JSON.
   - Confirm exactly one non-empty scalar `topicId`; reject `subcategoryId`, `subcategoryIds`, or inferred placement from tags/skills.
   - Count questions if the user specified a count.
   - Check every question type matches the requested type.
   - Check no old math delimiters remain in rendered fields.
   - Run backend tests only when behavior changed; for content-only edits, parser/schema spot checks are usually enough.

## Web Research Rules

Read `references/source-policy.md` when using outside sources. In short:

- Use sources to guide coverage, terminology, and difficulty; write original questions and explanations.
- Track provenance in working notes when useful, but avoid copying large passages into assessment YAML.
- Respect robots, terms, licenses, and attribution requirements.
- Cite sources in the final response when web research materially shaped content.

## Corpus Pipeline Decision

Recommend a maintained data corpus instead of ad hoc browsing when at least two are true:

- The same topics will be refreshed repeatedly.
- The user wants broad coverage across many courses or standards.
- Agents need retrieval over a local source library while offline.
- The project needs provenance, license, and refresh dates per source.
- The source set is stable enough to curate.

If building the corpus, prefer:

1. Licensed/OER source inventory with URLs, licenses, and allowed use.
2. Fetch jobs that respect robots and rate limits.
3. Chunking and metadata extraction by topic, source, license, date, and learning objective.
4. Retrieval for agents, not blind generation.
5. A scheduled refresh with change detection and human review before new content becomes active.

Do not use scraping to bypass site restrictions, paywalls, login walls, or licensing limits.

## Quality Bar

Good assessment content should be:

- Schema-valid and renderable in the existing web UI.
- Aligned to the requested course, topic, and difficulty.
- Solvable from the prompt without hidden assumptions.
- Clear about expected answer format.
- Explanatory enough to teach the method, not just state the answer.
- Free of copied textbook wording unless the license and attribution explicitly allow it.

## Useful Checks

Use the repository validation tests for important new content:

```powershell
dotnet test backend\QuizApp.sln --no-restore
```

For content-only work, add the assessment ID to the repository content-validation theory when appropriate and run the LaTeX scan from `docs/assessment-yaml-latex.md`.

Search for legacy math delimiters:

```powershell
rg -n '\\\\\\(|\\\\\\)|\\\\\\[|\\\\\\]' data/assessments
```
