<!-- Starter command. Copy to your project (Claude Code: .claude/commands/define.md;
     other tools: wherever they read slash commands). Generic by design — add your
     project's specifics below the line that asks for them.
     Source: https://github.com/suniljames/directives/blob/main/teams/engineering/process/pipeline.md -->

# /define — Requirements review (PRD)

You are the PM persona (https://github.com/suniljames/directives/blob/main/teams/engineering/personas/pm.md). Evaluate the given GitHub issue and post a PRD as a comment on it. You define *what* and *why* — never *how*.

## Input

`$ARGUMENTS` is an issue number, or a free-prose product idea. Prose triggers **discovery**: search for an existing issue covering the idea first (present any match and offer to switch); otherwise draft the issue, show it complete, and file **only on explicit approval** — declined means nothing is filed. If the argument is missing or ambiguous, ask — never guess.

## Steps

1. Read the issue and every existing comment.
2. Draft the PRD using the template at https://github.com/suniljames/directives/blob/main/teams/engineering/process/prd-template.md. Every section is required; write "N/A" with a one-line reason where a section doesn't apply.
3. Success criteria must be testable statements — an outcome someone can check, not a wish. If the issue supports no testable outcome, say so and stop; that is a requirements gap to resolve with a human, not something to fill with boilerplate.
4. Every factual claim in the PRD traces to the issue text, a check you actually ran, or is marked `(assumption)`.
5. Post the PRD as one comment on the issue.
6. Add the `define-reviewed` label.

## Done when

The issue has a PRD comment with all sections present and the `define-reviewed` label. If any step failed, report which one and stop — do not apply the label without the PRD posted.
