# Safety & Guardrails

Universal rules for all developers and AI agents, across all projects. These are non-negotiable — they apply regardless of team, pipeline mode, or domain.

## Behavioral Rules

- **Never delete** repositories, services, or databases
- **Never** `rm -rf` on broad paths (`/`, `~`, `.`, `/Users`, etc.)
- **Never** `git push --force` (use `--force-with-lease` if necessary)
- **Never** `git reset --hard`, `git clean -f`, `git branch -D main`
- **Never** `DROP DATABASE`, `DROP TABLE`, `TRUNCATE TABLE`
- **Never** pipe remote content to shell (`curl | bash`)
- **Never** `chmod 777`, `pkill -9`, `killall -9`
- **Never** commit secrets (.env files, API keys, credentials)
- **Stop and ask** if a destructive action seems genuinely necessary

## Safe Branch-Switching

1. Prefer `git worktree` over stash
2. If stashing: `git stash push -m "descriptive message"`
3. Never drop a stash after failed pop
4. Verify restoration after switching back

## Data Verification

- **Never report data loss without full verification.**
- Dashboard counts != database counts (dashboards show filtered views).
- Express uncertainty: *"Let me verify further before concluding."*

## Project-Specific Addenda

Projects may add domain-specific safety rules (PHI handling, PCI compliance, etc.). See each project's safety documentation.

Domain overlays in this repo:
- [`overlays/healthcare/safety-addendum.md`](../overlays/healthcare/safety-addendum.md) — HIPAA, PHI, patient data
