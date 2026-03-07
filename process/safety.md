# Safety & Guardrails

Universal rules for all developers and agents across all projects.

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
2. If stashing, use `git stash push -m "descriptive message"`
3. Never drop a stash after failed pop
4. Verify restoration after switching back

## Data Verification

- **Never report data loss without full verification.**
- Dashboard counts != database counts (dashboards show filtered views).
- Express uncertainty first: "Let me verify further before drawing conclusions."

## Project-Specific Addenda

Individual projects may add domain-specific safety rules (e.g., PHI handling for healthcare, PCI for fintech). See each project's safety documentation.

Domain overlays in this playbook:
- [`overlays/healthcare/safety-addendum.md`](../overlays/healthcare/safety-addendum.md) — HIPAA, PHI, patient data
