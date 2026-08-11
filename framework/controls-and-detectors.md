# Controls, Detectors & Gates

Design rules for anything that watches, blocks, or alerts — CI gates, monitors, guards, lint rules, review gates. The recurring failure is not controls that fire wrongly; it is controls that **cannot fire at all** while everyone believes they are covered.

## Every control must be able to go RED — and must have a listener

A required check that structurally cannot fail is a green light wired to nothing. Two obligations, both mandatory:

1. **Demonstrate the control can fire** before relying on it (see [verification.md](verification.md) — force-red). A control with zero firing history is unproven, and silence from it is not health.
2. **Name the listener.** A detector whose output nobody consumes (a log row, an unread email) is half a control. Put the listener at the natural chokepoint of the workflow it protects, not in a separate scheduled job that can itself die silently.

### The unfireable-control class

Recurring shapes, each found in production (all read green while checking nothing):

- A gate checking a **label/state no process ever sets**.
- A matcher pinned to a **format that appears in zero real artifacts** (spec↔spec tests all agreed; no test compared spec to artifact).
- A skip/convene predicate that is **always true in this codebase** — the seat reads as active while never running.
- An idempotency guard that **suppresses its own stated exit** ("add X and re-run" while the guard silently skips the re-run).
- A first-line slice (`head -1`) on an artifact whose **first line is the heading**, so the pattern can never match.
- An **unwatched cadence claim** ("runs quarterly") with no scheduler and no alarm on absence.

## Fail closed

- **Absence of evidence reads RED, never green.** Zero test results, a missing artifact, an empty audit, an unreachable data source — all RED. An empty result set can never APPROVE.
- **Emit verdicts from computed values, never unconditional literals.** `echo "All passed"` at the end of a step is a lie waiting for its moment. Compute the verdict from the rows; enforce a count invariant (rows rendered == rows counted == rows in the source) and treat disagreement as FAIL — never reconcile by editing the counts.
- **Exit codes must survive the plumbing.** `2>&1 | tee` without `pipefail`, a gating step ending in bare `true`, a summary line that reports the pipe's exit rather than the command's — each discards the real result.
- **Partial verdicts never round up.** FAIL > WAIVED > PASS; a waived row is named, attributed, and visible in the final verdict. All-waived escalates to a human rather than passing — that is an unexercised gate wearing a verdict.
- **A masker may only be removed once the thing it hid is green.** Fix the cause first, then flip the gate fail-closed; un-suppressing over a live failure wedges the main line with the same error inverted. Stage it: honest-but-report-only → fix → gate.

## Detector design

- **A count needs a worklist that shares its predicate.** A metric is half-built until an operator can list the exact rows behind it, from the metric's own query — not a re-expression that can drift.
- **Derive thresholds from measurement, never from design documents.** Measure the real distribution with the same instrument that will do the comparing; record values, sample size, and date beside the constant. An alarm that fires on healthy state trains the muting reflex.
- **Never join through a deletable/nullable key.** If deleting the evidence removes the row from the detector's candidate set, the count *falls* on the incident and the board reads green. Write the join key into an immutable payload at record time; decide both deletion directions deliberately — destroyed evidence must read RED.
- **Exclusions must be unrenewable.** Any carve-out hiding rows from a detector is only as strong as what bounds it. Enumerate every writer that can renew the excluded state; an indefinitely renewable exclusion is a bypass.
- **Prefer state-based detection over exit-code or exception reporting.** A reporter inside the process only sees runs that happened; a detector that surveys resulting state fires on crashed, deleted, suspended, never-provisioned, and never-ran alike.
- **When a design decision removes or derives away a data structure, every predicate written against it goes vacuously green.** After such a ruling, walk every gate and metric that names the structure and ask: can this still read RED? Key controls to the operator-visible condition, not the internal representation.
- **A red control is guilty until the instrument is verified.** Triage the instrument first: can it reach its data? Did it ever succeed? Does its data source predate what it judges? Never accept an Unknown/sentinel reading as an answer.
- **A diagnostic run can destroy the reading.** Before running a monitoring command by hand, ask which service normally runs it and whether it writes. Correct loudly if you clobbered the reading.

## Designing guards

- **Revoking one key is not a control.** Enumerate every path to the same capability (reset, token, SSO, admin override) and gate issuance *and* consumption. Before a new predicate denies anything, size the affected population in production.
- **Read-only is half a lockdown.** When a record anchors a control, blocking deletion is the smaller half — *editing* it reverses the control while leaving it in place. Lock the whole record; derive the locked set by introspection so future fields are locked by default.
- **Harden both halves of a symmetric pair in the same change.** Set/unset, grant/revoke, add/remove: a one-sided rail reads as protection that isn't there, and the destructive half is usually the one left open.
- **A closed path must leave a working exit.** A refusal is unfinished until every state that now reaches it has at least one named exit that you have executed. A refusal whose stated way out is inert is worse than none — the operator stops looking.
- **Close a writer by moving the write into the chokepoint,** not by guarding the call site. A guarded caller is still a writer, and it falsifies the chokepoint's sole-writer claim. Name every sanctioned bypass in the chokepoint's own doc so exclusivity stays checkable.
- **Duck-typed helpers fail soft.** A `getattr`-style accessor handed the wrong type returns a well-formed wrong answer (None, or a sibling object's id) with no exception. Accept types explicitly at id-resolving entry points; test the wrong-type call.
- **A stateless constraint cannot carve out a state transition.** It enforces on the resulting state, not the path, so it cannot exempt a legitimate transition into a forbidden state. Choose prevent-at-storage vs detect-and-alert explicitly.
- **A missing audit row is not evidence the write never happened.** Event hooks bind to specific senders/types and silently skip lookalikes (proxies, subclasses). Prove the write independently before concluding anything from the absence of its record.

---
*Distilled from a production multi-agent codebase, 2026-08. See also: [verification.md](verification.md).*
