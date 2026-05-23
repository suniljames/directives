# Multi-Agent Architecture

> **Canonical config:** [`agents.yml`](../agents.yml) — agent types, providers, assignments.
> **Role roster:** [`teams/engineering/manifest.yml`](../teams/engineering/manifest.yml)

One AI model acting as both [builder and validator](../docs/glossary.md) creates correlated failures — shared blind spots and no independent verification. The model that builds should not validate.

## Principle

Split roles across abstract **agent types** — a **builder** and a **validator** — backed by different LLM providers when available. Different models with different training and biases catch different things; the overlap in what they miss shrinks significantly. Types and assignments: [`agents.yml`](../agents.yml). Role mappings: [`manifest.yml`](../teams/engineering/manifest.yml).

## Agent Types

| Type | Purpose | Capabilities |
|------|---------|-------------|
| **Builder** | Creates work — implements, produces, publishes | create_deliverables, verify_quality, publish, integrate |
| **Validator** | Reviews work — audits, checks quality, flags issues | review_work, write_specifications, file_findings |

## Provider Assignment

Default assignments and fallback chains are in `agents.yml`. When the preferred provider is unavailable, the system falls back to the next provider in the chain. **"Unavailable" includes rate-limiting (HTTP 429) and credit/quota exhaustion — not just a missing binary.** This is the common trigger in practice: a provider that is installed and working can still be temporarily unusable.

### Role Swap on Provider Unavailability

The default assignment (builder ↔ validator → provider) is a *preference*, not a fixed identity. The roles are **bidirectional**: either provider can play either role, and the mapping swaps when a provider becomes unavailable.

- **Default (Scenario 1):** Claude Code = builder, Gemini = validator.
- **Swapped (Scenario 2):** Gemini = builder, Claude Code = validator — e.g. when Claude is out of credits, or when the operator simply launches a Gemini session to build.

The operative rule for whichever tool is running: **if your counterpart provider is rate-limited or out of credits, assume the open role.** A builder with no available validator runs the validator pass itself (in an isolated session, below); a tool launched to build when the usual builder is unavailable *is* the builder. Neither role goes unfilled because one provider is down.

In practice the launched CLI determines the builder: start Gemini and Gemini builds; start Claude Code and Claude builds. The validator is then the *other* provider, invoked as a bridge (see model designation in [`agents.yml`](../agents.yml)) — or, if that provider is also unavailable, the same provider in a fresh isolated session.

### Single-Provider Fallback

When only one provider is available, it runs both agent types in **isolated sessions**:

1. **Session isolation** — Validator runs in a separate session with no shared builder context.
2. **Mandatory fresh-eyes validation** — Required (not optional) in single-provider mode.
3. **Explicit role priming** — Validator prompt: *"You are the validator agent. You did NOT create this work. Review it independently."*

This is less effective than two different models but significantly better than one session doing both. The key is that the validator has no memory of the builder's reasoning — it can't inherit assumptions it never saw.

## Create-then-Review Flow

```
Builder creates → Validator reviews → Builder addresses feedback
```

The pattern is the same regardless of team. Here's the engineering example:

1. **PM (validator)** writes requirements and acceptance criteria
2. **EM (builder)** plans work, assigns tasks, oversees execution
3. **Engineer, Architect, Data, AI/ML, UX (builder)** implement the feature
4. **QA Engineer (validator)** tests against requirements
5. **Security Engineer (validator)** audits for vulnerabilities
6. **SRE (builder)** deploys and monitors
7. **Writer (validator)** documents the feature

A sales team would follow the same structure: Deal Strategist (builder) creates the proposal → Pricing Analyst and Legal Reviewer (validators) audit it → Deal Strategist addresses findings.

## Coordination Protocol

- **Structured artifacts** — PRDs, test reports, review comments follow defined formats
- **File-based exchange** — Both agents read/write to the repo. The repo is the source of truth.
- **Explicit acceptance criteria** — PM defines "done." QA verifies "done."
- **Label-driven coordination** — Agents check issue labels to determine pipeline stage
- **PR labels** — Autonomous PRs labeled `ai:autonomous`
- **Review findings** — Posted with [severity levels](../docs/glossary.md) (see the team's review framework in its manifest directory)

## Guiding Principles

1. **Builders need tooling.** Roles that create, produce, and publish belong on the builder.
2. **Validators should be independent.** Audit and review roles gain most from a different model.
3. **Keep the boundary clean.** Creating on one agent, reviewing on the other. Explicit handoffs.
4. **Rationale must be substantive.** Assignments based on capability and fit, not marketing.

---

## Native Session Specialists (`.claude/agents/`)

Claude Code supports a first-class sub-agent mechanism via YAML files in `.claude/agents/`. These are **session specialists** — agents scoped to a domain within a provider session. They are distinct from the provider-level builder/validator split described above.

### Terminology

| Concept | Where defined | What it controls |
|---------|--------------|-----------------|
| **Provider agents** | `agents.yml` | Which LLM provider backs each agent type (builder/validator) |
| **Session specialists** | `.claude/agents/*.md` | What a sub-agent focuses on *within* a Claude Code session |

Provider agents answer "which tool does the work." Session specialists answer "which domain does this sub-agent stay inside." Both layers are independent and composable.

### YAML Front-Matter Schema

Each file in `.claude/agents/` uses YAML front matter followed by the agent's system prompt:

```yaml
---
name: django-specialist
description: >
  Expert in Django ORM, migrations, admin customization, and URL routing.
  Invoke for any task touching models, views, serializers, or admin.py.
tools:
  - Read
  - Edit
  - Bash
  - Grep
---

You are a Django specialist. [system prompt body follows]
```

Required fields:
- `name` — kebab-case identifier, unique within the project
- `description` — one or two sentences used by Claude Code to **automatically decide when to invoke the agent** — this field is behaviorally significant, not just documentation. A vague or generic description silently degrades auto-invocation. Be specific about the domain and trigger conditions.
- `tools` — explicit list of tools this agent may use; omit tools the domain doesn't need

The body below the front matter is the agent's system prompt. Keep it focused on the domain.

### The Benefit: Scope Discipline

Session specialists reduce **scope drift** — the tendency of a general-purpose agent to wander into adjacent domains when given a large codebase. A `django-specialist` agent stays in the Django layer; a `data-integrity-agent` stays in data-health logic. Each specialist loads only the context its domain needs.

This is not about reducing session-start overhead (session startup cost is fixed regardless). The benefit is behavioral: specialists produce more focused, domain-accurate work because their system prompt constrains the reasoning surface.

### Minimum-Privilege Principle

Request only the tools a domain requires:
- A read-only analysis agent needs `Read`, `Grep` — not `Edit`, `Bash`, `Write`
- A specialist that generates code but doesn't run it needs `Read`, `Edit` — not `Bash`
- An agent that runs tests needs `Bash` with a narrow scope, not open-ended shell access

Over-permissioned specialists inherit all the blast radius of a general-purpose agent while providing none of the scope benefits.

**No sandbox isolation.** Session specialists do not run in a sandboxed environment. A specialist with `Bash` in its tool list can execute arbitrary shell commands with the same permissions as the parent session. Minimum-privilege tool lists are your only mitigation.

### Relationship to Orchestration

Session specialists operate below the scope of `orchestration.md`, which describes how external orchestrators route work between provider-level agents. Session specialists are an internal Claude Code mechanism — they are spawned within a single provider session, not across providers.

See [`framework/orchestration.md`](orchestration.md) for the provider-level contract.
