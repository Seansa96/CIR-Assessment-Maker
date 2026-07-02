# Antigravity Implementation Plan: Conics, Parametric Curves, and Polar Curves Assessment Program

## Status

- **Audience:** Antigravity IDE agent
- **Project:** CIR Assessment Maker
- **Primary goal:** Build a broad, deep, schema-authored assessment program for conic sections, parametric curves, and polar curves
- **Plan state:** Ready for implementation
- **Priority:** Content quality, taxonomy correctness, and reusable reference material

Before editing, read:

- `AGENTS.md`
- `GEMINI.md`
- `docs/agent-coexistence.md`
- `docs/assessment-yaml-latex.md`
- `docs/plans/antigravity-assessment-taxonomy-validation-and-ingest.md`
- `.codex/skills/assessment-question-pipeline/SKILL.md`
- Existing assessment files for `conceptLesson`, `workedExample`, `recallDrill`, `quiz`, and `test`
- `data/categories/precalculus.yaml`
- `data/categories/calculus-2.yaml`
- `data/areas.yaml`

Check `git status --short` before editing. Do not alter runtime state, especially:

- `.cir-processes.json`
- `data/retention/quizapp.db`
- `data/project-sessions/`
- `data/attempts/`
- `data/grades/`
- `logs/`

## Execution Constraints

- Create the reference base and question bank before drafting final assessments.
- Prioritize breadth, depth, and varied problem shape over speed.
- Avoid generating assessments that repeat the same question with changed coefficients.
- Quizzes and tests must be at least 10 questions and should normally be 10 to 15 questions.
- Every quiz/test family must have an easy version and a hard version.
- Use existing schemas and frontend capabilities. Do not add new assessment types or renderer features unless the current schema cannot represent the required content.
- Use schema-authored content only. Do not add frontend creator support.
- Create new subcategories, areas, or topic mappings if existing taxonomy cannot represent the content cleanly.
- Keep category, subcategory, area, assessment, section, item, and question IDs lowercase, hyphenated, and stable.
- Keep YAML/JSON as the authored source of truth.
- Do not manually patch the live SQLite database.
- Do not run broad exploratory tests. Run focused content validation and the minimum build/parser checks needed to ensure the application does not crash.
- At completion, report changed files, new assessment IDs, commands run, checks passed/failed, and any remaining manual review.

## Current Taxonomy Starting Point

Precalculus already has these useful topics:

- `precalc-conics` - Conic Sections
- `precalc-parametric` - Parametric Equations
- `precalc-polar` - Polar Coordinates
- `precalc-polar-graphs` - Polar Graphs

Calculus 2 currently has no dedicated parametric or polar calculus subcategories. Add them before creating Calc 2 assessments.

Recommended new Calculus 2 subcategories:

```yaml
- id: parametric-curves
  title: Parametric Curves
- id: parametric-derivatives
  title: Derivatives of Parametric Curves
- id: parametric-integrals
  title: Integrals of Parametric Curves
- id: polar-curves
  title: Polar Curves
- id: polar-calculus
  title: Calculus with Polar Curves
```

Recommended new Calculus 2 area:

```yaml
- id: calculus-parametric-polar
  title: Parametric and Polar Calculus
  description: Parametric motion, parametric derivatives and integrals, polar graph structure, and polar calculus techniques.
  categoryIds:
    - calculus-2
  subcategoryIds:
    - parametric-curves
    - parametric-derivatives
    - parametric-integrals
    - polar-curves
    - polar-calculus
```

Keep conic sections in Precalculus under `precalc-conics` unless a specific Calc 2 assessment requires conics only as a polar-curve support topic.

## Phase 1: Build The Reference Base First

Create a small reusable reference base before drafting assessments.

Recommended files:

- `docs/assessment-reference/conics-parametric-polar-reference.md`
- `docs/assessment-reference/conics-parametric-polar-question-bank.yaml`

If `docs/assessment-reference/` does not exist, create it.

### Reference Document Requirements

The reference document should include:

- Concept maps for each topic cluster.
- Formula tables with clear conditions of use.
- Decision trees for choosing methods.
- Worked method outlines.
- Common error catalogs.
- Expected answer-format conventions.
- Recommended question types for each topic.
- Difficulty ladders from recognition to synthesis.

Use original wording. The purpose is to make future assessment generation consistent, not to copy textbook material.

### Question Bank Requirements

The bank should be extensible and easy for future agents to pull from. Use a lightweight YAML structure like this:

```yaml
schemaVersion: 1
bankId: conics-parametric-polar
items:
  - id: conics-complete-square-circle-001
    topicId: precalc-conics
    difficulty: easy
    learningGoals:
      - learn
      - practice
    assessmentFits:
      - workedExample
      - quiz
    questionTypes:
      - symbolicResponse
      - multipleChoice
    promptSeed: |
      Convert a general second-degree equation into standard circle form.
    solutionOutline: |
      Group $x$ and $y$ terms, complete the square in each variable, then divide to isolate the radius.
    commonErrors:
      - Forgetting to add the completed-square constants to both sides.
      - Misidentifying the radius as $r^2$ instead of $r$.
    tags:
      - complete-the-square
      - standard-form
```

Minimum bank coverage before drafting final assessments:

- Conic Sections: at least 40 bank items.
- Basics of Parametric Curves: at least 30 bank items.
- Derivatives of Parametric Curves: at least 30 bank items.
- Integrals of Parametric Curves: at least 30 bank items.
- Polar Curves: at least 35 bank items.
- Calculus with Polar Curves: at least 35 bank items.
- Cumulative synthesis: at least 40 mixed bank items.

Bank items do not have to be final full questions, but each item must be specific enough to generate a distinct prompt and solution.

## Phase 2: Scope The Assessment Program

Create content for these topic clusters:

1. Conic Sections
2. Basics of Parametric Curves
3. Derivatives of Parametric Curves
4. Integrals of Parametric Curves
5. Polar Curves
6. Calculus with Polar Curves
7. Cumulative Parametric, Polar, and Conics Review

For each topic cluster, create:

- 1 concept lesson
- 1 recall drill
- 1 in-depth worked example
- 1 easy quiz, 10 to 15 questions
- 1 hard quiz, 10 to 15 questions

Create tests in easy and hard versions for:

- Conic Sections
- Parametric Curves
- Polar Curves
- Cumulative Parametric, Polar, and Conics Review

Tests should be 12 to 15 questions unless there is a strong reason to use exactly 10.

## Phase 3: Assessment Design Standards

### Concept Lessons

Use `assessmentType: conceptLesson`.

Each concept lesson should have:

- 8 to 12 sections.
- Clear section titles.
- A short introduction.
- At least 5 embedded checks.
- A mix of `multipleChoice`, `selectAll`, `symbolicResponse`, `numericResponse`, and short `freeResponse` self-check where appropriate.
- A final synthesis check.

Concept lessons should teach structure and decision-making, not simply list formulas.

### Recall Drills

Use `assessmentType: recallDrill`.

Each recall drill should have:

- 25 to 40 items.
- A mix of `flashcard`, `cloze`, `typed`, and `symbolic`.
- Items for formulas, conditions, warning signs, graph families, and method triggers.
- Repeated important facts in different forms, not exact duplicate prompts.

### Worked Examples

Use `assessmentType: workedExample`.

Each worked example should have:

- 1 or 2 substantial example problems.
- 8 to 14 steps.
- Step-by-step checks that force the learner to identify structure before calculating.
- Hints that name the relevant method, identity, or formula without fully solving the step.
- Explanations that state why the method is chosen and what would go wrong with nearby wrong methods.
- A final independent solve step using `symbolicResponse`, `numericResponse`, or `freeResponse` as appropriate.

### Quizzes

Use `assessmentType: quiz`.

Each easy quiz should:

- Have 10 to 12 questions.
- Prioritize recognition, setup, formula selection, and straightforward calculation.
- Include at least 3 question types.

Each hard quiz should:

- Have 12 to 15 questions.
- Include multi-step and mixed-representation problems.
- Include at least 4 question types when schema support allows.
- Include distractors based on common mistakes.

### Tests

Use `assessmentType: test`.

Each easy test should:

- Have 12 to 15 questions.
- Cover the full cluster breadth.
- Mix recognition, setup, and calculation.

Each hard test should:

- Have 12 to 15 questions.
- Require synthesis across multiple techniques.
- Use free response or symbolic response for at least several questions.
- Include graph/interpretation prompts where useful.

## Phase 4: Topic Coverage Requirements

### Conic Sections

Use category/subcategory:

```yaml
categoryId: precalculus
subcategoryIds:
  - precalc-conics
```

Cover:

- Standard forms of circles, ellipses, hyperbolas, and parabolas.
- Completing the square to reach standard form.
- Centers, vertices, co-vertices, foci, axes, radii, and asymptotes.
- Directrix and focus interpretation for parabolas.
- Eccentricity at an introductory level.
- Identifying conic type from an equation.
- Translating between graph features and equations.
- Common mistakes with signs, denominators, and square completion.

Recommended varied prompts:

- Match equation to conic type.
- Complete a standard form.
- Identify a missing parameter.
- Choose the correct graph feature.
- Explain why an equation is not a particular conic.
- Build an equation from described features.

### Basics of Parametric Curves

Use category/subcategory:

```yaml
categoryId: calculus-2
subcategoryIds:
  - parametric-curves
```

Cover:

- What a parameter represents.
- How parametric curves encode position over time or another independent variable.
- Eliminating the parameter.
- Orientation and tracing direction.
- Domain restrictions after eliminating the parameter.
- Common parameterizations of lines, circles, ellipses, and simple motion.
- Position vector interpretation.
- Speed as magnitude of the velocity vector when appropriate.

Recommended varied prompts:

- Identify orientation from sample parameter values.
- Eliminate a parameter and state the restricted domain.
- Match a parameterization to a graph description.
- Write a parameterization from a geometric description.
- Explain why two parameterizations can trace the same curve differently.

### Derivatives of Parametric Curves

Use category/subcategory:

```yaml
categoryId: calculus-2
subcategoryIds:
  - parametric-derivatives
```

Cover:

- $\frac{dy}{dx}=\frac{dy/dt}{dx/dt}$.
- Conditions where $dx/dt=0$ requires caution.
- Tangent line equations.
- Horizontal and vertical tangents.
- $\frac{d^2y}{dx^2}=\frac{d}{dt}\left(\frac{dy}{dx}\right)\big/\frac{dx}{dt}$.
- Concavity from parametric second derivative.
- Cusps or non-smooth behavior at special parameter values.

Recommended varied prompts:

- Compute slope at a parameter value.
- Find a tangent line.
- Identify horizontal or vertical tangents.
- Determine concavity at a point.
- Explain why a formula cannot be applied blindly when $dx/dt=0$.

### Integrals of Parametric Curves

Use category/subcategory:

```yaml
categoryId: calculus-2
subcategoryIds:
  - parametric-integrals
```

Cover:

- Area under a parametric curve:

  $$
  \int y\,dx=\int y(t)x'(t)\,dt.
  $$

- Signed area and the role of orientation.
- Arc length:

  $$
  L=\int_a^b\sqrt{\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2}\,dt.
  $$

- Distance traveled versus displacement.
- Surface area if it matches current course coverage.
- Choosing bounds in terms of $t$.

Recommended varied prompts:

- Set up an area integral from $x(t)$ and $y(t)$.
- Identify when orientation makes the area signed.
- Compute an arc length integral.
- Compare distance traveled to displacement.
- Choose correct parameter bounds from endpoint conditions.

### Polar Curves

Use category/subcategory:

```yaml
categoryId: calculus-2
subcategoryIds:
  - polar-curves
```

Cover:

- Polar coordinates and the meaning of $r$ and $\theta$.
- Conversion formulas:

  $$
  x=r\cos\theta,\qquad y=r\sin\theta,\qquad r^2=x^2+y^2.
  $$

- Negative $r$ and duplicate representations.
- Symmetry tests.
- Common families: circles, cardioids, limacons, roses, lemniscates, and spirals.
- Graph recognition.
- Intersections and repeated points.

Recommended varied prompts:

- Convert between polar and rectangular form.
- Match a polar equation to a graph family.
- Determine symmetry.
- Identify duplicated polar points.
- Explain why an intersection is missed if only equations are solved algebraically.

### Calculus With Polar Curves

Use category/subcategory:

```yaml
categoryId: calculus-2
subcategoryIds:
  - polar-calculus
```

Cover:

- Polar area:

  $$
  A=\frac12\int_\alpha^\beta r^2\,d\theta.
  $$

- Choosing bounds from symmetry and graph structure.
- Inner loops and region subtraction.
- Area between polar curves.
- Polar tangent slope:

  $$
  \frac{dy}{dx}=
  \frac{r'(\theta)\sin\theta+r(\theta)\cos\theta}
       {r'(\theta)\cos\theta-r(\theta)\sin\theta}.
  $$

- Horizontal and vertical tangents.
- Polar arc length:

  $$
  L=\int_\alpha^\beta\sqrt{r^2+\left(\frac{dr}{d\theta}\right)^2}\,d\theta.
  $$

Recommended varied prompts:

- Choose correct bounds for a polar area.
- Calculate a simple polar area.
- Identify when symmetry can reduce work.
- Set up area between curves.
- Compute or interpret a tangent slope.
- Recognize an inner-loop condition.

### Cumulative Review

Use category/subcategory:

```yaml
categoryId: calculus-2
subcategoryIds:
  - parametric-curves
  - parametric-derivatives
  - parametric-integrals
  - polar-curves
  - polar-calculus
```

The cumulative tests should also include conic-section support questions when they are needed to recognize shapes, but keep the primary category as Calculus 2.

Cover:

- Method selection across rectangular, parametric, and polar representations.
- Choosing whether to eliminate a parameter, differentiate parametrically, integrate parametrically, convert coordinates, or use polar area.
- Graph and equation interpretation.
- Mixed calculation and explanation prompts.

## Phase 5: File Naming And Metadata

Use predictable assessment filenames.

Recommended filenames:

- `precalculus-conic-sections-concept-lesson.yaml`
- `precalculus-conic-sections-recall.yaml`
- `precalculus-conic-sections-worked-example.yaml`
- `precalculus-conic-sections-easy-quiz.yaml`
- `precalculus-conic-sections-hard-quiz.yaml`
- `precalculus-conic-sections-easy-test.yaml`
- `precalculus-conic-sections-hard-test.yaml`
- `calc2-parametric-curves-basics-concept-lesson.yaml`
- `calc2-parametric-curves-basics-recall.yaml`
- `calc2-parametric-curves-basics-worked-example.yaml`
- `calc2-parametric-curves-basics-easy-quiz.yaml`
- `calc2-parametric-curves-basics-hard-quiz.yaml`
- `calc2-parametric-derivatives-concept-lesson.yaml`
- `calc2-parametric-derivatives-recall.yaml`
- `calc2-parametric-derivatives-worked-example.yaml`
- `calc2-parametric-derivatives-easy-quiz.yaml`
- `calc2-parametric-derivatives-hard-quiz.yaml`
- `calc2-parametric-integrals-concept-lesson.yaml`
- `calc2-parametric-integrals-recall.yaml`
- `calc2-parametric-integrals-worked-example.yaml`
- `calc2-parametric-integrals-easy-quiz.yaml`
- `calc2-parametric-integrals-hard-quiz.yaml`
- `calc2-parametric-curves-easy-test.yaml`
- `calc2-parametric-curves-hard-test.yaml`
- `calc2-polar-curves-concept-lesson.yaml`
- `calc2-polar-curves-recall.yaml`
- `calc2-polar-curves-worked-example.yaml`
- `calc2-polar-curves-easy-quiz.yaml`
- `calc2-polar-curves-hard-quiz.yaml`
- `calc2-polar-calculus-concept-lesson.yaml`
- `calc2-polar-calculus-recall.yaml`
- `calc2-polar-calculus-worked-example.yaml`
- `calc2-polar-calculus-easy-quiz.yaml`
- `calc2-polar-calculus-hard-quiz.yaml`
- `calc2-polar-curves-easy-test.yaml`
- `calc2-polar-curves-hard-test.yaml`
- `calc2-parametric-polar-cumulative-easy-test.yaml`
- `calc2-parametric-polar-cumulative-hard-test.yaml`

Every assessment should include `navigation`.

Examples:

```yaml
navigation:
  learningGoal: learn
  activityType: conceptLesson
  tags:
    - conic-sections
    - complete-the-square
```

```yaml
navigation:
  learningGoal: practice
  activityType: focusedPractice
  tags:
    - parametric-derivatives
    - tangent-lines
```

```yaml
navigation:
  learningGoal: evaluate
  activityType: formalTest
  tags:
    - polar-calculus
    - cumulative-review
```

Suggested learning-goal/activity mappings:

- Concept lessons: `learn` / `conceptLesson`
- Worked examples: `learn` / `guidedWorkedExample`
- Recall drills: `recall` / `mixedRecallSet`
- Easy and hard quizzes: `practice` / `focusedPractice`
- Tests: `evaluate` / `formalTest`

## Phase 6: Media And Graphs

Use generated diagrams when a visual prompt is genuinely helpful.

Recommended asset paths:

- `frontend/public/assessments/conics-parametric-polar/`

Use Python/matplotlib for:

- Conic graphs.
- Parametric traces with arrows for orientation.
- Polar curves.
- Region-shading diagrams for polar area.
- Comparison diagrams showing repeated polar points or symmetry.

Rules:

- Keep generated media stable and checked in as source assets only under `frontend/public/assessments/...`.
- Do not edit generated frontend output under `frontend/dist/`.
- Every media reference must include meaningful alt text.
- Keep prompt text in YAML, even when an image is included, so the assessment remains searchable and reviewable.

## Phase 7: Variety Rules

Before marking a topic complete, verify that its assessments include varied cognitive tasks.

Use these prompt families across the program:

- Recognition: identify the graph family, formula, or method.
- Recall: produce a formula or condition from memory.
- Setup: choose bounds, variables, or representation.
- Calculation: compute slope, area, arc length, tangent, or feature.
- Explanation: justify why a method applies.
- Error diagnosis: identify a false step or missing condition.
- Graph interpretation: infer algebraic behavior from a graph.
- Representation conversion: translate between rectangular, parametric, and polar forms.
- Synthesis: choose among multiple possible approaches.

Avoid these failure modes:

- Ten questions that only ask "compute the derivative."
- Ten questions that only ask for a formula.
- Every correct multiple-choice answer appearing in the same position.
- Reusing the same equation shape with only changed coefficients.
- Explanations that state only the final answer.
- Hard quizzes that are merely longer arithmetic.

## Phase 8: YAML And Schema Rules

Follow `docs/assessment-yaml-latex.md`.

Important rules:

- Use block scalars for long prompts, explanations, lesson content, and LaTeX-heavy text.
- Use single quotes for short inline LaTeX.
- Never put ordinary LaTeX backslashes inside double-quoted YAML strings.
- Use `$...$` for inline math and `$$...$$` for display math.
- Use `subcategoryIds`, not `subcategoryId`.
- Use `navigation.learningGoal`, not top-level `learningGoal`.
- Use `navigation.activityType`, not top-level `activityType`.
- For `symbolicResponse`, use `answer.expectedLatex`.
- For `numericResponse`, use `answer.value` and a non-negative `tolerance`.
- For free response, use `answer.gradingMode: selfCheck`.
- Keep question IDs unique inside each assessment.
- Keep recall item IDs unique inside each recall drill.
- Keep concept lesson section IDs unique.
- Keep worked example step IDs unique.

## Phase 9: Implementation Order

Implement in this order:

1. Taxonomy update:
   - Add missing Calculus 2 subcategories.
   - Add `calculus-parametric-polar` area.
   - Confirm Precalculus conics and Precalculus polar/parametric topics remain mapped.

2. Reference base:
   - Create the reference markdown.
   - Create the question bank YAML.
   - Include formulas, method triggers, common errors, and item seeds.

3. Conic Sections batch:
   - Concept lesson.
   - Recall drill.
   - Worked example.
   - Easy quiz.
   - Hard quiz.
   - Easy test.
   - Hard test.

4. Parametric Curves batch:
   - Basics concept lesson, recall drill, worked example, easy quiz, hard quiz.
   - Derivatives concept lesson, recall drill, worked example, easy quiz, hard quiz.
   - Integrals concept lesson, recall drill, worked example, easy quiz, hard quiz.
   - Easy parametric test.
   - Hard parametric test.

5. Polar Curves batch:
   - Polar curves concept lesson, recall drill, worked example, easy quiz, hard quiz.
   - Polar calculus concept lesson, recall drill, worked example, easy quiz, hard quiz.
   - Easy polar test.
   - Hard polar test.

6. Cumulative batch:
   - Easy cumulative test.
   - Hard cumulative test.
   - Include conics only where they support polar/parametric interpretation.

7. Validation and final taxonomy sweep.

## Phase 10: Final Sweep

Run a final sweep before reporting completion.

### Taxonomy Sweep

Verify:

- Every assessment `categoryId` exists.
- Every `subcategoryIds` entry exists in the relevant category file.
- Every subcategory used by the new assessments appears in at least one appropriate area in `data/areas.yaml`.
- No new assessment falls into `Other / Unmapped` unless explicitly intended, which should not happen for this project.
- New Calculus 2 parametric/polar subcategories are mapped to `calculus-parametric-polar`.
- Conic assessments use `precalc-conics` and are mapped through the existing Precalculus area structure.

### Content Sweep

Verify:

- Every quiz has 10 to 15 questions.
- Every test has 10 to 15 questions.
- Easy and hard versions exist for every quiz/test family required by this plan.
- Hard versions involve deeper method choice, synthesis, graph interpretation, or multi-step work, not just bigger numbers.
- Question-type variety exists in every quiz/test.
- Every explanation names the exact formula, identity, representation, or technique being used.
- Every media reference resolves to a stable `frontend/public/...` asset.
- Every graph/image has meaningful alt text.

### YAML Formatting Sweep

Run the LaTeX double-quote/backslash scan from `docs/assessment-yaml-latex.md` against changed YAML files.

Review any hits manually. If a hit contains LaTeX, convert the field to a block scalar or single-quoted scalar.

Also scan for:

- Trailing tabs.
- Duplicate IDs.
- `subcategoryId:` singular.
- Top-level `learningGoal:` or `activityType:` outside `navigation`.
- `expected:` used where `symbolicResponse` needs `expectedLatex`.
- `value:` omitted from `numericResponse`.

## Focused Validation

Add important new assessment IDs to the repository content-validation theory if that is the current repo convention.

Run focused checks only:

```powershell
dotnet build backend\QuizApp.sln --no-restore
dotnet test backend\QuizApp.sln --no-build --filter "FileAssessmentRepository|AssessmentValidator|NavigationCatalog"
```

If frontend media or rendering paths were changed, also run:

```powershell
Set-Location frontend
npm run build
```

Do not run repeated browser automation or broad exploratory tests. Leave manual interaction review to the user unless the app fails to start.

## Acceptance Criteria

The work is complete when:

- The reference markdown file exists.
- The question-bank YAML exists and has the minimum bank coverage specified in this plan.
- New Calculus 2 parametric/polar subcategories exist if they were missing.
- The relevant areas/topics are mapped in `data/areas.yaml`.
- Each requested topic has a concept lesson, recall drill, worked example, easy quiz, and hard quiz.
- Conic, parametric, polar, and cumulative tests exist in easy and hard versions.
- Quizzes and tests contain 10 to 15 questions.
- Assessment content uses varied wording, varied representations, and varied question types.
- YAML formatting passes the LaTeX/backslash review.
- No new assessment is orphaned from category/area/topic navigation.
- Focused backend checks pass, or failures are documented clearly.

## Completion Report

Report:

- Files changed.
- New category, subcategory, and area IDs.
- New assessment IDs grouped by topic.
- Question-bank coverage counts by topic.
- Commands run.
- Checks passed and failed.
- Any YAML scan warnings and how they were resolved.
- Any remaining manual checks the user should perform in the UI.

