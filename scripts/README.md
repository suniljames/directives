# Scripts (maintainer-facing)

Automation for maintaining this repo — nothing here is part of adopting the system. Adopters can skip this directory entirely.

- [`directives-audit.sh`](directives-audit.sh) → [`directives_audit.py`](directives_audit.py): a scheduled audit that scans the project repos listed in [`projects.yml`](../projects.yml) for two things: **promotion candidates** (generic assets worth moving upstream — a vocabulary disqualifier list in `projects.yml` gates auto-promotion) and **drift** (stale references to renamed files). Results append to a rolling monthly issue labeled `automation-log`; promoted slash commands land in [`templates/commands/`](../templates/commands/README.md).
- [`check-personal-directives.py`](check-personal-directives.py): consistency checks for [`AI.md`](../AI.md) and [`people/`](../people/README.md). Dependency-free, exits non-zero on failure, and meant to be run before any commit that touches those files. Catches revision/receipt drift, a paste block that bans words the full version allows, em dashes, and vendor names in files that must stay neutral. Invoked automatically by the [`pre-commit` hook](../hooks/README.md); `--root` points it at a tree other than this one, which is how the hook checks the index instead of the working tree.
- Modes: `--weekly` (full), `--drift-only` (daily), `--dry-run` (local testing). Requires `python3` + PyYAML + an authenticated `gh` CLI with triage permission on this repo.

---
[← Back to README](../README.md)
