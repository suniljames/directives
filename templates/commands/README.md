# templates/commands

Landing zone for slash-command files promoted from project repos by `scripts/directives-audit.sh` (see `projects.yml` → `shared_targets`).

- A command lands here only after project-specific vocabulary is stripped (the audit script's disqualifier list gates auto-promotion).
- Projects consume these by copying into their own `.claude/commands/` and re-adding project specifics there — link back here in a comment so drift is traceable.

Currently empty: promoted commands have so far been rejected by the vocabulary gate. That is the gate working, not a bug.
