# Multi-Agent Architecture

A single AI model acting as both builder and validator creates correlated failure modes — shared blind spots, single-model groupthink, and no independent verification. The model that builds the code should not be the same model that validates it.

## Principle

Split engineering agent roles across two LLM backends: a **builder/executor** and a **validator/risk manager**. The builder and validator should be different models to maximize independent verification.

## Role Assignments

### Builder / Executor (7 roles)

| # | Role | Rationale |
|---|------|-----------|
| 10 | **Engineering Manager** | Maintains consistent technical direction, rule adherence, and process enforcement. |
| 2 | **Software Engineer** | Primary code author. Requires integrated file editing, bash, git, multi-file operations. |
| 3 | **System Architect** | Architecture decisions grounded in intimate knowledge of the actual codebase. |
| 4 | **Data Engineer** | Implementation-heavy: writing migrations, building pipelines, optimizing queries. |
| 5 | **AI/ML Engineer** | AI integration — the builder knows its own SDK and API best. |
| 1 | **UX Designer** | Translates designs into frontend code. Requires generating and editing files. |
| 8 | **SRE** | Operational: running commands, reading logs, restarting services, editing configs. |

### Validator / Risk Manager (4 roles)

| # | Role | Rationale |
|---|------|-----------|
| 6 | **Security Engineer** | Cross-model validation catches blind spots the builder's model would share. |
| 7 | **QA Engineer** | Independent verification and validation (IV&V) — different model maximizes edge case coverage. |
| 11 | **PM (Product Manager)** | Separates "what to build" from "how to build it" across model boundaries. |
| 9 | **Tech Writer** | Independent reader of builder output — flags unclear code/architecture rather than filling gaps with shared assumptions. |

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
7. **Tech Writer (validator)** documents the feature.

## Coordination Protocol

- **Structured artifacts** — PRDs, test reports, security findings, and review comments follow defined formats.
- **File-based exchange** — Both agents read/write to the shared repository. The repo is the source of truth.
- **Explicit acceptance criteria** — The PM defines "done." The QA Engineer verifies "done." The EM orchestrates the path between them.
- **Label-driven coordination** — Agents check GitHub issue labels to determine which pipeline stage is complete before proceeding.
- **PR labels** — All autonomously created PRs are labeled `ai:autonomous`.
- **Review findings** — Posted as PR comments with severity levels (see [`code-review-framework.md`](code-review-framework.md)).

## Guiding Principles

1. **Builders need tooling.** Roles that touch code, infrastructure, or runtime belong on the builder agent.
2. **Validators should be independent.** Audit, review, and verification roles gain the most from running on a different model.
3. **Keep the boundary clean.** Concentrate building on one agent and auditing on the other. This simplifies coordination and makes handoff points explicit.
4. **Rationale must be technical, not marketing.** Assignments are based on demonstrated capability and architectural fit.
