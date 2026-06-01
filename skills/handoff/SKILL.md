---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up. Use when the user asks to hand off, summarize, checkpoint, compact, or prepare context for a fresh Codex session or another agent.
---

# Handoff

Write a concise Markdown handoff document so a fresh agent can continue the work without rereading the full conversation.

## Output Location

Save the handoff document in the user's OS temporary directory, not the current workspace.

- Prefer `${TMPDIR}` when it is set.
- Otherwise use `/tmp` on Unix-like systems.
- Use a descriptive filename such as `codex-handoff-YYYYMMDD-HHMMSS.md`.

Tell the user the full path after writing the file.

## Inputs

If the user passes arguments or describes the next session's purpose, treat that as the focus for the handoff. Tailor the summary, suggested skills, and next actions to that focus.

## Content

Include these sections when relevant:

- `Next Session Focus`: what the next agent should optimize for.
- `Current State`: goal, status, branch, repo, environment, and active constraints.
- `Important Context`: decisions, assumptions, user preferences, and non-obvious findings.
- `Artifacts To Reference`: paths or URLs for PRDs, plans, ADRs, issues, commits, diffs, reports, and generated files.
- `Suggested Skills`: skills the next agent should invoke and why.
- `Next Actions`: concrete steps in the recommended order.
- `Risks And Blockers`: unresolved questions, failing checks, missing approvals, or fragile assumptions.

Do not duplicate substantial content already captured in other artifacts. Reference those artifacts by path, commit, issue, PR, URL, or command instead.

## Redaction

Before writing, inspect the draft for sensitive data and redact it.

Redact secrets and credentials, including API keys, tokens, passwords, cookies, private keys, authorization headers, connection strings, and session identifiers.

Redact personal information unless it is necessary for the handoff. Prefer roles, usernames, or artifact references over full personal details.

Use clear placeholders such as `[REDACTED_API_KEY]`, `[REDACTED_TOKEN]`, or `[REDACTED_PERSONAL_INFO]`.

## Quality Bar

Keep the handoff brief but complete enough that another agent can proceed. Prefer precise bullets, file paths, commands already run, and remaining decisions over narrative recap.
