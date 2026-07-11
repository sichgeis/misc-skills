---
name: prepare-vibe-coded-repo
description: Assess and prepare a small personal or vibe-coded software repository for low-friction autonomous Codex development. Use when the user wants to bootstrap, simplify, or standardize repository guidance; improve AGENTS.md, README, feature tracking, validation, Git, approval, progress, or handoff conventions; make concurrent feature work understandable across Codex tasks; or check whether an existing lightweight process should be preserved. Inspect and propose changes read-only first, then align repository guidance on a feature branch only after approval. Do not use this skill for automatic product or code modernization.
---

# Prepare Vibe-Coded Repository

Establish the smallest guidance system that lets Codex understand product boundaries, select and continue feature work, run honest validation, operate within an explicit approval envelope, and leave a recoverable handoff.

Prefer `AGENTS.md`, `FEATURES.md`, and `README.md` when bootstrapping a small under-documented repository. Treat them as capability defaults, not mandatory filenames or a universal end state. Preserve or simplify specialized documentation when it already provides those capabilities.

## Operating Contract

Keep two phases distinct:

1. **Assess and propose:** inspect without modifying the repository, classify its current system, and propose an exact minimal change set.
2. **Approved alignment:** after approval, create or use an approved feature branch, make only the proposed documentation/process changes, validate them safely, and create one local commit.

Do not edit files, create branches, install dependencies, commit, push, or run externally consequential commands during assessment. Do not turn alignment into product work, source-code modernization, deployment, release, provider access, or cleanup of unrelated user work.

Before assessing or aligning, read [references/minimal-vibe-project-standard.md](references/minimal-vibe-project-standard.md) completely. Use the assets only as adaptable starting points; never copy them verbatim over existing instructions.

## Autonomy Model

Use repository state as durable memory. After a feature is approved, direct agents to repeat a bounded loop: implement the next coherent increment, validate it, update feature progress and evidence, create a focused commit when authorized, and continue until acceptance passes or a material blocker appears. Ask only when a decision falls outside the approved envelope.

Do not require Codex Goals, scheduled tasks, recurring automations, or an external task system. Use those orchestration features only when the user explicitly requests them and the work genuinely needs monitoring or scheduling. Treat separate Codex tasks as concurrent workers that coordinate through feature branches and the repository's current-work artifact.

## Assess Read-Only

1. Read every applicable repository instruction.
2. Record the repository root, current branch and commit, default branch when discoverable, remotes, and complete working-tree state. Treat every pre-existing change as user work.
3. Read the README, build/test/task configuration, and likely instruction, product, specification, planning, status, architecture, privacy, test, release, and deployment files.
4. Map artifacts to capabilities rather than checking filenames:
   - agent operating procedure and approval envelope;
   - bounded autonomous loop and durable repository state;
   - product intent, boundaries, and non-goals;
   - current feature status, ownership, progress, and next action;
   - canonical validation and honest automated/manual coverage;
   - release or deployment process when relevant;
   - specialized architecture, privacy, security, data, or safety constraints.
5. Inspect a small relevant Git-history slice: recent commits, the history of principal guidance/specification files, and evidence that documentation is maintained alongside behavior or backfilled later. Check whether a current-sounding plan or tracker mixes roadmap, live status, and history. When a generic plan or tracker path has earlier versions, inspect at least one relevant earlier version to detect reuse for unrelated work. If history is shallow or unavailable, state the limitation.
6. Classify the repository as **Bootstrap**, **Consolidate**, or **Preserve** using the reference.
7. Propose the smallest useful change set. For each relevant artifact, use exactly one action: `create`, `update`, `keep`, `consolidate`, `archive`, or `delete`. Explain what each consolidation, archive, or deletion preserves and what could otherwise be lost.

Do not use a numerical maturity score. Do not recommend structure merely to match the preferred filenames.

## Report And Stop

Keep the assessment brief and return:

1. **Mode:** Bootstrap, Consolidate, or Preserve, with one-sentence reasoning.
2. **What already works:** capabilities supported by concrete evidence.
3. **What blocks low-friction agent work:** only material ambiguity, drift, or missing guidance.
4. **Proposed changes:** a compact action/path/reason table containing the exact authorized scope.
5. **Preservation notes:** information retained, relocated, or at risk for every consolidation, archive, or deletion.
6. **Validation:** safe checks to run after alignment.
7. **Approval gate:** state that an unqualified approval authorizes the exact proposal, a repository-conventional feature branch, safe validation, and one local commit on that branch.

Stop after the proposal. If Preserve needs no changes, say so and do not manufacture an approval request.

## Interpret Approval

Treat an unqualified affirmative response such as “Okay,” “Approved,” “Go ahead,” or “Do it” as authorization for:

- creation of the branch named in the proposal, or use of an already-active dedicated branch named there;
- only the file actions explicitly listed in the proposal;
- safe local validation listed in the proposal; and
- one local commit on that branch.

Approval does not authorize direct commits to the default branch, pushing, unlisted deletions, product-code changes, dependency installation, deployment, release, provider calls, real external data, or other external effects. A narrowed approval narrows the implementation scope. Feedback without clear approval revises the proposal and remains read-only.

## Align After Approval

1. Recheck branch, commit, and working-tree state. Compare it with the assessment baseline.
2. Stop and ask for direction if the baseline changed materially, proposed files now overlap pre-existing changes, the approved branch cannot be created safely, or safe isolation is otherwise impossible.
3. Follow repository conventions for the branch name. Otherwise use `codex/prepare-vibe-repo`. Never commit the alignment directly to the default branch.
4. Implement only approved actions. Merge useful existing content into the selected artifacts. Preserve specialized documents with unique responsibilities.
5. When bootstrapping, adapt [assets/AGENTS.md](assets/AGENTS.md) and [assets/FEATURES.md](assets/FEATURES.md) to the repository. Remove unused placeholders and sections.
6. Run only approved, non-external validation. Never claim an unavailable or unrun command passed.
7. Review the diff for lost meaning, accidental product-code changes, unrelated files, stale cross-references, and secrets.
8. Stage only the approved paths and create one local commit using the repository convention or `docs: prepare repository for agent work`.
9. Confirm that every pre-existing change remains preserved and that the skill introduced no new uncommitted changes. Do not promise a clean tree when it was dirty before.

Finish with the branch, commit, validation evidence, preserved pre-existing changes, and any remaining limitation. Do not push.
