# Getting Started

Set up this system in your project. Adopt the full [pipeline](glossary.md) or start with the pieces that help most.

---

## Prerequisites

- A GitHub repository
- At least one AI tool (Claude Code, Gemini CLI, Cursor, ChatGPT, etc.)
- Familiarity with the [key concepts](concepts.md)

---

## Three Levels of Adoption

Pick one. Move up later if you want.

| Level | What you get | Time |
|-------|-------------|------|
| **1. Personas only** | Better AI reviews with zero config | 15 min |
| **2. + Pipeline** | Structured workflow with labels and gates | 30 min |
| **3. + Multi-agent** | Builder/validator split across providers | 1 hour |

---

## Level 1: Persona-Driven Reviews (15 minutes)

Use [persona](glossary.md) definitions to improve AI reviews. No config files, no pipeline, no multi-agent setup.

### Pick your personas

Browse [`teams/engineering/personas/`](../teams/engineering/personas/). You don't need all 11. Match your biggest gaps:

| Worried about... | Use |
|---|---|
| Accessibility, design | UX Designer |
| Code quality, patterns | Software Engineer |
| Architecture, coupling | System Architect |
| Database, migrations | Data Engineer |
| AI/LLM integration | AI/ML Engineer |
| Security vulnerabilities | Security Engineer |
| Test coverage, edge cases | QA Engineer |
| Operational reliability | SRE |
| User-facing copy, docs | Writer |

### Use them in your prompts

Copy-paste this into your AI tool:

```
Review this PR as the Security Engineer described in:
https://github.com/suniljames/directives/blob/main/teams/engineering/personas/security-engineer.md

Categorize findings as MUST-FIX, SHOULD-FIX, or NIT.
```

**Expected output:** Instead of *"Looks good, maybe add some tests"*, you'll get targeted findings like *"MUST-FIX: This endpoint accepts user input at line 47 without sanitization. SQL injection via the `name` parameter."*

That's it. You're already getting deeper reviews.

---

## Level 2: Pipeline + Personas (30 minutes)

Add the structured workflow: labels, stage gates, repeatable process.

### 1. Copy the templates

```bash
cp templates/CONTRIBUTING.md.template  your-project/CONTRIBUTING.md
cp templates/CLAUDE.md.template        your-project/CLAUDE.md
```

### 2. Set your pipeline mode

Edit `CONTRIBUTING.md`:

```markdown
<!-- team: engineering -->
<!-- pipeline-mode: autonomous -->
```

| Mode | Behavior |
|------|----------|
| **autonomous** | AI runs the full pipeline without stopping |
| **gated** | AI pauses after Design and Review for your approval |

### 3. Fill in project-specific sections

Templates have `TODO` markers. Add your tech stack, dev environment, and project docs.

### 4. Create slash commands

```
.claude/commands/
  define.md     # /define — Define requirements (PRD)
  design.md     # /design — Committee design review
  implement.md  # /implement — TDD implementation
  review.md     # /review — Code review & merge
  summarize.md  # /summarize — Stakeholder summary
```

See [pipeline docs](../teams/engineering/process/pipeline.md) for what each stage produces.

### 5. Set up labels

```bash
gh label create "pm-reviewed"     --color "6f42c1" --repo your-org/your-repo
gh label create "design-complete" --color "0e8a16" --repo your-org/your-repo
gh label create "implementing"    --color "fbca04" --repo your-org/your-repo
gh label create "merged"          --color "6e5494" --repo your-org/your-repo
gh label create "summarized"      --color "d4c5f9" --repo your-org/your-repo
gh label create "ai:autonomous"   --color "1d76db" --repo your-org/your-repo
```

### What the flow looks like

```mermaid
sequenceDiagram
    participant You
    participant AI as AI Agent
    participant GH as GitHub

    You->>GH: Create issue
    You->>AI: /define 42
    AI->>GH: Post PRD, add pm-reviewed label
    You->>AI: /design 42
    AI->>GH: Post committee reviews (sequential)
    AI->>GH: Add design-complete label
    You->>AI: /implement 42
    AI->>AI: Write failing tests, implement until green
    AI->>GH: Push feature branch
    You->>AI: /review
    AI->>GH: Create PR, run code review, squash merge
    AI->>GH: Close issue
```

---

## Level 3: Multi-Agent Setup (1 hour)

Split [builder and validator](glossary.md) across different LLM providers for genuinely independent reviews.

### 1. Configure agents.yml

The default [`agents.yml`](../agents.yml) maps Claude Code as builder, Gemini CLI as validator. Adjust for your providers:

```yaml
assignments:
  default:
    builder: claude-code      # Your primary coding AI
    validator: gemini-cli     # Your review/audit AI
```

### 2. Add validator agent config

Create `GEMINI.md` (or equivalent) in your project:

```markdown
# Validator Agent Config

You are the **validator** agent. You did NOT build this code.
Review independently using the personas assigned to you.

Refer to the [engineering directives](https://github.com/suniljames/directives)
for persona definitions and review process.
```

### 3. Assign roles to agent types

The [manifest](glossary.md) already does this — each role has an `agent:` field:

```yaml
roles:
  - id: security-engineer
    agent: validator        # Runs on the validator (Gemini)
  - id: software-engineer
    agent: builder          # Runs on the builder (Claude)
```

### 4. Single-provider fallback

Only one AI tool? Run both agent types in **separate sessions**:

```
Session 1 (Builder):
  "You are the builder agent. Implement the feature."

Session 2 (Validator — separate conversation):
  "You are the validator agent. You did NOT build this code.
   Review it independently."
```

The key: **never share conversation history** between sessions.

---

## Customizing Personas

**Add a persona:** Create `teams/engineering/personas/your-role.md` following the [template](../teams/TEMPLATE/personas/example-role.md), then add the role to `manifest.yml`.

**Change review order:** Edit `review_order` in the manifest. Engineering Manager is always last (`review_order: last`).

**Create a new team:** Copy `teams/TEMPLATE/` → `teams/your-team/`. See the [template manifest](../teams/TEMPLATE/manifest.yml) for field docs.

---

## Beyond Engineering

To create a non-engineering team:

1. **Copy the template:** `cp -r teams/TEMPLATE teams/sales`
2. **Define personas:** What roles review work?

   | Role | Focus |
   |---|---|
   | Deal Strategist | Win probability, positioning, account fit |
   | Pricing Analyst | Margins, discounts, deal structure |
   | Legal Reviewer | Contract terms, compliance, risk |
   | VP of Sales | Strategic alignment, forecast impact |

3. **Define pipeline stages:** What does work flow through?
4. **Define vocabularies:** What severity levels and categories apply?

Agent types, manifest structure, pipeline mechanics, and committee protocol all transfer directly. Only personas, stages, and vocabulary change.

---

## Adding Domain Overlays

Domain-specific requirements (healthcare, fintech)? Add an [overlay](glossary.md):

```
overlays/
  healthcare/        # HIPAA, PHI handling, patient safety
  your-domain/       # Your domain-specific rules
```

Overlays extend the base process. Reference them from your `CONTRIBUTING.md`.

---

## Project Structure After Setup

```
your-project/
  CONTRIBUTING.md           # Team, pipeline mode, tech stack
  CLAUDE.md                 # Builder agent config
  GEMINI.md                 # Validator agent config (optional)
  .claude/
    commands/
      define.md             # /define command
      design.md             # /design command
      implement.md          # /implement command
      review.md             # /review command
      summarize.md          # /summarize command
  docs/
    developer/
      code-review-lenses.md # Tech-specific review checklists
      project-context.md    # Project-specific persona knowledge
```

Link to directives, don't copy.

---

## Troubleshooting

**"My AI doesn't follow the persona well"** — Provide the full persona file, not just the role name. The backstory and interaction style anchor the AI's decisions.

**"The pipeline feels heavy for small changes"** — Use the ad-hoc work gate. The pipeline warns when you skip stages but doesn't block you. Skip to implementation for quick fixes.

**"I only have one AI tool"** — See single-provider fallback above. Level 1 persona reviews work with any single tool.

---

## Next Steps

- [Key Concepts](concepts.md) — Reference for all terminology
- [Why This Architecture?](why.md) — Philosophy behind these decisions
- [Glossary](glossary.md) — Definitions for every term
- [Pipeline details](../teams/engineering/process/pipeline.md) — Deep dive into each stage
- [Committee process](../teams/engineering/process/committee-process.md) — How the review protocol works
