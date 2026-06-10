---
name: walkthrough
description: "Guide a reviewer through a GitHub PR, stacked or staggered PR, branch, Jira issue, user story, or feature change as a calm code-navigation walkthrough with VS Code-friendly file and line links."
---

# Walkthrough

Use this skill when the user asks for `$walkthrough`, a PR walkthrough, stacked PR walkthrough, staggered PR walkthrough, Jira or user-story code walkthrough, branch walkthrough, review-prep guide, or code navigation guide for understanding a feature well enough to review or explain it.

The goal is to help the user follow the runtime flow in their editor. Do not merely summarize the diff.

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
3. Inspect nearby tests and existing implementation patterns, not only the modified lines.
4. Identify whether the PR is stacked by checking base/head relationships, PR body stack notes, linked PRs, branch names, and adjacent branches.
5. If stacked, explain earlier/later PRs that matter and clearly separate current-PR scope from adjacent PR scope.

For a Jira issue or user story:

1. Read the ticket or provided story where available.
2. Find related PRs, branches, code paths, and tests if discoverable.
3. Map acceptance criteria or story behavior to the code that implements it.

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
Happy path: <where data enters, main decisions, side effects, and result>
Fallback/error path: <fallbacks, exceptions, retries, guard clauses, or user-visible failures>
Cache/storage path: <where results are cached, stored, invalidated, or loaded; omit if not relevant>

**Tests**
- [test_file.ext](/absolute/path/test_file.ext:line) - `<test name>` protects <behavior>

**Review Notes**
<missing coverage, risks, or especially useful review focus, if any>
```

## Navigation step quality bar

Each navigation step must include:

- file path as a clickable local link when possible
- function/class/method/symbol to open
- key lines or symbols to look at
- what that code is responsible for
- what question the reviewer should ask while reading it

Order the steps by how the runtime flow should be read, not by diff order.

## Flow coverage

Explicitly point out:

- where data enters
- where decisions happen
- where side effects happen
- where results are stored, cached, returned, or emitted
- happy path behavior
- fallback and error behavior
- cache or storage behavior when present

If one of these does not exist or is not visible in the PR, say so briefly instead of inventing it.

## Test mapping

Mention tests that prove the behavior and map each test to the behavior it protects.

If tests are absent or only cover part of the behavior, say what is missing in practical review terms. Do not turn the walkthrough into a full code review unless the user asks for one.
