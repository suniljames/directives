<!-- Starter command. Copy to your project (Claude Code: .claude/commands/design.md).
     Source: https://github.com/suniljames/directives/blob/main/teams/engineering/process/committee-process.md -->

# /design — Committee design review

Convene the engineering committee on the given GitHub issue: every persona reviews in order, the Engineering Manager synthesizes, and the issue description becomes a self-contained spec.

## Input

`$ARGUMENTS` is an issue number. Missing or ambiguous → ask; never guess.

## Steps

1. Check the `define-reviewed` label. If missing, warn ("requirements were never PM-reviewed — proceed anyway?") and record the answer; this gate warns, it does not block.
2. If the issue reports something broken, prove the cause first (https://github.com/suniljames/directives/blob/main/framework/diagnosis.md, Phases 0–2). The committee designs against a proven cause; treat the issue body as a hypothesis.
3. Each persona in the manifest's review order (https://github.com/suniljames/directives/blob/main/teams/engineering/manifest.yml) posts one review comment, reading all prior comments first. Resolve seats by name against the manifest, never by position number.
4. The Engineering Manager posts last, **merging** the members' asks into one plan — not concatenating them. Default the plan to ONE pull request; every additional PR must name a forcing constraint (https://github.com/suniljames/directives/blob/main/teams/engineering/process/pipeline.md — "PR Slicing").
5. Update the issue description with the sections the process defines, including a Test Specification and 4–7 acceptance criteria, each with a `*Goes red if …*` line (https://github.com/suniljames/directives/blob/main/teams/engineering/process/acceptance-and-close.md).
6. Fresh-eyes validation: a new session with zero context reads only the updated description and must produce a coherent implementation plan without questions. Gaps found → fix the description and re-check.
7. Add the `design-complete` label.

## Done when

The issue description is a self-contained spec (fresh-eyes passed), the thread shows every persona's review plus the synthesis, and `design-complete` is applied. Any earlier step failed → report which and stop; do not label.
