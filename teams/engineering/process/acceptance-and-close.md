# Acceptance Criteria & the Close Gate

The contract between "the work is described" and "the work may be declared done". Two halves: how acceptance criteria are written (Design/Define time), and how they are verified at close (the Acceptance Walkthrough).

## Acceptance criteria

**Two artifacts, two altitudes — never conflate them:**

| | Acceptance criteria | Test specification |
|---|---|---|
| Audience | Operator (decides "done") | Developer (writes tests) |
| Altitude | Observable system behavior | Given/When/Then per test layer |
| Count | 4–7 items | As many as the design needs (often ~25) |
| Author | Design synthesis | QA |

Rationale: walking an operator through ~25 unit assertions is 25 rows of noise, which trains rubber-stamping — the exact failure the gate exists to prevent.

Rules for each criterion:

- **One observable outcome; the subject is system behavior** — never the code, the tests, or the plan.
- **Every criterion carries a falsifier on its own line: `*Goes red if …*`.** A statement with no stated way to fail is not a criterion; it is a wish, and it will be walked through as ✅ forever.
- **Banned phrasings** (each is either untestable or vacuously true): "clean/maintainable", "intuitive", "performance is acceptable", "no regressions", "all tests pass", "works as described in the plan". The last is the dominant false-GREEN: it carries a real link and a real sentence while proving only that the diff was applied.
- **Self-written test assertions do not satisfy acceptance criteria** — the criteria exist to check the tests' author, not to be authored by them.

Placement rules (these make the criteria machine-findable at close):

- Criteria live in the **issue/ticket body**, never a comment, under one exact anchored heading.
- Match the heading as an **anchored full line plus an absence check on deeper forms** — a `##` heading is a substring of `###`, so the absence half is what discriminates.
- **Exactly one such section.** Zero → the close gate reads RED. More than one → RED, never first-match. A re-run replaces in place.
- The heading IS the token — no parallel marker/ID. A second identity for one section, with nothing asserting the two agree, is a drift class.
- **Precedence is a direction, not a symmetry**: PRD success criteria govern; the body section restates them at implementation altitude; never overwrite upward.

**Honest limit (state it in the contract itself):** this moves the close gate from structural to semantic fail-closed. Nothing detects worthless-but-present criteria mechanically; the listeners are fresh-eyes validation at design time and the operator at close time. A green suite is not a quality signal here.

## The Acceptance Walkthrough (close gate)

Runs at merge/close, after review. Deliberately no committee — the code was already reviewed; this gate checks *outcomes*.

1. **Resolve the criteria source by fixed order, first hit wins:** PRD success criteria (matched by heading name) → issue-body acceptance criteria (via the executable anchored matcher) → else **RED: no auditable criteria**. An empty or prose-only section is not a hit — "all rows ✅" over zero rows is vacuously true. This matcher is deliberately a spec-to-**produced-artifact** check, not spec-to-spec ([verification.md](../../../framework/verification.md)).
2. **One row per criterion. Evidence = a permalink at the merge SHA plus one sentence stating how the evidence would go red.** A bare test *name* is not evidence (tests can be named and inert). "The code implements it" is not evidence. A criterion with no evidence is a ❌ row, never omitted.
3. **Verdict precedence is fixed:** any ❌ → FAIL; else any WAIVED → WAIVED; else PASS. **WAIVED never rounds to PASS anywhere.** Zero passes with some waived → escalate, do not close (an unexercised gate wearing a verdict).
4. **WAIVED is the only exit for an unfulfillable criterion**: operator-attributed, reason in the row, link to the operator's own words, linked follow-up. If operator and pipeline share one identity, the row says so — that is self-attestation, not separation of duties.
5. **The machine verdict line is computed from the rows, never a literal**, and the row counts must equal the criteria in the resolved source — on disagreement, post FAIL and stop. Never reconcile by editing the counts; that is the one edit that hides exactly the row you failed to render.
6. **Render failures first** (❌, then ⚠️, then ✅). Criterion text is untrusted input — render it fenced, newlines collapsed, so it cannot inject a heading or counterfeit the verdict line.
7. **Bypass flags are tiered.** A force flag may skip advisory gates (CI-state checks, label ordering). It never skips: repo-integrity checks, the close-keyword scan, or the walkthrough itself. Every bypass use emits an audit line.
8. Any ❌ → the issue ends OPEN (reopen if a close keyword already fired at merge).

## Close-keyword hazards

- The platform's issue-closing parser has no grammar: **"does NOT close #N" still closes #N**, and possessive forms ("closes #N's last criterion") still fire. Never let a close keyword precede an issue reference, even to deny it.
- **A squash merge promotes commit-message bodies onto the main branch**, where the parser reads them exactly as it reads a PR body. To ship code while keeping an issue open, purge close keywords from the PR body AND every commit body; use "Refs #N".

## Stakeholder summaries

Produce the plain-language summary **only when the issue is closing** — a summary of a slice reads as the whole thing to whoever receives it. The summary step is the walkthrough's *listener*: it refuses to post over a FAIL or a missing walkthrough (absence is a refusal, not a pass), reads the latest walkthrough (verdicts supersede), and names every waived criterion — telling a stakeholder "shipped and verified" over a waived criterion is telling them something untrue.

---
*Distilled from a production multi-agent codebase, 2026-08. See also: [coordination-contracts.md](coordination-contracts.md) (comment guards, machine lines), [pipeline.md](pipeline.md).*
