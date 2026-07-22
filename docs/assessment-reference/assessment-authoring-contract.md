# Assessment Authoring Contract

This is the authoritative quality contract for new and materially modified assessments. `AssessmentValidator` remains the schema authority; the question-bank and Source-to-Curriculum contracts remain the provenance and uniqueness authorities.

## Profiles and metadata

Every category declares `authoringProfile: stem|nonStem` and whether it permits directed projects. All non-STEM categories and Electrical Engineering/Electronics and Circuits permit directed projects.

New or modified assessments declare:

```yaml
authoring:
  visualRequirement: required # or notApplicable
  visualRationale: A free-body diagram is needed to interpret the setup.
  difficultyTier: easy # required for quizzes and tests; easy or hard
  # exceptionReason: Approved exception for a nonstandard count or format.
```

`notApplicable` requires a rationale. `required` requires usable original media with meaningful alt text. Animated SVG or video is required when a transformation, translation, rotation, or comparable operation is the core idea.

### Physics 1 Dynamics model metadata

New or materially modified Dynamics concept lessons and worked examples also declare their analysis model:

```yaml
authoring:
  physicsModel:
    modelId: inclinedPlane # forceModel|freeBodyDiagram|inclinedPlane|connectedSystem|staticEquilibrium|friction|uniformCircularMotion
    modelRole: foundation # foundation|application|synthesis
    requiredRepresentations: [systemBoundary, freeBodyDiagram, coordinateAxes, forceComponents]
```

This is a teaching-model declaration, not a tag. `systemBoundary` and `freeBodyDiagram` are required for all Dynamics model lessons and examples. Inclined-plane material also requires `coordinateAxes` and `forceComponents`; connected systems and static equilibrium require `motionConstraint`; friction requires a static-versus-kinetic decision branch; circular-motion material requires `radialDirection`. Dynamics lessons include an FBD/system-boundary choice or correction activity. Worked examples begin with the system, FBD, and axes before equations, use 2–4 related problem families, and surface a sign, force-pair, or constraint trap.

## Required progression

Concept lessons, worked examples, glossaries, and recall drills collectively prepare the learner for the easy quiz. Hard quizzes and hard tests may extend beyond the immediate topic only when their blueprints name prerequisite or extension objectives.

## Answers, feedback, and explanations

Every answer-bearing item—concept checks, worked-example steps, glossary drills, recall drills, quizzes, and tests—must include learner-visible, ordered reasoning from the givens to the conclusion. Use these Markdown labels in each explanation:

- `Solution:` states the result and shows each material procedural step in order. Mathematical or computational solutions include the relevant algebra, substitutions, intermediate results, techniques, and units when applicable.
- `Why it works:` names and applies the governing definition, theorem, principle, pattern, or technique. Conceptual and recognition items define the relevant term, expression, notation, or diagram cue and show the logical chain that identifies the result.
- `Common trap:` is required whenever a domain condition, boundary case, assumption, unit issue, or likely misconception materially affects correctness.

Multiple-choice explanations also include `Why the other choices fail:`. Briefly identify why each plausible distractor is incorrect; do not repeat the whole derivation for every choice.

Olympiad explanations also include `Prerequisites:` and `Further study:`. They give a complete modeling and solution path, justify non-obvious steps, name the necessary prerequisite concepts or theorems, and recommend targeted concepts or readings for the outside knowledge required. Generic advice such as “research more” is insufficient.

Missing required labels are blocking defects for new or materially modified content. The legacy baseline audit reports them without blocking catalog loading. A short-text heuristic is supplemental only; structural completeness, not a word count, determines sufficiency.

## Difficulty dimensions for STEM evaluation

A difficulty dimension is one distinct decision, transformation, representation change, constraint check, or model-building action required between the stated givens and a valid solution. Larger numbers, longer wording, repeated arithmetic, or repeated use of the same operation never create another dimension.

The controlled IDs are `simplification`, `identityConstruction`, `auxiliaryTechnique`, `modelOrDerivation`, `domainCondition`, `casePartition`, `parameterThreshold`, `reverseReasoning`, `proofJustification`, `representationTransfer`, `errorDiagnosis`, `estimationOrBounds`, `globalLocalReasoning`, and `counterexampleOrConstruction`.

Every scored STEM quiz/test item declares distinct `difficultyDimensions`, concise `difficultyEvidence`, and optional subject-specific tags. Tags explain a method branch such as `freeBodyDiagram`, `systemBoundary`, `vseprAccounting`, or `equilibriumPerturbation`; tags do not increase the count.

- Easy items require at least 2 dimensions.
- Hard items require at least 3 dimensions and at least one named prerequisite or extension objective.
- Olympiad items require at least 5 dimensions and at least one named extension objective.

Items must remain solvable from stated givens. Missing data, unstated conventions, ambiguity, and deceptive wording are defects, not difficulty dimensions. Mathematics commonly uses transformations, identities, cases, proof, bounds, and constructions; physics uses modeling, representations, system boundaries, coupled principles, constraints, and regime checks; chemistry uses representation construction, chemical accounting, competing models, exceptions, equilibrium/model chains, and evidence interpretation.

| Activity | Contract |
| --- | --- |
| Concept lesson | At least 7 active sections (target 8); every section has a substantive check. Checks are at least 70% multiple choice. STEM uses contextual visual aids; non-STEM uses code, traces, or interface evidence when relevant. |
| Worked example | 2–4 distinct problems, complete procedural reasoning, common traps/edge cases, and contextual visuals. STEM steps are 70% symbolic/free response; non-STEM steps are 70% free response/code. |
| Glossary | Definitions, equations/forms, and recognition cues; use cloze preferentially with flashcard/recognition support. |
| Recall drill | No advance overview; at least 70% cloze or typed recall. |
| Easy quiz | 10 attempt items; at least 70% multiple choice. STEM items each have at least 2 dimensions. Non-STEM procedural topics include code when applicable. |
| Hard quiz | 10 attempt items; at least 70% symbolic/free response for STEM or code/free response for non-STEM. STEM items each have at least 3 dimensions and named transfer context. |
| Olympiad quiz | STEM only; 5 multiple-choice items. Each item has at least 5 dimensions and a named extension objective. It may require comprehensive cross-STEM knowledge and outside study. Withhold diagrams where independently deciding to draw/model one is part of the challenge; explanations must give the full modeling and solution path. |
| Easy/hard test | 20 attempt items. STEM permits free/symbolic response only; non-STEM permits free response/code only. STEM easy items require 2 dimensions; hard items require 3 plus documented transfer context. Hard tests remain clear, not deceptive. |
| Olympiad test | STEM only; 5 exceptionally difficult items with 5 or more dimensions and a named extension objective, plus extensive documentation and explanations. Outside research/tool use and broad domain knowledge may be expected; each item must still state its answer format and necessary factual givens. |
| Directed project | Non-STEM plus Electrical Engineering/Electronics and Circuits only; requires real-world practice guidance and measurable completion checks. |

`interactiveExploration` is out of scope for this v1 policy beyond normal schema validation.

## Finals Practice areas

Finals Practice areas are exempt from the normal learn-to-practice progression and may contain only quizzes and tests. Each such area must contain at least one Easy Test, one Hard Test, and one Olympiad Test. Those tests retain their ordinary contract requirements: Easy and Hard Tests have 20 attempt items, Olympiad Tests have 5, and all count, difficulty-dimension, answer, explanation, and provenance requirements still apply.

## Enforcement

For newly created or materially modified STEM quiz/test items, missing or invalid difficulty dimensions, insufficient distinct dimensions, missing difficulty evidence, and absent required transfer objectives are blocking save-time defects.

For all newly created or materially modified answer-bearing items, missing explanation labels and placeholder text are blocking save-time defects. Thin explanations remain review warnings after the structural requirements are met.

Blocking checks apply when an assessment is saved: missing category profile or authoring metadata, invalid directed-project placement, absent visual declaration/rationale, required media missing, missing quiz/test tier, nonstandard 10/20 attempt counts without an exception, fewer than seven lesson sections, missing lesson checks, or a worked example outside the 2–4 problem range.

The baseline audit reports legacy and pedagogical findings without blocking catalog loading. Warnings cover the 70% response-type mix, depth signals, weak visual rationale, and likely curriculum drift. Approved question banks additionally require verified answers, no placeholder text, no parameter-only variants, and provenance.
