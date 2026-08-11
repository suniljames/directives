# Glossary

Every term this repo uses, in two tiers: the core vocabulary first, then the process-engineering terms you'll meet in `framework/` and `teams/`.

## Core terms — start here

| Term | Definition | Why it matters |
|------|-----------|----------------|
| **Agent type** | An abstract role describing *what kind* of work gets done — not which AI model does it. Currently two: builder and validator. | Lets you swap AI providers without rewriting your process. |
| **Builder** | The agent type that creates work — produces deliverables, verifies quality, publishes results. | Keeps creation and review separate. |
| **Validator** | The agent type that reviews work — audits deliverables, checks quality, flags issues. | Independent review catches blind spots the builder can't see. |
| **Persona** | A detailed character profile — title, backstory, expertise, review lens — that shapes how an AI agent thinks about a specific kind of work. | Produces deep, targeted feedback instead of shallow, generic observations. |
| **Committee** | All of a team's personas reviewing work in sequence, each reading prior feedback first. | Produces multi-perspective review that no single reviewer can match. |
| **Pipeline** | A multi-stage workflow (define → design → implement → review → deploy → summarize). Each stage produces artifacts the next consumes. | Your AI warns before a step gets skipped; labels track progress. |
| **Slash command** | A saved prompt file your AI tool runs by name (`/define 42` loads `define.md`). One per pipeline stage — [starters included](commands.md). | The pipeline's stages become one-word actions. |
| **Manifest** | The config file (`manifest.yml`) defining a team's roles, pipeline stages, and vocabularies. Single source of truth. | Change one file, update everywhere. No drift between docs and config. |
| **PRD** | Product Requirements Document — what `/define` produces: the problem, who it affects, success criteria, and scope. | Work starts from agreed requirements, not a vague prompt. |
| **Artifact** | Anything a pipeline stage produces for the next stage to consume — a PRD comment, a test spec, a review verdict. | Handoffs happen through visible, inspectable outputs, never side channels. |
| **Provider** | The AI tool that backs an agent type (Claude Code, Antigravity CLI, …). Defined in `agents.yml`. | Roles are stable; the AI behind them is swappable. |
| **Orchestrator** | Any tool that reads the config files and routes work between agents — or you, doing it by hand. | The system works with or without automation on top. |

## Process-engineering terms

| Term | Definition | Why it matters |
|------|-----------|----------------|
| **Acceptance walkthrough** | The close gate: one evidence row per acceptance criterion (a link to proof plus how that proof could fail), with a computed verdict. | Work is declared done against outcomes, not against the code having been written. |
| **Ad-hoc work gate** | The warning shown when you start work on an issue whose earlier pipeline stages never ran. Confirm to proceed; a note lands in the PR. | Skipping stages becomes a conscious choice, not an accident. |
| **Authorization moment** | The explicit decision that ends Design: value and cost rendered together, then authorize/defer/discuss. | Build spend is a decision someone made, never a silent slide into implementation. |
| **Comment guard** | The duplicate-prevention check on an automated comment: filtered by author, with named semantics (skip / confirm-overwrite / supersede). | A heading-only guard can be faked or can suppress a needed re-post; a gate's verdict must be correctable. |
| **Drain hook** | A backfill keyed on missing state, running before the work it gates, so it retires itself as the backlog drains. | Fixes a gap everywhere without a migration or a rule that outlives its purpose. |
| **Falsifier** | The `*Goes red if …*` line required on every acceptance criterion. | A statement with no stated way to fail is a wish, and will be checked off forever. |
| **Force-red** | Proving a test or check can fail: reintroduce the fault, watch it go red, restore, watch it go green. | A check verified only in the green direction is unverified. |
| **Fresh-eyes validation** | A zero-context session reads only the final spec and flags gaps. Catches assumptions the committee forgot to write down. | Specs stay self-contained for whoever implements them. |
| **Overlay** | Optional domain-specific rules (e.g., healthcare) layered on top of the base process. Additive, never replacing. | Keeps domain compliance separate from team fundamentals. |
| **Overwrite-to-consensus** | After committee deliberation, members whose positions changed edit their original comments to show final positions. | Readers see clean conclusions, not debate threads. |
| **Per-stage override** | An optional `stages` map on a manifest role that changes the role's agent type for specific pipeline stages (resolution: the stage entry wins, else the role's default). | Builder roles can act as validators during review without changing their default assignment. |
| **Pipeline mode** | How much human involvement a project requires. **Autonomous**: no human gates. **Gated**: pauses for human approval at key stages. | Tune from fully automated to human-in-the-loop. |
| **Severity level** | A tag on review findings. **MUST-FIX**: blocks integration. **SHOULD-FIX**: blocks the current round. **NIT**: does not block (but still gets fixed). | Shared vocabulary prevents disagreements about what's blocking. |
| **Three-tier model** | Configuration lives at three levels: Tier 1 (this repo — shared practices), Tier 2 (organization — optional), Tier 3 (project — tech stack and environment). | Each tier adds specificity without repeating the tier above. |
| **Unfireable control** | A check that structurally cannot fail — a gate on a label nothing sets, a matcher no real artifact satisfies, a skip condition that is always true. | Reads as coverage while checking nothing; every control must demonstrate it can go RED. |

Compliance and tooling acronyms are expanded where they appear (PHI, BAA, RLS in the [healthcare overlay](../overlays/healthcare/README.md); MCP in the [credentials template](../templates/credentials.md.template)).

---

[Back to README](../README.md) | [Docs index](README.md) | [Key Concepts](concepts.md) | [FAQ](faq.md)
