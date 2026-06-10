# Human Merge Train Procedure

The train ends on the handoff branch:

```text
<JIRA-KEY>-<short-slug>
```

Review from the bottom of the stack upward.

```text
<KEY>-<slug>
 └─ PR 1: train/<KEY>/01-...
     └─ PR 2: train/<KEY>/02-...
         └─ PR 3: train/<KEY>/03-...
```

## Merge order

1. Review PR 1.
2. Merge PR 1 into `<KEY>-<slug>`.
3. Fetch and confirm which commit landed on `<KEY>-<slug>`.
4. Retarget PR 2 to `<KEY>-<slug>` if GitHub does not do so automatically.
5. Rebase PR 2 to drop already-landed lower commits, especially after squash merges or rewritten lower branches:

```bash
git fetch origin
git switch train/<KEY>/02-...
git rebase --onto origin/<KEY>-<slug> origin/train/<KEY>/01-... train/<KEY>/02-...
git push --force-with-lease
```

6. Check PR 2 mergeability in GitHub before review continues.
7. Review and merge PR 2.
8. Repeat until the train is complete.
9. Run the final stack health gate before saying the train is ready.
10. Hand off `<KEY>-<slug>` to the human colleague.

Do not merge any train branch directly to `main`, `master`, `develop`, or the repository default branch unless explicitly requested.

## If a lower PR or branch changes

After changing, rebasing, amending, force-pushing, or merging any non-top train branch, repair every descendant train branch before review continues.

Do not repair a stale stack by merging the lower branch into the upper branch. Prefer `git rebase --onto`, because merge commits can preserve duplicate ancestry and delay the conflict.

Required checklist:

1. Record the old lower branch head SHA before changing it:

```bash
git rev-parse origin/train/<KEY>/01-...
```

2. Push the changed lower branch.
3. For each descendant, rebase onto its new base using the old base SHA or old upstream branch that the descendant actually contains:

```bash
git fetch origin
git switch train/<KEY>/02-...
git rebase --onto <new-base> <old-base-sha-or-branch> train/<KEY>/02-...
git push --force-with-lease
gh pr view <next-pr> --json mergeable,baseRefName,headRefName,headRefOid
```

4. If the rebase produced conflicts, resolve them, continue the rebase, and run focused tests for the conflicted files or behavior.
5. Repeat upward until every descendant branch has been repaired.

## If upper PRs show conflicts after a lower merge

First determine whether this is a real code conflict or a stack ancestry conflict.

An ancestry conflict often means the handoff branch contains the lower layer as a new commit SHA, while upper branches still descend from an older local SHA for that same layer. GitHub then sees duplicate parallel history and may show conflicts or repeated lower-layer diffs.

Check before editing code:

```bash
git fetch origin
git log --graph --oneline --decorate --all --branches='*<KEY>*'
git merge-base origin/<KEY>-<slug> origin/train/<KEY>/02-...
git cherry -v origin/<KEY>-<slug> origin/train/<KEY>/02-...
```

Repair by rebasing the next branch onto the updated handoff branch, then repeat upward for any descendants that still contain obsolete lower-layer commits. Push only agent-created train branches, and only with `--force-with-lease`.

## Final stack health gate

Before saying the train is ready, check every open train PR:

1. `git cherry -v <base> <head>` must not show stale lower-layer commits that already landed on the base.
2. `gh pr view <pr> --json mergeable,baseRefName,headRefName,headRefOid` must report `MERGEABLE`, or say GitHub is still recalculating.
3. The PR diff must contain only the intended layer scope. If it includes duplicate lower-layer work, repair the descendant branch with `rebase --onto` before continuing.
