# FAQ

Common questions from people who just found this repo.

---

**Do I need all of this?**

No. There are three adoption levels — [Quick start, Standard, and Full system](getting-started.md#adoption-levels). Quick start takes 15 minutes and uses zero config files — just persona definitions to improve your AI reviews. Add the pipeline or multi-agent setup later when you're ready.

---

**Engineering only?**

No. The architecture is team-agnostic. Engineering is the first fully-built team, but the same structure — [manifests, personas, pipelines](glossary.md) — works for sales, marketing, operations, or any team that uses AI agents. You define your own roles, stages, and vocabulary; the system provides the scaffolding.

---

**Can I use this without engineers?**

To evaluate it, and to run the Quick Start (persona-driven reviews): yes — anyone comfortable prompting an AI can do both. To operate the full pipeline on a real codebase: you'll want at least one person who can read a pull request and judge whether the AI's output is sound, because the pipeline produces code changes someone must be accountable for. What each level requires: [Cost & Requirements](cost-and-requirements.md).

---

**What does it cost?**

The system itself is free ([CC BY 4.0](../LICENSE)). Running it costs AI usage: persona reviews add little over plain prompting; a full 11-persona committee review is many model calls and is the deliberately expensive step. Honest numbers and the two levers that keep spend proportionate: [Cost & Requirements](cost-and-requirements.md).

---

**Need multiple AI tools?**

No. One AI tool works fine. The system includes a [single-provider fallback](getting-started.md#4-single-provider-fallback) that runs builder and validator in separate sessions on the same tool. You lose the benefit of different models' perspectives, but you still get independent review with no shared context.

---

**What if we don't use GitHub?**

Today, the pipeline assumes GitHub — issues, labels, and pull requests are its coordination layer. The personas and review protocol work anywhere you can prompt an AI, but stage tracking and the close gate would need re-plumbing onto your tracker. There is no ready-made adapter.

---

**Is this a framework I install?**

No. It's config files and documentation. Copy the [templates](../templates/README.md) into your project, fill in the blanks, and point your AI tool at them. No packages, no build step. You'll need GitHub, the [`gh` command-line tool](https://cli.github.com) for one setup step, and your AI tool.

---

**Just want better reviews?**

Start with [Quick start](getting-started.md#quick-start-persona-driven-reviews-15-minutes). Pick a [persona](../teams/engineering/personas/README.md) (e.g., Security Engineer), paste the persona file into your AI prompt, and ask it to review your work through that lens.

---

**How is this different from good prompting?**

Three things prompting alone doesn't give you:

1. **Personas** — Character profiles with backstories, expertise, and review lenses that produce deeper, more consistent feedback than "review this for issues."
2. **Pipeline** — A multi-stage workflow with labels and gates; your AI warns you before a step gets skipped, and progress is visible on the issue itself.
3. **Independence** — Splitting builder and validator across different sessions (or different AI models) so the reviewer can't share the builder's blind spots.

See [Why This Architecture?](why.md) for the full rationale behind each of these decisions.

---

**Who maintains this, and can I get help?**

One maintainer ([@suniljames](https://github.com/suniljames)), evolving it from production use. Open a GitHub issue on this repo for questions or proposals — see [CONTRIBUTING](../CONTRIBUTING.md).

---

[Back to README](../README.md) | [Glossary](glossary.md) | [Getting Started](getting-started.md)

---
[← Docs index](README.md) · [README](../README.md)
