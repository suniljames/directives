# Safety & Guardrails

Universal rules for all developers and AI agents, across all projects. These are non-negotiable — they apply regardless of team, pipeline mode, or domain.

Safety runs at two layers, and a reader must know which rule survives a bypass flag:

1. **Hook-enforced** — hard blocks the harness applies before a tool runs (example: Claude Code `PreToolUse` hooks). These cannot be bypassed, even with a permissions-skip flag.
2. **Behavioral** — soft guardrails the agent follows (this file).

**Promote a prose rule to a hook when it keeps being tested.** A behavioral rule that an agent has violated (or nearly violated) twice is a hook candidate — the prose version has demonstrated it does not hold under pressure. Keep the prose version too; the hook enforces, the prose explains.

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
3. Never drop a stash after failed pop — it is your only copy
4. Verify restoration (`git status` + `git stash list`) before declaring success

## Destructive Code Paths

Designing a delete/rewrite/disable-protection path that must exist? Follow [`data-safety.md`](data-safety.md): enumerate reverse references, allow-list what may go, fence before the deletes, restore captured protection state.

## Third-Party Hooks and Permission Settings

Before wiring a third-party tool as an agent hook (example: Claude Code hooks):

- **The compound risk:** a permissions-skip setting removes the confirmation gate for destructive operations; adding a third-party hook on top means both layers trust each other without independent verification.
- Read the hook source before installing — especially tools that intercept shell output.
- Verify provenance: pinned version + checksum, ideally a published release on a known registry.
- Make hooks fail-open (`exec hook-binary || exit 0`) so a crashed hook doesn't block the agent.
- Know the scope: a post-tool hook on the shell receives output from **every** command in the session — including ones that surface environment variables, API responses, and file contents.
- Document the tradeoff in your project's safety doc: what you gave up and why.

## Data Verification

- **Never report data loss without full verification.**
- Dashboard counts != database counts (dashboards show filtered views).
- Express uncertainty: *"Let me verify further before concluding."*

## Project-Specific Addenda

Projects may add domain-specific safety rules (PHI handling, PCI compliance, etc.). See each project's safety documentation.

Domain overlays in this repo:
- [`overlays/healthcare/safety-addendum.md`](../overlays/healthcare/safety-addendum.md) — HIPAA, PHI, patient data
