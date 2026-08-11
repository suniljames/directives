# Glossary

Quick reference for every term used in this repo.

| Term | Definition | Why it matters |
|------|-----------|----------------|
| **Acceptance walkthrough** | The close gate: one evidence row per acceptance criterion (permalink + how the evidence would go red), with a computed verdict. | Work is declared done against outcomes, not against the diff having been applied. |
| **Agent type** | An abstract role describing *what kind* of work gets done — not which AI model does it. Currently two: builder and validator. | Lets you swap AI providers without rewriting your process. |
| **Authorization moment** | The explicit operator decision that ends Design: value and cost rendered together, then authorize/defer/discuss. | Build spend is a decision someone made, never a silent slide into implementation. |
| **Builder** | The agent type that creates work — produces deliverables, verifies quality, publishes results. | Keeps creation and review separate. |
| **Comment guard** | The idempotency check on an automated comment: author-filtered, with named semantics (skip / confirm-overwrite / supersede). | A heading-only guard is spoofable and suppressible; a gate's verdict must be correctable. |
| **Drain hook** | A backfill keyed on missing state, running before the work it gates, so it self-extinguishes as the backlog drains. | Fixes a gap everywhere without a migration or a rule that outlives its purpose. |
| **Falsifier** | The `*Goes red if …*` line required on every acceptance criterion. | A statement with no stated way to fail is a wish, and will be walked through as ✅ forever. |
| **Force-red** | Proving a test/control can fail: reintroduce the fault, watch it go red, restore, watch it go green. | A check verified only in the green direction is unverified. |
| **Committee** | All of a team's **personas** reviewing work in sequence, each reading prior feedback first. | Produces multi-perspective review that no single reviewer can match. |
| **Fresh-eyes validation** | A zero-context sub-agent reads only the final spec and flags gaps. Catches assumptions the committee forgot to write down. | Ensures specs are self-contained for whoever implements them. |
| **Manifest** | A YAML file (`manifest.yml`) that defines a team's roles, pipeline stages, and vocabularies. Single source of truth. | Change one file, update everywhere. No drift between docs and config. |
| **Overlay** | Optional domain-specific rules (e.g., healthcare, fintech) layered on top of the base process. Additive, never replacing. | Keeps domain compliance separate from team fundamentals. |
| **Overwrite-to-consensus** | After committee deliberation, members whose positions changed edit their original comments to show final positions. | Readers see clean conclusions, not debate threads. |
| **Persona** | A detailed character profile — title, backstory, expertise, review lens — that shapes how an AI agent thinks about a specific kind of work. | Produces deep, targeted feedback instead of shallow, generic observations. |
| **Pipeline** | A multi-stage workflow (e.g., define → design → implement → review → deploy → summarize). Each stage produces artifacts the next consumes. | Prevents skipping steps. Tracks progress with labels. |
| **Per-stage override** | An optional `stages` map on a manifest role that overrides the role's default agent type for specific pipeline stages. Resolution: `role.stages[stage] \|\| role.agent`. | Lets builder roles act as validators during review without changing their default assignment. |
| **Pipeline mode** | How much human involvement a project requires. **Autonomous**: no human gates. **Gated**: pauses for human approval at key stages. | Lets you tune the system from fully automated to human-in-the-loop. |
| **Severity level** | A tag on review findings. **MUST-FIX**: blocks integration. **SHOULD-FIX**: blocks current round. **NIT**: suggestion only. | Shared vocabulary prevents disagreements about what's blocking. |
| **Three-tier model** | Configuration lives at three levels: Tier 1 (this repo — shared practices), Tier 2 (organization — optional), Tier 3 (project — tech stack and environment). | Prevents duplication. Each tier adds specificity without repeating the tier above. |
| **Unfireable control** | A check that structurally cannot fail — a gate on a label nothing sets, a matcher no real artifact satisfies, a skip predicate that is always true. | Reads as coverage while checking nothing; every control must demonstrate it can go RED. |
| **Validator** | The agent type that reviews work — audits deliverables, checks quality, flags issues. | Independent review catches blind spots the builder can't see. |

---

[Back to README](../README.md) | [Key Concepts](concepts.md) | [FAQ](faq.md)
