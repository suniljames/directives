# Multi-Agent Architecture

> **Canonical config:** [`agents.yml`](../agents.yml) — agent types, providers, assignments.
> **Role roster:** [`teams/engineering/manifest.yml`](../teams/engineering/manifest.yml)

A single AI model acting as both builder and validator creates correlated failure modes — shared blind spots, single-model groupthink, and no independent verification. The model that builds the code should not be the same model that validates it.

## Principle

Split engineering roles across abstract **agent types** — a **builder** and a **validator** — backed by different LLM providers when available. Agent types and provider assignments are defined in [`agents.yml`](../agents.yml). Role-to-agent-type mappings are in each team's [`manifest.yml`](../teams/engineering/manifest.yml).

## Agent Types

| Type | Purpose | Capabilities |
|------|---------|-------------|
| **Builder** | Implements features, writes code, deploys | edit_files, run_tests, deploy, merge |
| **Validator** | Reviews, audits, writes specs and docs | review_code, write_specs, file_issues |

## Provider Assignment

Default assignments and fallback chains are in `agents.yml`. When the preferred provider for an agent type is unavailable, the orchestrator (or the agent itself) falls back to the next provider in the chain.

### Single-Provider Fallback

When only one provider is available (e.g., orchestrator doesn't support Gemini yet), that provider runs both agent types in **isolated sessions**. Mitigations:

1. **Session isolation** — The validator pass runs in a separate session with no shared context from the builder pass.
2. **Mandatory fresh-eyes validation** — Required (not optional) in single-provider mode.
3. **Explicit role priming** — The validator session's prompt states: "You are the validator agent. You did NOT build this code. Review it independently."

## Build-then-Validate Flow

```
Builder implements --> Validator reviews --> Builder addresses feedback
```

1. **PM (validator)** writes requirements and acceptance criteria.
2. **EM (builder)** plans the work, assigns tasks, oversees execution.
3. **Engineer, Architect, Data, AI/ML, UX (builder)** implement the feature.
4. **QA Engineer (validator)** tests the implementation against requirements.
5. **Security Engineer (validator)** audits the code for vulnerabilities.
6. **SRE (builder)** deploys and monitors.
7. **Writer (validator)** documents the feature.

## Coordination Protocol

- **Structured artifacts** — PRDs, test reports, security findings, and review comments follow defined formats.
- **File-based exchange** — Both agents read/write to the shared repository. The repo is the source of truth.
- **Explicit acceptance criteria** — The PM defines "done." The QA Engineer verifies "done." The EM orchestrates the path between them.
- **Label-driven coordination** — Agents check GitHub issue labels to determine which pipeline stage is complete before proceeding.
- **PR labels** — All autonomously created PRs are labeled `ai:autonomous`.
- **Review findings** — Posted as PR comments with severity levels (see [`code-review-framework.md`](../teams/engineering/process/code-review-framework.md)).

## Guiding Principles

1. **Builders need tooling.** Roles that touch code, infrastructure, or runtime belong on the builder agent.
2. **Validators should be independent.** Audit, review, and verification roles gain the most from running on a different model.
3. **Keep the boundary clean.** Concentrate building on one agent and auditing on the other. This simplifies coordination and makes handoff points explicit.
4. **Rationale must be technical, not marketing.** Assignments are based on demonstrated capability and architectural fit.
