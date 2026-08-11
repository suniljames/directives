# Antigravity CLI (provider config)

Configuration for **Antigravity CLI** — the default validator provider in [`agents.yml`](../../agents.yml). Antigravity is a Gemini-based agentic CLI: its binary is `agy`, and it reads a `GEMINI.md` context file at the project root (the filename comes from its Gemini lineage).

---

## providers/ vs overlays/

| Directory | Purpose | Example |
|-----------|---------|---------|
| `providers/` | Per-provider configuration templates — how to prime a specific AI tool for its role | `providers/antigravity/GEMINI-template.md` |
| `overlays/` | Domain compliance addenda — rules for regulated industries, layered on top of the base process | `overlays/healthcare/` (HIPAA, PHI handling) |

Providers are about *which AI* and *how to configure it*. Overlays are about *what industry* and *what additional rules apply*. A project can use both: Antigravity as validator (provider config) in a healthcare app (domain overlay).

## Which provider should back which role?

[`agents.yml`](../../agents.yml) records each provider's `strengths` for exactly this decision. The shipped defaults: **Claude Code** as builder (content creation, iterative refinement, tool use, delivery) and **Antigravity** as validator (analysis, review, specification, documentation). Either can play either role — see [role swap](../../framework/agent-architecture.md).

## Files in this directory

- [`GEMINI-template.md`](GEMINI-template.md) — full reference template for a project's `GEMINI.md`. Covers identity, pipeline commands, session isolation, validator role declaration, and credential safety.

For a minimal starter, see [`templates/GEMINI.md.template`](../../templates/GEMINI.md.template). Copy the starter for a quick setup; use the full template when you need all sections.

---

## Adding another provider *(maintainers)*

To add a provider (e.g., `providers/openai/` for a ChatGPT CLI):

1. Create `providers/<provider-name>/README.md` explaining the provider's role in the system.
2. Create `providers/<provider-name>/<CONTEXT-FILE>-template.md` following the same 5-section structure as [`GEMINI-template.md`](GEMINI-template.md), named for the context file that provider actually reads.
3. Add an entry to the [`providers:` list in `agents.yml`](../../agents.yml): `id`, `name`, `binary` (CLI binary name on the system PATH), and `strengths`. Every provider directory must have a matching `agents.yml` entry — an example that isn't in the config is a broken example.
4. Link from this README and from the root `README.md` reference section.

---
[← Back to README](../../README.md)
