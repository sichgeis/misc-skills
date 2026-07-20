---
name: pr-babysit
description: Create or prepare a GitHub pull request from a mostly finished feature branch, apply a pragmatic final review pass, choose an available durable scheduler, session cron, event monitor, one-shot wait, or manual fallback for CI and review comments, handle relevant feedback, safely clean settled bot chatter, and return a copy-ready human-review handoff. Use when the user asks to create a PR and babysit it, put a PR on a heartbeat, wait for CI/review bots, or keep watching a PR after implementation is mostly complete.
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
6. Write a useful working PR body with:
   - summary
   - verification performed
   - scope and non-goals
   - review notes or risk areas
   - linked ticket or issue
   This working body may retain operational detail during review. Replace it with the concise human-facing description in [Human-Review Finalization](#human-review-finalization) only after the successful readiness gate passes.
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

Successful end criteria: Begin human-review finalization only when the local and remote branch are clean and pushed; required checks are green; significant feedback is answered, resolved, or deliberately deferred; the PR is open and non-draft; GitHub reports no merge conflict; and every non-human merge requirement is satisfied. Expected human approval may remain. Then save a concise human-facing PR description that preserves the Jira/issue link, inventory and safely clean only settled bot/agent chatter when authorized, re-verify readiness, stop or delete the watch created by this run, and return the exact final description, PR URL, and a copy-ready Slack review request. Never alter human-authored feedback. If the readiness gate does not pass, keep watching or report the blocker without performing final conversation cleanup.
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

## Human-Review Finalization

Run this phase only for a successful handoff. If the user asks to stop early, feedback begins oscillating, or a material blocker remains, stop making changes and report the state without cleaning the PR conversation.

### 1. Confirm The Readiness Gate

Require all of the following:

- The local and remote branch are clean, synchronized, and pushed.
- Required CI and checks are green.
- All significant feedback is answered, resolved, or deliberately deferred with durable context.
- The PR is open and non-draft.
- GitHub reports no merge conflict.
- Every non-human merge requirement is satisfied; expected human approval may remain.

Do not infer mergeability from green CI alone. Check GitHub's merge state, review decision, and required checks directly.

### 2. Finalize The PR Description

Before cleaning conversation history, save a concise human-facing description. Follow a mandatory repository PR template when it requires additional sections; otherwise use:

```markdown
## Summary

- <short change>
- <short change>

## Why

<one short plain-language explanation>

Jira: [<TICKET>](https://jira.example.com/browse/<TICKET>)
```

Keep `Summary` to a few bullets and `Why` to one short paragraph. Always preserve the original Jira or issue reference when one exists; omit the `Jira` line only when none exists. Remove babysitting-only material such as verification transcripts, feedback-disposition logs, bot discussion summaries, scope/non-goal bookkeeping, and review notes unless repository policy or a material human-review risk genuinely requires it.

### 3. Clean Settled Bot Conversation

Perform conversation cleanup only after the final description durably captures the human-facing context. Before deleting or minimizing content, confirm that the user explicitly requested cleanup or approved a babysitting plan that named it. Without that authorization, preserve the content, resolve settled threads when already authorized by the review workflow, and report the limitation.

1. Inventory top-level PR conversation comments, submitted review summaries, inline review comments, and review threads.
2. Classify every item by author and state. Distinguish automation, bots, and agents from human colleagues; when identity is uncertain, treat the author as human.
3. Never delete, hide, minimize, dismiss, or rewrite human-authored feedback.
4. Never remove an unresolved risk, requested change, decision, or follow-up unless it is captured in the final PR body or linked ticket.
5. For clearly settled automation content:
   - delete redundant top-level bot comments and agent disposition replies when authorized and safe;
   - resolve inline bot threads and leave them collapsed;
   - minimize settled bot-authored submitted review summaries or review comments as `RESOLVED` when GitHub supports it;
   - never dismiss a submitted review merely to reduce noise because dismissal creates additional timeline activity.
6. If deletion or minimization is unavailable, leave the item resolved or collapsed and record the limitation without failing the run.

Submitted review records are immutable. Prefer purpose-built GitHub capabilities; use REST deletion or GitHub GraphQL minimization only for capability gaps, after verifying the exact node, author, type, and settled state.

### 4. Re-verify And Stop The Watch

After cleanup, verify that:

- no human-authored feedback was removed or altered;
- no significant unresolved thread remains;
- the PR is still open, non-draft, pushed, green, and conflict-free; and
- the concise description and original Jira/issue reference remain intact.

Do not add a GitHub comment reporting cleanup. Record only aggregate counts for the final user response, such as comments deleted, threads resolved, items minimized, items preserved, and limitations.

Only after re-verification, delete the scheduler or cron job or stop the monitor using the capability that created it. A one-shot wait or manual fallback may have nothing to remove.

### 5. Return The Copy-Ready Handoff

Keep the final response short. Include:

- confirmation that babysitting ended and why;
- the exact final PR description in chat;
- the PR URL;
- aggregate cleanup results and material limitations in one short line; and
- this copy-ready Slack request:

```text
Please review <PR title>: <PR URL>

<one-sentence Why or concise PR description>
```

Do not reproduce removed bot transcripts or add a long verification report.

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

For authorized final cleanup, use purpose-built GitHub operations when available. Use `gh api` only for gaps such as deleting a verified bot-authored issue comment through REST or minimizing a verified bot-authored review summary/comment through GraphQL with classifier `RESOLVED`. Do not use review dismissal as cleanup.

## Response Style

During an active watch, keep status reports short and operational. After successful finalization, use the copy-ready handoff defined above instead.

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
