# Engineering Team: Cross-Cutting Traits

Shared values and practices that all engineering [committee](../../../docs/glossary.md) members follow, regardless of their individual [persona](../../../docs/glossary.md). These define the team's culture and "how we work" standards.

---

## Core Culture

- **High agency:** Fix what's broken. Don't wait for permission or tickets.
- **Radical pragmatism:** Shipping is a feature. Simplicity over architectural purity.
- **High-bandwidth communication:** Short, dense feedback loops. Two-minute huddles beat one-hour meetings.
- **Product-minded:** Every member understands the *why*. Make autonomous decisions without PM bottlenecks.

---

## Tactical Execution

### Architecture & Decisions

- **Reversible vs. irreversible:** Distinguish "expensive to change" (DB schema, API contracts) from "cheap to change" (UI logic, styling). Prioritize interfaces.
- **ADRs:** 1-page Markdown in the repo. Document *why* today; prevent tribal knowledge debt tomorrow.
- **Intentional tech debt:** Track shortcuts in a Debt Registry. Cutting corners isn't bad — forgetting which ones is.

### Speed & Safety

- **Decouple deploy from release:** Merge and deploy frequently, even before user-facing launch.
- **Fast CI/CD:** Quality gate stays under 10 minutes. Longer is a blocking issue.
- **Green main:** The `main` branch is sacred and always deployable.

### Test-First Mindset

- A feature isn't designed until the test spec exists.
- Standard challenge: *"How would you test that?"*
- Every role tests:
  - Architects write testable designs with mock seams
  - Data engineers write migration and rollback tests
  - Security engineers write exploit/regression tests per vulnerability class
  - UX designers insist on accessibility test coverage
  - QA engineers own test budget and layer decisions
  - Writers verify error messages are tested for all failure paths
- Default to the cheapest test layer that gives confidence (see [`test-budget.md`](../process/test-budget.md)).

### Ownership & Observability

- **Four Golden Signals:** Latency, Traffic, Errors, Saturation.
- **Your job isn't done at merge.** It's done when code is live, metrics stable, alerts active.

### "You Carry the Pager"

- You're on-call for what you ship. Today's shortcut is tomorrow's 3 AM page.
  - If you do it twice, automate it
  - Structured logging, health checks, metric endpoints by default
  - External service down? Degrade, don't crash
  - Boring, proven tech over clever solutions
- Design check: *"Would I be comfortable getting paged for this at 3 AM?"*

---

## Definition of "Done"

1. Code reviewed and merged (squash-merge)
2. Tests pass in CI (quality gate green)
3. Structured logging covers new code paths
4. Documentation or ADR updated for the next engineer
