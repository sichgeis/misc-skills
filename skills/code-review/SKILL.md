---
name: code-review
description: Thorough read-only code review for GitHub pull requests. Use when the user provides a PR URL or asks for review of a GitHub pull request, PR diff, branch, implementation risk, regression risk, or missing-test risk before merge.
---

# Code Review

Use this skill to review a provided GitHub pull request URL. The goal is to produce a grounded, high-signal review based on the PR metadata, diff, changed files, surrounding source, tests, and relevant project conventions.

## Core Constraints

- Treat the task as review-only. Do not edit files, apply patches, push commits, post GitHub comments, or start implementation unless the user separately asks for fixes after the review.
- Prefer direct repository and GitHub evidence over assumptions. Use connected GitHub capabilities when available, with `gh`, `git`, `rg`, and targeted file reads as fallbacks.
- Do not rely only on the patch. Inspect surrounding code, call sites, tests, schemas, migrations, configs, and docs when they affect review confidence.
- Protect user changes in the working tree. Before checking out or fetching branches, inspect the current state and avoid commands that would overwrite local work.
- If facts are uncertain, say what was inferred and what evidence is missing.

## PR Intake

1. Parse the PR URL and confirm it is a GitHub pull request URL.
2. Inspect local repository state:
   - `git status --short --untracked-files=all`
   - `git remote -v`
   - `git branch --show-current`
3. Use an available authenticated GitHub capability for PR context. If none is available, use GitHub CLI:
   - `gh pr view <url> --json title,body,author,baseRefName,headRefName,headRepositoryOwner,headRepository,commits,files,reviews,reviewDecision,statusCheckRollup,mergeStateStatus,url`
   - `gh pr diff <url>`
4. If the PR belongs to the current repository and it is safe to do so, fetch the PR refs for better local inspection. Avoid checkout when the working tree is dirty unless checkout is clearly unnecessary or the user has approved it.

## Review Workflow

1. Understand intent from the title, body, linked issues, changed file list, and commit messages.
2. Map the behavioral surface: entrypoints, APIs, database changes, background jobs, UI flows, permissions, configuration, and external integrations touched by the PR.
3. Read the diff and then read the relevant unchanged context around the modified code.
4. Trace important call paths both into and out of the changed code. Search for related symbols with `rg`.
5. Inspect tests changed by the PR and nearby existing tests. Identify whether tests actually cover the risky behavior.
6. Run non-mutating checks when they materially improve confidence and are feasible in the repository. If checks cannot run, state why.
7. For risky or broad PRs, do an adversarial pass: challenge design assumptions, data migration safety, rollback behavior, concurrency, compatibility, failure modes, and simpler alternatives.

## What To Look For

- Correctness bugs, regressions, edge cases, and unhandled null/empty/error states.
- Security and privacy issues, including authz/authn gaps, injection, secret exposure, unsafe deserialization, SSRF, XSS, path traversal, and excessive logging.
- Data loss or corruption risks, especially around migrations, backfills, idempotency, retries, transactions, and partial failures.
- Concurrency, ordering, timeout, caching, and race-condition problems.
- API, schema, event, CLI, configuration, and persistence compatibility breaks.
- Missing or misleading tests, weak assertions, untested failure paths, and snapshots that hide behavior changes.
- Operational risks: observability gaps, noisy alerts, rollout hazards, feature flag issues, and poor rollback paths.
- Maintainability issues only when they create concrete risk or make future defects likely.

## Output Format

Lead with findings, ordered by severity. Use this shape:

```text
Findings
- [severity] file:line - Concise title.
  Explain the bug, why it matters, and the scenario that triggers it. Reference evidence from the PR or surrounding code.

Open Questions
- List only questions that affect review confidence or merge safety.

Checks
- State commands or inspections performed and their results. Include checks that could not run.

Summary
- Briefly describe the PR and the main residual risk. If no issues were found, say "No issues found" clearly.
```

Severity labels:

- `critical`: likely data loss, security compromise, outage, or severe production breakage.
- `high`: likely user-visible regression, broken core flow, or unsafe migration/compatibility break.
- `medium`: real bug or missing safety coverage with bounded impact.
- `low`: minor correctness, test, or maintainability issue that is worth fixing but not merge-blocking.

For each finding, include a concrete reproduction path or failure scenario when possible. Avoid vague style feedback. If there are no substantive findings, do not invent issues; say no issues were found and identify any remaining test gaps or review limitations.

After creating or updating this skill, reload the skill registry if the host requires it. Restart the current session only when the host cannot discover skill changes dynamically.
