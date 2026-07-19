# Assessment Question-Bank Contract

The registry in `question-bank-registry.yaml` is the authority for whether a
question bank may generate assessments. A generator must reject every bank
whose status is not `approved`.

`quarantined` means the file remains available for forensic review but is not a
trusted content source. Changing a bank to `approved` requires passing the
question-bank audit and a human mathematical review.

## Approved bank schema

An approved bank uses this top-level shape:

```yaml
schemaVersion: 1
bankId: calc2-alternating-series
categoryId: calculus-2
topicIds:
  - alternating-series
minimumItemCount: 90
items: []
```

Every item must contain:

```yaml
- id: calc2-alternating-series-foundation-001
  topicId: alternating-series
  skills:
    - verify-alternating-series-hypotheses
  archetype: hypothesis-check
  difficulty: foundation
  reasoningDepth: 2
  difficultyEvidence: Requires checking both monotonicity and the zero limit.
  assessmentUses:
    - easy-quiz
  questionType: multipleChoice
  prompt: |
    Which condition fails for the series
    $\sum_{n=1}^{\infty}(-1)^{n-1}\frac{n}{n+1}$?
  answer:
    choiceId: c
  solutionOutline: |
    The magnitudes $n/(n+1)$ increase toward $1$, so they do not tend to zero.
    The term test therefore proves divergence before the alternating-series
    test can be used.
  commonTrap: Treating alternating signs alone as sufficient for convergence.
  verification:
    method: independent-derivation
    result: verified
  reviewStatus: verified
```

Prompts, answers, explanations, and outlines must use `$...$` or `$$...$$` for
rendered mathematics. LaTeX-bearing YAML must use a block scalar or a
single-quoted scalar.

## Quality rules

- Prompt and solution-outline text must be unique after normalization.
- Parameter-only substitutions do not create a new archetype.
- Every item belongs to exactly one declared topic.
- Hard and Olympiad items require a stated reason for their difficulty and at
  least two meaningful reasoning steps.
- Answers must have an explicit verification record and `reviewStatus:
  verified`.
- Generators select and format reviewed items; they never invent prompts,
  answers, distractors, explanations, or worked steps.
- Sibling assessments must use disjoint source item IDs unless an explicit
  cumulative-review allowlist documents the reuse.
- Generated assessment provenance is recorded in a sidecar manifest rather
  than inferred from assessment tags.

## Banned placeholder language

Approved banks and generated assessments may not contain:

- `Did you understand this step?`
- `Use the Ratio Test....`
- `A definition for this term.`
- `Identify the governing ... condition`
- `Find a structural reduction for ...`
- `translate the restriction into a usable equation or proof obligation`

These phrases are evidence that a template replaced mathematical instruction.
