# Directives Repo — Claude Code Config

This is a documentation repo. There is no application code, no tests, no build system (the only code is the maintainer audit script under `scripts/`).

## Map

- Start at [`README.md`](README.md) — it indexes everything.
- Agent roles/providers: [`agents.yml`](agents.yml) · cross-team rules: [`framework/`](framework/README.md) · team rosters/process: [`teams/`](teams/README.md) · starter files: [`templates/`](templates/README.md).
- Editing any file here? Apply [`framework/prompt-quality.md`](framework/prompt-quality.md) — these docs are process code for the agents that read them.

## Rules

- Follow the GitHub identity rules in any project that references these directives.
- Do not add project-specific content. This repo is generic by design.
- Persona files must not reference specific technologies (FastAPI, Next.js, etc.) — those belong in project repos.
- Process docs describe frameworks and philosophies, not tool-specific instructions.
