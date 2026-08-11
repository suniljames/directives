# Contributing to Directives

This repo is maintained by [@suniljames](https://github.com/suniljames) and evolves from production use of the system it describes. Content is licensed [CC BY 4.0](LICENSE) — fork and adapt freely, with attribution.

## Proposing changes

- **Questions and ideas:** open a GitHub issue.
- **Fixes and improvements:** open a PR. Docs here are process code for the agents that read them — hold your change to [`framework/prompt-quality.md`](framework/prompt-quality.md) (single source of truth, the no-op sentence test, checkable steps).
- Keep content **generic**: no project-specific vocabulary, no technology names in persona files (see [`CLAUDE.md`](CLAUDE.md) for the repo's own rules).

## What the automation does

A scheduled audit (see [`scripts/`](scripts/README.md)) scans downstream project repos for generic assets worth promoting upstream and for drift against this repo, logging to a rolling monthly issue labeled `automation-log`. Those issues are machine-generated — don't file work items in them.
