---
name: rollback-image-tag
description: Use when the user asks to roll back a bad applications-infra deployment by image tag, short git SHA, image SHA, bad deployed version, or prompt like "rollback bad tag 8A11D5C". Finds the commits that introduced the tag, restores previous image tags in Helm values files, opens a PR, and only merges when the environment and checks make that appropriate.
---

# Rollback Image Tag

## Overview

Roll back bad image tags in `applications-infra` from one central input: the bad tag. Treat timestamps, "minutes ago", service names, and incident details as optional hints, not required inputs.

Default repository: the locally available `applications-infra` checkout. Discover it from the current workspace, known project roots, or host project-discovery capabilities instead of assuming a user-specific absolute path.

If the user names another repo, use that repo instead. Before changing files, read the repository's applicable guidance, such as `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, or host-provided repository instructions.

## Safety Rules

1. Use the bad image tag as the primary identifier. Normalize it to lowercase, for example `8A11D5C` -> `8a11d5c`.
2. Never push directly to `master`. Always use a branch and PR.
3. Production paths require explicit user approval before merge or auto-merge. Paths containing `production` are production unless repo instructions say otherwise.
4. Non-production rollbacks may be merged or auto-merged only when the PR is approved by repo automation or a human and required checks pass.
5. Distinguish later unrelated commits in the same file. Roll back only the image tag changes introduced by the bad-tag commits.
6. If the candidate commits are not image-tag-only, or the batch crosses environments unexpectedly, stop and explain the risk before editing.

## Workflow

### 1. Normalize Inputs

Extract the bad tag from the user prompt. Prefer a hexadecimal-looking token or exact image tag; preserve non-hex tags if the user gives one explicitly.

```bash
BAD_TAG="<user-provided-tag-lowercase>"
REPO="<discovered-applications-infra-path>"
```

Ask a follow-up only when no plausible tag is present or the repo cannot be found.

### 2. Refresh and Inspect

```bash
cd "$REPO"
git status --short
git fetch origin master
```

If the worktree is dirty, do not overwrite user changes. Either continue only if the changes are unrelated or ask how to proceed. Once the worktree is safe, create a branch from the latest `origin/master`:

```bash
git switch -c "rollback/revert-<env-or-scope>-${BAD_TAG}" origin/master
```

Read the applicable repository guidance using the host's file-reading capability. Check the instruction files and contribution docs that exist in the repository rather than assuming a single filename.

In `applications-infra`, commit titles and PR titles use cluster prefixes such as `[dev-01]`, `[prod-01]`, or `[prod-us-01]`.

### 3. Find Current Bad-Tag Occurrences

Search current files first, prioritizing Helm values files:

```bash
rg -n --fixed-strings "$BAD_TAG" --glob '**/values.yaml'
rg -n "tag:[[:space:]]*['\"]?${BAD_TAG}['\"]?" --glob '**/values.yaml'
```

Record every path, YAML key context, repository image, and line number. If the tag appears outside `values.yaml`, inspect it but do not include it in the rollback unless it is clearly part of the same image deployment.

### 4. Identify the Introducing Commits

Use diff evidence, not commit messages alone.

Useful commands:

```bash
git log --all --date=iso --format='%H%x09%ad%x09%s' -G "tag:[[:space:]]*['\"]?${BAD_TAG}['\"]?" -- '**/values.yaml'
git log --all --date=iso --format='%H%x09%ad%x09%s' -S "$BAD_TAG" -- '**/values.yaml'
git show --unified=0 --find-renames <commit> -- <path>
```

A commit is a rollback candidate only when its diff adds the bad tag to an image tag field and removes a previous tag from the same field or image block.

For each candidate, capture:

- commit SHA and title
- commit timestamp
- changed path
- image repository or service key
- previous tag from the removed line or parent file
- bad tag from the added line

Prefer the commits that still explain the current bad-tag occurrences on `origin/master`. Ignore historical occurrences that were already superseded unless the user explicitly asks for a historical investigation.

### 5. Verify the Deployment Batch

Before editing, confirm the candidate commits form a plausible rollback batch:

- same cluster or explicitly intended cluster set
- close timestamp window, unless the user explains otherwise
- image-tag-only changes in `values.yaml`
- related services or a clear deployment group
- no cross-environment copy-paste mismatch
- no production path hidden among development paths

Inspect each candidate:

```bash
git diff --name-only <commit>^ <commit>
git show --stat --oneline <commit>
git show --unified=0 <commit> -- <path>
```

If one commit updates multiple image tags, include only if all updates are part of the bad deployment batch. If a file contains later unrelated changes, keep those later changes.

Be especially careful with files that contain multiple image blocks. A later commit in the same `values.yaml` may change a different image key and must be preserved.

### 6. Restore Previous Tags

When every candidate commit is image-tag-only, prefer a no-commit revert because it preserves later unrelated changes outside the reverted hunks:

```bash
git revert --no-commit <candidate-commits-newest-first>
```

If `git revert` conflicts, wants to change unrelated lines, or cannot apply cleanly, abort and manually restore only the affected tag lines:

```bash
git revert --abort
git show <commit>^:<path>
```

Manual restoration must preserve the current file's unrelated content. Only replace the bad tag in the exact image block introduced by the candidate commit. Do not globally replace the tag across the repository unless every occurrence was verified as part of the same rollback batch.

### 7. Validate Locally

Inspect the diff first:

```bash
git diff --stat
git diff --check
git diff -- <touched-files>
```

Confirm the bad tag is gone from the affected scope:

```bash
rg -n --fixed-strings "$BAD_TAG" <affected-cluster-or-group-path>
```

If remaining occurrences are intentionally out of scope, record why.

Parse touched YAML files when Ruby is available:

```bash
ruby -ryaml -e 'ARGV.each { |f| YAML.load_file(f); puts "ok #{f}" }' <touched-yaml-files>
```

If the repo has validation commands, run the narrowest relevant ones. In `applications-infra`, GitHub CI runs yamllint for changed non-template YAML files using `.github/yamllint-config.yaml`; local YAML parsing plus PR checks are usually the practical baseline unless yamllint is installed.

### 8. Commit, Push, and Open PR

Infer the environment prefix from touched paths. For `applications-infra`:

```text
aws-eu-west-development-01/ -> [dev-01]
aws-eu-west-production-01/  -> [prod-01]
aws-us-east-production-01/  -> [prod-us-01]
```

Use a branch name like:

```text
rollback/revert-<env>-<scope>-${BAD_TAG}
```

Use a commit and PR title like:

```text
[dev-01] Revert <scope> image tags from <bad-tag>
```

The PR body must include:

- bad tag
- commits found and why they were included
- mapping of each restored image tag, for example `<path>: <bad-tag> -> <previous-tag>`
- validation commands and results
- explicit production status: non-production, production, or mixed
- merge plan: auto-merge, manual merge after approval, or stop for user approval

Create the PR against `master`:

```bash
git push -u origin HEAD
gh pr create --base master --head "$(git branch --show-current)" --title "<title>" --body-file <body-file>
```

### 9. Merge Decision

After opening the PR, use an available GitHub capability to inspect checks, reviews, draft state, and mergeability. With GitHub CLI:

```bash
gh pr checks <pr-url> --watch
gh pr view <pr-url> --json reviewDecision,mergeStateStatus,isDraft,url
```

For non-production only: merge or enable auto-merge when checks pass and the repo's approval/automation state is acceptable.

For production or mixed production/non-production: stop after the PR is ready and ask the user for explicit approval before merge or auto-merge. Include the exact production paths in the message.

## Final Response

Report:

- normalized bad tag
- commits found
- files changed and old tag -> restored tag mappings
- validation performed
- PR URL
- merge or auto-merge status, including whether production approval is still required

If anything was intentionally left out of scope, say so clearly.
