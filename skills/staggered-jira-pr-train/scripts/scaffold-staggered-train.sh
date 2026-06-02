#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  scaffold-staggered-train.sh JIRA_KEY SHORT_SLUG layer-slug...

Example:
  scaffold-staggered-train.sh PROJ-123 checkout-timeouts mechanical-refactor behavior tests-docs

Creates:
  feature/PROJ-123-checkout-timeouts
  train/PROJ-123/01-mechanical-refactor
  train/PROJ-123/02-behavior
  train/PROJ-123/03-tests-docs

The script only scaffolds and pushes branches. Implement and commit each layer before opening PRs.
USAGE
}

if [[ $# -lt 3 ]]; then
  usage
  exit 2
fi

KEY="$1"
SLUG="$2"
shift 2
LAYERS=("$@")

if ! command -v git >/dev/null 2>&1; then
  echo "git is required" >&2
  exit 1
fi

DEFAULT_BRANCH=""
if command -v gh >/dev/null 2>&1; then
  DEFAULT_BRANCH="$(gh repo view --json defaultBranchRef -q .defaultBranchRef.name 2>/dev/null || true)"
fi

if [[ -z "$DEFAULT_BRANCH" ]]; then
  DEFAULT_BRANCH="$(git remote show origin | sed -n '/HEAD branch/s/.*: //p')"
fi

if [[ -z "$DEFAULT_BRANCH" ]]; then
  echo "Could not determine default branch. Set it manually and rerun from a clean repo." >&2
  exit 1
fi

HANDOFF="feature/${KEY}-${SLUG}"

git fetch origin

git switch -c "$HANDOFF" "origin/${DEFAULT_BRANCH}"
git push -u origin "$HANDOFF"

PREV="$HANDOFF"
INDEX=1

echo
echo "Created handoff branch:"
echo "  $HANDOFF"
echo
echo "Creating train branches:"

for LAYER in "${LAYERS[@]}"; do
  NUM="$(printf "%02d" "$INDEX")"
  BRANCH="train/${KEY}/${NUM}-${LAYER}"

  git switch -c "$BRANCH" "$PREV"
  git push -u origin "$BRANCH"

  echo "  $BRANCH -> $PREV"

  PREV="$BRANCH"
  INDEX=$((INDEX + 1))
done

cat <<EOF

Next:
1. Implement and commit each layer on its own branch.
2. Open draft PRs bottom-up:
   - train/.../01-* -> $HANDOFF
   - train/.../02-* -> train/.../01-*
   - train/.../03-* -> train/.../02-*
3. Merge bottom-up into $HANDOFF.
EOF
