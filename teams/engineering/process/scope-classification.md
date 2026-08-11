# Scope Classification

How pipeline commands decide, mechanically and audibly, how much process an issue gets (a lightweight "trivial" path vs the full committee). One classifier, shared by every command — never a per-command copy.

## Two lists, deliberately asymmetric

Maintain two path/topic lists that answer **different questions**, and protect the asymmetry:

- A **broad risky-path list** answers *"does the full committee convene?"* — err inclusive.
- A **narrow high-risk-domain list** answers *"how risky should the operator read this build as?"* — err selective.

Deriving the operator-facing risk tier from the broad list makes nearly every issue read High and destroys the signal; deriving committee convening from the narrow list skips review where it is needed. Both lists are correct, they point opposite ways, **do not harmonise them** — record that intent next to the lists, or a future cleanup will merge them.

## Rule 0: never-trivial overrides

Certain labels/marks force the full path regardless of size, each with its stated reason (a reason-less rule gets deleted by the next confused editor). Record the project's canonical never-trivial list in the same classifier file as the two lists above — one authority, not per-command copies. Examples:

- Freshly-discovered/auto-filed issues — brevity of an auto-drafted body must not skip security review.
- Deletion/dead-code issues — a deletion is never trivial.
- Anything touching an irreversible-value domain (pay, billing, data-retention obligations) — belt-and-braces with the always-on review seat; this rule governs whether the *whole committee* convenes, which is a different question.

## Announce before spending

Print the classification verdict **before any money or review time is spent**: mode, the rule that fired, the roster that will convene, and the override flag that forces the full path. The operator can interrupt a wrong classification only if they see it first. Leave an audit-trail comment naming the rule that fired.

## The trivial path is never silent

The lightweight path still produces its artifacts (test-spec stub, acceptance criteria, audit comment) — it skips deliberation, not evidence. If the issue body supports no falsifiable acceptance criterion, that is itself the signal it is not trivial: reclassify rather than invent filler.

---
*Distilled from a production multi-agent codebase, 2026-08. See also: [committee-process.md](committee-process.md), [fan-out-safety.md](../../../framework/fan-out-safety.md).*
