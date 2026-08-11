# Cost & Requirements

What this system needs to run, and what it costs. Read this before committing to the Standard or Full System path.

## What you need

- **A GitHub repository** for the project. The pipeline coordinates through GitHub issues, labels, and pull requests — there is no GitHub-free mode today.
- **One AI coding tool** (Claude Code, Antigravity CLI, Cursor, etc.) with a paid plan or API access.
- **The `gh` command-line tool** ([cli.github.com](https://cli.github.com)) for the label setup step, authenticated to an account that can create labels on your repo.
- **A local copy of this repo** (clone or download) to copy templates and commands from — or reference files by URL if your tool can fetch them.
- **For the Full System path only:** a second AI tool, so builder and validator run on different models.

## What you don't need

- No servers, packages, databases, or build steps — nothing installs.
- No engineers on staff to *evaluate* it, and the Quick Start (persona-driven reviews) is runnable by anyone comfortable prompting an AI. Operating the full pipeline on a real codebase does assume someone who can read a pull request — see the [FAQ](faq.md).

## What it costs to run

The system's costs are AI usage costs. Honest guidance, since exact numbers depend on your model and codebase:

- **Persona reviews (Quick Start):** one model call with a bigger prompt. Marginal cost over plain prompting is small.
- **A full committee review (`/design` or `/review`):** 11 personas each reading the issue plus all prior comments, then a synthesis — many long model calls per round, up to 3 rounds. This is the expensive step, and it is deliberate: you are buying independent scrutiny. Budget it for work that warrants it.
- **The whole pipeline per task:** several times the cost of "just ask the AI to build it." The trade is cost and elapsed time for caught defects, auditable decisions, and work a stakeholder can follow.
- **A wide anchor, so you can budget-screen the idea** (from production use at 2026 frontier-model API prices — your numbers will differ): a single persona review adds well under a dollar; a full committee design review on a mid-sized issue lands in the single dollars to low tens of dollars; a complete pipeline run on a real feature, tens of dollars. Wrong for your stack in either direction — which is why the pilot below is the real answer.

Two levers keep spend proportionate:

1. **Not every task needs the committee.** Route small changes through a lighter path and reserve the full roster for risky ones (the engineering team's rules for this: [scope classification](../teams/engineering/process/scope-classification.md)).
2. **Measure a pilot.** Run one real task end-to-end, read your provider's usage dashboard, and set expectations from your own numbers — not from anyone's estimate, including this page's.

---
[← Docs index](README.md) · [README](../README.md)
