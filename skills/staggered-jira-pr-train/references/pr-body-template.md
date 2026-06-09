# Staggered PR Train Body Template

## Stack position

This is PR `<i>/<N>` in the `<JIRA-KEY>` train.

Base: `<base branch>`  
Head: `<head branch>`  
Previous PR: `<link or none>`  
Next PR: `<link or none>`  
Final handoff branch: `<JIRA-KEY>-<short-slug>`

## Review scope

Explain what the reviewer should focus on in this PR only.

## Out of scope

Explain what intentionally belongs to another PR in the train.

## Behavior change

Yes/No.

If yes, describe exactly what changes from the user's point of view.

## Suggested review order

1. Start with ...
2. Then inspect ...
3. Ignore or skim ...

## Tests

- [ ] `<command>` - `<result>`
- [ ] Not run: `<reason>`

## Risks

List known risks, migrations, compatibility concerns, and edge cases.

## Jira

`<JIRA-KEY or URL>`

## Merge-train note

Review and merge this train bottom-up. The final landing target is the handoff branch, not the repository default branch.
