#!/bin/bash
# directives-audit.sh — thin wrapper around directives_audit.py.
#
# Called from launchd plists (see suniljames/dotfiles/launchd/). Keeps the
# shell surface simple so the plist doesn't need to hunt for python3.
#
# Modes:
#   --weekly      Full audit: promotion candidates + drift + draft PRs
#   --drift-only  Lightweight: only check for broken refs and stale names
#   --dry-run     Don't post issue comments or open PRs (for local testing)
#
# Relies on PATH containing python3 (homebrew or system). The launchd plist
# sets PATH explicitly; interactive use picks up shell PATH.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

exec python3 "$SCRIPT_DIR/directives_audit.py" --repo-root "$REPO_ROOT" "$@"
