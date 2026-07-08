---
name: gm-refactor
description: 'Refactor code toward readable, pragmatic structure using the "Goldene Mitte" style: preserve visible control flow, extract meaningful domain actions and noisy stable details, avoid trivial helper indirection, reduce surprising mutation, and verify behavior with focused tests. Use when the user asks for refactoring, readable refactoring, cleanup, simplification, decomposition, reducing complexity, or "goldene Mitte" refactor work.'
---

# GM Refactor

Use this skill when refactoring code for readability and maintainability. The goal is die goldene Mitte: enough structure that a developer can scan the code and understand the story, but not so much structure that simple logic is hidden behind chains of tiny helpers.

## Core Principle

Readable refactoring keeps the top-level control flow visible while moving distracting details behind names that explain intent.

- Keep obvious conditions inline when the condition is already clear.
- Extract helpers for meaningful domain actions, outcomes, contracts, logging, fallback construction, context setup, result merging, or behavior worth testing in isolation.
- Prefer code that can be read top to bottom without constant jumping.
- Make invariants explicit with focused assertions or comments when they protect behavior.
- Preserve behavior unless the user explicitly asks for a behavioral change.

## Workflow

1. Inspect the relevant files, tests, call sites, and local conventions before editing.
2. Identify the current story: inputs, decisions, side effects, outcomes, and error paths.
3. Choose small refactoring steps that preserve behavior.
4. Keep the orchestration path readable: decisions and outcomes should remain visible in order.
5. Extract only helpers that earn their name by hiding real detail or naming a real domain action.
6. Prefer derived values over mutating shared input when that clarifies ownership.
7. Run focused tests or the narrowest useful validation available.
8. Report what changed, how behavior was verified, and any residual risk.

## Extraction Heuristics

Extract a helper when it does one of these:

- Names a meaningful domain action or outcome.
- Keeps the caller at one level of abstraction.
- Encapsulates noisy but stable details such as logging, fallback construction, context setup, or result merging.
- Makes a behavioral branch easier to verify in isolation.
- Avoids mutating shared input and returns a derived value instead.
- Collapses repeated behavior without hiding important branching.

Avoid extracting a helper when it only wraps a trivial condition or expression.

Usually too much indirection:

```python
def _should_bypass_cache(request):
    return not request.load_from_storage
```

Often clearer inline:

```python
if not request.load_from_storage:
    return self._extract_requested_pages_without_cache(request)
```

## Functional Style

Use functional style to reduce surprising mutation, not as ceremony.

- Prefer derived values when ownership is clearer:

```python
request = replace(request, relevant_page_indices=missing_page_indices)
```

- Prefer comprehensions for simple data derivation:

```python
missing_page_indices = [
    page.page_index
    for page in stored_results
    if page.error == OcrPage.MISSING_FROM_CACHE_ERROR
]
```

- Keep stateful loops when the state is central to behavior. Retry loops, fallback chains, streaming, accumulation with early exits, and "last successful response" logic can be clearer when written directly.

## Refactoring Stance

- Optimize for the next maintainer reading the code, not for maximum extraction.
- Respect existing naming, module boundaries, dependency direction, and test style.
- Avoid broad rewrites unless the requested change requires them.
- Do not introduce new abstractions just to make code look cleaner.
- Do not mix unrelated formatting churn with behavioral or structural refactors.
- When a refactor exposes a bug, stop and make the behavioral change explicit in the response or ask if the change is not clearly implied.

## Review Checklist

Before finishing, ask:

- Can the top-level method be read without jumping around constantly?
- Do helper names describe behavior rather than implementation mechanics?
- Are obvious conditions still obvious in place?
- Did extraction remove noise, or did it only move code elsewhere?
- Are side effects, mutation, and invariants clear?
- Do tests or validation cover the branches touched by the refactor?

The desired result is calm code: the main method tells the story, helpers carry real detail, and simple logic stays close to where it matters.
