# Key Concepts

How the pieces work, mechanically. Read [Why This Architecture?](why.md) first if you're still deciding whether to adopt — this page is for when you're ready to understand the machinery.

**Contents:** [Core idea](#the-core-idea) · [Agent types](#agent-types) · [Personas](#personas) · [Pipeline](#the-pipeline) · [Pipeline modes](#pipeline-modes) · [Committee](#the-committee) · [Manifests](#manifests) · [Severity](#severity-levels) · [Three tiers](#the-three-tier-model) · [Overlays](#domain-overlays)

---

## The Core Idea

*Define how work gets done. Make it repeatable. Let the structure scale with you.*

Most AI setups are ad-hoc: you prompt a model, get output, and hope for the best. This system replaces that with a defined process — **[agent types](glossary.md)** that separate creation from review, **[personas](glossary.md)** that shape how each agent thinks, and a **[pipeline](glossary.md)** that warns before a step gets skipped. Everything is configured through **[manifests](glossary.md)** — structured config files — so a change lands in one place and every doc and agent reads the same truth.

The pattern works for any team — engineering, sales, marketing, operations — not just software. You define the roles, the stages, and the vocabulary. The system provides the scaffolding.

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

An **[agent type](glossary.md)** describes *what kind of work* gets done — not *which AI model* does it. There are two types:

| Type | What it does |
|------|-------------|
| **Builder** | Creates deliverables, verifies quality, publishes, integrates |
| **Validator** | Reviews work, audits quality, writes specifications, flags issues |

**Key insight:** the model that *builds* should not be the same model that *validates*. When one agent does both, its blind spots repeat in every phase — it reviews work it created and misses the same things twice.

| Single agent | Two agent types |
|---|---|
| Reviews its own work | A different agent reviews |
| Same blind spots in both tasks | Independent perspectives catch more |
| "Looks good to me" | "Wait, did you consider...?" |

### Provider assignment

Agent types are backed by **LLM providers** (the AI tools that do the work — Claude Code, Antigravity CLI, etc.). The mapping lives in [`agents.yml`](../agents.yml):

```yaml
# Default: Claude builds, Antigravity validates
assignments:
  default:
    builder: claude-code
    validator: antigravity-cli
```

If a provider isn't available, the system falls back — even running both types on the same provider in **isolated sessions** (separate conversations that share no history) so the reviewer can't inherit the builder's assumptions. Why that matters: [Why This Architecture? → single-provider fallback](why.md).

---

## Personas

*A panel of specialists, each with their own lens.*

A **[persona](glossary.md)** is a character profile that shapes how an AI agent approaches work. Each persona has a title, backstory, expertise, and review focus — a professional identity the agent reasons from.

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
| **PM** | Requirements, acceptance criteria, user value (pipeline only — not a code reviewer) |

### Why personas matter

Without a persona, AI feedback is generic: *"Consider adding error handling."*

With the **Security Engineer** persona: *"MUST-FIX: This endpoint accepts user input without validation — an attacker could inject SQL via the `name` parameter."*

**Beyond engineering:** A sales team might use Deal Strategist, Pricing Analyst, Legal Reviewer, and VP of Sales. A marketing team might use Brand Strategist, SEO Specialist, and Copy Editor. The structure is identical — only the expertise changes.

### Cross-cutting traits

All personas on a team share a common culture defined in [`cross-cutting-traits.md`](../teams/engineering/personas/cross-cutting-traits.md). For the engineering team, these include values like radical pragmatism, test-first thinking, and ops ownership. This ensures consistency across personas while allowing each to bring their specialized lens.

---

## The Pipeline

*An assembly line. Each station checks the last.*

A **[pipeline](glossary.md)** takes a task from start to finish through a defined sequence of stages. Each stage produces artifacts the next one consumes, and GitHub labels track which stages are complete.

```mermaid
graph LR
    A["Define<br/><code>/define</code>"] --> B["Design<br/><code>/design</code>"]
    B --> C["Implement<br/><code>/implement</code>"]
    C --> D["Review<br/><code>/review</code>"]
    D --> E["Deploy & Verify"]
    E --> F["Summarize<br/><code>/summarize</code>"]

    style A fill:#6f42c1,color:#fff
    style B fill:#0e8a16,color:#fff
    style C fill:#fbca04,color:#000
    style D fill:#6e5494,color:#fff
    style E fill:#0075ca,color:#fff
    style F fill:#d4c5f9,color:#000
```

The engineering team's pipeline has six stages (other teams define their own):

| Stage | What happens (engineering) | Who | Label |
|---|---|---|---|
| Define | PM writes a PRD with acceptance criteria | Validator | `define-reviewed` |
| Design | Committee reviews feasibility, architecture, UX, security | Both | `design-complete` |
| Implement | Tests written first (failing), then code until they pass | Builder | `implementing` |
| Review | Up to 3 rounds of committee review, then merge | Both | `merged` |
| Deploy & Verify | Deploy, health-check, close the issue | Builder | — |
| Summarize *(optional)* | Stakeholder summary of what was delivered and why | Validator | `summarized` |

The pipeline is advisory, not a hard block. If you skip a stage, the system warns you and asks for confirmation — but it won't prevent you. Hotfixes happen, and the process should support them rather than getting in the way.

### Pipeline modes

Projects declare a mode in their `CONTRIBUTING.md` to control how much human involvement is required:

| Mode | Behavior |
|---|---|
| **Autonomous** | Runs end-to-end without human gates |
| **Gated** | Pauses after Design and Review for human approval |

---

## The Committee

*Each reviewer reads all prior feedback first.*

A **[committee](glossary.md)** is the full team of personas reviewing work in sequence. Each persona reads everything that came before, so later reviewers build on (or challenge) earlier observations rather than duplicating them.

```mermaid
graph TD
    A["Task arrives"] --> B["UX Designer reviews"]
    B --> C["Software Engineer reviews<br/><em>reads prior comments</em>"]
    C --> D["...remaining personas,<br/>in manifest order..."]
    D --> E["Engineering Manager<br/>synthesizes all feedback"]
    E --> F["Members update comments<br/>to final positions"]
    F --> G["Zero-context agent checks<br/>the spec stands alone"]

    style A fill:#333,color:#fff
    style B fill:#0075ca,color:#fff
    style C fill:#0075ca,color:#fff
    style D fill:#0075ca,color:#fff
    style E fill:#6f42c1,color:#fff
    style F fill:#0e8a16,color:#fff
    style G fill:#fbca04,color:#000
```

### Key rules

1. **Sequential posting** — Each persona reads *all* prior comments first. No parallel reviews. This prevents redundant observations and lets later reviewers address gaps the earlier ones missed.
2. **[Overwrite-to-consensus](glossary.md)** — After the Engineering Manager synthesizes all feedback, members whose positions changed edit their original comments to show their final stance. Readers see clean conclusions, not a debate thread they have to interpret.
3. **[Fresh-eyes validation](glossary.md)** — A zero-context sub-agent reads only the final spec and flags anything ambiguous. This catches assumptions the committee built during discussion but forgot to write down — the "curse of knowledge" problem.

---

## Manifests

*One file, one truth.*

A **[manifest](glossary.md)** is the single source of truth for a team's configuration: who's on the team, what the pipeline looks like, and what vocabulary they use. When the manifest changes, the change is immediately authoritative — no drift between docs and config.

```yaml
# teams/engineering/manifest.yml (simplified)
team: engineering

roles:
  - id: ux-designer
    name: UX Designer
    agent: builder           # which agent type runs this role...
    stages:
      review-merge: validator  # ...with per-stage overrides (here: reviews as validator)
    persona: personas/ux-designer.md
    review_order: 1          # position in committee sequence

pipeline:
  - stage: pm-review
    command: /define
    agent: validator
    label:
      name: define-reviewed

vocabularies:
  severity_levels:
    - id: must-fix
      blocks: merge
```

One config edit changes the system's behavior everywhere ([the full list of what one-line changes buy you](why.md#solution-4-manifests-make-it-configurable)).

Every team gets its own manifest. A sales team would define different roles, stages, and vocabularies — but the structure is the same.

---

## Severity Levels

Review findings use a shared [severity vocabulary](glossary.md) so there's no ambiguity about what blocks progress:

| Severity | Meaning | Blocks? |
|---|---|---|
| **MUST-FIX** | Correctness issue, security risk, data loss risk | Merge |
| **SHOULD-FIX** | Quality issue, missing edge case, unclear naming | Current round |
| **NIT** | Style preference, minor suggestion | Nothing |

---

## The Three-Tier Model

Configuration lives at three levels. Each adds specificity without duplicating the tier above. See [glossary](glossary.md).

| Tier | Where | What |
|------|-------|------|
| **1. Directives** (this repo) | `suniljames/directives` | Team scaffolding, personas, framework, templates |
| **2. Organization** (optional) | `<org>/.github` or org-level repo | Domain compliance, org-specific workflows, shared CI |
| **3. Project** | Each project repo | Tech stack, architecture, environment config |

The directives repo provides the *what* and *why*. The project repo provides the *how* and *where*. The organization tier is optional — useful when multiple projects share domain-specific requirements (like HIPAA compliance) but not needed for most setups.

---

## Domain Overlays

An **[overlay](glossary.md)** adds domain-specific rules (healthcare privacy law, payment-card compliance, etc.) on top of the base process. Overlays are additive — they extend the base, never replace it.

The distinction from provider configs, in one line: **providers are about *which AI* and *how to configure it*; overlays are about *what industry* and *what additional rules apply*.** A healthcare app using Antigravity as validator uses both — one provider config, one domain overlay.

---

## Next Steps

- [Why This Architecture?](why.md) — The business case behind these decisions
- [Getting Started](getting-started.md) — Set this up in your own project
- [FAQ](faq.md) — Quick answers to first-visit questions
- [Glossary](glossary.md) — Quick reference for all terms
