# CIR Assessment Maker

CIR Assessment Maker is a local-first quiz, test, Worked Example, Recall Drill, Guided Project, and grade-tracking app for personal STEM study.

The core learning loop is:

```txt
Load assessment -> answer questions -> review feedback -> commit scores -> find weak topics -> study deliberately
```

The app is intentionally local-first. Authored content and configuration are file-backed; durable attempts and committed grades use embedded SQLite, while actively running attempts live in memory.

Developer and agent collaboration guidance:

* [Shared repository instructions](AGENTS.md)
* [Codex and Gemini coexistence report](docs/agent-coexistence.md)

## Current State

Implemented:

* ASP.NET Core Web API backend
* Astro + TypeScript frontend
* YAML and JSON assessment loading
* File-backed authored content and configuration
* SQLite attempt and grade retention
* In-memory active attempt sessions
* Categories and subcategories
* Practice and scored modes
* Quiz and test assessments
* Schema-only Worked Example assessments
* Recall Drill assessments
* Guided Project assessments
* Resumable attempt sessions
* Save and quit, quit early, review, delete, and bulk delete attempt flows
* Grade log with category, area, question-type, and weak-topic analytics
* Markdown + LaTeX rendering with `remark-math`, `rehype-katex`, and KaTeX
* Symbolic math input with MathLive
* Symbolic equivalence checks through CortexJS Compute Engine
* Code questions through a Piston-compatible runner adapter
* Image/media schema support

Supported question types:

* `multipleChoice`
* `selectAll`
* `freeResponse`
* `numericResponse`
* `symbolicResponse`
* `code`

## Run Locally

Start the backend:

```bash
dotnet run --project backend/src/QuizApp.Api --urls http://localhost:5000
```

Start the frontend:

```bash
cd frontend
npm install
npm run dev
```

Open:

```txt
http://127.0.0.1:4321
```

Run backend tests:

```bash
dotnet test backend/QuizApp.sln
```

Build the frontend:

```bash
cd frontend
npm run build
```

## Project Layout

```txt
backend/
  src/
    QuizApp.Api/             API endpoints and contracts
    QuizApp.Core/            Domain models, validation, scoring, services
    QuizApp.Infrastructure/  File/SQLite repositories and external adapters
  tests/
    QuizApp.Tests/           Validation, scoring, attempts, analytics tests

frontend/
  src/pages/index.astro      App shell and assessment flow
  src/styles/global.css      UI styling

data/
  settings.yaml              App defaults
  areas.yaml                 Manual area mappings for analytics
  categories/                Category and subcategory files
  assessments/               Authored assessment files
  retention/quizapp.db       Durable attempts and committed grades
  project-sessions/          Guided-project working sessions
  attempts/                  Legacy attempt JSON migration input
  grades/                    Legacy grade-log migration input
  samples/                   Sample media/files
```

## Assessment Types

Use `assessmentType` to choose the kind of experience.

### Quiz

Use `quiz` for short practice loops, topic checks, and rapid repetition.

Good for:

* Concept checks
* Homework-style drills
* Mixed question practice
* Low-friction remediation

Default length: 15 questions. Maximum: 50 questions.

### Test

Use `test` for longer, more formal self-assessment.

Good for:

* Exam simulation
* Larger review sessions
* Scored checkpoints
* Periodic progress measurement

Default length: 25 questions. Maximum: 200 questions.

### Worked Example

Use `workedExample` for guided, active-learning tutorials. Worked examples are authored directly in YAML or JSON. The frontend creator intentionally does not create them.

Good for:

* Learning a new method
* Walking through a multi-step procedure
* Remediating a weak skill
* Replacing passive note review with guided action

Worked examples show one step at a time. The user can revisit previous completed steps, but future steps remain locked until the current step is completed.

### Recall Drill

Use `recallDrill` for production-from-memory practice. Users attempt recall, reveal the expected answer, and rate the result as Easy, Correct, Needs Review, or Forgot Completely.

Good for:

* Formula and identity recall
* Definitions and syntax patterns
* Concept relationships
* Recognizing which technique applies

### Guided Project

Use `guidedProject` for longer programming exercises with multiple editable files and required/bonus checks. Guided Projects are schema-authored and use the configured Piston-compatible code runner.

Good for:

* Multi-class or multi-file programming exercises
* Deeper practice beyond isolated functions
* Incremental completion with hidden checks

## Modes

### Practice Mode

Use practice mode while learning.

Practice mode:

* Shows feedback after each answer
* Shows explanations immediately
* Lets free-response answers be self-checked right away
* Can still be committed to the grade log if you want to track it

### Scored Mode

Use scored mode for benchmarking.

Scored mode:

* Hides correctness until completion
* Hides explanations until completion
* Tracks final score
* Can auto-commit depending on settings
* Requires pending free-response self-checks to be resolved before committing

## Categories And Subcategories

Categories live in `data/categories/`.

Example:

```yaml
schemaVersion: 1
id: calculus-2
title: Calculus II

subcategories:
  - id: u-sub-integration
    title: U-Substitution

  - id: volumes-of-solids
    title: Volumes of Solids

  - id: integration-techniques
    title: Integration Techniques
```

Rules of thumb:

* Use stable lowercase IDs.
* Prefer hyphenated IDs, for example `area-between-curves`.
* Do not rename IDs casually after attempts exist; attempts and analytics depend on stable IDs.
* Put broad subjects in categories and specific skills in subcategories.

## Area Mappings For Analytics

Areas are manual groupings used by the Grade Log dashboard. They let several subcategories roll up into a broader study area.

Areas live in `data/areas.yaml`.

Example:

```yaml
schemaVersion: 1
areas:
  - id: integration
    title: Integration
    categoryIds:
      - calculus-2
    subcategoryIds:
      - u-sub-integration
      - integration-techniques
      - volumes-of-solids

  - id: kinematics
    title: Kinematics
    categoryIds:
      - physics-1
    subcategoryIds:
      - constant-acceleration-2d
```

Use areas when you want the grade log to answer questions like:

* "How am I doing in integration overall?"
* "Am I weak in kinematics, or just one subtopic?"
* "Which broad review bucket deserves attention first?"

## Basic Assessment Schema

Quiz and test assessments use `questions`.

```yaml
schemaVersion: 1
id: area-between-curves-basic
title: Area Between Curves Basic Quiz
assessmentType: quiz
categoryId: calculus-2
subcategoryIds:
  - area-between-curves
modeDefault: practice
randomizeQuestions: true
attemptQuestionCount:
questionTimerSeconds:
assessmentTimerSeconds:
questions:
  - id: q001
    type: multipleChoice
    prompt: "What does the area between two curves represent?"
    choices:
      - id: a
        text: "The accumulated vertical difference between two functions over an interval"
      - id: b
        text: "The slope of the upper function"
    answer:
      choiceId: a
    explanation: "Area between curves measures the accumulated difference between upper and lower functions."
```

Required top-level fields:

* `schemaVersion`
* `id`
* `title`
* `assessmentType`
* `categoryId`
* `subcategoryIds`
* `modeDefault`
* `randomizeQuestions`
* Optional `attemptQuestionCount` for sampling a quiz/test attempt from a larger authored question bank
* `questions` for quiz/test
* `workedExamples` for worked examples
* `guidedProject` for Guided Projects
* `items` for Recall Drills

## Markdown And LaTeX Formatting

Prompts, choices, explanations, hints, and worked-example text support Markdown and LaTeX.

Inline math:

```yaml
prompt: 'Use $v_x=v_{0x}+a_xt$ to find the velocity component.'
```

Display math:

```yaml
prompt: |
  A particle has constant acceleration.

  $$
  x(t)=x_0+v_{0x}t+\frac12a_xt^2
  $$

  Solve for $x(t)$ after substituting the given values.
```

Tips:

* Wrap inline equations in `$...$`.
* Wrap display equations in `$$...$$`.
* Do not put LaTeX backslashes inside double-quoted YAML strings. Prefer block strings with `|` for longer text and single quotes for short inline LaTeX.
* Use `\,` for small spacing in integrals. Prefer `'$\int f(x)\,dx$'` instead of a double-quoted string with escaped backslashes.
* Use explanations to name the exact formula or subconcept used, not just the broad topic.
* See [Assessment YAML LaTeX Authoring](docs/assessment-yaml-latex.md) before adding LaTeX-heavy assessments.

Good explanation pattern:

```yaml
explanation: |
  Use the x-component velocity equation

  $$
  v_x=v_{0x}+a_xt
  $$

  Substitute $v_{0x}=12$ and $a_x=3$ to get $v_x=12+3t$.

  Related topic: Velocity component formula; identify the x-axis data and substitute into $v_x=v_{0x}+a_xt$.
```

## Media And Images

Questions, choices, and answers can include image media.

```yaml
media:
  - type: image
    src: /samples/washer-diagram.png
    alt: Washer cross-section diagram
    caption: Region rotated around the x-axis.
```

Choice media:

```yaml
choices:
  - id: a
    text: "Disk method"
    media:
      - type: image
        src: /samples/disk-method.png
        alt: Disk method diagram
```

Store app-served assets under `frontend/public/` or another path the frontend can reach. Public paths should usually start with `/`.

## Question Types

### Multiple Choice

Use for one correct answer.

```yaml
- id: q001
  type: multipleChoice
  prompt: "Which derivative rule applies to $\\sin(x^2)$?"
  choices:
    - id: a
      text: "Product rule"
    - id: b
      text: "Chain rule"
    - id: c
      text: "Quotient rule"
  answer:
    choiceId: b
  explanation: "The outer function is sine and the inner function is $x^2$, so this is a chain rule problem."
```

Best for:

* Concept recognition
* Formula selection
* Misconception checks
* Quick recall

### Select All

Use when multiple answers are correct.

```yaml
- id: q002
  type: selectAll
  prompt: "Which are valid setup steps for area between curves?"
  choices:
    - id: a
      text: "Identify the upper function"
    - id: b
      text: "Identify the lower function"
    - id: c
      text: "Integrate upper minus lower"
  answer:
    choiceIds: [a, b, c]
  explanation: "The setup requires determining upper/lower functions and integrating their vertical difference."
```

Best for:

* Multi-step setup knowledge
* Lists of conditions
* Checking whether a user knows every required part of a method

### Free Response

Free response is human self-check. The app does not use AI or keyword grading for it.

```yaml
- id: q003
  type: freeResponse
  prompt: "Explain why constant acceleration lets us separate 2D motion into x- and y-components."
  answer:
    expected: "The acceleration components are constant, so each axis can be modeled independently with the one-dimensional constant-acceleration equations."
    gradingMode: selfCheck
    keyPoints:
      - "Motion is split into x- and y-components."
      - "Each component uses its own acceleration."
      - "The same 1D kinematic equations apply separately."
  explanation: "Component equations work because vector motion can be decomposed into independent perpendicular axes."
```

Behavior:

* The user submits written text first.
* The answer locks.
* In practice mode, the expected answer, key points, and explanation appear immediately.
* The user marks the response correct or needs review.
* In scored mode, self-check happens after completion.

Best for:

* Concept explanations
* Method summaries
* Reflection
* Cases where wording can vary

### Numeric Response

Use when the final answer is a number with tolerance.

```yaml
- id: q004
  type: numericResponse
  prompt: |
    A particle starts from rest and accelerates at $3.0\,m/s^2$ for $4.0\,s$.
    What is its speed?
  answer:
    value: 12
    tolerance: 0.01
  explanation: |
    Use $v=v_0+at=0+3.0(4.0)=12\,m/s$.
```

Best for:

* Final decimal answers
* Unit conversion checks
* Physics and chemistry computations

Do not use `numericResponse` for full algebraic expressions or integrals. Use `symbolicResponse` instead.

### Symbolic Response

Use when the user should enter an expression, equation-like expression, derivative, or antiderivative.

Expression equivalence:

```yaml
- id: q005
  type: symbolicResponse
  prompt: |
    Enter an expression equivalent to $(x+1)^2$.
  answer:
    expectedLatex: 'x^2+2x+1'
    equivalenceMode: expression
    variables: [x]
    tolerance: 0.000001
  explanation: "Expanding $(x+1)^2$ gives $x^2+2x+1$."
```

Derivative equivalence for antiderivatives:

```yaml
- id: q006
  type: symbolicResponse
  prompt: |
    Find an antiderivative of $x^2$.
  answer:
    expectedLatex: '\frac{x^3}{3}+C'
    equivalenceMode: derivative
    variables: [x]
    tolerance: 0.000001
  explanation: "Differentiating $\\frac{x^3}{3}+C$ gives $x^2$."
```

Equivalence modes:

* `expression`: simplify/compare expressions, with numeric sampling fallback.
* `derivative`: compare derivatives with respect to the first variable, useful for indefinite integrals where constants may differ.

Best for:

* Algebraic expressions
* Trigonometric identities
* Symbolic kinematics formulas
* Antiderivatives
* Simplification/factoring checks

### Code Questions

Code questions currently support Python and C++ through a Piston-compatible code runner.

Important: code questions do not run inside this app by themselves. To use `type: code`, you need a separate containerized code-running service. The app is designed to call a local Piston-compatible API at:

```txt
http://localhost:2000/api/v2
```

In practice, that means you should run Piston or another compatible service in Docker, then point the app's Code runner URL setting at that service. Without the runner, code questions can still be authored and loaded, but submissions will not execute successfully.

High-level setup:

1. Install Docker Desktop.
2. Start Docker Desktop and confirm containers can run.
3. Run a Piston-compatible code runner container locally.
4. Expose the runner on port `2000`.
5. Confirm the API is available at `http://localhost:2000/api/v2`.
6. In this app, open Settings and set Code runner URL to `http://localhost:2000/api/v2`.

For less technical users, use external setup guides rather than trying to memorize Docker commands:

* Docker Desktop documentation: <https://docs.docker.com/desktop/>
* Piston project: <https://github.com/engineer-man/piston>
* Piston API v2 documentation: <https://piston.readthedocs.io/en/latest/api-v2/>

If Docker is unfamiliar, start with Docker Desktop first. Once Docker can run a basic container, then set up Piston. Treat the code runner as a separate local service that this app talks to, not as part of the frontend or backend.

```yaml
- id: q007
  type: code
  prompt: |
    Write a Python function `sum_even_to_n` that returns the sum of all even integers from `2` through `n`.
  language: python
  functionName: sum_even_to_n
  starterCode: |
    def sum_even_to_n(n):
        # Return the sum of even integers from 2 through n.
        return 0
  tests:
    - input: "6"
      expected: "12"
    - input: "1"
      expected: "0"
    - input: "10"
      expected: "30"
  answer: {}
  explanation: "Use `range(2, n + 1, 2)` to step through even numbers."
```

Best for:

* Small functions
* Loop practice
* Debugging basics
* Input/output logic

Code runner settings live in the Settings page:

* Code runner URL, default `http://localhost:2000/api/v2`
* Compile timeout
* Run timeout

## Worked Example Schema

Worked examples use `workedExamples`, not `questions`.

```yaml
schemaVersion: 1
id: linear-substitution-worked-example
title: Linear Substitution Worked Example
assessmentType: workedExample
categoryId: calculus-2
subcategoryIds:
  - u-sub-integration
modeDefault: practice
randomizeQuestions: false
workedExamples:
  - id: we001
    title: Solving an integral with linear substitution
    problem: "Evaluate $\\int 2(3x+1)^4\\,dx$."
    steps:
      - id: s001
        title: Check direct integration
        instruction: "Before substituting, decide whether the integrand is already in a simple antiderivative form."
        type: multipleChoice
        prompt: "Can this integral be handled cleanly by direct integration without rewriting the inner expression?"
        choices:
          - id: yes
            text: "Yes"
          - id: no
            text: "No"
        answer:
          choiceId: no
        hint: "Look for a composed expression and ask whether its derivative also appears as a constant factor."
        explanation: "The derivative of $3x+1$ is constant, so substitution is the cleaner bookkeeping move."

      - id: s002
        title: Define the substitution
        instruction: "Choose $u$ to be the inner expression whose derivative is present up to a constant factor."
        type: freeResponse
        prompt: "What should $u$ equal?"
        answer:
          expected: "$u=3x+1$"
          gradingMode: selfCheck
        hint: "Use the expression inside the fourth power."
        explanation: "Set $u=3x+1$. Then $du=3\\,dx$, so $dx=\\frac{du}{3}$."
```

Worked Example authoring guidance:

* Keep them shorter than quizzes.
* Each step should teach or test one decision.
* Use hints for the name of the method, formula, identity, or next move.
* Use explanations to remediate wrong attempts.
* Mix question types as needed.
* Put the most important formula/manipulation directly in the step explanation.

## Validation Rules

The backend validates assessment files before use.

Common validation checks:

* Missing assessment IDs
* Missing category IDs
* Missing prompts
* Duplicate question IDs
* Invalid assessment type
* Invalid question type
* Multiple choice without choices
* Multiple choice answer ID not found in choices
* Select-all answer IDs not found in choices
* Quiz over 50 questions
* Test over 200 questions
* Invalid timers
* Invalid symbolic metadata
* Invalid code question metadata
* Worked examples without steps

## Grade Log And Analytics

The Grade Log is now a lightweight analytics dashboard.

It shows:

* Overall committed average
* Committed score count
* Attempt session count
* Weakest category
* Weakest area
* Weakest question type
* Category averages
* Area averages
* Question-type performance
* Committed scores
* Attempt history

Attempt history supports:

* Continue
* Save and quit
* Quit early
* Review
* Commit
* Delete
* Bulk delete
* Filtering
* Sorting

Use the Grade Log to answer:

* Which category is weakest?
* Which broad area should I review first?
* Am I missing a topic, or a question type?
* Are free responses still awaiting self-check?
* Do practice attempts and scored attempts tell different stories?

Committed grades are the official averages. Completed attempts can still inform diagnostic question-type performance.

## Learning Workflow

A useful study loop:

1. Start with a Worked Example for a new or shaky method.
2. Take a short practice quiz immediately after.
3. Read every explanation, especially for wrong answers.
4. Commit meaningful practice scores when they reflect real effort.
5. Use the Grade Log to find weak categories, areas, and question types.
6. Create or select another assessment targeting the weakest area.
7. Use scored mode only when you want a benchmark.

Recommended mode choices:

* New material: Worked Example
* First independent practice: quiz in practice mode
* Fluency building: repeated quizzes
* Exam readiness: test in scored mode
* Concept repair: free-response-heavy practice
* Formula manipulation: symbolicResponse-heavy practice
* Calculation accuracy: numericResponse questions
* Programming fundamentals: code questions

## Authoring Good Assessments

Good assessments are specific.

Prefer:

```txt
Related topic: Velocity component formula; identify v0x and ax, then substitute into vx = v0x + ax t.
```

Over:

```txt
Related topic: Kinematics.
```

Good prompts ask for one thing at a time. Good explanations name the exact formula, law, theorem, identity, or reasoning step the user should have used.

For STEM questions:

* Include the relevant equation in the explanation.
* State why the chosen method applies.
* Show the substitution or manipulation.
* Mention common traps when useful.
* Use `keyPoints` for free-response rubrics.
* Use areas to group related subcategories for review.

## Settings

The Settings page controls:

* Default mode
* Default question order
* Default quiz length
* Default test length
* Question timer default
* Assessment timer default
* Scored attempt auto-commit behavior
* Code runner URL and timeouts

Timers are present in the schema/settings but remain simple for now. Assessments are untimed unless configured.

## Notes And Limitations

Current intentional boundaries:

* No authentication
* No cloud sync
* No public deployment workflow
* SQLite retention currently covers attempts and grades; authored content remains file-backed
* No AI grading
* No LMS integration
* Worked Example creation is schema-only
* Recall Drill and Guided Project creation are schema-only
* Code question execution requires a local/containerized Piston-compatible runner

Planned improvements live in `planned-features.md`.
