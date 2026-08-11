# Verification

How to know a change actually works — as opposed to knowing your tests pass.

**The core problem: a fix and its test come from the same mental model.** A passing suite therefore confirms your assumptions rather than checking them. The only escapes are independent instruments: force the test red, execute the control adversarially, run the real environment, or hand the work to a reviewer who does not share the assumption. Every rule below is one of those instruments.

## Force-red protocol

Proving a test can fail is part of writing it.

1. **Commit before injecting a fault.** File-level restore (`git checkout -- <file>`) reverts every uncommitted edit, and fails outright on an untracked file — leaving the fault in place and contaminating every later result. Restore with `git checkout HEAD -- <file>`, end with a clean `git status`, and re-run green on the restored tree.
2. **Reintroduce the bug → watch the test fail → restore → watch it pass.** A fix verified only in the green direction is unverified.
3. **A force-red that won't go red is a claim about your selector before it is a claim about the test.** Confirm the mutation actually applied (exact node, exact line) and run the baseline in the same breath.
4. **A partial mutation is not a disproof.** A green force-red has three causes — the mutation missed, the mutation was partial (the property is implemented by two conditions), or the test truly can't fail. Assume the first two until eliminated. Also confirm the injected fault is one the code path can actually encounter.
5. Treat an unexpected injection result as a harness failure before believing it.

## Tests

- **A test must not compute the value under test.** If the test derives the expected value with the same helper the production code should call, it passes with every production call site deleted. Let production derive it.
- **The fixture must make the correct answer and the failure-mode answer disagree.** If the right derivation and the lazy fallback produce the same value on your fixture, both implementations pass. Construct data where they differ.
- **Write the test to fail the naive implementation.** Ask what the laziest correct-looking implementation would do, and make an assertion that implementation fails. Where the failure mode is under-reporting, presence assertions are decorative — assert magnitudes and relationships.
- **Assert the definition, not a mention.** `assert name in text` is vacuous when the name appears anywhere else (prose, comments, imports). Extract the line that defines the property and assert on it; a missing definition line reads RED, never green-by-absence.
- **A spec↔spec test never sees the artifact.** Comparing two specifications measures agreement, not correspondence — a contract mandated in N places and satisfied in none passes all N. At least one check must compare the spec to a *produced* artifact, ideally using the consumer's own executable matcher.
- **Anchor source-greps on the call, not the copy.** Well-written modules quote their own behavior in prose, so a regex that can match a docstring reads prose. Prefer AST/structural checks for structural claims.

## Controls and boundaries

- **Prove a control by executing it against adversarial input.** A docstring, a config entry, or a test asserting a token appears in the control's source is not evidence it works. Acceptance criterion for the control's test: it fails when the guard is deleted.
- **Don't claim a boundary you didn't check.** Finish "X is what stops Y" with the query, URL, or grep that verifies it — or weaken the claim. Grep for callers before citing any control as live.
- **A comment asserting something runs — or is impossible — is a claim to verify, not a constraint to design around.** Documented impossibilities are worse than documented behavior: nobody re-tests them, and a false one silently scopes out the correct fix. When you disprove one, grep for its restatements and delete them all.
- **Config declaration is not live state — in either direction.** A declared-but-unset value and a live-but-undeclared value are both real failure modes. Probe the running system, and pair the probe with a negative control (a value that cannot exist) so it can't pass vacuously.

## Environment

- **Run the environment, don't reason about it.** Any plan whose correctness depends on an external system's behavior (database privileges, CI runner provisioning, cloud IAM, container bootstrap) is a hypothesis. Reproduce it on a throwaway instance before writing code. Review catches wrong reasoning; it never catches a wrong shared fact.
- **Verify at the layer the user touches.** Tests validate the layer they target and can exercise a path production never uses. Trace the real runtime path and hit the real endpoint before declaring done.
- **A structural claim about rendered output is verified by rendering** — not by reading the source. (Markdown tables, templates, emails: the renderer catches what N readers miss.)
- **Prove a pre-existing failure in place.** Check out the base revision in the same working tree; a copied snapshot changes the environment and proves nothing. Reproducible is not attributable.

## Independent eyes

- **Specialist review catches what your own tests cannot** — because the specialist does not share your mental model. Brief reviewers adversarially ("try to defeat this"), not confirmationally ("review this"). Expect a finding; a clean pass is the surprising outcome.
- Reviewer *convergence* is not independent confirmation when all reviewers read the same brief — they are reasoning from the same text, not from the system.

---
*Distilled from a production multi-agent codebase, 2026-08. See also: [controls-and-detectors.md](controls-and-detectors.md), [diagnosis.md](diagnosis.md).*
