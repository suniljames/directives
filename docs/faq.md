# FAQ

Common questions from people who just found this repo.

---

**Do I need all of this?**

No. There are three adoption levels — [Quick start, Standard, and Full system](getting-started.md#adoption-levels). Quick start takes 15 minutes and uses zero config files — just persona definitions to improve your AI reviews. Add the pipeline or multi-agent setup later when you're ready.

---

**Engineering only?**

No. The architecture is team-agnostic. Engineering is the first fully-built team, but the same structure — [manifests](glossary.md), [personas](glossary.md), [pipelines](glossary.md) — works for sales, marketing, operations, or any team that uses AI agents. You define your own roles, stages, and vocabulary; the system provides the scaffolding.

---

**Need multiple AI tools?**

No. One AI tool works fine. The system includes a [single-provider fallback](getting-started.md#4-single-provider-fallback) that runs builder and validator in separate sessions on the same tool. You lose the benefit of different model architectures, but you still get independent review with no shared context.

---

**Is this a framework I install?**

No. It's config files and documentation. Copy the [templates](../templates/) into your project, fill in the blanks, and point your AI tool at them. No packages, no dependencies, no build step. Everything runs through tools you already have — GitHub, your AI CLI, and your existing workflow.

---

**Just want better code reviews?**

Start with [Quick start](getting-started.md#quick-start-persona-driven-reviews-15-minutes). Pick a [persona](../teams/engineering/personas/) (e.g., Security Engineer), paste the link into your AI prompt, and ask it to review your PR through that lens. The persona file gives the AI a professional identity that shapes how it thinks about the problem — the difference in feedback quality is immediate.

---

**How is this different from good prompting?**

Three things prompting alone doesn't give you:

1. **Personas** — Character profiles with backstories, expertise, and review lenses that produce deeper, more consistent feedback than "review this for issues." The backstory isn't fluff — it anchors the AI's decision-making.
2. **Pipeline** — A multi-stage workflow with labels and gates that prevents steps from being skipped. Visible progress tracking through GitHub labels.
3. **Independence** — Splitting builder and validator across different sessions (or different AI models) so the reviewer can't share the builder's blind spots.

See [Why This Architecture?](why.md) for the full rationale behind each of these decisions.

---

[Back to README](../README.md) | [Glossary](glossary.md) | [Getting Started](getting-started.md)
