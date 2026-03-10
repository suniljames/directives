# Engineering Committee Process

> **How to read this:** This document defines the protocol for multi-persona reviews of GitHub issues and PRs. The [committee](../../../docs/glossary.md) is your team's full roster of [personas](../../../docs/glossary.md) reviewing work in sequence. Start with Core Principles, then read Process for the step-by-step flow.

## Core Principles

1. **Sequential review** — Members post in strict order. Each reads all prior comments first. This builds cumulative insight — later reviewers can build on, challenge, or extend earlier observations rather than duplicating them.
2. **[Overwrite-to-consensus](../../../docs/glossary.md)** — After deliberation, members whose positions changed edit their comments to show final positions. Readers see clean conclusions, not a debate thread they need to interpret.
3. **Shared component reuse** — Every design must seek reuse opportunities across templates, components, services, and utilities.

## Committee Members

> **Canonical roster:** [`manifest.yml`](../manifest.yml) — roles, agent assignments, review order.

Full persona definitions: [`personas/`](../personas/). Shared culture: [`cross-cutting-traits.md`](../personas/cross-cutting-traits.md).

The review order follows a deliberate funnel: user impact → implementation → cross-cutting concerns → operability → communication. This ensures foundational questions (does it solve the right problem?) are settled before detailed ones (is the error message clear?).

| Role | Agent | Persona |
|------|-------|---------|
| UX Designer | Builder | [`ux-designer.md`](../personas/ux-designer.md) |
| Software Engineer | Builder | [`software-engineer.md`](../personas/software-engineer.md) |
| System Architect | Builder | [`system-architect.md`](../personas/system-architect.md) |
| Data Engineer | Builder | [`data-engineer.md`](../personas/data-engineer.md) |
| AI/ML Engineer | Builder | [`ai-ml-engineer.md`](../personas/ai-ml-engineer.md) |
| Security Engineer | Validator | [`security-engineer.md`](../personas/security-engineer.md) |
| QA Engineer | Validator | [`qa-engineer.md`](../personas/qa-engineer.md) |
| SRE | Builder | [`sre.md`](../personas/sre.md) |
| Writer | Validator | [`writer.md`](../personas/writer.md) |
| Engineering Manager | Builder | [`engineering-manager.md`](../personas/engineering-manager.md) |
| PM | Validator | [`pm.md`](../personas/pm.md) |

## Review Protocol

- Members post in strict order, each reading all prior comments first.
- A member may reference, agree with, challenge, or build on any prior point.
- Engineering Manager posts last, synthesizing all feedback into a final plan.
- No parallel posting — sequential so each persona genuinely absorbs prior feedback.

## Process

1. Read the issue and all existing context.
2. **If UI/UX change:** UX Designer generates SVG mockups first (see below).
3. Each member posts their review **in order**, reading all prior comments.
4. Engineering Manager synthesizes all feedback into a final plan.
5. **Overwrite-to-consensus:** Members whose positions materially changed edit their comments.
6. Update issue title and description:
   - Non-technical Explainer (end-user value)
   - Technical Details
   - Root Cause (if applicable)
   - Proposed Solution
   - Implementation Plan
   - Documentation Updates
   - Test Specification
7. **Fresh-Eyes Validation** (see below).
8. Apply labels/tags.
9. Proceed per the project's [pipeline mode](pipeline.md#pipeline-modes).

## UX Mockup Generation (UI/UX Changes Only)

- **When:** User-facing UI changes. Skip for backend/API/infra issues.
- **Format:** SVG. Renders natively in GitHub's blob viewer.
- **Storage:** `docs/mockups/<issue-number>/`
- **Viewports:** Mobile (<=480px), Tablet (481-1024px), Desktop (>1024px)
- **States:** Default, error, success, loading for each viewport where they differ.
- **Process:**
  1. Generate SVGs into `docs/mockups/<issue-number>/`.
  2. Commit and push to the working branch.
  3. Construct blob links: `https://github.com/<owner>/<repo>/blob/<branch>/docs/mockups/<issue-number>/<filename>.svg`
  4. Post a comment with clickable text links. Subsequent members reference these.

### SVG Linking in GitHub Issues

GitHub's Content Security Policy blocks inline rendering of SVGs from `raw.githubusercontent.com`. Image embeds (`![alt](raw.githubusercontent.com/...)`) produce broken images or plain-text downloads.

**Do:** Use markdown text links pointing to the blob URL:
```markdown
[Portal Chooser — Mobile](https://github.com/OWNER/REPO/blob/BRANCH/docs/mockups/42/portal-chooser-mobile.svg)
```

**Do not:** Use image embed syntax:
```markdown
![Portal Chooser](https://raw.githubusercontent.com/OWNER/REPO/BRANCH/docs/mockups/42/portal-chooser-mobile.svg)
```

## Overwrite-to-Final-Consensus

- **Goal:** Readers see clean final positions, not a debate thread.
- **Timing:** After Engineering Manager posts, members review the full thread once more.
- **Rule:** Any member whose position **materially changed** edits their original comment to reflect their final stance.
- **UX Designer:** If mockups need revision, delete old SVGs, generate revised ones, commit, overwrite comment.
- **Footer:** `*Updated to final position after committee deliberation.*`
- **Engineering Manager's comment** is always last and authoritative by default.

## Fresh-Eyes Validation

Catches assumptions the committee forgot to write down. Inspired by the [Anthropic doc-coauthoring skill](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring)'s "Reader Testing" pattern.

**When:** After step 6 (issue updated), before step 8 (labels). Mandatory.

**How:**
1. Spawn a fresh sub-agent with zero prior context.
2. Provide **only** the updated issue description (no committee comments).
3. Prompt: *"You are a senior developer picking up this issue cold. Produce a step-by-step implementation plan. Flag anything ambiguous, context-dependent, or too vague to implement without guessing."*
4. If gaps flagged: Engineering Manager updates the description. Out-of-scope gaps get `[Context: ...]` annotations.
5. If the sub-agent produces a coherent plan with no questions, validation passes.

**Why it works:** Committee members build shared context cumulatively. A zero-context agent simulates the experience of whoever actually implements the work.

## Test Specification Format

QA Engineer produces a structured spec as part of their review and the issue description. Given/When/Then with explicit layer assignments:

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

- E2E criteria dependent on mockups are annotated `[mockup-dependent]`.
- During overwrite phase, QA updates only criteria whose *behavior* changed. Service-layer criteria are typically stable.

## Deployment Failure Escalation

Escalate to the committee when:
- Deployments repeatedly fail without clear cause
- Multiple configuration layers interact (platform + config files + CI)
- Production outage >4 hours without resolution
- Cache behavior causes data inconsistency

Committee analysis covers: SRE (observability, rollback), Architecture (config management), Security (audit trail), Data (analytics impact).
