---
name: ui-feature-screenshot
description: Run local UI applications and dependencies, navigate to a PR or newly implemented feature, validate it through the best available UI-driving capability, and capture screenshots as evidence. Use when asked to start a frontend/backend stack, open a local UI, prove a UI feature works, prepare PR/demo screenshots, or visually verify a feature in a real local app.
---

# UI Feature Screenshot

Use this skill to produce trustworthy screenshots of a local UI feature. Prefer real app data and real backend/API paths. Stub only unrelated platform dependencies needed to make the local app usable.

## Core Workflow

1. Ground in the project.
   - Inspect `README`, package manifests, Docker Compose files, env examples, dev scripts, and app entrypoints.
   - Identify frontend URL, backend URL, required services, auth/user/company setup, and the feature route.
   - If this repo has a matching project reference, read it before running anything.

2. Start the stack.
   - Start only required dependencies.
   - Use the project's normal dev commands when available.
   - If env vars are missing, infer from local config and prior project references where safe.
   - Use local support stubs only for unrelated services such as auth, users, companies, or projects.
   - Do not mock the feature under test unless the user explicitly asks for mock screenshots.

3. Verify services before UI work.
   - Use an available HTTP client or request capability to check health endpoints or root pages.
   - Check feature API endpoints directly when the feature depends on backend data.
   - Record status codes and key labels, not large payloads.

4. Drive the UI.
   - Prefer the host's built-in browser or UI automation capability when it supports deterministic navigation, assertions, and screenshots.
   - Otherwise use an available project-native browser test setup or a transient automation tool such as Playwright without changing project dependencies.
   - Use an installed compatible browser when possible; do not assume Chrome is present.
   - Preload localStorage/session state only for normal app context such as selected company or cached user identity.
   - Intercept browser requests only for environment gates that block local validation, such as feature-flag evaluation. Keep feature data real.

5. Capture evidence.
   - Save screenshots in the host's temporary directory, under a descriptive `<project-or-feature>-screenshots/` folder. Prefer PNG when the capture capability supports it.
   - Capture the entry point, primary feature view/dialog, meaningful expanded/details state, and any related secondary UI.
   - Wait for transitions/animations to settle before screenshotting.
   - Verify expected labels/data are visible before each screenshot.
   - Inspect screenshots with an available image-viewing capability when possible; otherwise verify the files and UI assertions and state that visual inspection was unavailable.

6. Cleanup.
   - Stop foreground dev servers, helper stubs, and UI automation sessions started for the task.
   - Leave long-lived Docker dependencies running only when that matches the local workflow or the user asked for it.
   - Do not stop services the user said were already running unless explicitly requested.

## UI Automation Rules

- Choose capabilities in this order: host-provided UI automation, project-native browser tests, then a transient external automation tool.
- Require deterministic navigation, assertions, and screenshot capture regardless of the chosen tool.
- Use a compatible installed browser; when using Playwright, select an available browser or channel rather than assuming system Chrome.
- Use fixed viewport screenshots unless the user asks for responsive screenshots.
- Prefer text/role selectors derived from the rendered DOM.
- Avoid broad text dumps in final output.
- Return the screenshot paths or host-native attachments. Add inline Markdown images or file links only when the host supports and renders them.

## Validation Rules

Before final response, confirm:

- frontend loaded successfully;
- backend/API dependencies used by the feature returned success;
- screenshots exist and are non-empty;
- screenshots contain the requested UI states;
- feature data was not mocked unless explicitly requested;
- repo-tracked files were not changed unless the user requested implementation work.

## Project References

- For `hypatos/enrichment-hub`, read `references/enrichment-hub.md`.
- Add new project references over time as repeated local setup patterns become known.
