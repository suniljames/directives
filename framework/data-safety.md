# Data Safety

Rules for code paths that delete, rewrite, or disable protection on domain data. Complements [`safety.md`](safety.md) (behavioral never-do rules) — this file is about *designing* destructive paths that must exist.

## Before any delete path

- **Enumerate reverse references by introspection**, never by hand-listing tables. A hand-kept list stops covering whichever model is added next.
- **Cascading deletion is the greater danger, not blocking constraints.** A blocking FK refuses loudly; a cascade takes the children silently — so a fence that checks only blockers reads as thorough while destroying records nobody agreed to lose. Same for null-on-delete: it silently mutates surviving rows.
- **Allow-list what MAY go.** The safe default for the next referencing model added is "blocked", not "deleted". A guard that enumerates what is protected fails open; a guard that enumerates what may go fails closed.
- **Query with the unfiltered manager/scope.** A filtered default scope hides a real blocker.

## Deletion fences

- **The fence runs BEFORE the deletes it guards**, and every subsequent delete is scoped to what the fence *cleared*. A fence evaluated after the deletes reports a save that already didn't happen.
- **Pin both directions in tests**: blocked ⇒ the delete stands down; cleared ⇒ it does not. Watch for second-order blocks — rows you spared may protect rows the same routine was about to delete.
- Derive fence allow-lists from a full fixture, never by widening the list to clear a failure.

## Disabling protection for maintenance

- **Capture the exact prior state; restore the captured state and assert equality.** "Re-enable" is often a weaker verb than what was there (protection modes have more than two states); restoring merely-"enabled" silently downgrades hardening, and a "not disabled" assertion reads green over it.
- Wrap in the closest thing to `try/finally` the layer allows — and know when the layer autocommits (DDL) so there is no rollback to rely on.
- **Found-disabled-on-entry is an incident**, not a baseline to restore. A downgraded state is evidence.
- Prefer scoped, self-expiring bypasses (transaction-local settings) over persistent state toggles. Before adding a bypass, ask whether it is needed at all.

## Values someone is owed

For pay, billing, refunds — any number with a legal or trust obligation attached:

- **A correction needs a reconstructed authority**, not a plausible value. If the live record, its history, and its snapshot disagree, that is an operator decision presented with the cost of each option — never a value you pick to clear a metric.
- **A loud fail-closed refusal beats a silent wrong number.**
- **Read-only surfaces explaining what *was* paid/committed read the frozen record** — never re-derive from the live engine, even a correct one. "What did we pay" and "what would we pay now" are different questions; if a frozen total must be split for display, distribute it so the parts sum by construction.
- Frozen records never silently re-price; corrections are explicit, auditable events.

---
*Distilled from a production multi-agent codebase, 2026-08. See also: [controls-and-detectors.md](controls-and-detectors.md) → Designing guards.*

---
[← Framework index](README.md) · [README](../README.md)
