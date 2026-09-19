# App Flow and Performance Audit

**Date:** 2026-09-19  
**Scope:** Read-only review of the current frontend, search flow, assessment lifecycle, styles, and API structure. No files were changed during the audit itself.  
**Purpose:** Preserve improvement opportunities for app flow, performance, and future assessment-creation tooling.

## Highest-priority improvements

### 1. Make assessment switching feel safe and deliberate

Starting another assessment currently uses a blocking browser confirmation and permanently deletes an in-progress attempt. That conflicts with the app’s saved-session model and makes switching feel risky. Prefer a clear in-app choice to **pause and switch**, **discard and switch**, or **stay**. Show the active assessment and its status consistently, and make the result of each choice explicit.

### 2. Give search its own clear flow

Search results hide the navigator stages, but selecting a result only changes selection and reveals the start action. The search results remain in the main catalog view, so they continue to dominate after the user has moved on. Add a clear “Search results” state with result count, loading/empty/error feedback, and a simple way to clear or return to browsing. After starting an assessment, collapse or dismiss the search view while keeping the active session accessible.

### 3. Replace browser alerts with styled, contextual messages

Several important failures still use `alert()`, including starting or restarting an assessment and committing a score. These interrupt the user and don’t follow the app’s existing inline status patterns. Add shared alert/toast styles and a reusable notification area with appropriate accessibility announcements. Reserve confirmation dialogs for decisions that need them, and style those in-app too.

### 4. Improve feedback during session transitions

Starting, pausing, resuming, completing, and saving can involve multiple API calls and rerenders. Some actions change button text while work runs, but users need a more consistent sense of what is happening, whether their progress is saved, and what to do if an action fails. Use a shared transition pattern: disable conflicting actions, provide a visible progress/status message, preserve the current view on failure, and restore controls reliably. The start flow also removes an existing attempt before the replacement attempt is successfully created; that ordering risks losing the old session if the new start fails.

## Search and navigation details

The search implementation debounces suggestions, but it doesn’t cancel or sequence requests. A slower earlier response could replace results for a newer query. Search also logs suggestion failures to the console without showing a useful state to the user. Add request cancellation or query sequencing, visible pending/error states, and keyboard navigation for suggestions and results. The markup uses listbox roles, but the interaction currently supports clicking and Enter/Space only; arrow-key navigation and clearer selection announcements would make it easier to use with a keyboard or assistive technology.

Assessment navigation has both the guided navigator and classic picker. A small cleanup pass could clarify how they relate, make the active selection and current session more prominent, and ensure changing categories or clearing search doesn’t leave stale selection state.

## Performance and maintainability

- `frontend/src/pages/index.astro` is about **8,140 lines**, concentrating application state, UI rendering, API calls, and event handling in one file. That makes behavior harder to trace and raises the cost of future creator-tool work. A gradual extraction by feature—assessment navigation, attempt/session controls, analytics, and authoring—would improve maintainability without requiring a full rewrite.
- `frontend/src/styles/global.css` is about **3,400 lines** and contains duplicated assessment-search style blocks. Consolidating duplicated selectors is a low-risk cleanup and makes later UI refinements easier.
- `loadGrades()` refreshes grade summary, analytics, and completed-assessment data, then rerenders analytics and history. Since it runs after several attempt actions, it may add avoidable delay to common transitions. Consider refreshing only the data affected by an action, and measure before making broader caching changes.
- The search UI could also avoid rerendering unrelated navigator state while results are loading or updated.

## Foundations for more user-friendly assessment creation

There is already useful authoring infrastructure: source imports and import-job status, source search, curriculum manifests, question blueprints, draft review, and coverage views. That gives a good base for a more guided creator.

Build toward a creator that starts with **what the user wants to make**, then guides them through a small number of validated steps: choose activity and topic, define learning goals, add questions or sections, preview the assessment, validate it, and save a draft. Reuse the existing manifests and validation contracts so the guided experience produces content the current app can load. Keep source import and generated drafts reviewable, and make validation issues actionable at the field or question where they occur.

## Suggested priority order

| Priority | Work | Why |
|---|---|---|
| **P0** | Safer switch/pause/discard flow; transition status and error handling | Protects attempts and addresses session friction |
| **P1** | Search results as a dismissible, accessible state | Fixes the search flow that continues to dominate the main view |
| **P1** | Shared styled alerts and confirmations | Removes blocking, inconsistent feedback from important actions |
| **P2** | Extract frontend features into smaller modules; consolidate duplicate CSS | Creates room to improve features without growing the central page further |
| **P2** | Guided assessment-creation flow built on existing authoring services | Lays foundations for the planned creator expansion |
| **P3** | Measure and optimize repeated catalog, analytics, and session requests | Targets performance based on observed user-facing delays |

## Audit limitations

This pass did not include a live browser walkthrough, performance profiling, or test runs. Performance items are audit leads rather than measured bottlenecks.
