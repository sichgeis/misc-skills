# Misc Skills

Personal Codex skills that are too small or specific for a larger shared plugin.

## Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml
    assets/           # optional adaptable output templates
    references/       # optional detailed guidance loaded as needed
    scripts/          # optional deterministic helpers
```

Each skill lives in `skills/<skill-name>/` and follows the Codex skill format.

## Find Local Project

`find-local-project` catalogs and locates local Git repositories beneath
`/Users/christian/hypatos` and `/Users/christian/projects`. Its deterministic
helper produces machine-local JSON and Markdown catalogs outside this
repository, keeping the versioned skill source portable and the generated
inventory out of Git.

Invoke it with a prompt such as:

```text
Use $find-local-project to find my local prompting service repository.
```

The skill also includes a macOS `launchd` installer that refreshes the generated
catalog at login and daily at 09:00 local time:

```bash
python ~/.codex/skills/find-local-project/scripts/install_daily_refresh.py install
```

## Prepare A Vibe-Coded Repository

`prepare-vibe-coded-repo` establishes a lightweight operating system for small
personal projects. It first assesses existing repository guidance, then
classifies the project as Bootstrap, Consolidate, or Preserve and proposes the
smallest useful change set. Only after approval does it align the repository,
validate the result, and create one local commit. Small sequential projects
default to main; branches or worktrees remain available when isolation helps.

Invoke it with a prompt such as:

```text
Use $prepare-vibe-coded-repo to assess this repository and propose the smallest
useful setup for autonomous vibe-coded development.
```

The default bootstrap uses `AGENTS.md`, `FEATURES.md`, and `README.md`, while
preserving equivalent or specialized documentation that already works well.

## Install

Install all skills into the local Codex skills directory:

```bash
task install
```

When `CODEX_HOME` is unset, skills are installed into `~/.codex/skills`.
Restart Codex after installing new or updated skills.

## Useful Tasks

```bash
task list      # list skills in this repo
task validate  # validate each skill folder
task install   # install all skills locally
```
