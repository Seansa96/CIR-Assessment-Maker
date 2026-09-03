# Source-to-Curriculum Manifest Contract

The Authoring Workspace keeps original files, extracted text, private page images,
reviewed transcriptions, and `corpus.db` in the gitignored `data/source-library/` directory. Those files
are private reference material and are never inputs to the assessment catalog.

Tracked authoring manifests are JSON documents (valid YAML) under this folder:

- `curriculum-manifests/`: category, area, objectives, prerequisites, required
  activities, and source IDs.
- `content-manifests/`: approved instructional artifact metadata, visual
  requirement, objective, and source chunk IDs.
- `question-blueprints/`: approved question reasoning metadata, source chunk
  IDs, method steps, misconception, and meaningful variation axes.

Tracked manifests must not embed verbatim source text. They can only cite a
private source chunk by its stable `src-...:chunk-0001` or `src-...:page-0808` ID.
The workspace rejects missing chunk references and writes approved artifacts only
after a draft review state is changed to `approved`.

## Reviewed PDF page-image extraction

For equation- or diagram-dependent PDF material, render the selected inclusive
page range from the source's private original PDF. This creates stable
`page-image` chunks whose PNG paths remain under that source's private
`page-images/` directory. OCR is not part of this workflow.

Each page-image chunk begins in `draft` review state with an empty transcription.
An author must enter a nonempty transcription that captures the relevant
mathematics, labels, and diagram relationships, then explicitly approve it after
checking it against the image. A page-image chunk is rejected from packet export,
content manifests, and question blueprints until both conditions hold:

1. Its transcription is nonempty.
2. Its transcription review state is `approved`.

Text-only chunks retain their existing behavior. When PDF text loses equation or
diagram fidelity, text-only chunks may remain searchable but cannot substitute
for reviewed page-image evidence in the extraction gate.

An agent handoff packet is disposable JSON containing selected private chunks,
their source manifests, objectives, required artifacts, and the output contract.
Importing a response creates a `needsReview` draft. Approval validates and
publishes content manifests and question blueprints; it does not directly create
live assessment YAML. The existing approved question-bank generator remains the
only assessment materialization path.
