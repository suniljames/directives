# AGENTS.md

Instructions for any coding agent working in this repo, whichever tool you are.

**This repo's agent configuration lives in [`CLAUDE.md`](CLAUDE.md).** The filename names one tool; the contents are tool-agnostic. Read it first.

**One rule is worth repeating here,** because it is the one whose failure ships straight to a human's daily workflow:

> Editing [`AI.md`](AI.md) or anything under [`people/`](people/README.md)? Follow the checklist in [`people/README.md`](people/README.md) and run `python3 scripts/check-personal-directives.py` before committing.

A `pre-commit` hook enforces this, but git never installs hooks automatically: in a fresh clone, run `git config core.hooksPath hooks` first, and treat an unset `core.hooksPath` as the checker not running at all.

Those files are live instructions that assistant accounts read every day. A change that leaves the revision date stale, or a rule updated in one copy and not the other, is not caught by review. It is caught by the checker, or not at all.

---
[← Back to README](README.md)
