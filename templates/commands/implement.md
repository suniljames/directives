<!-- Starter command. Copy to your project (Claude Code: .claude/commands/implement.md).
     Add your project's quality-gate command (lint/typecheck/test/build) where marked.
     Source: https://github.com/suniljames/directives/blob/main/teams/engineering/process/pipeline.md -->

# /implement — Test-first implementation

Implement the given GitHub issue test-first on an isolated branch.

## Input

`$ARGUMENTS` is an issue number. Missing or ambiguous → ask; never guess.

## Steps

1. Check the `design-complete` label. If missing, warn ("this design was never committee-reviewed — proceed anyway?") and record the answer.
2. Create an isolated branch (or worktree) named with the issue number. Add the `implementing` label.
3. Read the Test Specification from the issue. No spec → derive minimal given/when/then assertions from the issue description, and say you did. If the issue body lacks acceptance criteria, add 4–7 falsifiable ones now, before any code (https://github.com/suniljames/directives/blob/main/teams/engineering/process/acceptance-and-close.md).
4. Write failing tests first and **commit them before any feature code**. Run them; confirm they fail for the right reason. For a bug fix, the failing test must reproduce the reported symptom — and must not compute the expected value with the same code under test.
5. Implement until green. Run the full quality gate after each meaningful change: `<your project's lint + typecheck + test + build command>`.
6. Refactor once green; commit refactor-only passes separately.
7. Before handoff: all tests green on a full run (not just the ones you touched); state in the PR description whether this change can affect any value a critical downstream computation reads (pay, billing, data-retention) — answer either way, silence is not an answer.
8. If a validator provider is configured (see `agents.yml`), run its review bridge now and proceed only on ALL CLEAR.
9. Push the branch and **open a pull request** referencing the issue (`Refs #N` — use a close keyword only if you intend the merge to close it). Do not merge — that is `/review`'s job.

## Done when

A pull request is open with failing-tests-first history, the full quality gate passes, and the issue carries `implementing`. Any gate you could not run → say which and stop; never report green you didn't see.
