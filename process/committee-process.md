# Engineering Committee Process

The engineering committee convenes for critical review of issues requiring cross-functional analysis.

## Core Principles

1. **Sequential, iterative review** — Members post in strict order. Each reads all prior comments.
2. **Overwrite-to-final-consensus** — After deliberation, members whose positions changed overwrite their comments.
3. **Shared component reuse** — Every design must seek reuse opportunities across templates, components, services, and utilities.

## Committee Members

Full persona definitions with backgrounds, expertise, and review lenses are in [`personas/`](../personas/). Shared team culture: [`cross-cutting-traits.md`](../personas/cross-cutting-traits.md).

The committee follows a deliberate funnel order: user impact, then implementation, then cross-cutting concerns, then operability, then communication.

| # | Role | Agent | Persona |
|---|------|-------|---------|
| 1 | UX Designer (15y) | Builder | [`01-ux-designer.md`](../personas/01-ux-designer.md) |
| 2 | Senior Software Engineer (15y) | Builder | [`02-software-engineer.md`](../personas/02-software-engineer.md) |
| 3 | System Architect (15y) | Builder | [`03-system-architect.md`](../personas/03-system-architect.md) |
| 4 | Principal Data Engineer (15y) | Builder | [`04-data-engineer.md`](../personas/04-data-engineer.md) |
| 5 | Principal AI/ML Engineer (15y) | Builder | [`05-ai-ml-engineer.md`](../personas/05-ai-ml-engineer.md) |
| 6 | Principal Security Engineer (15y) | Validator | [`06-security-engineer.md`](../personas/06-security-engineer.md) |
| 7 | Principal QA Engineer (15y) | Validator | [`07-qa-engineer.md`](../personas/07-qa-engineer.md) |
| 8 | Senior SRE (15y) | Builder | [`08-sre.md`](../personas/08-sre.md) |
| 9 | Principal Writer (15y) | Validator | [`09-writer.md`](../personas/09-writer.md) |
| 10 | Engineering Manager (20y) | Builder | [`10-engineering-manager.md`](../personas/10-engineering-manager.md) |
| 11 | Senior PM (15y) | Validator | [`11-pm.md`](../personas/11-pm.md) |

## The Judge (Principal Engineer)

A 20-year veteran who has occupied every seat at this table. Expert in systems thinking and Total Cost of Ownership (TCO). They synthesize the committee's feedback to resolve multidimensional conflicts (e.g., "Model Accuracy vs. Inference Latency" or "Data Depth vs. Privacy Compliance"). Their final plan moves beyond technical "correctness" to prioritize business outcomes, operational sustainability, and the mitigation of technical debt.

## Iterative Review Protocol

- Members post in strict order. Each reads all prior comments before composing their review.
- A member may reference, agree with, challenge, or build on any prior point.
- The Judge posts last, synthesizing all feedback into a final unified plan.
- No parallel posting — comments are produced sequentially so each persona genuinely absorbs prior feedback.

## UX Mockup Generation (UI/UX Changes Only)

- **When:** User-facing UI changes (new page, layout change, new component, modified form, dashboard change). Skip for purely backend/API/infra issues.
- **Design Direction:** Purpose, tone, design system alignment, typography, motion, anti-patterns.
- **Format:** SVG (renders natively in GitHub and browsers).
- **Storage:** `docs/mockups/<issue-number>/` — one directory per issue.
- **Naming:** `<descriptive-name>.svg` (e.g., `dashboard-redesign.svg`, `form-validation-error.svg`).
- **Responsive viewports:** Mobile (<=480px), Tablet (481-1024px), Desktop (>1024px).
- **Multiple states:** Default, error, success, loading for each viewport where they differ.
- **Process:** UX Designer generates mockups, commits to branch, then posts their committee comment with embedded GitHub-relative links to the SVGs. All subsequent members reference these mockups.

## Overwrite-to-Final-Consensus

- **Goal:** A fresh agent reading the issue sees clean, authoritative final reviews — not a debate thread.
- **Timing:** After The Judge posts, members review the full thread one final time.
- **Rule:** Any member whose recommendation, approach, or risk assessment **materially changed** during deliberation overwrites (edits) their original GitHub comment to reflect their final position.
- **UX Designer specifically:** If mockups need revision (based on Writer, Judge, or other feedback): delete old SVGs, generate revised SVGs, commit/push, overwrite comment with new mockup links.
- **Footer marker:** Each overwritten comment includes: `*Updated to final position after committee deliberation.*`
- **The Judge's comment** is always written last and is authoritative by default.

## Process

1. Read the issue and all existing context.
2. **If UI/UX change:** UX Designer generates SVG mockups first (see UX Mockup Generation above).
3. Each member posts their critical review **in order**, reading all prior comments.
4. The Judge synthesizes all feedback into a final, unified plan.
5. **Overwrite-to-final-consensus:** Members whose positions materially changed overwrite their comments.
6. Update issue title and description to include:
   - **Non-technical Explainer** (end-user value proposition)
   - **Technical Details**
   - **Root Cause** (if applicable)
   - **Proposed Solution**
   - **Implementation Plan**
   - **Documentation Updates**
   - **Test Specification**
7. **Fresh-Eyes Validation** (see below).
8. Apply all labels/tags as appropriate.
9. Proceed according to the project's [pipeline mode](pipeline.md#pipeline-modes) — either continue autonomously or notify and wait for authorization.

## Fresh-Eyes Validation

Catches "curse of knowledge" gaps — assumptions the committee made that a future implementer won't share. Inspired by the [Anthropic doc-coauthoring skill](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring)'s "Reader Testing" pattern.

### When
After step 6 (issue description updated) and before step 8 (labels). Mandatory for all committee reviews.

### How
1. Spawn a fresh sub-agent with zero prior context.
2. Provide **only** the updated issue description (not the committee comments or conversation history).
3. Prompt the sub-agent:
   > "You are a senior developer picking up this issue for the first time. Read the issue description below and attempt to produce a step-by-step implementation plan. Flag anything that is ambiguous, assumes context you don't have, or lacks enough detail to implement without guessing. List your questions as bullet points."
4. If the sub-agent flags gaps:
   - The Judge reviews each gap and updates the issue description to address it.
   - Gaps that are genuinely out-of-scope are noted as `[Context: ...]` annotations in the Implementation Plan section.
5. If the sub-agent produces a coherent plan with no questions, validation passes.

### Why This Works
Committee members build context cumulatively — each reads all prior comments. By the Judge's synthesis, the group has deep shared context that may not be fully captured in the issue description. A zero-context sub-agent simulates the experience of the developer who will actually implement the work, ensuring the issue description is self-contained.

## Test Specification Format

The QA Engineer produces a structured **Test Specification** as part of their committee review and as the corresponding section in the issue description. This specification provides Given/When/Then acceptance criteria with explicit layer assignments, enabling the developer to scaffold failing tests as the first implementation step.

```markdown
## Test Specification

### Service Layer
- GIVEN <precondition>
  WHEN <service method call>
  THEN <expected result/side effect>

### API/Endpoint Layer
- GIVEN <auth state>
  WHEN <HTTP method + path>
  THEN <status code, response body>

### Component Layer
- GIVEN <component props/state>
  WHEN <user interaction>
  THEN <rendered output>

### E2E / Browser
- GIVEN <user role, viewport, page state>
  WHEN <user interaction>
  THEN <visible feedback, navigation>
  MARKERS: @smoke | @security | (none)
```

### Rules

- **E2E criteria** that depend on mockup details are annotated `[mockup-dependent]`.
- **During the overwrite phase**, QA updates only criteria whose *behavior* changed (not just UI treatment). Service-layer criteria are typically stable through the overwrite cycle.

## Deployment Failure Escalation

Escalate to the committee if:
- **Deployments repeatedly fail** without clear cause
- **Multiple configuration layers interact** (platform dashboard + config files + CI)
- **Production outage lasts >4 hours** without resolution
- **Cache behavior causes data inconsistency** or serves stale artifacts

The committee provides multidimensional analysis covering:
- **SRE**: Deployment observability gaps, SLO impact, rollback procedures
- **Architecture**: Configuration management, single source of truth
- **Security**: Audit trail, configuration tampering risks
- **Data**: Impact on analytics, user data collection
