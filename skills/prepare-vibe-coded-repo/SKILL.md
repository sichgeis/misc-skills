---
name: prepare-vibe-coded-repo
description: Assess and prepare a small personal or vibe-coded software repository for low-friction autonomous coding-agent development. Use when the user wants to bootstrap, simplify, or standardize repository guidance; improve CLAUDE.md, AGENTS.md, CONTRIBUTING.md, README, feature tracking, validation, Git, approval, progress, or handoff conventions; make sequential or concurrent agent work understandable; or check whether an existing lightweight process should be preserved. Inspect and propose changes read-only first, then align repository guidance only after approval, defaulting to direct main-branch work for small sequential projects and using branches or worktrees only when isolation is justified. Do not use this skill for automatic product or code modernization.
---

# Prepare Vibe-Coded Repository

Establish the smallest guidance system that lets coding agents understand product boundaries, select and continue feature work, run honest validation, operate within an explicit approval envelope, and leave a recoverable handoff.

Prefer one canonical operating document, one current-work surface, and a user/developer README when bootstrapping a small under-documented repository. The canonical operating document may be `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, or an established repository equivalent. Preserve an automatically discovered entry file for every target host: Codex requires `AGENTS.md`, and Claude Code requires `CLAUDE.md`. When an entry file is not canonical, make it a thin pointer rather than a duplicated rule set. `FEATURES.md` and `README.md` remain useful defaults, not mandatory filenames or a universal end state. Preserve or simplify specialized documentation when it already provides the needed capabilities.

## Operating Contract

Keep two phases distinct:

1. **Assess and propose:** inspect without modifying the repository, classify its current system, and propose an exact minimal change set.
2. **Approved alignment:** after approval, use the proposed Git mode, make only the proposed documentation/process changes, validate them safely, and create one local commit. Default to the current main branch for small sequential projects unless repository rules or concrete risk justify isolation.

Do not edit files, create branches, install dependencies, commit, push, or run externally consequential commands during assessment. Do not turn alignment into product work, source-code modernization, deployment, release, provider access, or cleanup of unrelated user work.

Before assessing or aligning, read [references/minimal-vibe-project-standard.md](references/minimal-vibe-project-standard.md) completely. Use the assets only as adaptable starting points; never copy them verbatim over existing instructions.

## Autonomy Model

Use repository state as durable memory. After a feature is approved, direct agents to repeat a bounded loop: implement the next coherent increment, validate it, update feature progress and evidence, create a focused commit when authorized, and continue until acceptance passes or a material blocker appears. Ask only when a decision falls outside the approved envelope.

Do not require host goals, scheduled tasks, recurring automations, or an external task system. Use those orchestration features only when the user explicitly requests them and the work genuinely needs monitoring or scheduling. Treat separate agent tasks as workers that coordinate through the repository's current-work artifact; add branches or worktrees only when tasks actually run concurrently or otherwise need isolation.

## Assess Read-Only

1. Discover and read every applicable repository instruction. Check common host and repository entry points such as `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `.github/copilot-instructions.md`, scoped instruction files, and links from those files. Follow pointers to their canonical source instead of treating each entry file as independent truth.
2. Record the repository root, current branch and commit, default branch when discoverable, remotes, and complete working-tree state. Treat every pre-existing change as user work.
3. Read the README, build/test/task configuration, and likely instruction, product, specification, planning, status, architecture, privacy, test, release, and deployment files. Identify whether operating rules are canonical in one document, intentionally scoped, or duplicated across host-specific files.
4. Map artifacts to capabilities rather than checking filenames:
   - one canonical agent operating procedure and approval envelope, plus thin host pointers where needed;
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
7. **Approval gate:** state that an unqualified approval authorizes the exact proposal, its named Git mode and commit target, safe validation, and one local commit. Default the proposal to direct work on main for a small sequential project.

Stop after the proposal. If Preserve needs no changes, say so and do not manufacture an approval request.

## Interpret Approval

Treat an unqualified affirmative response such as “Okay,” “Approved,” “Go ahead,” or “Do it” as authorization for:

- use of the commit target named in the proposal, normally main for a small sequential project, plus branch or worktree creation only when explicitly proposed;
- only the file actions explicitly listed in the proposal;
- safe local validation listed in the proposal; and
- one local commit on the approved target.

Approval authorizes the proposed local commit even when main is the named target. It does not authorize pushing, unlisted deletions, product-code changes, dependency installation, deployment, release, provider calls, real external data, or other external effects. A narrowed approval narrows the implementation scope. Feedback without clear approval revises the proposal and remains read-only.

## Align After Approval

1. Recheck branch, commit, and working-tree state. Compare it with the assessment baseline.
2. Stop and ask for direction if the baseline changed materially, proposed files now overlap pre-existing changes, or the approved Git mode cannot preserve unrelated work safely.
3. For a small sequential project, stay on main and commit there unless the repository or user requires another workflow. Use a branch for parallel, broad, risky, experimental, or easily reviewable isolated work. Use a worktree only when simultaneous checkouts provide a concrete benefit. Do not create either as ceremony.
4. Implement only approved actions. Merge useful existing content into the selected artifacts. Preserve specialized documents with unique responsibilities.
5. When bootstrapping, adapt [assets/AGENTS.md](assets/AGENTS.md) as content for the chosen canonical operating document, regardless of its final filename, and adapt [assets/FEATURES.md](assets/FEATURES.md) for the chosen current-work surface. Remove unused placeholders and sections. Ensure every target host retains its automatically discovered entry file: `AGENTS.md` for Codex and `CLAUDE.md` for Claude Code. If that file is not canonical, make it a short pointer to the canonical operating document and include only genuinely host-specific loading syntax.
6. Run only approved, non-external validation. Never claim an unavailable or unrun command passed.
7. Review the diff for lost meaning, accidental product-code changes, unrelated files, stale cross-references, and secrets.
8. Stage only the approved paths and create one local commit using the repository convention or `docs: prepare repository for agent work`.
9. Confirm that every pre-existing change remains preserved and that the skill introduced no new uncommitted changes. Do not promise a clean tree when it was dirty before.

Finish with the commit target, commit, validation evidence, preserved pre-existing changes, and any remaining limitation. Do not push.
