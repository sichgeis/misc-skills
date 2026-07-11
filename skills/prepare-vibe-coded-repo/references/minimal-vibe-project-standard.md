# Minimal Vibe-Coded Repository Standard

## Contents

- [Purpose](#purpose)
- [Capability standard](#capability-standard)
- [Autonomous work model](#autonomous-work-model)
- [Operating modes](#operating-modes)
- [Artifact equivalence](#artifact-equivalence)
- [Minimal artifact guidance](#minimal-artifact-guidance)
- [Preservation and consolidation](#preservation-and-consolidation)
- [Git and approval behavior](#git-and-approval-behavior)
- [Examples](#examples)

## Purpose

Optimize small personal projects for low-friction work by successive or concurrent Codex tasks. Prefer the easiest system that reliably preserves product meaning, active feature state, truthful validation, authority, and the next action.

The default bootstrap is `AGENTS.md`, `FEATURES.md`, and `README.md`. These filenames are not the standard by themselves. An existing artifact system is equally valid when it provides the same capabilities clearly and proportionately.

## Capability Standard

A prepared repository lets an agent determine, without reconstructing the project from all source code or prior conversations:

1. what the project does, for whom, and what must not change;
2. which documents own durable product, technical, privacy, or release truth;
3. which feature is proposed, approved, active, blocked, or done;
4. the scope, non-goals, acceptance conditions, current progress, evidence, and next action for active work;
5. the canonical validation commands and which important checks remain manual;
6. the Git baseline, branch convention, commit expectations, and treatment of unrelated changes;
7. what an agent may do autonomously and which actions require approval; and
8. how another task resumes work safely.

Do not require every capability to have its own file. Separate an artifact only when it prevents real ambiguity, loss of important rationale, unsafe behavior, or repeated context reconstruction.

## Autonomous Work Model

Use the repository as the durable coordination layer. Conversation state, a Codex Goal, or a scheduled task may disappear or be invisible to another task; accepted scope, progress, evidence, blockers, and the next action must remain discoverable in the repository.

After a feature is approved, use this loop:

1. select the smallest coherent increment from the approved scope;
2. implement it without reopening reversible in-scope decisions;
3. run focused checks and the canonical validation appropriate to the increment;
4. update the current-work artifact with progress, evidence, decisions when needed, and exactly one next action;
5. review the diff and create a focused commit when authorized; and
6. repeat until acceptance passes or a material blocker requires user input.

Stop for decisions outside the approval envelope, not for routine implementation choices. A blocker is material when it changes product meaning, accepted scope, privacy, permissions, cost, providers, dependencies, destructive data handling, external communication, release/deployment authority, or another explicit repository boundary.

Do not make Codex Goals, scheduled tasks, recurring automations, or an external issue tracker prerequisites for autonomy. Introduce them only when the user explicitly requests them and the work benefits from time-based monitoring, recurring checks, or coordination that repository state alone cannot provide. A `Goal` field in `FEATURES.md` names the feature outcome; it does not require activation of a Codex Goal.

Separate Codex tasks may work concurrently when each owns a feature section and branch. Shared durable documents remain authoritative; tasks must preserve unrelated changes and reconcile shared-file conflicts explicitly.

## Operating Modes

### Bootstrap

Use when little usable guidance exists and important capabilities must be inferred from source or conversation.

Default recommendation:

- create or improve a concise `README.md` for project purpose and entry points;
- create an `AGENTS.md` operating procedure; and
- create a compact `FEATURES.md` current-work surface.

Adapt to existing equivalents rather than creating duplicates. Do not add separate architecture, privacy, release, test-plan, ADR, archive, feature-directory, or run-tracker structures unless present risk demands them.

### Consolidate

Use when useful information exists but active status, instructions, or ownership are fragmented, duplicated, stale, or mixed with historical narrative. Treat a generic planning or tracker path reused for unrelated features as a discoverability problem even when Git retains every earlier version. Prefer a stable current-work owner and feature-specific names only when reuse has caused real ambiguity; do not introduce an archive hierarchy by default.

Prefer small edits that clarify responsibility and remove duplication. Preserve specialized durable documents. Introduce `FEATURES.md` only when it takes over a current-work responsibility from another artifact; name the replaced responsibility and update or remove the old duplicate in the same approved change.

### Preserve

Use when the current system is coherent, proportionate, maintained, and sufficient for safe agent work. Recommend no change or only a small correction tied to concrete friction. Never reformat a healthy system into the bootstrap layout for consistency.

## Artifact Equivalence

Map capabilities before recommending filenames:

| Capability | Common artifacts | Evidence of quality |
| --- | --- | --- |
| Agent operating procedure | `AGENTS.md`, `CONTRIBUTING.md`, scoped instruction files | Names required reading, commands, boundaries, Git rules, approvals, and handoff behavior |
| Product intent and non-goals | README, product spec, design brief | Describes users, workflow, accepted scope, and constraints without conflicting with current behavior |
| Active feature work | `FEATURES.md`, roadmap, issue tracker, feature spec, run document | Identifies status, accepted behavior, progress, validation, blocker, and next action at the needed depth |
| Canonical validation | Taskfile, Makefile, package scripts, CI config, test guide | One discoverable command works in the real environment; manual gaps are stated honestly |
| Architecture and data flow | Architecture document, diagrams, code-level conventions | Owns durable boundaries and invariants rather than temporary progress |
| Privacy and safety | Security/privacy spec, threat model, agent rules | Records data, permissions, providers, retention, logging, and non-negotiable constraints when relevant |
| Release/deployment | Release guide, package scripts, CI/CD, operations guide | Describes the actual candidate, validation, version, tag, deploy/install, verification, and rollback path needed by the project |

A filename earns no credit by existing. Check whether its content is current, specific, non-contradictory, and corroborated by configuration, source, validation, or history.

## Minimal Artifact Guidance

### `AGENTS.md`

Keep it short enough to read at the start of every task. Include only repository-wide operating knowledge:

- mission and important boundaries;
- required sources of truth and conflict precedence;
- start-of-task baseline checks;
- canonical validation and honest limitations;
- feature workflow and `FEATURES.md` responsibility when used;
- the autonomous implementation/validation/progress/commit loop;
- Git, branch, commit, and unrelated-change rules;
- autonomy and approval boundaries; and
- progress, completion, and handoff expectations.

Do not duplicate detailed product behavior, architecture, release procedures, or feature state. Link to the artifact that owns each responsibility.

### `FEATURES.md`

Use as the current work surface for small projects, not as a replacement for all durable specifications.

Use this compact shape and omit fields that add no information:

```markdown
## Feature name

- Status: Proposed | Approved | In progress | Blocked | Done
- Branch: `codex/feature-name`
- Goal:
- Scope:
- Non-goals:
- Acceptance:
- Progress:
- Validation:
- Next action:
```

Add `Decisions` only when non-obvious rationale must survive handoff. Active features should have exactly one actionable next step. Omit `Branch`, `Progress`, or `Next action` from completed features when they no longer help.

Concurrent tasks should own separate feature sections and branches. Accept occasional conflicts in this shared small file as a reasonable simplicity tradeoff. When a feature becomes too complex for one section, split only that feature into a dedicated specification; do not pre-create a hierarchy.

Shorten or remove completed details only when:

- lasting behavior is represented in the appropriate current source of truth;
- rationale, safety constraints, and important non-goals do not remain only in code or Git history; and
- the exact deletion is listed in the approved proposal.

### `README.md`

Keep it user/developer-facing: purpose, supported workflow, setup, and obvious commands. Do not turn it into the agent constitution, active progress log, or detailed release history.

## Preservation And Consolidation

Preserve a specialized document when it owns distinct durable knowledge. Typical examples include product behavior and non-goals, architecture and data flow, privacy/provider invariants, automated/manual test coverage, and signing, packaging, installation, deployment, or rollback procedures.

Target duplicated status and planning information before durable knowledge. For each proposed action:

- `create`: name the missing capability it will own;
- `update`: name the ambiguity or stale rule corrected;
- `keep`: name its unique responsibility;
- `consolidate`: name the destination, the retained information, and all references to update;
- `archive`: use only an existing repository convention or a specifically justified location, and explain why current readers no longer need the artifact;
- `delete`: list the exact path, prove its useful information exists elsewhere, and identify any information that would be lost.

Never make broad cleanup authorization implicit. Do not delete a file merely because Git retains its history. Git is recovery evidence, not the only acceptable source for current product meaning, safety constraints, or consequential rationale.

## Git And Approval Behavior

During assessment, inspect status before history or checks and record every staged, unstaged, and untracked path. Do not change branches or files.

After approval:

- recheck the baseline before mutation;
- use the approved repository-conventional feature branch, defaulting to `codex/prepare-vibe-repo`;
- never commit directly to the default branch;
- preserve pre-existing changes byte-for-byte unless an overlapping file was explicitly included and its integration was approved;
- stage only approved paths;
- create one local commit and do not push; and
- leave no new uncommitted changes from the alignment.

A dirty tree is not automatically a blocker. Proceed only when approved edits and staging can be isolated without hiding, overwriting, committing, or relocating unrelated user work. If proposed paths overlap existing changes, the baseline changed materially, branch creation is unsafe, or the distinction between user and skill changes cannot be proven, remain read-only and ask for direction.

Safe validation may read files, parse configuration, or run established local checks that have no external consequence. Do not install dependencies or use real accounts, credentials, providers, production data, deployments, releases, or destructive commands under the alignment approval.

## Examples

### Sparse personal tool: Bootstrap

The repository has source, a thin README, and an undocumented test command. Create `AGENTS.md`, improve README setup, and create `FEATURES.md` for the two known ideas. Do not add architecture or release documents when the tool has no meaningful architecture or release process.

### Fragmented personal application: Consolidate

The README, a scratch plan, and several current-sounding notes repeat feature status. Keep the README user-facing, consolidate current status into `FEATURES.md`, and retain a privacy note that uniquely owns stored-data rules. Delete or archive a scratch note only when its unique content and exact disposition appear in the approved proposal.

### Mature small application: Preserve or Consolidate

The repository has maintained product, architecture, privacy, test, and release documents plus a canonical task command. Preserve those responsibilities. If one implementation plan mixes roadmap, current status, and historical narrative, propose a small consolidation of current feature state only. Add `FEATURES.md` only if it replaces that responsibility rather than duplicating it.
