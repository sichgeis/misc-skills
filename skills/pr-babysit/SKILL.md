---
name: pr-babysit
description: Create or prepare a GitHub pull request from a mostly finished feature branch, apply a pragmatic final review pass, choose an available durable scheduler, session cron, event monitor, one-shot wait, or manual fallback for CI and review comments, handle relevant feedback, update the PR description, and stop babysitting when the PR is ready for human review. Use when the user asks to create a PR and babysit it, put a PR on a heartbeat, wait for CI/review bots, or keep watching a PR after implementation is mostly complete.
---

# PR Babysit

Use this skill when a feature branch is mostly done and the user wants the coding agent to create or shepherd a GitHub PR until it is ready for human review.

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
7. If the PR should be watched, choose and set up the appropriate available watch mode after the PR URL exists.

## Watch Mode Selection

Choose the strongest available capability that actually matches the requested lifetime. Do not call every mechanism a heartbeat, and do not imply persistence that the host does not provide.

1. **Durable scheduler:** use when the user wants watching to survive the current conversation or client session. Confirm that the scheduler is durable, record the created job ID, cadence, and cleanup method, and use the babysitting prompt below. If the host cannot prove durability, do not describe it as durable.
2. **Session cron:** use for periodic checks while the current session remains alive. State any host limits, including session-only lifetime or automatic expiry, and keep the job ID so it can be deleted when ending.
3. **Event monitor:** use for event-driven or continuous watching within the current session, such as streaming CI or PR events. Cover success and failure terminal states, filter noise, and stop the monitor when the PR reaches an end criterion.
4. **One-shot wait:** use when only one pending check, review, or workflow completion needs to finish. Wait once and return; do not create recurring automation.
5. **Manual fallback:** when none of the above exists, perform the current check, return the reusable babysitting prompt and exact manual command/checklist, and say that continued watching was not scheduled.

Prefer an event monitor over polling when a suitable event stream exists. Prefer a one-shot wait over recurring work when one completion is all that remains. Never use an internal subagent as a persistence substitute.

Use a babysitting prompt tailored to the ticket, repository, PR URL, branch, and reviewer expectations. For a durable scheduler or session cron, keep the prompt explicit enough that a future run can operate without the original conversation.

Template:

```text
Babysit <TICKET-KEY or short PR name> PR

Check GitHub PR <PR URL> for CI status and new review comments, especially <expected bots/reviewers>. If checks are failing, inspect the failing logs and fix only issues relevant to this PR branch. If review comments exist, treat them as suggestions: apply them when they improve correctness, readability, tests, maintainability, or the explicit API/contract for this slice; push back politely when they would over-scope <ticket/epic slice>, introduce unnecessary indirection, or conflict with repository conventions. For every processed review comment, either answer it, resolve it, or mark it handled in the appropriate GitHub thread. Keep replies very concise and readable; use a small table when it makes several comment outcomes easier to scan.

Use the gm-refactor lens when relevant: keep the main flow readable, extract only meaningful stable details, avoid broad rewrites, reduce surprising mutation, and verify with focused tests. Push justified fixes to the PR branch and report what changed, what is still pending, and any comments deliberately not applied.

End criteria: If CI is green or only blocked by expected human-review requirements, and there is nothing significant left to improve, or if bot/reviewer comments begin flipflopping or asking for scope churn rather than clear correctness/readability improvements, stop making code changes. Before ending, update the GitHub PR description one final time with the final summary, verification, accepted review feedback, and deliberately deferred/non-applied comments. Make sure the PR is ready for human review, not draft unless intentionally still draft, on the correct branch, and cleanly pushed. Then stop and delete the watch job or monitor if this run created one, and notify the user that babysitting has ended and why.
```

For recurring polling, choose a cadence that matches the repo's CI/review timing. If unknown, use about 7 minutes during active review. Do not impose a cadence on an event monitor or one-shot wait.

## Watch Run Workflow

On each recurring run or relevant monitor event:

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

End the active watch when one of these is true:

- CI is green or only blocked by expected human approval/review requirements.
- There are no significant unresolved review comments.
- Remaining comments are deliberate non-goals for this small slice.
- Bot or reviewer feedback starts flipflopping, repeating, or asking for scope churn instead of clear improvements.
- The user asks to stop.

Before deleting or stopping a watch created by this run:

1. Ensure the local and remote branch state is clean and pushed.
2. Mark the PR ready for review if it should no longer be draft.
3. Update the PR description one final time with:
   - final summary
   - verification
   - accepted feedback
   - deferred or non-applied comments with brief rationale
   - current status and remaining human-review needs
4. Confirm processed review comments are answered, resolved, or marked handled.
5. Delete the scheduler or cron job, or stop the monitor, using the same capability that created it. If this was a one-shot wait or manual fallback, there may be nothing to delete.
6. Notify the user that babysitting ended, why, and whether any session-lifetime limitation affected the watch.

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
