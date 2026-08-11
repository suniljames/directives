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

Two roster rules:

- **Resolve seats by NAME against the canonical roster, never by ordinal or a count literal.** Renumbering a seat must not silently change who reviews, and a restated count ("all 9") is drift waiting to happen — every prose restatement of roster size eventually disagrees with the table.
- **Domains with irreversible computed values (pay, billing, retention, compliance) get an always-convening seat with no skip predicate.** Its output contract: **state the conclusion either way** — on an unaffected issue, say so in two lines and name *why* there is no path from this change into the critical computation. Silence is not the same claim, and is not falsifiable. Skip predicates on other seats must be conditions that can actually be true in this codebase — a seat whose skip condition always holds reads as active while never running ([controls-and-detectors.md](../../../framework/controls-and-detectors.md)).

## Review Protocol

- Members post in strict order, each reading all prior comments first. (A committee may instead draft in parallel batches for speed — if so, the fan-out follows [fan-out-safety.md](../../../framework/fan-out-safety.md): plan posted before the batch, set-based reconciliation before synthesis.)
- A member may reference, agree with, challenge, or build on any prior point.
- **Member convergence is zero evidence of correctness** — every seat is reasoning from the same issue text, not from the system. Independent confirmation requires an independent instrument (reproduction, the codebase, production data).
- **Before coining any user-facing term, action name, or status label, check how the product already says it** for the nearest analogous object, and cite the precedent.
- Engineering Manager posts last, synthesizing all feedback into a final plan.
- **Synthesis means merging the members' asks, not concatenating them.** A final plan
  that assigns each member's concern its own phase has not been synthesized. The
  Implementation Plan is where PR count is really decided, so apply
  [PR Slicing — fewest, not smallest](pipeline.md#pr-slicing--fewest-not-smallest) here:
  default to one PR, and name a forcing constraint for any boundary you keep.
- In the sequential regime, no parallel posting — each persona genuinely absorbs prior feedback. In the parallel-batch regime, that absorption moves to the reconciliation and synthesis steps instead; pick one regime per review and say which.

## Process

1. Read the issue and all existing context. **Treat the issue body as a hypothesis, not a brief.** Bug-shaped issues ("broken", "failing", "missing") run [Diagnosis](../../../framework/diagnosis.md) Phases 0–2 first, so the committee designs against a *proven* cause; give one member an explicit mandate to reproduce the issue's claims, and state in the synthesis which original claims survived. A confidently-written issue reads as verified and often isn't.
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
   - Acceptance criteria — 4–7 operator-decidable outcomes, each with a falsifier line; see [acceptance-and-close.md](acceptance-and-close.md)
   Consumers cite these sections **by heading name, never by number** — posted artifacts are immutable at rest, so numbering forks across template versions.
7. **Fresh-Eyes Validation** (see below).
8. **Authorization moment** (see below).
9. Apply labels/tags.
10. Proceed per the project's [pipeline mode](pipeline.md#pipeline-modes).

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
[Settings Panel — Mobile](https://github.com/OWNER/REPO/blob/BRANCH/docs/mockups/42/settings-panel-mobile.svg)
```

**Do not:** Use image embed syntax:
```markdown
![Settings Panel](https://raw.githubusercontent.com/OWNER/REPO/BRANCH/docs/mockups/42/settings-panel-mobile.svg)
```

### Auditing mockups (if a mockup-quality gate exists)

- **Rasterize, then audit the rendered image — never the SVG source as text.** Feeding markup to a reviewer produces findings about the markup, not the design.
- If a vision model does the audit, stamp a **sentinel token into each image that the model must echo back**; a mismatch means it never saw the image → the verdict is COULD_NOT_EVALUATE, not a pass.
- **An empty audit can never APPROVE** — fold per-image verdicts fail-closed.
- **Keep severity deliberately coarse** (per-image PASS/FAIL on critical defects). A fine-grained rubric produces hundreds of findings, and noise trains rubber-stamping.

## Overwrite-to-Final-Consensus

- **Goal:** Readers see clean final positions, not a debate thread.
- **Timing:** After Engineering Manager posts, members review the full thread once more.
- **Rule:** Any member whose position **materially changed** edits their original comment to reflect their final stance.
- **UX Designer:** If mockups need revision, delete old SVGs, generate revised ones, commit, overwrite comment.
- **Footer:** `*Updated to final position after committee deliberation.*`
- **Engineering Manager's comment** is always last and authoritative by default.
- **If the synthesis changed the mechanism, re-run this pass for every member whose recommendation assumed the old mechanism** — and re-check the Test Specification for criteria phrased in the old terms.
- **Items marked "optional" or "defer to the synthesizer" must be explicitly decided.** Undecided options vanish silently.

## Fresh-Eyes Validation

Catches assumptions the committee forgot to write down. Inspired by the [Anthropic doc-coauthoring skill](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring)'s "Reader Testing" pattern.

**When:** After step 6 (issue updated), before step 8 (authorization) and step 9 (labels). Mandatory.

**How:**
1. Spawn a fresh sub-agent with zero prior context.
2. Provide **only** the updated issue description (no committee comments).
3. Prompt: *"You are a senior developer picking up this issue cold. Produce a step-by-step implementation plan. Flag anything ambiguous, context-dependent, or too vague to implement without guessing."*
4. If gaps flagged: Engineering Manager updates the description. Out-of-scope gaps get `[Context: ...]` annotations.
5. If the plan is sliced into more than one PR, check that **every boundary past the
   first names a forcing constraint** from
   [PR Slicing](pipeline.md#pr-slicing--fewest-not-smallest). An unjustified boundary —
   or one resting on a reason that section rules out — is a FAIL.
6. Check the required description sections are present, **enumerated by name — never by
   count** (a count literal stays green while the wrong section is missing). Check the
   acceptance criteria parse as issue-specific, falsifiable outcomes
   ([acceptance-and-close.md](acceptance-and-close.md)); boilerplate that cannot go red is a FAIL.
7. If the sub-agent produces a coherent plan with no questions, validation passes.

**Why it works:** Committee members build shared context cumulatively. A zero-context agent simulates the experience of whoever actually implements the work.

## Authorization Moment

Design ends at an explicit operator decision, with value and cost visible together — never a silent slide into implementation.

Render, in one place:

1. **Value** — the PRD's Business Case, matched **by heading name**. If absent, say so with a fixed literal ("No recorded business case") — never invent one.
2. **Cost** — the delivery estimate: PR count with a named forcing constraint per boundary ([PR Slicing](pipeline.md#pr-slicing--fewest-not-smallest)), size, risk tier citing the named input that triggered it, and ongoing operational cost. Ship confidence labels in pairs (stamped vs unstamped must be distinguishable), and attach an action to low confidence ("if two issues are close on cost, decide on value").
3. **Conflict flag** — the product-view cost (PRD) and build-view cost (estimate) are deliberately distinct figures, but must use the **same canonical null spelling**; otherwise the flag fires on every zero-vs-zero pair and trains the operator to ignore the one signal meant to stop them. When the two genuinely disagree, show both.

Then, in **gated mode** (or whenever an operator is present): ask **authorize / defer / discuss** — and wait. In **autonomous mode** the rendered block is still mandatory as the audit record, and the pipeline proceeds — except when the value section is absent or the conflict flag fires, which escalate to a human even in autonomous mode. An estimate is cited from named inputs, never bare judgment; "a bare tier word is an unconditional literal wearing prose."

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
