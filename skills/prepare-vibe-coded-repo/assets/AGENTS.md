# Agent Instructions

Adapt this file to the repository. Remove every placeholder and section that does not prevent real ambiguity.

## Mission

[Describe the project, primary user, main workflow, and most important boundary in one short paragraph.]

## Start Every Task

1. Read `README.md`, `FEATURES.md`, and [other durable sources of truth].
2. Inspect the current branch, commit, and complete working-tree state.
3. Preserve all pre-existing changes and keep unrelated work out of commits.
4. Identify the feature section and confirm its approved scope before implementation.
5. Verify the canonical validation command before relying on it.

## Sources Of Truth

- `README.md`: supported user/developer workflow.
- `FEATURES.md`: current feature scope, progress, evidence, and next action.
- [Existing product, architecture, privacy, testing, or release document]: [unique responsibility].

If sources conflict, stop long enough to identify and reconcile the owning source. Current progress never overrides durable product or safety constraints.

## Working Agreement

- Use `[canonical validation command]` for the normal validation path.
- Keep feature behavior, checks, affected durable documentation, and `FEATURES.md` aligned.
- Use `[branch convention]` branches and commit coherent milestones.
- Preserve unrelated user work. Never hide, discard, or include it in a feature commit.
- Never claim an unavailable or unrun check passed; record manual-only gaps honestly.

## Autonomy And Approval

After a feature is approved, proceed autonomously through [implementation/checks/local commits/feature-branch pushes as appropriate].

Repeat until acceptance passes or a material blocker appears:

1. Implement the next coherent increment within the approved scope.
2. Run focused checks and the canonical validation appropriate to that increment.
3. Update `FEATURES.md` with progress, evidence, decisions when needed, and exactly one next action.
4. Review the diff and create a focused commit when authorized.

Use repository files as durable memory across tasks. Do not require Codex Goals, scheduled tasks, recurring automations, or an external task system. Use them only when the user explicitly requests them and the work genuinely needs monitoring or scheduling.

Stop for unapproved changes to product meaning, scope, privacy, permissions, cost, providers, dependencies, destructive data handling, external communication, deployment, release, the default branch, or tags. Do not ask again for actions already explicitly authorized.

## Progress And Handoff

- Keep the active feature section current with status, decisions when needed, validation, blocker, and exactly one next action.
- At completion, report delivered behavior, validation evidence, limitations, branch/commit state, and the remaining human action.
- Leave the repository recoverable by another task without requiring the prior conversation.
