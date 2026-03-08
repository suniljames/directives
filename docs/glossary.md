# Glossary

Quick reference for every term used in this repo.

| Term | Definition | Why it matters |
|------|-----------|----------------|
| **Agent type** | An abstract role describing *what kind* of work gets done — not which AI model does it. Currently two: builder and validator. | Lets you swap AI providers without rewriting your process. |
| **Builder** | The agent type that creates work: writes code, runs tests, deploys. | Keeps creation and review separate. |
| **Committee** | All of a team's **personas** reviewing work in sequence, each reading prior feedback first. | Produces multi-perspective review that no single reviewer can match. |
| **Fresh-eyes validation** | A zero-context sub-agent reads only the final spec and flags gaps. Catches assumptions the committee forgot to write down. | Ensures specs are self-contained for whoever implements them. |
| **Manifest** | A YAML file (`manifest.yml`) that defines a team's roles, pipeline stages, and vocabularies. Single source of truth. | Change one file, update everywhere. No drift between docs and config. |
| **Overlay** | Optional domain-specific rules (e.g., healthcare, fintech) layered on top of the base process. Additive, never replacing. | Keeps domain compliance separate from team fundamentals. |
| **Overwrite-to-consensus** | After committee deliberation, members whose positions changed edit their original comments to show final positions. | Readers see clean conclusions, not debate threads. |
| **Persona** | A detailed character profile — title, backstory, expertise, review lens — that shapes how an AI agent thinks about a specific kind of work. | Produces deep, targeted feedback instead of shallow, generic observations. |
| **Pipeline** | A multi-stage workflow (e.g., define → design → implement → review → deploy → summarize). Each stage produces artifacts the next consumes. | Prevents skipping steps. Tracks progress with labels. |
| **Pipeline mode** | How much human involvement a project requires. **Autonomous**: no human gates. **Gated**: pauses for human approval at key stages. | Lets you tune the system from fully automated to human-in-the-loop. |
| **Severity level** | A tag on review findings. **MUST-FIX**: blocks merge. **SHOULD-FIX**: blocks current round. **NIT**: suggestion only. | Shared vocabulary prevents disagreements about what's blocking. |
| **Three-tier model** | Configuration lives at three levels: Tier 1 (this repo — shared practices), Tier 2 (organization — optional), Tier 3 (project — tech stack and environment). | Prevents duplication. Each tier adds specificity without repeating the tier above. |
| **Validator** | The agent type that reviews work: audits code, writes specs, files issues. | Independent review catches blind spots the builder can't see. |

---

[Back to README](../README.md) | [Key Concepts](concepts.md) | [FAQ](faq.md)
