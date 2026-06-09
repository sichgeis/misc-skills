---
name: staggered-jira-pr-train
description: "Turn a Jira issue into a GitHub-native staggered PR train: split refactors, behavior changes, tests, and docs into stacked branches and draft PRs that merge bottom-up into one handoff branch instead of directly to main."
---

# Staggered Jira PR Train

Use this skill when the task starts from a Jira issue, ticket key, or ticket URL and the desired output is a human-reviewable GitHub PR train. The goal is to make coding-agent work easier for humans to review by separating mechanical refactors, behavior changes, tests, and docs into distinct PR layers.

## Outcome

Create a GitHub-native stacked PR train whose final landing target is a single handoff branch for the Jira issue.

The final branch is:

```text
<JIRA-KEY>-<short-slug>
```

The train branches are:

```text
train/<JIRA-KEY>/01-<layer-slug>
train/<JIRA-KEY>/02-<layer-slug>
train/<JIRA-KEY>/03-<layer-slug>
...
```

The PR chain must look like this:

```text
main or default branch
 └─ <JIRA-KEY>-<short-slug>                          # handoff branch, do not review directly
     └─ train/<JIRA-KEY>/01-<prep-or-refactor>       # PR 1 targets handoff branch
         └─ train/<JIRA-KEY>/02-<behavior-change>    # PR 2 targets PR 1 branch
             └─ train/<JIRA-KEY>/03-<tests-docs>     # PR 3 targets PR 2 branch
```

After the train is reviewed and merged bottom-up, the handoff branch contains the complete Jira implementation and can be handed to a human colleague. Do not open or merge directly to `main`, `master`, `develop`, or the repository default branch unless the user explicitly asks.

## Hard rules

1. Never mix a pure mechanical refactor with a behavior change in the same PR.
2. Keep every PR layer reviewable on its own. Prefer fewer than 400 changed lines and fewer than 10 files per layer; if that is impossible, explain why.
3. Every branch must compile and pass the relevant tests if the repository makes that possible.
4. Create draft PRs by default. Mark ready only if the user explicitly requests it.
5. Do not merge PRs unless the user explicitly asks you to merge and CI/test status is acceptable.
6. The bottom PR in the stack targets the handoff branch, not the repository default branch.
7. The upper PRs target the branch immediately below them.
8. Use exact Jira issue key casing in branch names and PR titles.
9. When the Jira issue is ambiguous, make the smallest reasonable implementation and document assumptions in the train summary.
10. If the repository has an `AGENTS.md`, `CONTRIBUTING.md`, PR template, branch naming convention, or CI instructions, follow them unless they conflict with this skill's safety and reviewability rules. Repository branch naming rules win for the handoff branch.

## Inputs to infer

Infer these from the prompt, current branch, Jira URL, Jira issue content, or repository conventions:

- Jira key, for example `PROJ-123`
- Jira title
- acceptance criteria
- repository default branch
- intended handoff branch
- test command
- required PR template fields
- whether refactoring is required

If the Jira issue content is not available through tools or local context, ask for the issue text or URL before implementing. If the key is available but the full issue is not, proceed only when the user supplied enough acceptance criteria.

## Step 1: understand the Jira issue

Before coding:

1. Read the Jira issue and linked context when available.
2. Extract:
   - problem statement
   - acceptance criteria
   - user-visible behavior
   - affected modules
   - likely tests
   - non-goals
   - risks and migration concerns
3. Inspect the repository for relevant docs and test commands.
4. Identify generated files, lockfiles, snapshots, schema outputs, and formatting-only changes.

## Step 2: design the train

Create a short train plan before coding. Use the smallest number of layers that keeps review humane.

Preferred layer types, in order:

1. `characterization-tests` - tests documenting current behavior, if useful and passing.
2. `mechanical-refactor` - renames, moves, extraction, dead-code cleanup, formatting, type tightening. No behavior change.
3. `foundation` - schema/model/API plumbing needed before behavior changes. Minimal or no user-visible behavior.
4. `behavior` - the actual Jira feature/fix.
5. `tests-docs` - feature tests, docs, examples, changelog, cleanup.

Omit layers that are not needed. Split any layer that becomes too large or mixes concerns.

Write the plan in this form:

```text
Jira: <KEY> <title>
Handoff branch: <KEY>-<slug>
Train:
1. train/<KEY>/01-... -> <KEY>-<slug>
   Scope: ...
   Behavior change: No/Yes
   Expected tests: ...
2. train/<KEY>/02-... -> train/<KEY>/01-...
   Scope: ...
   Behavior change: No/Yes
   Expected tests: ...
```

## History reshaping

When converting an already-implemented branch into a PR train, optimize the train for human review, not for preserving the original coding chronology.

You may use history reshaping on new train branches, such as cherry-pick, reset --soft, restore from commits, interactive rebase, or rebuilding patches from the final diff, when this makes PR layers clearer.

Allowed reshuffling examples:

- Move later pure refactors before behavior changes if they make the behavior PR smaller or easier to read.
- Split one implementation commit into foundation, behavior, tests, and docs layers.
- Combine tiny related commits into one reviewable layer.
- Rebuild train branches from the final feature diff when the original commit history mixes concerns.

Rules:

- Do not rewrite or force-push shared/user branches unless explicitly approved.
- Do not mutate the original implementation branch while building the train; create train branches from default, handoff, or disposable work branches.
- Force-push only agent-created train branches, and only when it improves stack clarity.
- Preserve the final behavior and test coverage.
- Document any reshaping in the train summary.
- Each train branch must still compile/pass relevant checks where feasible.

## Step 3: create the branch train

Use the repository default branch as the starting point unless the user specifies another base.

Example commands:

```bash
DEFAULT_BRANCH="$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null || git remote show origin | sed -n '/HEAD branch/s/.*: //p')"
git fetch origin

git switch -c "<KEY>-<slug>" "origin/${DEFAULT_BRANCH}"
git push -u origin "<KEY>-<slug>"

git switch -c "train/<KEY>/01-<layer-slug>" "<KEY>-<slug>"
# implement layer 1, commit, push

git switch -c "train/<KEY>/02-<layer-slug>" "train/<KEY>/01-<layer-slug>"
# implement layer 2, commit, push

git switch -c "train/<KEY>/03-<layer-slug>" "train/<KEY>/02-<layer-slug>"
# implement layer 3, commit, push
```

Commit messages should include the Jira key and the layer:

```text
<KEY>: refactor <area> for <feature>
<KEY>: implement <behavior>
<KEY>: add tests for <behavior>
```

## Step 4: implement one layer at a time

For each branch:

1. Start from the branch immediately below it.
2. Make only the changes for that layer.
3. Run the narrowest meaningful tests first, then broader tests when practical.
4. Commit only that layer.
5. Push the branch.
6. Record test results and known limitations.

If a necessary change would violate the layer boundary, stop and either:
- move the change to a more appropriate later layer, or
- split the current layer and update the train plan.

## Step 5: create draft PRs

Create draft PRs bottom-up.

Example:

```bash
gh pr create \
  --draft \
  --base "<KEY>-<slug>" \
  --head "train/<KEY>/01-<layer-slug>" \
  --title "[<KEY>] 1/N: <layer title>" \
  --body-file "/tmp/<KEY>-01-pr-body.md"

gh pr create \
  --draft \
  --base "train/<KEY>/01-<layer-slug>" \
  --head "train/<KEY>/02-<layer-slug>" \
  --title "[<KEY>] 2/N: <layer title>" \
  --body-file "/tmp/<KEY>-02-pr-body.md"
```

Every PR body must include:

```text
## Stack position
This is PR <i>/<N> in the <KEY> train.

Base: <base branch>
Head: <head branch>
Previous PR: <link or "none">
Next PR: <link or "none">
Final handoff branch: <KEY>-<slug>

## Review scope
What the reviewer should focus on.

## Out of scope
What intentionally belongs to another PR.

## Behavior change
Yes/No. If yes, describe exactly what changes.

## Suggested review order
1. ...
2. ...

## Tests
- [ ] <command> - <result>
- [ ] Not run: <reason>

## Risks
Known risks, migration notes, or edge cases.

## Jira
<issue key or URL>
```

After all PRs exist, update each PR body or add a comment with the full stack map and review order.

## Step 6: merge-train instructions for humans

Provide these instructions in the final response and in the top comment on each PR:

```text
Merge order:
1. Review and merge PR 1 into <KEY>-<slug>.
2. Fetch and confirm which commit landed on <KEY>-<slug>.
3. Retarget PR 2 to <KEY>-<slug> if GitHub does not do so automatically.
4. Rebase PR 2 so already-landed lower commits are dropped from its ancestry:
   git fetch origin
   git switch train/<KEY>/02-...
   git rebase --onto origin/<KEY>-<slug> origin/train/<KEY>/01-... train/<KEY>/02-...
   git push --force-with-lease
5. Check PR 2 mergeability in GitHub before review continues.
6. Review and merge PR 2.
7. Repeat until the train is complete.
8. At the end, <KEY>-<slug> is the complete handoff branch.
```

Prefer merge commits for intermediate train merges when the repository allows them, because they preserve ancestry and make stacked branch retargeting easier. If the repository requires squash merges, or if a lower PR landed as a different commit SHA than the train branch commit, rebase the next branch after each merge using `git rebase --onto` as shown above.

## Maintaining rewritten stacks

If you amend, rebase, or otherwise rewrite a lower train branch, immediately repair every descendant train branch before asking reviewers to continue.

Example after rewriting `train/<KEY>/01-...`:

```bash
git fetch origin

git switch train/<KEY>/02-...
git rebase --onto origin/train/<KEY>/01-... <old-01-commit-or-branch> train/<KEY>/02-...
git push --force-with-lease

git switch train/<KEY>/03-...
git rebase --onto origin/train/<KEY>/02-... <old-02-commit-or-branch> train/<KEY>/03-...
git push --force-with-lease
```

Use the old upstream that each descendant branch actually contains. Do not guess: inspect the graph first.

Helpful checks:

```bash
git log --graph --oneline --decorate --all --branches='*<KEY>*'
git merge-base origin/<KEY>-<slug> origin/train/<KEY>/02-...
git cherry -v origin/<KEY>-<slug> origin/train/<KEY>/02-...
```

After each lower PR merge, fetch, retarget the next PR if needed, rebase the next train branch onto the updated handoff branch, push with `--force-with-lease`, and check GitHub mergeability. If upper descendants still contain obsolete lower-layer commits, repeat the same cleanup upward through the stack.

Distinguish conflict types:

- Normal code conflict: Git reports file conflicts during rebase. Resolve the files, continue the rebase, and rerun relevant tests.
- Ancestry/stack conflict: GitHub shows conflicts or duplicate diffs because the handoff branch contains a lower layer as one commit SHA while an upper branch still descends from an older SHA for the same logical layer. Repair ancestry with `rebase --onto` before editing code.

Force-push only agent-created train branches, and only with `--force-with-lease`.
