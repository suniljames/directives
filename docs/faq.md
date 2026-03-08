# FAQ

Common questions from people who just found this repo.

---

**Do I need all of this?**

No. Three adoption levels — pick one. [Level 1](getting-started.md#level-1-persona-driven-reviews-15-minutes) takes 15 minutes and uses zero config files. Add pipeline or multi-agent setup later if you want.

---

**Engineering only?**

No. The architecture is team-agnostic. Engineering is the first fully-built team, but the same structure — [manifests](glossary.md), [personas](glossary.md), [pipelines](glossary.md) — works for sales, marketing, operations, or any team that uses AI agents.

---

**Need multiple AI tools?**

No. One AI tool works fine. The system includes a [single-provider fallback](getting-started.md#step-4-single-provider-fallback) that runs builder and validator in separate sessions on the same tool.

---

**Is this a framework I install?**

No. It's config files and documentation. Copy the [templates](../templates/) into your project, fill in the blanks, and point your AI tool at them. No packages, no dependencies, no build step.

---

**Just want better code reviews?**

Start with [Level 1](getting-started.md#level-1-persona-driven-reviews-15-minutes). Pick a [persona](../teams/engineering/personas/) (e.g., Security Engineer), paste the link into your AI prompt, and ask it to review your PR through that lens. Done.

---

**How is this different from good prompting?**

Three things prompting alone doesn't give you:

1. **Personas** — character profiles with backstories, expertise, and review lenses that produce deeper feedback than "review this for issues."
2. **Pipeline** — a multi-stage workflow with labels and gates that prevents steps from being skipped.
3. **Independence** — splitting builder and validator across different sessions (or different AI models) so the reviewer can't share the builder's blind spots.

See [Why This Architecture?](why.md) for the full rationale.

---

[Back to README](../README.md) | [Glossary](glossary.md) | [Getting Started](getting-started.md)
