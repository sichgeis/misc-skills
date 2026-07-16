---
name: find-local-project
description: Discover, catalog, and locate Christian's local Git repositories under /Users/christian/hypatos and /Users/christian/projects. Use when Christian asks Codex to find, locate, identify, list, refresh, or work with a local project or repository that is not already the current workspace.
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

   The `find` command refreshes automatically when the catalog is missing.

3. Report the best matching absolute path, category, remote, and summary. If
   multiple candidates are close, show the small candidate set and ask which
   one the user means.

4. Do not assume that locating a repository grants permission to modify it.
   For implementation work, start or move the task to that repository as its
   workspace. If the current task intentionally spans repositories, confirm
   that the relevant paths are available under the current sandbox.

## Catalog

The defaults are:

- Work repositories: `/Users/christian/hypatos`
- Other projects: `/Users/christian/projects`
- JSON catalog: `$CODEX_HOME/local-projects.json`, or
  `~/.codex/local-projects.json` when `CODEX_HOME` is unset
- Human-readable catalog: the corresponding `local-projects.md`

Discovery recognizes `.git` directories and files. It stops descending after
finding a repository, which avoids treating nested generated checkouts as
independent durable projects. It also skips common caches, dependencies,
worktree collections, and build-output directories.

Use `--root CATEGORY=PATH` to add or replace roots for a one-off refresh. Use
`--json PATH --markdown PATH` when testing without writing to the Codex home.

## Daily Refresh on macOS

Install the versioned `launchd` job after installing the skill:

```bash
python scripts/install_daily_refresh.py install
```

It refreshes the catalog when loaded and every day at 09:00 local time. Logs
are written beneath `~/.codex/logs`. Inspect or remove it with:

```bash
python scripts/install_daily_refresh.py status
python scripts/install_daily_refresh.py uninstall
```

After creating or updating this skill, restart the coding agent so it can load
the updated skill manifest.
