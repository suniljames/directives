# Coordination Contracts

Mechanics that let multiple agents (and humans) coordinate through the repo and issue tracker without stepping on each other: comment idempotency, label state machines, machine-readable verdicts, and platform gotchas. The repo is the source of truth — agents coordinate through artifacts, never through inter-agent messages.

## Comment guards (idempotency)

Automated comments need a guard against double-posting — and the guard's design is where controls quietly die.

- **A heading-only guard is spoofable in both directions.** Any account can post a comment starting with the expected heading. The guard then either accepts the counterfeit as the real artifact (fatal when the comment is evidence a gate consumes) or is suppressed by it (silently skipping a post that should have happened). **Filter by author** (the pipeline account of record — designate it once per project, e.g. in the project's contributing/config file, and cite it rather than restating it) plus an anchored prefix match.
- **Include a discriminator in the match string** (the PR number, the round number) so a stale artifact does not suppress the current one.
- **The calling contract must name which of three semantics applies:**
  - `skip` — post once, never again. For one-time reports only.
  - `confirm-overwrite` — ask before replacing.
  - `supersede` — post again unconditionally; newest wins; **every consumer reads the last match, never the first**.
- **A gate's verdict uses `supersede` — a verdict must be correctable.** The failure that produced this rule: a close gate's FAIL message told the operator to "fix and re-run" while its own `skip` guard silently suppressed the re-run. A refusal whose stated way out is inert is worse than one with no exit at all, because the operator stops looking.

## Label state machines

Define every lifecycle label in one table with these columns: **Label | Applied by | Removed by | Gated by** ("gated by" = which command refuses or warns on its presence/absence). This table shape makes unfireable gates visible by construction — a label with a "gated by" entry but no "applied by" entry is a check that can never fire (a real gate checked a label no command had ever applied).

- Separate **lifecycle** labels (ordered, at most one active) from **category** labels (unordered, may coexist).
- **Constants centralize; idioms don't**: names/colors/descriptions live in the canonical table; the create-and-apply snippet may stay inline per command.

## Machine-readable verdict lines

When a comment carries a verdict a downstream step parses:

- **Compute the line from the data, never emit a literal** ([controls-and-detectors.md](../../../framework/controls-and-detectors.md)).
- **Parse it with a line-anchored first-match** (`grep -m1 '^VERDICT_NAME:'`), never a first-line slice — the first line of the artifact is usually the heading, and a `head -1` consumer can never match (a real listener could only ever refuse).
- Under `supersede` semantics, **read the last artifact, not the first** — the first match is the corrected FAIL or the replaced stale PASS.

## Derive-once blocks

For any value every command needs (repo slug, project root, account of record): derive it in one canonical block, **validate it, and abort with a named message if validation fails** — then use it explicitly everywhere. When such a block is copy-pasted, the validation paragraph is what the copies lose; that is the argument for single-sourcing even trivial snippets ([prompt-quality.md](../../../framework/prompt-quality.md)).

## Every control names its listener

A verdict, walkthrough, or report that "someone will check" is unfinished. Name the consumer, and put the check at the natural chokepoint of the workflow (the summary step refuses to run without a green walkthrough) rather than in a separate scheduled watcher that can die silently.

## Platform gotchas (GitHub examples)

- **Issue search does not index comment bodies.** A search-based "nothing references X" conclusion is a confident false negative for anything living in comments. Enumerate explicitly, and write the measurement down *before* acting — the pre-change state becomes unobservable the moment you change it.
- **Programmatic body edits can silently destroy content** (example: `gh api -f body=@file` sends the literal path string, exit 0). Verify body length after every programmatic edit; keep the source file until verified.
- **Workflows triggered on an event replay that event's payload on re-run** — editing the artifact (PR body) does not re-fire the trigger; push a fresh commit to re-trigger.
- **Verify prior steps landed from version-control history, not prose.** A later change claiming an earlier one shipped is not evidence. A step that is a pure data operation leaves no commit and still needs an auditable record.

---
*Distilled from a production multi-agent codebase, 2026-08. See also: [acceptance-and-close.md](acceptance-and-close.md), [fan-out-safety.md](../../../framework/fan-out-safety.md).*

---
[← Process index](README.md) · [README](../../../README.md)
