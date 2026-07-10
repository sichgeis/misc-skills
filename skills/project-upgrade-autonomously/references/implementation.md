# Phase 2: Approved Autonomous Implementation

## Contents

- [Create the completion contract](#create-the-completion-contract)
- [Establish a safe Git baseline](#establish-a-safe-git-baseline)
- [Create the upgrade tracker](#create-the-upgrade-tracker)
- [Plan at two levels](#plan-at-two-levels)
- [Run the stage loop](#run-the-stage-loop)
- [Communicate at boundaries](#communicate-at-boundaries)
- [Respect authorization boundaries](#respect-authorization-boundaries)
- [Handle blockers](#handle-blockers)
- [Verify and hand off](#verify-and-hand-off)

Begin only after clear approval. Keep implementation within the accepted recommended scope and non-goals.

## Create the Completion Contract

Restate the accepted scope, success criteria, constraints, non-goals, and verification surface compactly.

When Goals are available, create an active Goal for the accepted upgrade. Define:

- the desired end state
- evidence that proves completion
- behavior and data that must not regress
- repository and external-action boundaries
- how to choose the next action after each stage
- what constitutes a genuine blocker

Do not set a token budget unless requested. Keep the Goal active until every accepted stage and the final evidence check pass. If Goals are unavailable, use the repository tracker and staged loop as the durable completion contract.

## Establish a Safe Git Baseline

Before changing implementation code:

1. Read all applicable repository instructions.
2. Inspect the branch, upstream, remotes, recent history, working-tree status, diffs, and untracked files.
3. Preserve all existing work. Never discard, reset, overwrite, or hide user changes.
4. Review pre-existing changes before including them anywhere. Never commit secrets, credentials, real user data, local databases, caches, build output, OS metadata, or unexpectedly large generated files. Pause when intent is genuinely unclear.
5. Unless already on an appropriate dedicated branch, create one from the current state. Prefer `codex/project-upgrade`, adding a short unique suffix when needed. Do not perform a multi-stage upgrade on the default or protected branch.
6. If the tree is dirty, commit only safe, intended pre-existing work as a clearly labeled pre-upgrade snapshot. If the tree is clean, record the current commit without creating an empty commit.
7. Push the snapshot or clean baseline branch and establish its upstream.
8. Confirm a clean working tree before implementation.

Normal commits and pushes to this dedicated branch are authorized by approval. Do not force-push, rewrite shared history, merge into the default branch, open a pull request, create a release, or deploy unless separately requested.

When an update from the base branch is necessary, prefer rebasing onto the current base over merging the base into the upgrade branch. Rebase only when safe; ask first when the branch appears shared or history rewriting could surprise collaborators.

If no usable remote exists, authentication fails, or the baseline cannot be pushed safely, stop and report the exact blocker. Do not treat a local commit as a pushed snapshot.

## Create the Upgrade Tracker

Create a concise Markdown tracker inside the repository, following an established convention when one exists; otherwise use `docs/project-upgrade.md`.

Include:

- overarching product outcome
- accepted scope and explicit non-goals
- success and acceptance criteria
- baseline branch and commit
- staged plan with `Pending`, `In progress`, `Completed`, or `Blocked` status
- important dependencies and risks
- decisions and meaningful deviations
- validation evidence by stage
- current blocker, if any
- the single next action

Keep exactly one stage `In progress`. Treat the tracker as a handoff and recovery artifact, not a diary. Create, commit, and push the initial tracker before the first implementation stage.

## Plan at Two Levels

Maintain:

- a high-level staged plan for the complete accepted upgrade
- a just-in-time detailed plan before each stage, informed by prior results

For each stage, identify the exact objective, affected behavior, likely files, invariants, approach, tests, smoke checks, risks, and completion criteria before editing.

Update the high-level plan when evidence requires it. Do not silently expand scope. Allow small internal adjustments required for an approved outcome; request approval for new user-visible features, major architectural changes, destructive migrations, or materially different behavior.

## Run the Stage Loop

For every accepted stage:

1. Send a short update naming the stage, intended outcome, and first action.
2. Mark the stage `In progress` in the tracker.
3. Inspect the relevant implementation and create the just-in-time plan.
4. Implement the smallest coherent change that satisfies the criteria.
5. Add or update focused tests for changed behavior where practical.
6. Run the most relevant tests, type checks, lint checks, builds, and functional or UI smoke checks.
7. Diagnose failures. Never weaken tests, delete required behavior, or broaden mocks merely to pass checks. Separate pre-existing failures from regressions.
8. Review the complete diff for correctness, unintended behavior, security, privacy, data safety, complexity, generated files, and scope drift.
9. Update user-facing documentation when behavior or setup changes.
10. Mark the stage `Completed` only after its criteria and validation pass; record concise evidence.
11. Commit the coherent stage with a descriptive message and push it.
12. Confirm the pushed state and clean tree, report the outcome, and continue automatically.

Leave the branch usable after each stage. Isolate behavior-preserving refactors needed for later work and verify them independently. Avoid unrelated cleanup.

## Communicate at Boundaries

Provide concise updates when:

- the baseline and branch are established
- the tracker and plan are created
- a stage starts or completes
- evidence materially changes the plan
- a blocker appears
- final validation starts or ends

State one concrete outcome and the next action. Do not narrate routine commands.

Treat compatible user feedback during implementation as an addition or correction to the accepted Goal. If it replaces or materially expands the objective, pause, explain the impact, and confirm the revised contract.

## Respect Authorization Boundaries

Approval covers in-scope repository edits, tests, ordinary local development commands, commits, and pushes to the dedicated branch.

Require fresh approval for:

- destructive actions or data deletion
- processing or modifying real user data
- credential or secret changes
- deployment, release, publishing, purchases, or third-party messages
- external-system writes other than the authorized Git push
- force-pushes or shared-history rewrites
- merging into the default branch
- material expansion of product or architectural scope

## Handle Blockers

Exhaust safe in-scope diagnostics and alternatives first. When only one stage is blocked, record it and continue independent stages when coherent.

Stop when no defensible path remains, a consequential choice would materially change the outcome, or continuation would cross an authorization boundary. Report:

- exact blocker and evidence
- attempts made
- affected stages
- smallest user action or input needed to resume

Never claim completion while an accepted critical item remains blocked.

## Verify and Hand Off

After all stages appear complete:

1. Compare the repository against every accepted requirement and non-goal.
2. Run the broadest relevant non-destructive validation: tests, type checks, linting, build, packaging, and functional or visual smoke checks as applicable.
3. Recheck the primary workflow, security, privacy, error handling, data safety, reliability, and user-visible performance.
4. Inspect the final diff and stage history for accidental changes or missing documentation.
5. Confirm every stage commit is pushed and the working tree is clean.
6. Update the tracker with final status, evidence, limitations, deferred work, and the next recommended human action.
7. Commit and push the final tracker update when it is not already part of the last stage.
8. Mark the Goal complete only when concrete evidence supports the accepted end state and no required work remains.

Return a final handoff containing:

- outcome for the user's workflow
- accepted scope completed
- stage-by-stage summary with commit identifiers
- validation commands and results
- functional and technical changes
- security, privacy, reliability, and performance improvements
- known limitations, deferred ideas, and unresolved risks
- how to run or use the improved application
- branch name, clean and pushed status, and safest rollback point
- recommended manual review before merge or release

Do not merge, release, or deploy. Finish with a clean, pushed, reviewable upgrade branch and an evidence-backed handoff.
