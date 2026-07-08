---
description: Refactor the current code using the Goldene Mitte readability style.
---

Refactor the requested code using the `gm-refactor` skill.

The user invoked `/gm-refactor` with this request:

```text
$ARGUMENTS
```

If `$ARGUMENTS` was not expanded by this agent, infer the requested refactor target from the text after `/gm-refactor` in the user's message.

Inspect the relevant files, tests, and call sites first. Preserve behavior unless the request explicitly calls for a behavior change. Keep visible control flow inline, extract only helpers that name meaningful actions or hide real detail, and run focused validation before responding.
