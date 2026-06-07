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

Creation is intentionally a placeholder until the core loop is stable.
