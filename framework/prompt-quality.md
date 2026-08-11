# Prompt Quality

Applies whenever you write or edit a file the agent process itself runs on: slash-command specs, agent definitions, root context files (`CLAUDE.md` and counterparts), or a prompt embedded in a script. In an AI-driven shop, **the process is its prompt files, and a prompt defect has the blast radius of a code defect** — defective prompts have caused real outages.

A skill/command file exists to wrangle **determinism** out of a stochastic system. Predictability — the agent taking the same *process* every run — is the root virtue; every check below serves it.

## Checklist

1. **Single source of truth.** Each rule lives in exactly one authoritative place; everything else points there. Two copies of a rule will drift, and the stale copy reads as authority. Corollary: **keep a consumer registry** — every file that points at a contract is listed by the contract, and a test (or review step) fails when a consumer silently drops its pointer. A dropped pointer loses the behavior; that is the quiet failure mode of prompt files.
2. **Checkable completion criteria.** Every step ends on a verifiable done/not-done condition. A gate-shaped step must additionally be *able to be red* ([controls-and-detectors.md](controls-and-detectors.md)).
3. **The no-op sentence test.** Read each sentence alone and ask: does any run behave differently because this sentence exists? If not, delete the whole sentence — don't trim words from it. Vibes ("be careful", "think deeply") fail this test.
4. **Context-load budget.** Every always-loaded line costs every future session. Keep detail behind a pointer, and make the *pointer's wording* — not its target — carry the trigger for when to follow it.
5. **Fail closed on the unhappy path.** State what happens when the input is missing, malformed, or ambiguous. Absence of evidence reads RED, never as success.
6. **No background steps a prompt cannot await.** A prompt that backgrounds a long command ends the turn and never resumes; the step silently never completes.
7. **Prove the edit by executing it.** Run the changed command end-to-end at least once. A prompt is code, and untested code is broken.
8. **Split vs inline.** Split into a separate file only for a distinct independent trigger or material shared by more than one consumer; otherwise inline. Every new file costs cognitive or context load.
9. **Constants centralize; idioms don't.** Shared *values* (names, labels, literals) live in one canonical file; the surrounding *idiom* (the shell snippet that uses them) may stay inline per consumer. When single-sourcing, also record what deliberately must NOT be merged — two similar lists that answer different questions are protected asymmetry, not drift.
10. **Validation is what copies lose.** When a snippet is duplicated across files, the abort/validation half is what goes missing first — which is the argument for single-sourcing even trivial snippets.

## Root context files

Root config (`CLAUDE.md` or counterpart) has one job: behavioral rules and an index. Detail lives in sub-documents loaded on demand. See [claude-md-authoring.md](../docs/claude-md-authoring.md) for the progressive-disclosure checklist. For keeping these files (and every other knowledge store) current without losing hard-won rules, see [knowledge-pruning](../teams/engineering/process/knowledge-pruning.md).

---
*Distilled from a production multi-agent codebase, 2026-08 (checklist core adapted from the mattpocock/skills skill-quality discipline).*
