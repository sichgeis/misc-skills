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
9. Hand off `<KEY>-<slug>` to the human colleague.

Do not merge any train branch directly to `main`, `master`, `develop`, or the repository default branch unless explicitly requested.

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
