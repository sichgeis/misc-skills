# Human Merge Train Procedure

The train ends on the handoff feature branch:

```text
feature/<JIRA-KEY>-<short-slug>
```

Review from the bottom of the stack upward.

```text
feature/<KEY>-<slug>
 └─ PR 1: train/<KEY>/01-...
     └─ PR 2: train/<KEY>/02-...
         └─ PR 3: train/<KEY>/03-...
```

## Merge order

1. Review PR 1.
2. Merge PR 1 into `feature/<KEY>-<slug>`.
3. Retarget PR 2 to `feature/<KEY>-<slug>` if GitHub does not do so automatically.
4. If the repo squash-merged PR 1, rebase PR 2 to drop already-landed lower commits:

```bash
git fetch origin
git switch train/<KEY>/02-...
git rebase --onto origin/feature/<KEY>-<slug> origin/train/<KEY>/01-... train/<KEY>/02-...
git push --force-with-lease
```

5. Review and merge PR 2.
6. Repeat until the train is complete.
7. Hand off `feature/<KEY>-<slug>` to the human colleague.

Do not merge any train branch directly to `main`, `master`, `develop`, or the repository default branch unless explicitly requested.
