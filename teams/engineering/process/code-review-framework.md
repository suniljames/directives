# Code Review Framework

Each engineering committee member reviews the PR diff through a role-specific lens.

## Severity Levels

| Severity | Meaning | Blocks merge? |
|----------|---------|---------------|
| **MUST-FIX** | Correctness bug, security vulnerability, data loss risk, or broken contract | Yes |
| **SHOULD-FIX** | Code quality issue, missing edge case, poor naming, or maintainability concern | Yes (in current round) |
| **NIT** | Style preference, minor suggestion, optional improvement | No |

**Severity governs blocking, not whether a finding gets fixed.** The builder fixes ALL findings — MUST-FIX, SHOULD-FIX, and NIT — in the current round. Follow-up issues are reserved for genuinely new scope needing its own design cycle, never for bugs or in-scope cleanups ("we'll file a follow-up" is how findings die). A NIT differs from a SHOULD-FIX only in that an unresolved NIT cannot hold the merge if a round limit is hit.

Scope note: **a review verdict covers only the diff the reviewer saw.** Lines elsewhere that depend on the changed lines are not vouched for — the full suite, not the review, is the check on those.

## Review Lenses by Role

Each project provides its own technology-specific review checklists. Below is the generic focus area for each role.

**Skip predicates must be able to be true — and able to be false.** State each skip condition explicitly per lens, and check it against reality: a lens whose skip condition is *always* true in this codebase is a dead seat that reads as active ([controls-and-detectors.md](../../../framework/controls-and-detectors.md) — the unfireable-control class). The irreversible-value lens (see [committee-process.md](committee-process.md) → roster rules) has **no** skip condition and must state its conclusion either way.

**Jurisdiction tie-break** when two lenses claim one finding: the test-infrastructure lens owns the harness, QA owns the assertion, SRE owns the listener, Data owns the predicate.

**Cite helpers for the question they answer, not the domain they live in** — check what a helper takes and what question it answers, not what its module is called. A correctly-named helper answering the wrong question is the hardest bug to re-review.

### UX Designer
**Skip if:** No frontend files in the diff.
- Accessibility compliance (contrast, alt text, ARIA, focus management)
- Semantic HTML, form UX, tab order, keyboard navigation
- Responsive behavior (mobile-first, touch targets)
- Design system compliance (component library tokens, no hardcoded values)
- Visual hierarchy, motion with reduced-motion respect

### Software Engineer
- Code quality: DRY, dead code, complexity
- Naming clarity, readability (functions under 30 lines)
- API framework patterns: schema validation, dependency injection, proper status codes
- Frontend patterns: server vs client rendering, proper data fetching
- Edge cases: empty inputs, null handling, error states

### System Architect
- Service layer separation (routing -> business logic -> data access)
- Multi-tenancy enforcement, tenant context propagation
- Coupling and cohesion, circular dependencies
- Frontend routing patterns: layouts, error boundaries

### Data Engineer
- Migration safety: reversible, separate data from schema migrations
- Query performance: N+1, missing indexes, eager loading
- ORM patterns: relationships, async sessions, transaction boundaries
- Data isolation policy correctness

### AI/ML Engineer
**Skip if:** No AI/LLM code in the diff.
- API integration: retry logic, timeout handling, cost tracking
- Prompt injection risks, sensitive data in prompts
- Fallback behavior when AI service unavailable
- Token/cost management

### Security Engineer
- Injection vectors (SQL, XSS, template injection)
- Auth bypass: missing middleware, role checks
- Sensitive data exposure in logs, errors, URLs, API responses
- CSRF, secret handling, input validation
- Multi-tenant data leakage

### QA Engineer
- Test coverage for changed/added code
- Edge cases, assertion quality, fixture adequacy
- Test isolation, mock boundaries
- Correct test layer per test budget (cheapest layer that gives confidence)
- Harness honesty (MUST-FIX: any masker that lets a real failure report green, or a change that makes the suite unable to fail):
  - `2>&1 | tee` (or any pipe) on a gating command without `pipefail`
  - a gating step ending in a bare `true` (or equivalent exit-code discard)
  - a results checker that cannot assert an expected artifact **count** — zero results must read RED, not pass
  - a quarantine/skip entry with no exit condition

### SRE
- Error handling: graceful degradation for external services
- Structured logging with context
- Health checks, container resource usage
- Connection handling: timeouts, pool awareness

### Writer
- User-facing copy: helpful errors, clear labels
- API response messages: clear, no sensitive data
- Code comments: explain *why*, not *what*
- Commit message conventions
