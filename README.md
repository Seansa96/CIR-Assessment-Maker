# CIR Assessment Maker

Local-first quiz/test app for STEM study, self-assessment, attempt review, and grade logging.

## Stack

- Backend: ASP.NET Core Web API, C#, file-backed repositories, YAML/JSON assessment files
- Frontend: Astro, TypeScript, localhost-first UI
- Storage: files under `data/`

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

Open the Astro dev server at `http://127.0.0.1:4321`.

## Backend Tests

```bash
dotnet test backend/QuizApp.sln
```

## Project Layout

```txt
backend/
  src/
    QuizApp.Api/             ASP.NET Core API endpoints
    QuizApp.Core/            Domain models, repository interfaces, validation, scoring
    QuizApp.Infrastructure/  File-backed YAML/JSON repositories
  tests/
    QuizApp.Tests/           Validation, scoring, attempt, and grade-log tests

frontend/
  src/pages/index.astro      MVP app shell and core assessment flow
  src/styles/global.css      Local UI styling

data/
  settings.yaml
  categories/
  assessments/
  attempts/
  grades/
  samples/
```

## MVP Flow

1. Load categories and assessments from local files.
2. Start a practice or scored attempt.
3. Save the randomized question order on the attempt.
4. Submit multiple-choice, select-all, or free-response self-check answers.
5. Complete the attempt and review results.
6. Commit the score to the grade log.

Assessment File Format

Assessments can be defined in either JSON or YAML format. Both formats support the same schema and are intended to be human-readable and easy to edit by hand.

Every assessment consists of:

Metadata
Configuration options
A collection of questions
Answers and explanations
Assessment Structure
Field	Description
schemaVersion	Schema version used by the file.
id	Unique identifier for the assessment.
title	Display name shown to the user.
assessmentType	Either quiz or test.
categoryId	Parent category identifier.
subcategoryIds	One or more subcategories associated with the assessment.
modeDefault	Default mode (practice or scored).
randomizeQuestions	Whether questions should be shuffled by default.
questionTimerSeconds	Optional per-question timer.
assessmentTimerSeconds	Optional overall assessment timer.
questions	Collection of assessment questions.
JSON Example
{
  "schemaVersion": 1,
  "id": "integration-techniques-mini",
  "title": "Integration Techniques Mini Quiz",
  "assessmentType": "quiz",
  "categoryId": "calculus-2",
  "subcategoryIds": ["integration-techniques"],
  "modeDefault": "practice",
  "randomizeQuestions": false,
  "questionTimerSeconds": null,
  "assessmentTimerSeconds": null,
  "questions": [
    {
      "id": "q001",
      "type": "multipleChoice",
      "prompt": "Which technique is often useful for integrals involving products of functions?",
      "choices": [
        {
          "id": "a",
          "text": "Integration by parts"
        },
        {
          "id": "b",
          "text": "Direct substitution only"
        }
      ],
      "answer": {
        "choiceId": "a"
      },
      "explanation": "Integration by parts is designed for products where differentiating one factor simplifies the integral."
    }
  ]
}
YAML Example
schemaVersion: 1
id: area-between-curves-basic
title: Area Between Curves Basic Quiz
assessmentType: quiz
categoryId: calculus-2
subcategoryIds:
  - area-between-curves

modeDefault: practice
randomizeQuestions: true

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

      - id: c
        text: "The x-coordinate of an intersection point"

    answer:
      choiceId: a

    explanation: >
      Area between curves measures the accumulated difference
      between upper and lower functions.

  - id: q002
    type: freeResponse
    prompt: "Explain what the integral represents in an area-between-curves problem."

    answer:
      expected: >
        It represents the accumulated difference between
        the upper and lower functions over an interval.
      gradingMode: selfCheck

    explanation: >
      The integral sums vertical differences over the interval.
Supported Question Types
Multiple Choice

Single correct answer.

- id: q001
  type: multipleChoice

  prompt: "Which derivative rule is used here?"

  choices:
    - id: a
      text: "Product Rule"

    - id: b
      text: "Chain Rule"

    - id: c
      text: "Quotient Rule"

  answer:
    choiceId: b

  explanation: >
    The chain rule applies because one function
    is composed inside another.
Select All That Apply

Multiple correct answers.

- id: q002
  type: selectAll

  prompt: "Which of the following are trigonometric identities?"

  choices:
    - id: a
      text: "sin²(x) + cos²(x) = 1"

    - id: b
      text: "1 + tan²(x) = sec²(x)"

    - id: c
      text: "sin(x) = x²"

  answer:
    choiceIds:
      - a
      - b

  explanation: >
    The first two are standard Pythagorean identities.
Free Response

Used for open-ended conceptual questions.

The MVP uses self-check grading.

- id: q003
  type: freeResponse

  prompt: >
    Explain the difference between velocity and acceleration.

  answer:
    expected: >
      Velocity describes the rate of change of position,
      while acceleration describes the rate of change of velocity.

    gradingMode: selfCheck

  explanation: >
    Velocity measures motion. Acceleration measures how that motion changes.
Practice vs Scored Mode
Practice Mode

Practice mode is designed for learning and immediate feedback.

Features:

Immediate answer checking
Explanations available after submission
Scores tracked locally
Optional grade-log commit after completion

Recommended for:

Studying
Reviewing notes
Learning new material
CIR remediation exercises
Scored Mode

Scored mode simulates a traditional assessment.

Features:

Answers hidden until completion
Explanations hidden until completion
Final score revealed at the end
Grade-log support

Recommended for:

Exam preparation
Benchmarking progress
Periodic self-assessment
Assessment Limits

Current defaults:

Type	Default Length	Maximum Length
Quiz	15 Questions	50 Questions
Test	25 Questions	200 Questions

These values may be customized through application settings.

Validation Rules

Assessment files are validated before use.

Validation includes:

Missing IDs
Duplicate question IDs
Missing prompts
Invalid question types
Invalid answer references
Invalid assessment types
Question count limits
Schema version compatibility

Invalid assessments will not be loaded until corrected.

Future Question Types

Planned question types include:

Matching
Ordering
Fill-in-the-Blank
Numerical Response
Equation Entry
Multi-Part Questions
Diagram-Based Questions
Programming Questions
Proof / Rubric-Based Responses

These are not required for the MVP but are planned for future releases.
