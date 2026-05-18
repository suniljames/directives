# providers/gemini/

LLM provider configuration templates for Gemini CLI.

---

## providers/ vs overlays/

These two directories serve different purposes and should not be confused:

| Directory | Purpose | Example |
|-----------|---------|---------|
| `providers/` | Per-LLM-provider configuration templates — how to prime a specific AI tool for its role | `providers/gemini/GEMINI-template.md` |
| `overlays/` | Domain compliance addenda — rules and vocabulary for regulated industries layered on top of the base process | `overlays/healthcare/` (HIPAA, PHI handling) |

Providers are about *which AI* and *how to configure it*. Overlays are about *what industry* and *what additional rules apply*. A project can use both: Gemini as validator (provider config) in a healthcare app (domain overlay).

---

## Files in this directory

- [`GEMINI-template.md`](GEMINI-template.md) — full reference template for a project `GEMINI.md` file. Covers identity, pipeline commands, session isolation, validator role declaration, and credential safety.

For a minimal starter, see [`templates/GEMINI.md.template`](../../templates/GEMINI.md.template) in the root. Copy that to your project for a quick start; refer to the full template here when you need all sections.

---

## Adding another provider

To add a provider (e.g., `providers/openai/` for a ChatGPT CLI):

1. Create `providers/<provider-name>/README.md` explaining the provider's role in the system
2. Create `providers/<provider-name>/<PROVIDER>-template.md` following the same 5-section structure as `GEMINI-template.md`
3. Add an entry to the [`providers:` list in `agents.yml`](../../agents.yml) with the required fields: `id`, `name`, `binary` (CLI binary name on the system PATH), and `strengths` (short description for assignment rationale)
4. Link from this README and from the root `README.md` reference section
