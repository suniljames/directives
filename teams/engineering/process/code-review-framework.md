# Code Review Framework

The rules for the **Review stage**: how committee members review a PR diff, what severities mean, and what blocks a merge. (Its design-stage counterpart — how the committee reviews a *plan* — is [committee-process.md](committee-process.md).)

## Severity Levels

| Severity | Meaning | Blocks merge? |
|----------|---------|---------------|
| **MUST-FIX** | Correctness bug, security vulnerability, data loss risk, or broken contract | Yes |
| **SHOULD-FIX** | Code quality issue, missing edge case, poor naming, or maintainability concern | Yes (in current round) |
| **NIT** | Style preference, minor suggestion, optional improvement | No |

**Severity governs blocking, not whether a finding gets fixed.** The builder fixes ALL findings — MUST-FIX, SHOULD-FIX, and NIT — in the current round. Follow-up issues are reserved for genuinely new scope needing its own design cycle, never for bugs or in-scope cleanups ("we'll file a follow-up" is how findings die). A NIT differs from a SHOULD-FIX only in that an unresolved NIT cannot hold the merge if a round limit is hit.

Scope note: **a review verdict covers only the diff the reviewer saw.** Lines elsewhere that depend on the changed lines are not vouched for — the full suite, not the review, is the check on those.

## Review Lenses by Role

**Each role's lens lives in its persona file** (`## Code Review Lens` section) — the single home for per-role checklists, so they cannot drift across documents:

| Role | Lens | Skip condition |
|------|------|----------------|
| [UX Designer](../personas/ux-designer.md) | Accessibility, responsive behavior, design-system compliance | No frontend files in the diff |
| [Software Engineer](../personas/software-engineer.md) | Code quality, API patterns, edge cases | — |
| [System Architect](../personas/system-architect.md) | Layer separation, coupling, tenant isolation | — |
| [Data Engineer](../personas/data-engineer.md) | Migration safety, query performance, data isolation | — |
| [AI/ML Engineer](../personas/ai-ml-engineer.md) | LLM integration, prompt-injection risk, cost | No AI/LLM code in the diff |
| [Security Engineer](../personas/security-engineer.md) | Injection, auth bypass, data exposure | — |
| [QA Engineer](../personas/qa-engineer.md) | Coverage, assertion quality, test layers | — |
| [SRE](../personas/sre.md) | Degradation, logging, resource handling | — |
| [Writer](../personas/writer.md) | User-facing copy, comments, commit messages | — |

Projects add technology-specific checklists in their own `docs/developer/code-review-lenses.md`.

**Skip predicates must be able to be true — and able to be false.** Check each against reality: a lens whose skip condition is *always* true in this codebase is a dead seat that reads as active ([controls-and-detectors.md](../../../framework/controls-and-detectors.md) — the unfireable-control class). The irreversible-value lens (see [committee-process.md](committee-process.md) → roster rules) has **no** skip condition and must state its conclusion either way.

**Jurisdiction tie-break** when two lenses claim one finding: the test-infrastructure lens owns the harness, QA owns the assertion, SRE owns the listener, Data owns the predicate.

**Cite helpers for the question they answer, not the domain they live in** — check what a helper takes and what question it answers, not what its module is called. A correctly-named helper answering the wrong question is the hardest bug to re-review.

## Harness Honesty

Cross-cutting checks applied to any change touching CI, tests, or gating scripts — MUST-FIX: any masker that lets a real failure report green, or a change that makes the suite unable to fail:

- `2>&1 | tee` (or any pipe) on a gating command without `pipefail`
- a gating step ending in a bare `true` (or equivalent exit-code discard)
- a results checker that cannot assert an expected artifact **count** — zero results must read RED, not pass
- a quarantine/skip entry with no exit condition
