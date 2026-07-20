---
name: walkthrough
description: "Guide a reviewer through a GitHub PR, stacked or staggered PR, branch, Jira issue, user story, or feature change as a calm, host-aware data-flow walkthrough with precise code locations."
---

# Walkthrough

Use this skill when the user asks for `$walkthrough`, a PR walkthrough, stacked PR walkthrough, staggered PR walkthrough, Jira or user-story code walkthrough, branch walkthrough, review-prep guide, or code navigation guide for understanding a feature well enough to review or explain it.

The goal is to help the user follow the runtime flow in their editor. Do not merely summarize the diff or produce a review report.

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

Prefer connected GitHub and Jira capabilities when available. Use local repository inspection, `git`, and authenticated CLIs such as `gh` as fallbacks.

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

Adapt navigation to the current host while keeping every code location precise.

- Prefer host-native code references when the host can open files directly.
- Otherwise use absolute paths with line numbers. Format them as Markdown links such as `[file.py](/absolute/path/file.py:42)` only when the host renders local links; plain `/absolute/path/file.py:42` is the fallback.
- Prefer one primary code location per navigation step, pointing to the best starting line.
- Put the function, class, method, or symbol name next to the location.
- Use GitHub URLs when the file is not available locally or the host cannot expose local paths.
- Keep language calm, compact, and concrete. Assume the user has had a long day.
- Explain domain terms at the point where they first matter.
- Write like a guided editor tour: tell the user what to open, what symbol or line to inspect, what the line means, and where to jump next.
- Prefer narrative sections over checklist cards. Do not use repeated `Responsibility`, `Look at`, or `Ask yourself` blocks unless the user explicitly asks for review questions.
- Quote only tiny snippets that anchor the walkthrough. Explain their plain meaning immediately after the snippet.

## Walkthrough structure

Use this structure unless the user asks for a different format:

````markdown
Yes. Let’s walk it like you are navigating through the code.

**Start Here**
Open [file.ext](/absolute/path/file.ext:line).

This is <the entry point and its role in the use case>. The main method/class/function is `<SymbolName>`.

The typical use case is <brief business/user context>. The important data is <request, event, object, payload, or state>.

The important flow starts around [line](/absolute/path/file.ext:line):

**Stack Scope**
<only include when stacked or staggered; explain earlier/later PRs and what is in or out of scope here>

1. <first thing the entry point does>
2. <second thing>
3. <third thing>

The key call/branch is here:
[file.ext:line](/absolute/path/file.ext:line)

```python
<small important snippet>
```

Plain meaning:
<short explanation of what the snippet means for this use case>

**<Next Code Area>**
Now jump to [file.ext](/absolute/path/file.ext:line).

This code <role in the flow>. The part to read is:
[file.ext:line](/absolute/path/file.ext:line)

```python
<small important snippet>
```

Plain meaning:
<short explanation, including any domain term when it first matters>

**Fallback / Error Path**
<include only when relevant; explain the important fallback, guard, exception, retry, or user-visible failure>

**Cache / Storage / Side Effect**
<include only when relevant; explain where results are cached, stored, emitted, invalidated, returned, or handed to another system>

**Tests**
- [test_file.ext](/absolute/path/test_file.ext:line) - `<test name>` protects <behavior>

**Domain Terms**
<include only when several terms would clutter the tour; otherwise explain terms inline>

**Review Notes**
<missing coverage, risks, or especially useful review focus, if any>

**Full Path In One Breath**
1. [file.ext:line](/absolute/path/file.ext:line)  
   <one-line step>
2. [file.ext:line](/absolute/path/file.ext:line)  
   <one-line step>

The one-sentence version: <complete data-flow summary from entry point to exit/completion point>.
````

Keep the same spirit when the exact headings or location format differ. The example uses Markdown links, but use host-native references or plain absolute `path:line` locations when local links are unavailable. The walkthrough should feel like a person guiding the user through files, not a form being filled in.

Avoid front-loading separate `Problem`, `Feature In One Sentence`, `Data Involved`, `Entry Point`, `Exit Point`, and `Runtime Flow` sections unless the user asks for a structured report. Weave that information into `Start Here`, the narrative sections, and `Full Path In One Breath`.

## Guided tour quality bar

Each tour section should usually include:

- a host-native code reference, local link, or absolute `path:line` location
- function/class/method/symbol to open
- a key line, branch, call, or tiny snippet to inspect
- plain-language meaning of that code in the current use case
- where to jump next

Order the sections by how the runtime flow should be read, not by diff order. Name sections after the code area or concept, such as `The Request Object`, `LLM OCR Provider`, `Image Provider Contract`, `Old Document Fallback`, or `Cache Piece`.

Briefly summarize flow sections that are not relevant to the PR, but do not skip over the data path so much that the user loses where the request came from or where it exits.

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

If one of these does not exist or is not visible in the PR, say so briefly in the relevant tour section instead of inventing it.

When several entry or exit points exist, pick one primary pair and mention the others only if they affect the review. You may summarize unrelated flow sections in one sentence so the walkthrough keeps focus while still giving the user the surrounding data-flow context.

## Test mapping

Mention tests that prove the behavior and map each test to the behavior it protects. Put tests after the main code tour so they do not interrupt the runtime path.

If tests are absent or only cover part of the behavior, say what is missing in practical review terms. Do not turn the walkthrough into a full code review unless the user asks for one.
