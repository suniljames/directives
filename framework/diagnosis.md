# Diagnosis

A discipline for anything reported as broken, failing, flaky, or slow where the cause is not yet **proven**. Teams typically wire it into their pipeline: bug-shaped issues run Phases 0–2 before design, and a bug fix's failing test is the Phase-1 loop (see [`teams/engineering/`](../teams/engineering/process/pipeline.md) for the worked example).

**The core rule: no red-capable check, no theorizing.** Every expensive misdiagnosis starts with a hypothesis formed before holding an instrument that can go red on the actual bug.

## Phase 0 — Rule out the known impostors (5 minutes)

Before reading a line of implementation, check the failures this environment produces that *look like* code bugs: stale caches, unseeded data, shared-state contamination, a dead sync job, a hung wrapper. **Maintain a repo-local impostor list** — every project accumulates its own; the list is the cheapest diagnostic asset you can own.

Also: a red monitoring control is guilty until the instrument is verified ([controls-and-detectors.md](controls-and-detectors.md)); check service status pages before debugging "weird" failures.

## Phase 1 — Build the reproduction loop

Produce **one command you have already run at least once** that goes red on this exact symptom and will go green when fixed. Construction routes, cheapest first: failing test → scripted HTTP call → CLI/management command → browser automation → differential loop → bisect harness. Then tighten: faster, sharper, deterministic. For non-deterministic bugs, raise the reproduction rate rather than chasing a clean repro.

**If you genuinely cannot build a loop, stop and say so** — list what you tried and ask for a captured artifact. Run the environment; don't reason about it.

## Phase 2 — Confirm the exact symptom

The loop must reproduce the *user's* symptom, not a nearby different failure — a nearby failure means a wrong fix that closes the ticket and not the bug. Then minimise the reproduction one cut at a time.

## Phase 3 — Hypotheses before probes

Write 3–5 ranked hypotheses **before testing any**, each with a falsifiable prediction ("if H2, then X will appear in Y"). No prediction = a vibe; discard it. Treat comments and docs as claims to verify, not evidence — grep for the call.

## Phase 4 — One variable at a time

Each probe maps to a named hypothesis's prediction. Tag debug output with a unique prefix so cleanup is one grep.

## Phase 5 — Fix and force red

Watch the loop fail → fix → **reintroduce the bug, watch it fail again, restore** → re-run against the original un-minimised scenario. Full force-red protocol (including commit-before-injecting): [verification.md](verification.md). The permanent regression test must not compute the value under test.

## Phase 6 — Cleanup and retrospective

Remove tagged probes; leave the regression test. Then answer: **which verification layer was missing, and what concrete check would have caught this earlier?** The answer becomes a directive, a gate, or an impostor-list entry — not a memory.

---
*Distilled from a production multi-agent codebase, 2026-08 (structure adapted from the mattpocock/skills bug-diagnosis discipline). See also: [reasoning-framework.md](reasoning-framework.md) → Diagnose mode.*
