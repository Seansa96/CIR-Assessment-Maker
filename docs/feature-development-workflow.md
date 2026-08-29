# Feature Development Workflow

## Branches and worktrees

`main` is the production/release branch. Do not begin feature work there or merge unreviewed agent work directly into it.

`develop` is the integration branch. It is checked out only at `C:\Users\SeanS\Downloads\cir_app_integration` and is where reviewed feature branches are merged and validated together.

| Worktree | Branch | Purpose |
| --- | --- | --- |
| `C:\Users\SeanS\Downloads\cir_app` | `main` | Production checkout; preserve any local user work. |
| `C:\Users\SeanS\Downloads\cir_app_integration` | `develop` | Integration and release verification. |
| `C:\Users\SeanS\Downloads\cir_app_chatgpt` | `agent/chatgpt` | ChatGPT agent feature work. |
| `C:\Users\SeanS\Downloads\cir_app_antigravity` | `agent/antigravity` | Antigravity IDE agent feature work. |

The existing `cir_app_server` worktree remains dedicated to `codex/server-lan-access`.

## Feature loop

1. In the assigned agent worktree, inspect status and fetch current `develop` before beginning work.
2. Create a task branch from `develop` using an ownership-prefixed name, such as `agent/chatgpt/course-editor` or `agent/antigravity/catalog-search`.
3. State file ownership in the task handoff before editing. Serialize broad changes to `frontend/src/pages/index.astro`.
4. Make narrow commits by concern. Do not commit runtime state, generated output, local databases, logs, or another agent's uncommitted work.
5. Run the relevant backend, frontend, and content validation commands. Record failures and pre-existing failures in the handoff.
6. Review the feature branch against `develop`, then merge it only in `cir_app_integration` after resolving conflicts and re-running the combined checks.

## Handoffs and integration

Use the handoff format in `docs/agent-coexistence.md`. A handoff must name the branch, base commit, owned files, validation performed, remaining risks, and intended merge target.

The integration owner is the only actor that merges into `develop`. If two features edit the same frontend region or assessment file, integrate one first, rebase the second branch on the updated `develop`, and resolve the conflict in the owning feature branch.

## Release flow

1. In the integration worktree, verify `develop` is clean and all intended feature commits are present.
2. Run the regression checks appropriate to the combined change.
3. Merge `develop` into `main` only from a clean release operation; tag and push if a release tag is desired.
4. Refresh agent worktrees from the new `develop` head before assigning the next feature.

Never reset, clean, delete, or switch branches in another agent's occupied worktree. Use the helper scripts below to inspect or set up the standard layout.

## Helper scripts

- `utility_user_scripts/setup_agent_worktrees.ps1 -RepositoryPath <production-checkout>` creates or validates the standard clean worktrees. It refuses non-empty non-worktree target directories and never removes branches or directories.
- `utility_user_scripts/agent_worktree_status.ps1 -RepositoryPath <any-worktree>` prints every registered worktree's branch, HEAD, dirty status, upstream, and any active index lock.
