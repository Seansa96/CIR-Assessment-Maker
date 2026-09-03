---
name: source-to-curriculum
description: Create or audit CIR Source-to-Curriculum (S2C) imports, packets, manifests, derived lessons, worked examples, question blueprints, and assessment banks. Use whenever local reference PDFs, EPUBs, documents, images, OCR, source chunks, or agent handoff packets are used to author curriculum content.
---

# Source-to-Curriculum

Use this workflow for every S2C task. Do not generate publishable content from a source until the extraction gate passes.

## 1. Extraction gate — hard stop

Import the source through the Authoring Workspace and inspect its manifest and chunks.

Proceed only when all are true:

- manifest is nonempty and records source ID, SHA-256, format, extractor/version, status, and chunk count;
- `chunks.json`/API chunk retrieval succeeds and selected chunks have nonempty text;
- extraction warnings are reviewed; when equations, diagrams, or exercises are not extracted faithfully, render the relevant private PDF pages and select only page-image chunks with nonempty, human-reviewed transcriptions in `approved` state;
- duplicate import or stale hash status is understood.

**Stop and report the failure** if a manifest is empty, chunk count is zero, chunks are absent, extraction is partial in the target exercises, or needed page-image evidence has a blank or unapproved transcription. OCR may create a future draft, but it can never approve a transcription. Do not create a test “from memory” or infer that an `original.pdf` is an adequate source record.

## 2. Define the curriculum before drafting

Create or update a tracked curriculum manifest under `docs/assessment-reference/curriculum-manifests/`.

For each target topic, declare stable objective IDs, prerequisites, required activities, and source IDs. Keep one objective group per focused assessment. A cumulative assessment needs an explicit review topic and a documented objective mix.

## 3. Export a minimal packet

Export a packet containing only the selected source chunks, objective IDs, category/topic IDs, and output constraints. Record the packet ID.

Never put verbatim source text into tracked assessment YAML. Write original instruction, scenarios, explanations, and visuals; preserve source references only as chunk IDs/provenance.

## 4. Blueprint before questions

Create a question blueprint for every proposed bank item. Each blueprint must include:

- stable ID, objective ID, source chunk IDs, and review state;
- question type; givens; unknown; representation/diagram requirement; governing principle; method steps;
- likely misconception; difficulty evidence; answer-verification method;
- variation axes and a reasoning signature.

For scored STEM quiz/test items, also include controlled `difficultyDimensions`, `subjectDifficultyTags`, `difficultyEvidence`, and prerequisite/extension objective IDs. Easy items need 2 distinct dimensions; hard items need 3 plus prerequisite/extension transfer; Olympiad items need 5 plus an extension objective. Subject tags explain a method branch but never increase the dimension count.

Use `numericResponse` for single numerical quantities, with a verified value and tolerance. Use `symbolicResponse` for algebraic/derivation results. Use `freeResponse` only when self-assessment is genuinely intended.

## 5. Uniqueness gate — hard stop

Reject a candidate if it differs only in numbers, names, or superficial wording.

Require at least **two** changed semantic dimensions from this set: scenario, representation, unknown, constraints, governing relation, method branch. A changed parameter that is unused in the calculation is a defect, not variation. The same reasoning signature may appear at most once unless the documented change requires a different solution approach.

## 6. Build and review

Drafts remain `needs-review` until all required checks pass:

- every item links to a blueprint and source chunks;
- every scored STEM item satisfies its tier's distinct difficulty-dimension and transfer-objective requirement;
- all answers are independently verified;
- every answer-bearing item uses `Solution:` and `Why it works:` to show ordered reasoning; multiple choice also uses `Why the other choices fail:`; Olympiad items also use `Prerequisites:` and `Further study:` with targeted preparation;
- diagram-to-prompt consistency is checked when a diagram is required;
- prompts provide all needed givens and units;
- lessons have meaningful depth and visuals; worked examples expose intermediate reasoning;
- quizzes/tests meet required topic coverage and easy/hard balance.

Only approved blueprints may be materialized into assessment files. Do not create “sample” assessments that bypass provenance or review state.

## 7. Deliverable checklist

Before declaring S2C work complete, report:

1. source ID, hash status, extractor, chunk count, and unresolved OCR warnings;
2. curriculum manifest and packet IDs;
3. blueprint IDs, review states, and duplicate/uniqueness results;
4. assessment IDs, topic placement, type counts, and answer-verification results;
5. validation commands run and any timeout/failure.

## CIR locations

- Private source data: `data/source-library/` (never track or publish verbatim extraction).
- Tracked curriculum contracts: `docs/assessment-reference/`.
- Published assessment definitions: `data/assessments/`.
- API endpoints: `/api/authoring/sources`, `/sources/{id}`, `/sources/search`, `/packets`, `/drafts`, `/coverage`.
