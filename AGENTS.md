# AGENTS.md

## Project Purpose

This project is a local-first quiz/test application designed for personal STEM study, self-assessment, and grade tracking.

The core goal is to support a fast learning loop:

Load assessment → answer questions → review feedback → score attempt → optionally commit grade → identify weak topics.

This app is not intended to be a mature public LMS in the first version.

## Tech Stack

Backend:

* ASP.NET Core Web API
* C#
* File-backed storage for MVP
* YAML/JSON assessment loading

Frontend:

* Astro
* TypeScript
* Localhost-first UI

## Development Priorities

Prioritize the core loop before advanced features.

The MVP must support:

1. Loading assessments from YAML/JSON
2. Browsing by category and subcategory
3. Taking quizzes/tests
4. Practice mode
5. Scored mode
6. Multiple choice questions
7. Select-all questions
8. Free response self-check questions
9. Attempt recording
10. Grade log committing
11. Basic settings
12. Assessment validation

Do not overbuild the creation workflow yet.

## Architectural Rules

* Separate domain logic from API controllers.
* Do not directly couple the application to raw YAML files.
* Use repository interfaces so file-backed storage can later be replaced with SQLite.
* Keep assessment definitions separate from user attempts.
* Store stable IDs for categories, subcategories, assessments, and questions.
* Save randomized question order in each attempt.
* Validate assessment files before loading them into active use.

## Data Rules

Every assessment file should include:

* schemaVersion
* id
* title
* assessmentType
* categoryId
* subcategoryIds
* questions

Every question should include:

* id
* type
* prompt
* answer
* explanation where appropriate

Question IDs must be unique within an assessment.

## Modes

Practice mode:

* Shows correctness after each answer
* Allows explanations immediately after answering
* Tracks score
* Asks whether to commit score to grade log

Scored mode:

* Hides correctness and explanations until the end
* Tracks score
* May commit score depending on settings

## Question Types

MVP question types:

* multipleChoice
* selectAll
* freeResponse with selfCheck grading

Planned but not required for MVP:

* matching
* ordering
* numeric tolerance
* equation input
* generated tests
* full assessment editor

## Testing Expectations

Add tests for:

* Assessment validation
* Scoring multiple choice
* Scoring select-all
* Free response self-check attempt flow
* Randomized order persistence
* Grade log commit behavior

## Coding Style

* Prefer clear names over clever abstractions.
* Keep domain models explicit.
* Avoid premature optimization.
* Avoid large controller methods.
* Keep frontend components simple and readable.
* Do not add external services unless required.

## Current MVP Boundary

Do not implement the following unless explicitly requested:

* Authentication
* Cloud sync
* Multi-user support
* Full database migration
* Multi-category tests
* Rich assessment editor
* AI grading
* Public deployment
* Advanced analytics
