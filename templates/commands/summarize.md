<!-- Starter command. Copy to your project (Claude Code: .claude/commands/summarize.md).
     Optional stage — run it when non-technical stakeholders follow the work.
     Source: https://github.com/suniljames/directives/blob/main/teams/engineering/manifest.yml -->

# /summarize — Stakeholder summary

Write a plain-language summary of what shipped for the given issue, posted as an issue comment. The reader is a non-technical stakeholder.

## Input

`$ARGUMENTS` is an issue number. Missing or ambiguous → ask; never guess.

## Steps

1. Confirm the issue's work is actually finished: PR merged, issue closing or closed, and — if your process ran an acceptance walkthrough — its verdict is green. **A missing or failed walkthrough is a refusal, and a summary of unfinished work reads as finished to whoever receives it — if anything remains, refuse and say what remains.**
2. Read the merged PR and the issue thread.
3. Write ≤300 words: what changed for the people who use the product, why it matters, and anything the reader must do. No section headers, no jargon, short sentences; describe actions as what a person does in a browser.
4. If anything the issue promised was NOT delivered or was deferred, name it — a summary that omits the gap tells the stakeholder something untrue.
5. Post as one comment; add the `summarized` label.

## Done when

The issue has a plain-language summary comment and the `summarized` label — or your refusal naming what's unfinished.
