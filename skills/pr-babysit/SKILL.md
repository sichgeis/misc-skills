---
name: pr-babysit
description: Create or prepare a GitHub pull request from a mostly finished feature branch, apply a pragmatic final review pass, set up a heartbeat/automation to monitor CI and review comments, handle relevant feedback, update the PR description, and stop babysitting when the PR is ready for human review. Use when the user asks to create a PR and babysit it, put a PR on a heartbeat, wait for CI/review bots such as hy-review-bot or Claude, or keep watching a PR after implementation is mostly complete.
---

# PR Babysit

Use this skill when a feature branch is mostly done and the user wants Codex to create or shepherd a GitHub PR until it is ready for human review.

The goal is not to endlessly perfect the branch. The goal is to make the PR clean, scoped, reviewed by automation, responsive to useful feedback, and then stop.

## Operating Principles

- Keep the feature's original scope intact. Treat the PR as a small reviewable slice, not a chance to grow the epic.
- If the user invokes or references `$gm-refactor`, use that lens explicitly: preserve readable endpoint/service flow, extract only meaningful stable details, avoid broad rewrites, and verify with focused tests.
- Treat bot and reviewer comments as suggestions. Apply comments that improve correctness, readability, maintainability, tests, or an explicit API/contract. Push back politely on comments that over-scope the slice, add unnecessary indirection, or conflict with the intended design. Always answer, resolve, or otherwise mark handled any review comment you process.
- Fix only failures relevant to this PR branch. Do not chase unrelated flaky infrastructure or failures already present on the base branch unless the user asks.
- Prefer rebasing the PR branch onto the latest base branch over merging the base branch into the PR branch, unless the user explicitly requests a merge or rebasing would be unsafe for a shared branch.
- Do not merge the PR unless the user explicitly asks and the repo's merge conditions are satisfied.

## Initial PR Workflow

When starting from a local mostly finished branch:

1. Inspect repository guidance: `AGENTS.md`, `CONTRIBUTING.md`, PR templates, test docs, and branch conventions.
2. Identify the base branch and compare the feature branch against it.
3. Review the implementation before opening the PR:
   - read the diff and important touched files
   - run focused tests and linters where practical
   - check for accidental debug code, unrelated churn, generated-file surprises, and stale TODOs
   - apply a small readability pass only when it improves the current feature
4. Confirm the branch is clean except for intentional changes, commit them, and push.
5. Create a draft PR by default unless the user asked for a ready PR or repo conventions say otherwise.
6. Write a PR body with:
   - summary
   - verification performed
   - scope and non-goals
   - review notes or risk areas
   - linked ticket or issue
7. If the PR should be watched, set up the heartbeat after the PR URL exists.

## Heartbeat Setup

Use the available automation tools instead of inventing raw scheduling text. If automation tools are not already loaded, search for `automation_update` with `tool_search` and use the discovered tool.

Use a heartbeat prompt tailored to the ticket, repository, PR URL, branch, and reviewer expectations. Keep the prompt explicit enough that a future Codex run can operate without the original conversation.

Template:

```text
Babysit <TICKET-KEY or short PR name> PR

Check GitHub PR <PR URL> for CI status and new review comments, especially <expected bots/reviewers>. If checks are failing, inspect the failing logs and fix only issues relevant to this PR branch. If review comments exist, treat them as suggestions: apply them when they improve correctness, readability, tests, maintainability, or the explicit API/contract for this slice; push back politely when they would over-scope <ticket/epic slice>, introduce unnecessary indirection, or conflict with repository conventions. For every processed review comment, either answer it, resolve it, or mark it handled in the appropriate GitHub thread. Keep replies very concise and readable; use a small table when it makes several comment outcomes easier to scan.

Use the gm-refactor lens when relevant: keep the main flow readable, extract only meaningful stable details, avoid broad rewrites, reduce surprising mutation, and verify with focused tests. Push justified fixes to the PR branch and report what changed, what is still pending, and any comments deliberately not applied.

End criteria: If CI is green or only blocked by expected human-review requirements, and there is nothing significant left to improve, or if bot/reviewer comments begin flipflopping or asking for scope churn rather than clear correctness/readability improvements, stop making code changes. Before ending, update the GitHub PR description one final time with the final summary, verification, accepted review feedback, and deliberately deferred/non-applied comments. Make sure the PR is ready for human review, not draft unless intentionally still draft, on the correct branch, and cleanly pushed. Then delete this heartbeat automation and notify the user that babysitting has ended and why.
```

Choose a cadence that matches the repo's CI/review timing. If unknown, use a moderate interval that is frequent enough to catch bot feedback without spamming, for example every 30-60 minutes during active review.

## Heartbeat Run Workflow

On each heartbeat run:

1. Read the PR state:
   - title, body, base/head branches, draft status
   - CI/check status and failing job names
   - latest commits and whether the branch is behind the base
   - new review comments, unresolved threads, and bot comments
2. If checks fail:
   - inspect logs for the failing jobs
   - distinguish PR-caused failures from flakes or base-branch failures
   - implement the smallest relevant fix
   - run focused local validation when possible
   - commit and push the fix
3. If review comments exist:
   - group comments by theme
   - apply high-signal correctness/readability/test/API-contract feedback
   - answer, resolve, or mark handled every processed comment or thread
   - leave or draft a concise reply for comments that are out of scope, duplicative, or not worth the added complexity
   - keep replies easy to read; use short bullets or a small table when summarizing multiple comment outcomes
   - avoid fighting style-only comments unless they create meaningful churn
4. If the branch is stale:
   - prefer rebase onto the latest base branch
   - ask before rebasing if the branch appears shared, protected, or has non-agent commits that make rewriting unsafe
5. Update the user with:
   - what was checked
   - what changed, if anything
   - validation run
   - comments applied or deliberately deferred
   - current blocking condition

## Ending Babysitting

End the heartbeat when one of these is true:

- CI is green or only blocked by expected human approval/review requirements.
- There are no significant unresolved review comments.
- Remaining comments are deliberate non-goals for this small slice.
- Bot or reviewer feedback starts flipflopping, repeating, or asking for scope churn instead of clear improvements.
- The user asks to stop.

Before deleting the heartbeat:

1. Ensure the local and remote branch state is clean and pushed.
2. Mark the PR ready for review if it should no longer be draft.
3. Update the PR description one final time with:
   - final summary
   - verification
   - accepted feedback
   - deferred or non-applied comments with brief rationale
   - current status and remaining human-review needs
4. Confirm processed review comments are answered, resolved, or marked handled.
5. Delete the heartbeat automation using the automation tool that created or manages it.
6. Notify the user that babysitting ended and why.

## Useful GitHub Checks

Prefer GitHub app tools when available. Use `gh` as needed for precise CI, review-thread, and PR operations.

Common commands:

```bash
gh pr view <PR-URL> --json title,body,baseRefName,headRefName,isDraft,mergeStateStatus,reviewDecision,statusCheckRollup
gh pr checks <PR-URL>
gh pr diff <PR-URL>
gh pr view <PR-URL> --comments
gh run view <RUN-ID> --log-failed
```

For unresolved review-thread state, use the GitHub tools or GraphQL when flat comments are not enough.

## Response Style

Keep status reports short and operational:

```text
Checked <PR>. CI: <state>. Reviews: <state>.
Changed: <summary or "nothing">.
Verified: <commands or "not run, reason">.
Pending: <human review / failing check / none>.
Deferred: <comments intentionally not applied, if any>.
```

When reporting several review comments, prefer a compact table:

```text
| Comment | Decision | Status |
| --- | --- | --- |
| Rename helper | Applied | Resolved |
| Split follow-up scope | Deferred: outside this slice | Replied |
```
