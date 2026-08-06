# Technical Document Patterns

Use these patterns when a rewrite needs more than sentence-level editing. Keep
the patterns proportional to the document. Do not add sections that have no
useful content.

## Repository Documentation

Prefer this order when it fits the subject:

1. State the purpose and scope.
2. Define the contract, model, or important terms.
3. Describe the normal flow.
4. State configuration values and defaults.
5. Describe failures, exceptions, and fallback behavior.
6. Add a compact example or outcome matrix when it resolves ambiguity.

Put conditions before behavior:

```markdown
If the primary endpoint returns a retryable error, the client retries the
request twice. If both retries fail, the client sends the request to the
fallback endpoint.
```

Use a table when readers must compare three or more exact mappings:

```markdown
| Input state | Action | Result |
| --- | --- | --- |
| Valid | Process the request | Return the result |
| Retryable error | Retry twice | Return the result or use the fallback |
| Invalid | Reject the request | Return a validation error |
```

Keep code blocks for literal configuration, commands, payloads, or output. Do
not put ordinary prose in a code block.

## Jira Stories and Acceptance Criteria

Use only the sections that help engineering and product readers make a
decision:

1. State the intended outcome.
2. Add the relevant context or problem.
3. Describe the required behavior.
4. List testable acceptance criteria.
5. Separate real exclusions or open questions from committed scope.

Write each acceptance criterion as a condition and observable result:

```markdown
- If the request contains a valid token, the API returns the requested record.
- If the token is missing, the API returns `401 Unauthorized`.
- If the record does not exist, the API returns `404 Not Found`.
```

Preserve the strength of each requirement. Do not convert a suggestion into a
mandatory criterion or weaken a mandatory criterion.

## Knowledge-Base Notes

Lead with the durable statement that a future reader needs. Then organize the
supporting material:

1. State the durable fact, decision, or relationship.
2. Explain the mapping or behavior.
3. Link the evidence or source.
4. Separate unresolved questions from established knowledge.

Example:

```markdown
The worker uses the account region to select an endpoint.

- `eu` uses `https://eu.example.test`.
- `us` uses `https://us.example.test`.

Source: [Service configuration](https://example.test/configuration)

Open question: The configuration does not define behavior for other regions.
```

Do not turn a tentative observation into a durable fact. Keep uncertainty when
the evidence is incomplete.

## Procedures and Runbooks

- State prerequisites before the steps.
- Use numbered steps for the required sequence.
- Put one action in each step.
- State the expected result after a step when it helps the operator detect a
  failure.
- Put rollback or recovery behavior next to the condition that requires it.
- Keep commands and literal output in code blocks.

## Error Messages

Include the failure and the next useful action:

```text
The upload failed because the file exceeds 20 MB. Select a smaller file and try
again.
```

Do not blame the user. Do not claim a cause unless the system knows it.
