# Source-to-Curriculum Manifest Contract

The Authoring Workspace keeps original files, verbatim extraction, OCR output,
and `corpus.db` in the gitignored `data/source-library/` directory. Those files
are private reference material and are never inputs to the assessment catalog.

Tracked authoring manifests are JSON documents (valid YAML) under this folder:

- `curriculum-manifests/`: category, area, objectives, prerequisites, required
  activities, and source IDs.
- `content-manifests/`: approved instructional artifact metadata, visual
  requirement, objective, and source chunk IDs.
- `question-blueprints/`: approved question reasoning metadata, source chunk
  IDs, method steps, misconception, and meaningful variation axes.

Tracked manifests must not embed verbatim source text. They can only cite a
private source chunk by its stable `src-...:chunk-0001` ID. The workspace rejects
missing chunk references and writes approved artifacts only after a draft review
state is changed to `approved`.

An agent handoff packet is disposable JSON containing selected private chunks,
their source manifests, objectives, required artifacts, and the output contract.
Importing a response creates a `needsReview` draft. Approval validates and
publishes content manifests and question blueprints; it does not directly create
live assessment YAML. The existing approved question-bank generator remains the
only assessment materialization path.
