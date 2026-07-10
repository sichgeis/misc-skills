# Phase 1: Repository Assessment

## Contents

- [Assessment boundary](#assessment-boundary)
- [Build the product and technical model](#build-the-product-and-technical-model)
- [Review perspectives](#review-perspectives)
- [Evidence and prioritization](#evidence-and-prioritization)
- [Required assessment report](#required-assessment-report)
- [Stop at the approval gate](#stop-at-the-approval-gate)

## Assessment Boundary

Keep this phase read-only. Do not modify files, install or upgrade dependencies, activate a Goal, create commits, or push.

You may:

- read relevant repository files and applicable instructions such as `AGENTS.md`
- inspect the working tree, branch, remotes, history, and existing diffs
- inspect documentation, manifests, configuration, entry points, tests, scripts, packaging, and dependencies
- trace important code paths and data flows
- run existing non-destructive tests, linting, type checks, builds, and safe smoke checks
- run the application locally when doing so needs no new installation, external account, destructive operation, or real user data

Do not begin with broad questions. Investigate first and ask only when a missing fact materially prevents a responsible assessment.

## Build the Product and Technical Model

Establish an evidence-based model before recommending changes:

1. Determine the application's intended purpose, target user, operating environment, main inputs and outputs, stored data, integrations, and important constraints.
2. Trace at least one important workflow end to end, from the user's first action through processing, persistence, and visible result.
3. Identify the main components and their responsibilities.
4. Compare documented, tested, implemented, and likely intended behavior; call out conflicts.
5. Validate important assumptions with existing checks or safe application use when practical.

## Review Perspectives

### Function and workflow

Look for missing or inconsistent behavior, unnecessary manual steps, awkward sequencing, unclear feedback, weak defaults, and poor empty, loading, error, retry, cancellation, or recovery states.

Consider grounded improvements such as safer automation, batching, previews, undo, shortcuts, better outputs, clearer progress, fewer context switches, or a simpler interaction model. Prefer reduced friction over feature growth. Separate practical recommendations from speculative ideas.

### Correctness, reliability, and data safety

Inspect input validation, error handling, state transitions, persistence, concurrency, retries, idempotency, atomic writes, migrations, backups, partial failures, cleanup, and interruption recovery.

Prioritize paths that could silently lose, overwrite, duplicate, corrupt, or disclose user data.

### Security and privacy

Use a realistic threat model. Inspect secrets handling, subprocess execution, command construction, paths, permissions, unsafe deserialization, injection, network exposure, authentication when applicable, sensitive logs, temporary files, dependencies, and trust boundaries.

Do not invent an internet-scale threat model for an offline local tool. Tie each concern to a concrete code path or credible scenario.

### Implementation quality

Look for correctness problems, surprising behavior, unnecessary complexity, duplication, tight coupling, fragile abstractions, dead code, unclear ownership, inconsistent conventions, dependency misuse, and areas that are difficult to change safely.

Do not recommend rewrites because another architecture is fashionable.

### Performance and resource use

Look for user-visible problems: slow startup, blocking work, repeated disk or network access, unnecessary recomputation, excessive memory use, inefficient large-data handling, redundant API or model calls, missing batching, or poor UI responsiveness.

Separate observed or strongly evidenced problems from speculative micro-optimizations.

### Verification and maintainability

Assess coverage of important behavior and failure paths. Review type checking, linting, diagnostics, logs, configuration, documentation, setup, packaging, updating, backup, uninstall, and cleanup behavior where relevant.

## Evidence and Prioritization

Support every finding with at least one concrete artifact:

- a file and relevant symbol or line
- an observed execution result
- a failing or missing test around specific behavior
- a traced user workflow
- a reproducible failure scenario

Classify each finding as one of:

- confirmed defect
- credible risk
- design limitation
- workflow opportunity
- hypothesis requiring validation

For each finding, provide:

- category and title
- evidence
- real-world impact or failure scenario
- recommended change
- priority: `Critical`, `High`, `Medium`, or `Low`
- effort: `Small`, `Medium`, or `Large`
- confidence: `High`, `Medium`, or `Low`
- disposition: `implement now`, `schedule later`, `investigate first`, or `leave unchanged`

Require a concrete explanation for `Critical` or `High`. Exclude generic best practices, cosmetic preferences, and upgrades that solve no identified problem. Say when an area is already sound.

## Required Assessment Report

Return the report in this order:

1. **What this application is**
   - purpose, intended user, and current primary workflow
   - inputs, outputs, stored data, integrations, architecture, and data flow
   - assumptions and unresolved product questions
2. **Executive assessment**
   - what works well
   - the largest risks or gaps
   - the three highest-return improvements
3. **Prioritized findings**
   - a compact evidence-based table using the fields above
   - only the most important findings in the main table
   - genuinely minor observations in a short separate section
4. **Functional and workflow improvements**
   - current workflow and proposed workflow
   - expected user benefit
   - implementation implications, tradeoffs, and downsides
5. **Recommended implementation scope**
   - exact changes recommended for approval now
   - explicit non-goals and deferred ideas
   - acceptance criteria for the complete upgrade
   - make clear that this is what a simple approval authorizes
6. **Staged implementation plan**
   - a small number of coherent, reviewable stages
   - objective, likely files or components, dependencies, risks, validation, and completion criteria per stage
   - foundational safety and correctness before dependent functional improvements
7. **Baseline validation**
   - checks run and results
   - important behavior currently untested
   - remaining uncertainties
8. **Approval request**
   - invite approval, rejection, narrowing, expansion, or revision
   - state unambiguously that “Okay, do it” authorizes the complete recommended scope and the defined commits and pushes

## Stop at the Approval Gate

After presenting the report, stop and wait. Do not modify the repository or activate a Goal.

Treat clear approval according to `SKILL.md`. If feedback does not clearly authorize implementation, revise the proposal and request approval again.
