---
name: find-local-project
description: Discover, catalog, and locate Christian's local Git repositories under /Users/christian/hypatos and /Users/christian/projects. Use when Christian asks a coding agent to find, locate, identify, list, refresh, or work with a local project or repository that is not already the current workspace.
---

# Find Local Project

Use the bundled script as the source of truth for local project discovery.

## Workflow

1. If the user asks to refresh or enumerate projects, run:

   ```bash
   python scripts/local_projects.py refresh
   python scripts/local_projects.py list
   ```

2. If the user names or describes a project, run:

   ```bash
   python scripts/local_projects.py find "<query>"
   ```

   The `find` command refreshes automatically only when neither the current catalog nor a readable legacy catalog exists.

3. Report the best matching absolute path, category, remote, and summary. If multiple candidates are close, show the small candidate set and ask which one the user means.

4. Do not assume that locating a repository grants permission to modify it. For implementation work, start or move the task to that repository as its workspace. If the current task intentionally spans repositories, confirm that the relevant paths are available under the current sandbox.

## Catalog

The defaults are:

- Work repositories: `/Users/christian/hypatos`
- Other projects: `/Users/christian/projects`
- Shared JSON catalog:
  - `$LOCAL_PROJECTS_HOME/local-projects.json` when the skill-specific override is set;
  - otherwise `$XDG_STATE_HOME/local-projects/local-projects.json` when `XDG_STATE_HOME` is set;
  - otherwise `~/.local/state/local-projects/local-projects.json`.
- Human-readable catalog: the corresponding `local-projects.md`.

For compatibility, read commands may use the legacy `$CODEX_HOME/local-projects.json` or `~/.codex/local-projects.json` when the neutral default catalog is absent. This is a non-destructive fallback: it does not move, rewrite, or delete the legacy catalog. An explicit `LOCAL_PROJECTS_HOME` or `--json` path is authoritative and does not fall back elsewhere.

Discovery recognizes `.git` directories and files. It stops descending after finding a repository, which avoids treating nested generated checkouts as independent durable projects. It also skips common caches, dependencies, worktree collections, and build-output directories.

Use `--root CATEGORY=PATH` to add or replace roots for a one-off refresh. Use `--json PATH --markdown PATH` when testing without writing to shared state.

## Optional Daily Refresh on macOS

The installer source can manage a neutral `launchd` label, `com.christian.local-project-catalog`, with logs beneath the neutral catalog state directory. Installation migrates away from the legacy `com.christian.codex.local-project-catalog` job by unloading it and removing its plist; `status` and `uninstall` also recognize both labels.

Installing, loading, unloading, enabling, kickstarting, or uninstalling a `launchd` job changes system persistence. Do not run any of those actions unless the user explicitly authorizes that persistence action. Source inspection, payload generation, imports, compilation, and injected-runner tests are safe alternatives when only validation was requested.

When explicitly authorized, the commands are:

```bash
python scripts/install_daily_refresh.py install
python scripts/install_daily_refresh.py status
python scripts/install_daily_refresh.py uninstall
```

The installed job refreshes the catalog when loaded and every day at 09:00 local time.

After creating or updating this skill, restart the coding agent if its host requires a restart to reload skill manifests.
