# Pipeline & Workflow

End-to-end development lifecycle. Each stage produces artifacts the next stage consumes.

> **Canonical stage definitions:** [`manifest.yml`](../manifest.yml) — stages, labels, agent assignments.

## Pipeline Modes

Projects choose one of two modes in their `CONTRIBUTING.md`:

| Mode | Behavior | Best for |
|------|----------|----------|
| **Autonomous** | No human review gates. Pipeline runs end-to-end without stopping. | Solo AI agent, trusted automation |
| **Gated** | Agents notify and wait for human authorization before creating PRs and merging. | Teams with human contributors, early-stage projects |

Default: **autonomous**. To use gated mode, add to your project's `CONTRIBUTING.md`:

```markdown
pipeline-mode: gated
```

In gated mode, the committee process pauses after Design and after Review to wait for human authorization. See [`committee-process.md`](committee-process.md) step 9.

## Stages

| Stage | Purpose | Produces | Label |
|-------|---------|----------|-------|
| **1. Define** | Evaluate the issue, write a PRD with acceptance criteria | PRD comment on the GitHub issue | `define-reviewed` |
| **2. Design** | Engineering committee reviews feasibility, architecture, UX, security | Design decision + test specification comments | `design-complete` |
| **3. Implement** | TDD: scaffold failing tests -> implement -> green -> refactor | Code in a feature branch, all tests passing | `implementing` |
| **4. Review** | CI gate -> eng-committee code review (up to 3 rounds) -> squash merge | Merged PR | `merged` |
| **5. Deploy & Verify** (automatic) | Rebuild, health check, close issue | Running deployment | Issue closed |
| **6. Summarize** (optional) | Plain-language stakeholder summary | Summary comment | `summarized` |

Each agent implements this pipeline using its own tooling. The labels and artifacts are the shared contract — tooling is agent-specific.

## Label Lifecycle

```
Define      -> adds `define-reviewed`
Design      -> checks `define-reviewed`, adds `design-complete`
Implement   -> checks `design-complete`, adds `implementing`
Review      -> checks CI + labels, after merge: adds `merged`, removes `implementing`
Summarize   -> adds `summarized` (optional, after deploy)
```

## Ad-hoc Work Gate

When working on issues **without** using the full pipeline (e.g., quick fixes, ad-hoc tasks), check for lifecycle labels before creating a PR:

- If `define-reviewed` is missing: the PM hasn't reviewed the requirements
- If `design-complete` is missing: the committee hasn't reviewed the design

If either label is missing, warn:

> **Lifecycle labels missing on #\<issue\>:**
> - [ ] `define-reviewed` (PM review)
> - [ ] `design-complete` (committee review)
>
> Skipping stages may result in incomplete requirements or unreviewed designs. Proceed anyway? [Y/n]

If confirmed, add a note to the PR description:
> **Note:** This PR skipped the following lifecycle stages: ...

This gate is advisory — it warns and asks for confirmation, but does not hard-block.

## Who Does What

| Stage | Validator (Adversarial Peer) | Builder |
|-------|-----------|---------|
| 1. Define | Writes the PRD, adds `define-reviewed` | — |
| 2. Design | Security + QA lenses, test specification | Architecture, UX, data, SRE lenses |
| 3. Implement | — | TDD: scaffold tests -> implement -> green |
| 4. Review | Security + QA review, post findings | Addresses ALL findings, merges |
| 5. Deploy & Verify | — | Rebuild, health check, close issue |
| 6. Summarize | Writer summary | — |

### Adversarial Mandate
The Validator MUST act as an **adversarial peer**. It does not default to
agreement. Its role is to challenge implementation risks, identify mechanical
flaws, and advocate for architectural integrity.

### Fix-ALL Mandate
The Builder MUST fix **ALL** findings from a `/review` (MUST-FIX, SHOULD-FIX,
and NITs). Follow-up issues are reserved strictly for significant architectural
shifts or feature expansions.

## Handoff Protocol

- **The repo is the source of truth.** All handoffs happen through files, PR comments, and issue comments — never through inter-agent messages.
- **Structured artifacts** follow defined formats (see [`committee-process.md`](committee-process.md) for test spec format, [`prd-template.md`](prd-template.md) for PRDs).
- **Label-driven coordination.** Agents check GitHub issue labels to determine which pipeline stage is complete before proceeding.
- **Machine-to-Machine Signaling.** Use `review:in-progress` labels for
  visibility and detailed comment "data packets" for handoffs.
- **Coordination log.** For multi-agent projects, use a [`WORKLOG.md`](../../../templates/worklog.md.template) to track current context and handoff state.

## Implement Workflow (Stage 3)

### 1. Setup
- Create isolated branch or worktree
- Verify dev services are running

### 2. Scaffold Tests (RED)
1. Read the **Test Specification** from the GitHub issue
2. If no Test Specification: write 2-3 criteria from the issue description
3. Write failing tests at appropriate layers (see [`test-budget.md`](test-budget.md))
4. Commit: `test(#<issue>): scaffold failing tests`
5. Run tests to confirm they fail correctly

> **Service tests first.** Start with the cheapest test layer — fastest, no UI dependency.

### 3. Implement (GREEN -> REFACTOR)
- Write minimum code to pass tests
- Run the full quality gate after each meaningful change
- Refactor once green
- Commit early and often

### 4. Verify (pre-PR)
- All tests GREEN
- Full quality gate passes (lint + typecheck + test + build)
- **Automated Validator Bridge.** Call `gemini /review` (or equivalent).
- **Only proceed to Review if the Validator returns ALL CLEAR.**

## PR Slicing — fewest, not smallest

**Default to ONE PR.** The target is the largest change that can be safely shipped and
verified at once — never the smallest reviewable diff. Every boundary past the first must
name a forcing constraint from the closed list below, **in the recommendation itself**. A
boundary with no named constraint is a defect in the plan, not a style preference.

Why this is a rule and not advice: a plan that states a PR count without attaching an
objective to it leaves a vacuum, and the default prior — small PRs are virtuous — fills
it. Two structural forces push the same way. A committee has many members each raising
their concern as a separable slice, and a synthesis step that concatenates rather than
merges turns every member's ask into its own phase. And splitting is the blame-safe
choice for whoever proposes it: nobody is criticized for five PRs, while one large PR
that goes wrong is visible. The result is a plan optimized for the proposer's comfort
rather than for delivery.

**The cost being minimized is real.** Each boundary is a full CI run, a review round, a
merge, and a rebase-collision window against every other branch in flight. On most teams
that pipeline latency, not diff size, is the binding constraint on how fast work lands.
Reviewer attention is a real cost too — but it is paid per *concept*, and splitting one
concept across phases raises it rather than lowering it.

### Legitimate reasons to split

A second (or third) PR is justified **only** by one of these, named explicitly:

1. **Deploy or data sequencing through the live environment.** A migration or backfill
   must be applied and verified in production before the code depending on it can ship;
   or a suppression may only be removed after the failure it hid is actually fixed.
2. **Ship-dark-then-enable.** Something ships inert and is switched on as a separate,
   separately-authorized step — because enabling it before the environment is clean would
   make it fire on known-bad state from birth. Merging these two is a defect, so this
   split is mandatory rather than merely permitted.
3. **A human or console step must run between the halves** — a flag flip, an
   infrastructure setting, a credential rotation: anything not present in the diff.
4. **Part of the scope is still awaiting authorization.** Ship what is authorized.
5. **A half is genuinely blocked** on an external answer, vendor, or upstream fix, and
   the unblocked half delivers standalone value.

Anything not on this list merges into the preceding PR. Extending the list is a change to
this document, not a per-issue judgment call.

### Not reasons to split

Each of these is a reason to write a clearer PR description, never to open a second PR:

- "reviewability" / "easier to review" / "smaller diff"
- "logical separation" / "separation of concerns" / "distinct layers"
- tests, docs, or bookkeeping files in their own PR
- one PR per committee member, per file, per module, or per acceptance criterion
- "de-risking" with no named forcing constraint — an untestable half is not lower risk,
  it is unverified for longer
- "the issue lists N deliverables" — a deliverable list is not a merge plan

### Do not wait to be asked

If the question *"in how few PRs can this be delivered, and why?"* would lower the
number, then the lower number was the recommendation. Present that one, with the forcing
constraint stated for each boundary you kept. An operator having to ask means the plan
was optimizing for the wrong thing.

**Genuinely multi-phase issues** — those where a boundary is forced by the list above —
complete each phase as a separate PR, in the stated order.

## Session Isolation

- **Every code change must be associated with a GitHub issue.**
- **The main checkout must stay on `main`.** All feature work happens in isolated branches or worktrees.
- **Issue-Number Worktree Naming.** Worktrees MUST be named with the issue
  number (e.g., `issue-1523`) for easy identification and session auditing.
