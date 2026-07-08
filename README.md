# Misc Skills

Personal Codex skills that are too small or specific for a larger shared plugin.

## Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml
    commands/        # optional command or prompt compatibility wrappers
```

Each skill lives in `skills/<skill-name>/` and follows the Codex skill format.

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
