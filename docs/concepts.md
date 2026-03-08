# Key Concepts

Plain-language guide to every idea in this system. Read this first if you're new.

---

## The Core Idea

*One person builds. A different person inspects.*

Most AI setups use a single model for everything: creating work, reviewing it, shipping it. Same blind spots in every phase. This system fixes that by splitting work across **[agent types](glossary.md)**, giving each agent **[personas](glossary.md)** that shape how it thinks, and connecting everything through a **[pipeline](glossary.md)** that prevents skipping steps.

The pattern works for any team — engineering, sales, marketing, operations — not just software.

```mermaid
graph LR
    A["Task arrives"] --> B["Agents plan<br/>and design"]
    B --> C["Work produced<br/>following process"]
    C --> D["Independent review<br/>catches blind spots"]
    D --> E["Delivered and<br/>verified"]

    style A fill:#333,color:#fff
    style B fill:#0075ca,color:#fff
    style C fill:#fbca04,color:#000
    style D fill:#6f42c1,color:#fff
    style E fill:#0e8a16,color:#fff
```

---

## Agent Types

An **[agent type](glossary.md)** describes *what kind of work* gets done — not *which AI model* does it. Two types:

| Type | What it does |
|------|-------------|
| **Builder** | Writes code, runs tests, deploys, merges PRs |
| **Validator** | Reviews code, audits security, writes specs, files issues |

**Key insight:** the model that *builds* should not be the same model that *validates*.

| Single agent | Two agent types |
|---|---|
| Reviews its own work | A different agent reviews |
| Same blind spots in both tasks | Independent perspectives catch more |
| "Looks good to me" | "Wait, did you consider...?" |

### Provider assignment

Agent types are backed by **LLM providers** (Claude Code, Gemini CLI, etc.). The mapping lives in [`agents.yml`](../agents.yml):

```yaml
# Default: Claude builds, Gemini validates
assignments:
  default:
    builder: claude-code
    validator: gemini-cli
```

If a provider isn't available, the system falls back — even running both types on the same provider in **isolated sessions** so they can't share context.

---

## Personas

*A panel of specialists, each with their own lens.*

A **[persona](glossary.md)** is a character profile that shapes how an AI agent approaches work. Each has a title, backstory, expertise, and review focus.

The engineering team has 11 personas. Each sees problems differently:

| Persona | Focus |
|---|---|
| **UX Designer** | Accessibility, design systems, responsive behavior |
| **Software Engineer** | Code quality, patterns, readability |
| **System Architect** | Service boundaries, coupling, scalability |
| **Data Engineer** | Schema design, migrations, query performance |
| **AI/ML Engineer** | LLM integration, prompt safety, cost |
| **Security Engineer** | Vulnerabilities, auth, data exposure |
| **QA Engineer** | Test coverage, edge cases, test layers |
| **SRE** | Reliability, logging, health checks |
| **Writer** | User-facing copy, error messages, docs |
| **Engineering Manager** | Synthesizes all feedback, makes final calls |
| **PM** | Requirements, acceptance criteria, user value |

### Why personas matter

Without a persona, AI feedback is generic: *"Consider adding error handling."*

With the **Security Engineer** persona: *"MUST-FIX: This endpoint accepts user input without validation — an attacker could inject SQL via the `name` parameter."*

Personas bring depth that generic prompting can't match.

**Beyond engineering:** A sales team might use Deal Strategist, Pricing Analyst, Legal Reviewer, and VP of Sales. A marketing team might use Brand Strategist, SEO Specialist, and Copy Editor. The structure is identical — only the expertise changes.

### Cross-cutting traits

All personas share a team culture defined in [`cross-cutting-traits.md`](../teams/engineering/personas/cross-cutting-traits.md) — values like radical pragmatism, test-first thinking, and ops ownership.

---

## The Pipeline

*An assembly line. Each station checks the last.*

A **[pipeline](glossary.md)** takes a task from start to finish. Each stage produces artifacts the next consumes. GitHub labels track progress.

```mermaid
graph LR
    A["Define<br/><code>/define</code>"] --> B["Design<br/><code>/design</code>"]
    B --> C["Implement<br/><code>/implement</code>"]
    C --> D["Review<br/><code>/review</code>"]
    D --> E["Deploy & Verify<br/><em>(automatic)</em>"]
    E --> F["Summarize<br/><code>/summarize</code>"]

    style A fill:#6f42c1,color:#fff
    style B fill:#0e8a16,color:#fff
    style C fill:#fbca04,color:#000
    style D fill:#6e5494,color:#fff
    style E fill:#0075ca,color:#fff
    style F fill:#d4c5f9,color:#000
```

| Stage | What happens | Who | Label |
|---|---|---|---|
| Define | PM writes a PRD with acceptance criteria | Validator | `pm-reviewed` |
| Design | Committee reviews feasibility, architecture, UX, security | Both | `design-complete` |
| Implement | TDD: failing tests → implement → green → refactor | Builder | `implementing` |
| Review | Up to 3 rounds of review, then squash merge | Both | `merged` |
| Deploy & Verify | Rebuild, health check, close issue (automatic) | Builder | Issue closed |
| Summarize | Stakeholder summary | Validator | `summarized` |

### Pipeline modes

Projects declare a mode in their `CONTRIBUTING.md`:

| Mode | Behavior |
|---|---|
| **Autonomous** | Runs end-to-end without human gates |
| **Gated** | Pauses after Design and Review for human approval |

---

## The Committee

*Each reviewer reads all prior feedback first.*

A **[committee](glossary.md)** is the full team of personas reviewing work in sequence. Not a meeting — a structured protocol.

```mermaid
graph TD
    A["Task arrives"] --> B["UX Designer reviews"]
    B --> C["Software Engineer reviews<br/><em>reads prior comments</em>"]
    C --> D["... each persona in order ..."]
    D --> E["Engineering Manager<br/>synthesizes all feedback"]
    E --> F["Overwrite-to-consensus"]
    F --> G["Fresh-eyes validation"]

    style A fill:#333,color:#fff
    style B fill:#0075ca,color:#fff
    style C fill:#0075ca,color:#fff
    style D fill:#0075ca,color:#fff
    style E fill:#6f42c1,color:#fff
    style F fill:#0e8a16,color:#fff
    style G fill:#fbca04,color:#000
```

### Key rules

1. **Sequential posting** — Each persona reads *all* prior comments first. No parallel reviews. This builds cumulative insight.
2. **[Overwrite-to-consensus](glossary.md)** — After the Engineering Manager synthesizes, members whose positions changed edit their original comments. Readers see clean final positions, not a debate thread.
3. **[Fresh-eyes validation](glossary.md)** — A zero-context sub-agent reads only the final spec and flags anything ambiguous. Catches "curse of knowledge" gaps.

---

## Manifests

A **[manifest](glossary.md)** is a YAML file — the single source of truth for a team's config: who's on the team, what the pipeline looks like, what vocabulary they use.

```yaml
# teams/engineering/manifest.yml (simplified)
team: engineering

roles:
  - id: ux-designer
    name: UX Designer
    agent: builder           # which agent type
    persona: personas/ux-designer.md
    review_order: 1          # position in committee sequence

pipeline:
  - stage: pm-review
    command: /define
    agent: validator
    label:
      name: pm-reviewed

vocabularies:
  severity_levels:
    - id: must-fix
      blocks: merge
```

Change the manifest → the change cascades everywhere. Add a persona, reorder the review sequence, adjust severity levels — all in one place.

Every team gets its own manifest. A sales team would define different roles, stages, and vocabularies. Same structure, different content.

---

## Severity Levels

Review findings use a shared [severity vocabulary](glossary.md):

| Severity | Meaning | Blocks? |
|---|---|---|
| **MUST-FIX** | Correctness bug, security vulnerability, data loss risk | Merge |
| **SHOULD-FIX** | Code quality issue, missing edge case, poor naming | Current round |
| **NIT** | Style preference, minor suggestion | Nothing |

---

## The Three-Tier Model

Configuration lives at three levels. Each adds specificity without duplicating the tier above. See [glossary](glossary.md).

| Tier | Where | What |
|------|-------|------|
| **1. Directives** (this repo) | `suniljames/directives` | Team scaffolding, personas, framework, templates |
| **2. Organization** (optional) | `<org>/.github` or org-level repo | Domain compliance, org-specific workflows, shared CI |
| **3. Project** | Each project repo | Tech stack, architecture, environment config |

The directives repo provides the *what* and *why*. The project repo provides the *how* and *where*.

---

## Domain Overlays

An **[overlay](glossary.md)** adds domain-specific rules (HIPAA, PCI, etc.) on top of the base process. Additive — never replaces.

---

## Next Steps

- [Why This Architecture?](why.md) — The philosophy behind these decisions
- [Getting Started](getting-started.md) — Set this up in your own project
- [Glossary](glossary.md) — Quick reference for all terms
