# Assessment Validation Error Remediation Report

## 1. Issue Counts by Code
| Code | Description |
| --- | --- |
| `DUPLICATE_ID` | Duplicate assessment IDs across authored files |
| `INVALID_ACTIVITY_TYPE` | Navigation activity type not in accepted taxonomy |
| `INVALID_QUESTION_TYPE` | Question type unsupported or incorrectly shaped |
| `INVALID_RECALL_ITEM_TYPE` | Recall items use invalid item types |
| `INVALID_SYMBOLIC_EQUIVALENCE_MODE` | Symbolic response missing or invalid `equivalenceMode` |
| `INVALID_SYMBOLIC_TOLERANCE` | Symbolic response missing or negative `answer.tolerance` |
| `MISSING_CONCEPT_LESSON` | Concept lesson missing top-level `lesson` |
| `MISSING_PROMPT` | Missing prompt for questions/steps |
| `MISSING_RECALL_EXPECTED` | Recall answers missing required expected content |
| `MISSING_WORKED_EXAMPLE_PROBLEM` | Worked examples lack a `problem` field |
| `MISSING_WORKED_EXAMPLE_STEP_TITLE` | Worked example steps lack titles |
| `MULTIPLE_CHOICE_ANSWER_NOT_FOUND` | Answer IDs don't match available choices |
| `MULTIPLE_CHOICE_WITHOUT_CHOICES` | Multiple choice missing `choices` |
| `UNKNOWN_SUBCATEGORY_ID` | Assessment topic IDs do not exist in category |

## 2. Affected Files by Group
- **AoPS Olympiad Math**: `aops-olympiad-alg-*`, `aops-olympiad-geometry-*`, `aops-olympiad-trig-*`
- **Calculus 2**: `calc2-parametric-*`, `calc2-polar-*`
- **Precalculus**: `precalculus-conic-sections-*`
- **Physics**: Momentum, Collisions, Impulse files, `phys-n2-force-id-drill.yaml`, `phys-fric-force-id-drill.yaml`, `phys-m2d-frame-id-drill.yaml`
- **Chemistry**: Various legacy quiz files

## 3. Duplicate IDs & Taxonomy
- Need to manually scan for `DUPLICATE_ID` during Batch A.
- `physics-momentum-collisions-collisions` subcategory must be mapped correctly.

## 4. Checklist for Remediation
- [ ] Batch A: Duplicate IDs and Taxonomy Warnings
- [ ] Batch B: Concept Lessons (add `lesson`, `introduction`, `sections`)
- [ ] Batch C: Worked Examples (add `problem`, step `title`, `instruction`, valid `type`, `prompt`, `answer`)
- [ ] Batch D: Quizzes and Tests (ensure valid choices, symbolic metadata)
- [ ] Batch E: Recall Drills (supported item types, expected fields)
- [ ] Batch F: Chemistry & Physics legacy files
