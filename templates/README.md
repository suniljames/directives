# Templates

Starter files you copy **into your own project** (they don't run here). Each file's opening comment says where it goes and who fills it in.

| Template | Copy to | You need it when |
|---|---|---|
| [`CONTRIBUTING.md.template`](CONTRIBUTING.md.template) | `CONTRIBUTING.md` | Always (Standard path and up) — declares your team and pipeline mode. |
| [`CLAUDE.md.template`](CLAUDE.md.template) | `CLAUDE.md` | Your builder runs on Claude Code. |
| [`GEMINI.md.template`](GEMINI.md.template) | `GEMINI.md` | You run a second provider as validator (Full System path). Full reference version: [`providers/antigravity/`](../providers/antigravity/README.md). |
| [`commands/`](commands/README.md) | `.claude/commands/` (or your tool's equivalent) | Standard path — the five pipeline slash commands, ready to use. |
| [`pm-context.md.template`](pm-context.md.template) | `docs/developer/pm-context.md` | You use `/define` — gives the PM persona your product's domain knowledge. **A founder can fill this in personally.** |
| [`stakeholder-context.md.template`](stakeholder-context.md.template) | `docs/developer/stakeholder-context.md` | Non-engineers interact with your agents. **Also founder-fillable.** |
| [`credentials.md.template`](credentials.md.template) | `docs/developer/CREDENTIALS.md` | Agents need programmatic access to your services. |
| [`worklog.md.template`](worklog.md.template) | `WORKLOG.md` | Multiple agents hand work off across sessions. |

---
[← Back to README](../README.md)
