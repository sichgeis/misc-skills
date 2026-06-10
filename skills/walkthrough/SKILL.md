---
name: walkthrough
description: "Guide a reviewer through a GitHub PR, stacked or staggered PR, branch, Jira issue, user story, or feature change as a calm data-flow code walkthrough with VS Code-friendly file and line links."
---

# Walkthrough

Use this skill when the user asks for `$walkthrough`, a PR walkthrough, stacked PR walkthrough, staggered PR walkthrough, Jira or user-story code walkthrough, branch walkthrough, review-prep guide, or code navigation guide for understanding a feature well enough to review or explain it.

The goal is to help the user follow the runtime flow in their editor. Do not merely summarize the diff.

Every walkthrough should orient the user before code navigation: name the typical use case, the data or request involved, where that data enters the system, and where the use case exits.

## Required input

The user must provide at least one concrete target:

- GitHub PR URL or PR number with enough repo context
- branch name with enough repo context
- Jira issue key or URL
- user story or short feature description with repo context
- local files/tabs plus a clear review target

If the prompt lacks a GitHub hint, PR link, branch, Jira ID, repo hint, or concrete story reference, ask what exactly they want walked through before investigating.

## Investigation workflow

Prefer connected GitHub and Jira tools when available. Use local repository inspection, `git`, and `gh` as fallback.

For a GitHub PR:

1. Inspect title, description, linked issues, commits, changed files, base branch, and head branch.
2. Read enough changed and surrounding code to reconstruct the runtime path.
3. Identify the typical business/user use case, the relevant input data or request, one best entry point, and one best exit point.
4. Inspect nearby tests and existing implementation patterns, not only the modified lines.
5. Identify whether the PR is stacked by checking base/head relationships, PR body stack notes, linked PRs, branch names, and adjacent branches.
6. If stacked, explain earlier/later PRs that matter and clearly separate current-PR scope from adjacent PR scope.

For a Jira issue or user story:

1. Read the ticket or provided story where available.
2. Find related PRs, branches, code paths, and tests if discoverable.
3. Map acceptance criteria or story behavior to the code that implements it.
4. Identify the typical business/user use case, the relevant input data or request, one best entry point, and one best exit point.

For business or domain context, use Obsidian wiki reads when useful and available: scan relevant project notes, read likely matches, and use them only to explain the walkthrough context. Do not create or update wiki notes during a normal walkthrough.

The entry point can be a REST controller, message handler, CLI command, scheduled job, service method, or another concrete boundary. Choose the most helpful point for understanding the reviewed use case, not necessarily the first changed line. The exit point should be where the use case returns a response, emits an event, writes state, hands off to another system, or otherwise completes.

## Output rules

Optimize for VS Code plugin use.

- Use clickable local file links whenever files exist locally.
- Format local links as Markdown absolute-path links with line numbers: `[file.py](/absolute/path/file.py:42)`.
- Prefer one primary link per navigation step, pointing to the best starting line.
- Put the function, class, method, or symbol name next to the link.
- Use GitHub links only when the file is not available locally.
- Keep language calm, compact, and concrete. Assume the user has had a long day.
- Explain domain terms at the point where they first matter.

## Walkthrough structure

Use this structure unless the user asks for a different format:

```markdown
**Problem**
<plain-language problem the feature solves>

**Feature In One Sentence**
<one sentence>

**Typical Use Case**
<brief real-world or business context for the request/data flow>

**Data Involved**
<main request, event, object, payload, or state being processed>

**Entry Point**
[file.ext](/absolute/path/file.ext:line) - `SymbolName`: <where the data enters and why this is the best starting point>

**Exit Point**
[file.ext](/absolute/path/file.ext:line) - `SymbolName`: <where the use case returns, emits, stores, or completes>

**Stack Scope**
<only include when stacked or staggered; explain earlier/later PRs and what is in or out of scope here>

**Navigation Order**
1. [file.ext](/absolute/path/file.ext:line) - `SymbolName`
   Responsibility: <what this code does>
   Look at: <key lines, symbols, branches, or calls>
   Ask yourself: <review question>

**Domain Terms**
- `<term>`: <brief meaning>

**Runtime Flow**
Happy path: <how the data moves from the entry point to the exit point; be brief on steps unrelated to this review>
Fallback/error path: <fallbacks, exceptions, retries, guard clauses, or user-visible failures>
Cache/storage path: <where results are cached, stored, invalidated, or loaded; omit if not relevant>

**Tests**
- [test_file.ext](/absolute/path/test_file.ext:line) - `<test name>` protects <behavior>

**Review Notes**
<missing coverage, risks, or especially useful review focus, if any>
```

## Navigation step quality bar

Each navigation step may include:

- file path as a clickable local link when possible
- function/class/method/symbol to open
- key lines or symbols to look at
- what that code is responsible for
- is there anything particular to notice or mention about this step

Order the steps by how the runtime flow should be read, not by diff order.

## Flow coverage

Explicitly point out:

- the typical use case and business context for the flow
- the data or request being processed
- the concrete entry point where data enters
- the concrete exit point where the use case completes
- where decisions happen
- where side effects happen
- where results are stored, cached, returned, or emitted
- happy path behavior
- fallback and error behavior
- cache or storage behavior when present

If one of these does not exist or is not visible in the PR, say so briefly instead of inventing it.

When several entry or exit points exist, pick one primary pair and mention the others only if they affect the review. You may summarize unrelated flow sections in one sentence so the walkthrough keeps focus while still giving the user the surrounding data-flow context.

## Test mapping

Mention tests that prove the behavior and map each test to the behavior it protects.

If tests are absent or only cover part of the behavior, say what is missing in practical review terms. Do not turn the walkthrough into a full code review unless the user asks for one.
