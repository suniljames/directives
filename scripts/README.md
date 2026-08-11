# Scripts (maintainer-facing)

Automation for maintaining this repo — nothing here is part of adopting the system. Adopters can skip this directory entirely.

- [`directives-audit.sh`](directives-audit.sh) → [`directives_audit.py`](directives_audit.py): a scheduled audit that scans the project repos listed in [`projects.yml`](../projects.yml) for two things: **promotion candidates** (generic assets worth moving upstream — a vocabulary disqualifier list in `projects.yml` gates auto-promotion) and **drift** (stale references to renamed files). Results append to a rolling monthly issue labeled `automation-log`; promoted slash commands land in [`templates/commands/`](../templates/commands/README.md).
- Modes: `--weekly` (full), `--drift-only` (daily), `--dry-run` (local testing). Requires `python3` + PyYAML + an authenticated `gh` CLI with triage permission on this repo.

---
[← Back to README](../README.md)
