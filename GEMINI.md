# Gemini Project Context

@./AGENTS.md
@./skills/caveman/SKILL.md
@./docs/agent-reports/assessment-taxonomy-ingest-incident.md

## Gemini-Specific Startup

- Treat the imported `AGENTS.md` as the shared repository contract.
- For substantial changes, inspect `docs/agent-coexistence.md` before editing.
- For assessment creation or review, load `skills/assessment-question-pipeline/SKILL.md` only when the task concerns assessment content.
- For S2C imports, source-grounded curriculum generation, or authoring packets, load `skills/source-to-curriculum/SKILL.md` before creating content. Its extraction and provenance gates are mandatory.
- Do not edit `.codex/`, Codex configuration, or Codex skill mirrors unless the user explicitly asks for agent-infrastructure maintenance.
- Do not create a second independent project instruction document that duplicates `AGENTS.md`; update the shared contract instead.
- Use `/memory show` when diagnosing unexpected Gemini instructions and `/memory reload` after changing this file or imported context.

## Coexistence Rules

- Check `git status --short` before and after work.
- Assume uncommitted changes may belong to the user or Codex.
- Work with existing changes; do not reset, clean, or rewrite them.
- Avoid runtime-state files listed in `AGENTS.md`.
- In the final response, identify files changed, tests/checks run, and anything not verified.

## Official Context Reference

Gemini CLI loads root and hierarchical `GEMINI.md` context files and supports `@file.md` imports:

<https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md>
