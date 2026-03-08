# Why This Architecture?

The thinking behind the system. Read this to understand *why* the pieces exist, not just *what* they do.

---

## The Problem: One Agent, Correlated Failures

AI agents can create, review, and deliver work across many domains. But when one model does all of that, its blind spots repeat in every phase.

```mermaid
graph TD
    A["Single AI Agent"] --> B["Creates the work"]
    A --> C["Reviews the work"]
    A --> D["Delivers the work"]
    B --> E["Same blind spots<br/>in ALL phases"]
    C --> E
    D --> E

    style A fill:#d73a49,color:#fff
    style E fill:#d73a49,color:#fff
```

The model that wrote a SQL query won't notice it's injectable during review — it wrote it that way on purpose. The model that drafted a proposal won't catch the pricing error during QA — it chose those numbers.

This is grading your own homework.

**Non-technical example:** Imagine a marketing team where the same person writes the ad copy, reviews it for brand compliance, and approves the budget. They'll miss the same things at every step because they made the original decisions.

---

## Solution 1: Split Builder and Validator

**Key insight: the model that builds should not validate.**

```mermaid
graph LR
    subgraph "Builder Agent"
        B1["Writes code"]
        B2["Runs tests"]
        B3["Deploys"]
    end
    subgraph "Validator Agent"
        V1["Reviews code"]
        V2["Audits security"]
        V3["Writes specs"]
    end
    B1 -->|"PR + artifacts"| V1
    V1 -->|"Findings"| B1

    style B1 fill:#0075ca,color:#fff
    style B2 fill:#0075ca,color:#fff
    style B3 fill:#0075ca,color:#fff
    style V1 fill:#6f42c1,color:#fff
    style V2 fill:#6f42c1,color:#fff
    style V3 fill:#6f42c1,color:#fff
```

Two different models with different training, architectures, and biases catch different things. The overlap in what they miss shrinks.

### What if you only have one provider?

The system runs both [agent types](glossary.md) in **isolated sessions** — separate conversations with no shared context. The validator is primed: *"You did NOT build this code. Review it independently."*

Not as good as two different models. Significantly better than one session doing both.

---

## Solution 2: Personas Create Depth

**Key insight: "review this code" produces shallow feedback. A specific [persona](glossary.md) produces targeted, deep feedback.**

| Generic prompt | Persona-driven prompt |
|---|---|
| "Review this PR for issues" | Security Engineer reviews for: injection, auth bypass, data exposure, CSRF |
| "Looks good, maybe add some tests" | "MUST-FIX: This endpoint accepts user input at line 47 without sanitization. SQL injection via `name` parameter." |

Each persona has:

- **A backstory** — anchors decision-making (not decoration)
- **Core expertise** — what they evaluate
- **A review lens** — specific checklist of things to find
- **An interaction style** — how they communicate findings

### Why multiple?

Real work is multi-disciplinary. Architecturally sound code might be inaccessible. Code passing all tests might have a SQL injection. A sales proposal with great positioning might have wrong pricing.

No single reviewer — human or AI — holds all lenses simultaneously. [Personas](glossary.md) make them explicit.

---

## Solution 3: Pipeline Prevents Skipping Steps

**Key insight: without a defined workflow, agents (like humans) skip steps under pressure.**

```mermaid
graph TD
    A["GitHub Issue"] --> B{"PM Review<br/><code>/pm</code>"}
    B -->|"PRD posted"| C{"Design Review<br/><code>/design</code>"}
    C -->|"Committee reviews"| D{"Implementation<br/><code>/implement</code>"}
    D -->|"TDD: tests first"| E{"Code Review<br/><code>/ramd</code>"}
    E -->|"Up to 3 rounds"| F{"Deploy & Verify"}
    F -->|"Health check"| G["Issue Closed"]

    style A fill:#333,color:#fff
    style B fill:#6f42c1,color:#fff
    style C fill:#0e8a16,color:#fff
    style D fill:#fbca04,color:#000
    style E fill:#6e5494,color:#fff
    style F fill:#0075ca,color:#fff
    style G fill:#333,color:#fff
```

Each stage has a **label** tracking completion, **checks** the previous label, and **produces artifacts** the next stage consumes.

Skip PM review and jump to implementation? The system warns you. You can override — it's advisory, not a hard block — but you make a conscious choice.

### Why labels, not a database?

The source of truth lives where the work lives — GitHub. Labels are visible, inspectable, and need zero infrastructure.

---

## Solution 4: Manifests Make It Configurable

**Key insight: hardcoding personas, stages, and review order in docs creates maintenance debt.**

Three config files drive everything:

| File | Scope | Changes when... |
|------|-------|----------------|
| `agents.yml` | Global | You add an LLM provider (rare) |
| `manifest.yml` | Per-team | You adjust the team or process (occasional) |
| `CONTRIBUTING.md` | Per-project | A project needs a different mode (per-project) |

Add a persona → one manifest entry. Change review order → edit one number. Swap LLM provider → update one line. Add a team → copy `teams/TEMPLATE/` and fill in roles.

---

## Solution 5: Fresh-Eyes Validation

**Key insight: [committee](glossary.md) members build shared context during review. That context doesn't always make it into the final spec.**

```mermaid
graph TD
    A["Committee reviews"] --> B["Shared context built"]
    B --> C["Issue description updated"]
    C --> D{"Did ALL context<br/>make it in?"}
    D -->|"Gap"| E["Fresh-eyes sub-agent<br/>reads ONLY the description"]
    E --> F["Flags: 'What does<br/>existing pattern mean?'"]
    D -->|"Complete"| G["Validation passes"]

    style D fill:#d73a49,color:#fff
    style E fill:#fbca04,color:#000
```

A zero-context agent simulates the experience of whoever will actually do the work. Catches assumptions the committee forgot to write down.

---

## Design Principles

| Principle | What it means |
|-----------|--------------|
| **Decouple roles from providers** | "Security Engineer" means a review role, not "Gemini." Swap providers without rewriting process. |
| **Repo is the source of truth** | All coordination through files, PRs, issues, labels. No side channels. |
| **Advisory gates, not hard blocks** | Pipeline warns when you skip stages. Doesn't prevent you. Hotfixes happen. |
| **Configuration over convention** | Machine-readable manifests, not documentation you have to interpret. |
| **Additive domain overlays** | Healthcare needs HIPAA. Fintech needs PCI. Additions, not replacements. |
| **Team-agnostic scaffolding** | The architecture doesn't assume engineering. Any team can fill it with their own content. |

---

## Next Steps

- [Key Concepts](concepts.md) — Quick reference for all terminology
- [Getting Started](getting-started.md) — Set this up in your own project
- [Glossary](glossary.md) — Definitions for every term
