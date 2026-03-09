# Orchestrator Integration

How external orchestrators (Maestro, future alternatives) consume the directives config files to route work across AI agents.

> This document is **orchestrator-agnostic**. It describes the contract — what an orchestrator reads and how it should behave — not any specific tool's configuration format.

## Config Files an Orchestrator Reads

| File | Location | What it provides |
|------|----------|-----------------|
| [`agents.yml`](../agents.yml) | Repo root | Agent types, LLM providers, default assignments, fallback chains |
| `teams/<name>/manifest.yml` | Per-team directory | Role roster, pipeline stages, labels, vocabularies, settings |
| Per-project `CONTRIBUTING.md` | Project repo root | Team reference (`<!-- team: engineering -->`), pipeline mode, provider overrides |

### Reading Order

1. **`agents.yml`** — Learn what agent types exist, what providers are available, and the default assignment of providers to agent types.
2. **Project `CONTRIBUTING.md`** — Learn which team this project belongs to (`<!-- team: ... -->`) and what pipeline mode it uses (`<!-- pipeline-mode: ... -->`).
3. **`teams/<team>/manifest.yml`** — Learn the role roster, pipeline stages, and vocabularies for the project's team.

## Agent Spawning

For each agent type defined in `agents.yml`, the orchestrator spawns one agent session:

```
For each agent_type in agents.yml.agent_types:
  1. Resolve provider: check project overrides → default assignments → fallback chain
  2. Verify provider binary exists on the system (agents.yml.providers[id].binary)
  3. Spawn a session with that provider's CLI
  4. Prime the session with the agent type's role context
```

### Provider Resolution

```
1. Check project CONTRIBUTING.md for <!-- provider-overrides: {validator: chatgpt-cli} -->
2. If no override: use agents.yml.assignments.default[agent_type]
3. If default provider unavailable: walk agents.yml.assignments.fallback_order[agent_type]
4. If no provider available: skip this agent type (warn the user)
```

### Single-Provider Mode

When the same provider backs both agent types (fallback scenario), the orchestrator must:

- Run each agent type in a **separate, isolated session** (no shared conversation history)
- Prime the validator session with: "You are the validator agent. You did NOT build this code."
- Never merge builder and validator sessions

## Pipeline Execution

The orchestrator reads `manifest.yml.pipeline` to know the stage sequence. For each stage:

```yaml
# From manifest.yml
- stage: design-review
  command: /design
  agent: [builder, validator]    # which agent types participate
  label:
    name: design-complete        # GitHub label to apply on completion
    color: "0e8a16"
  produces: "Design decision + test specification comments"
```

### Routing Logic

| `agent` value | Orchestrator behavior |
|---------------|----------------------|
| `builder` | Route to builder agent only |
| `validator` | Route to validator agent only |
| `[builder, validator]` | Route to both — builder first, then validator, or in parallel depending on the stage |

### Stage Sequencing

Stages run in the order listed in the manifest's `pipeline` array. The orchestrator checks for the previous stage's label on the GitHub issue before advancing:

```
Before starting stage N:
  If stage N-1 has a label defined:
    Check GitHub issue for that label
    If missing: warn and ask whether to proceed (ad-hoc work gate)
```

### Pipeline Modes

Read from `<!-- pipeline-mode: ... -->` in the project's `CONTRIBUTING.md`.

| Mode | Orchestrator behavior |
|------|----------------------|
| `autonomous` | Run all stages without human gates |
| `gated` | Pause after Design and after Review for human authorization |

## Role-Level Stage Overrides

A role's `agent` field defines its default agent type. The optional `stages` map overrides that default for specific pipeline stages — a **per-stage override**.

```yaml
# From manifest.yml
- id: software-engineer
  agent: builder              # default
  stages:
    review-merge: validator   # per-stage override
```

### Resolution Logic

```
effective_agent(role, stage) = role.stages[stage] || role.agent
```

Two-step lookup: if the role has a `stages` entry for the current stage, use it. Otherwise, fall back to `role.agent`. If the `stages` field is missing or empty, the role always uses its default `agent` type.

### How This Interacts with Pipeline `agent`

The pipeline and role levels answer different questions:

| Level | Field | Question it answers |
|-------|-------|-------------------|
| Pipeline stage | `agent: [builder, validator]` | Which agent sessions are active for this stage? |
| Role | `stages: { review-merge: validator }` | Which session does this specific role run on? |

The pipeline `agent` field gates participation — it tells the orchestrator which sessions to spawn. The role `stages` map routes individual roles to the correct session. Both are needed.

### Session-Switch Priming

When a per-stage override moves a role from one agent session to another (e.g., a builder-default role acting as validator during Review), the orchestrator must re-prime the session. Apply the same independence priming used in Single-Provider Mode:

> "You are the validator agent. You did NOT build this code."

This ensures the role operates with genuine independence, regardless of its default assignment.

### Edge Cases

- **Missing `stages` field:** Falls back to `role.agent`. Backward-compatible with manifests that don't use overrides.
- **Empty `stages: {}`:** Same as missing — falls back to `role.agent`.
- **Invalid stage key:** Silently ignored (fail-open). Keys must match `pipeline[].stage` IDs exactly.
- **Redundant entries:** Only include overrides that differ from the default. If `agent: builder` and `stages: { implement: builder }`, the `implement` entry is redundant — omit it.

### Logging Recommendation

Orchestrators should log routing decisions when applying per-stage overrides, so operators can trace which session handled each role at each stage.

## Orchestration Patterns

Different orchestration tools offer different execution models. Here's how each maps to the pipeline:

### Pattern 1: Sequential Pipeline (Playbooks / Auto Run)

Best for: `/implement`, `/review` — stages with a clear linear flow.

The orchestrator executes pipeline stages as a sequence of tasks. Each task is assigned to the appropriate agent type based on the manifest's `agent` field. The orchestrator waits for each task to complete before advancing.

Markdown-based orchestrators (like Maestro's playbooks) can consume the pipeline directly — each stage becomes a markdown document with checkbox tasks.

### Pattern 2: Multi-Agent Deliberation (Group Chat)

Best for: `/design` — stages requiring cross-functional discussion.

The orchestrator runs multiple agents in a shared conversation where a moderator routes questions to the appropriate agent. The committee review order from `manifest.yml` (roles sorted by `review_order`) determines the sequence.

### Pattern 3: Parallel Independent Agents

Best for: builder implementing one issue while validator reviews a separate PR.

The orchestrator runs agents in parallel on independent tasks. No coordination needed — each agent operates on a different issue/PR.

## Label and Vocabulary Contract

The orchestrator uses labels and vocabularies from the manifest to interact with GitHub:

### Labels

```yaml
# From manifest.yml — the orchestrator creates/applies these labels
pipeline[].label.name   → GitHub issue label name
pipeline[].label.color  → GitHub label hex color
```

### Severity Levels

When parsing validator review comments, the orchestrator looks for the severity prefixes defined in `manifest.yml.vocabularies.severity_levels`:

```
MUST-FIX: ...   → blocks merge
SHOULD-FIX: ... → blocks current review round
NIT: ...        → informational, does not block
```

### Review Loop

The orchestrator enforces `manifest.yml.settings.max_review_rounds`. If MUST-FIX findings remain after the maximum rounds, the orchestrator escalates to the user rather than merging.

## Remote Agent Execution

When agents run on a remote machine (e.g., Mac Mini via SSH/Tailscale) and the orchestrator runs locally (e.g., MacBook Pro):

- The orchestrator connects to the remote machine to spawn agent CLI sessions
- `agents.yml.providers[].binary` must be available on the **remote** machine's PATH
- The project repo must be accessible on the remote machine
- The orchestrator handles I/O bridging between its local UI and the remote agent process

## Adding a New Orchestrator

To support a new orchestrator tool:

1. Read `agents.yml` for agent types and provider assignments
2. Read the project's `CONTRIBUTING.md` for team and pipeline mode
3. Read the team's `manifest.yml` for the pipeline definition
4. Map the pipeline stages to the orchestrator's native task format
5. Implement provider resolution with fallback chain support
6. Implement label checking/application via the GitHub API

No changes to the directives, manifests, or project configs should be needed.
