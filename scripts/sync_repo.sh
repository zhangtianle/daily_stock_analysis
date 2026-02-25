#!/usr/bin/env bash
set -euo pipefail

# Sync current branch with a target upstream branch and detect merge conflict markers.
# Usage:
#   scripts/sync_repo.sh origin main
#   scripts/sync_repo.sh upstream main

REMOTE="${1:-origin}"
TARGET_BRANCH="${2:-main}"

if ! git remote get-url "${REMOTE}" >/dev/null 2>&1; then
  echo "[ERROR] Remote '${REMOTE}' is not configured."
  exit 1
fi

echo "[INFO] Fetching ${REMOTE}/${TARGET_BRANCH} ..."
git fetch "${REMOTE}" "${TARGET_BRANCH}" --prune

echo "[INFO] Rebasing current branch onto ${REMOTE}/${TARGET_BRANCH} ..."
git rebase "${REMOTE}/${TARGET_BRANCH}"

echo "[INFO] Scanning for unresolved conflict markers ..."
if rg -n "^<<<<<<< |^>>>>>>> |^=======$" --glob '!*.md' >/dev/null; then
  echo "[ERROR] Unresolved merge conflict markers found."
  rg -n "^<<<<<<< |^>>>>>>> |^=======$" --glob '!*.md' || true
  exit 2
fi

echo "[OK] Sync completed and no unresolved conflict markers detected."
