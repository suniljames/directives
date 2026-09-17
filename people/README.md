# People

Personal directives: how a specific person expects an AI assistant to engage with them and to write for them. `teams/` defines the agents; `people/` defines who they work for.

This is the tier above the team scaffolding, and it is orthogonal to it. A personal profile travels with the person across every project, every org, and every assistant. It is vendor-neutral: no profile here names a model or a tool.

| Profile | Whose |
|---|---|
| [`sunil-james/`](sunil-james/README.md) | Sunil James. The worked example: a working agreement plus a writing style guide. |

## Changing these files

`AI.md` at the repo root and everything under `people/` is a live instruction set that assistant accounts read every day. Before committing any change to them:

1. **Let the hook run.** A `pre-commit` hook runs the checker automatically on any commit touching these files. Activate it once per clone with `git config core.hooksPath hooks` (see [`hooks/`](../hooks/README.md)), and verify with `git config --get core.hooksPath`. To check by hand at any point: `python3 scripts/check-personal-directives.py`.
2. **Bump the revision date when a rule changes.** `AI.md` carries that date twice: the `**Revision:**` line and the `[directives YYYY-MM-DD]` receipt token that assistants echo back. Change both, or the receipt stops distinguishing a fresh fetch from a cached one. Cosmetic edits don't need a bump; rule changes do.
3. **Change a rule everywhere it lives.** `sunil-james/paste-block.md` duplicates a subset of `AI.md` by hand, because it has to work in instruction fields that cannot fetch a URL. The checker warns when `AI.md` moves without it.
4. **Keep instruction files vendor-neutral.** Write "you" or "the assistant." A profile's own `README.md` is operator documentation and may name platforms where setup requires it.
5. **Don't quietly assert a rule the person didn't state.** If a change adds a rule inferred from context rather than one they gave you, mark it in place with the `***SKJ***` marker and a note on where it came from, then ask. Only they can rule on it.
6. **No em dashes.** The hardest rule in the style guide and the easiest to reintroduce while editing. The checker catches it.

To add a profile, copy the shape of `sunil-james/`: a `README.md` index, a working agreement (how to engage), and a style guide (how to write). Keep both files free of vendor names so any assistant can read them.

---
[← Back to README](../README.md)
