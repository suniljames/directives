# CLAUDE.md Authoring Guide

For whoever maintains your project's AI config files — skip this if you're evaluating the system. A `CLAUDE.md` is the config file Claude Code reads at the start of every session (other providers read their own equivalent); this guide keeps those files lean, loading the right context without accumulating clutter.

---

## Root CLAUDE.md Contract

The root `CLAUDE.md` has one job: behavioral rules and an index. Nothing else.

**What belongs in the root:**
- Identity and authority rules (which GitHub account, which AI provider)
- Pre-authorized actions (what the agent may do without confirmation)
- Pipeline command table (the five or six slash commands and their stages)
- An index table pointing to sub-documents

**What does not belong in the root:**
- Inline implementation detail ("when doing migrations, always run `make migrate-pg`")
- Environment setup instructions longer than one line
- Rule lists that exceed 8 bullets (the checklist limit below)
- Anything that only applies to one workflow or one file type

If you find yourself writing a paragraph of inline rules, that content belongs in a sub-document. Link to it from the index table.

**Why:** Claude Code loads the root `CLAUDE.md` in every session, regardless of what the session is actually doing. Every line of inline content is a line of irrelevant context for sessions that don't need it. Thin roots mean lower token usage and less cognitive noise.

---

## Sub-Document Structure

Sub-documents live in a referenced directory (typically `docs/developer/` or `.claude/docs/`). Claude Code follows links in the root and loads them on demand.

**When to create a sub-document:**
- The topic has more than 5–6 rules or steps
- The content only applies to a specific workflow (migrations, testing, deploys)
- You're writing a runbook, reference table, or checklist

**Naming conventions:**
- Be specific: `TESTING.md` is better than `DOCS.md`
- Be consistent within your project — pick a casing convention and stick to it across all sub-documents

**How Claude Code loads them:**
Link sub-documents in the root index table with a relative path. Claude Code follows the link and loads the referenced file automatically when the session reaches content that references it. No `@` include syntax is needed — standard markdown links work.

```markdown
| Topic | File | Description |
|-------|------|-------------|
| Testing | See `docs/developer/TESTING.md` | Backend selection, safety directives |
| Workflow | See `.claude/docs/WORKFLOW.md` | Issue lifecycle, commit rules |
```

---

## Progressive Disclosure Checklist

Use this to audit an existing `CLAUDE.md` or review a new one before merging.

**Root file (should be true of every item):**
- [ ] No inline rule list exceeds 8 bullets
- [ ] No inline section exceeds 15 lines
- [ ] Every block of > 5 rules points to a sub-document via a link
- [ ] The index table covers every major workflow the project uses
- [ ] The root file fits on a single screen without scrolling

**Sub-documents (should be true of each one):**
- [ ] The document has a single, clear topic
- [ ] The title matches what the root index calls it
- [ ] Cross-references use relative paths (not absolute URLs pointing to main branch)
- [ ] No duplication of content already in the root

**Common failure modes:**
- "Critical Rules" block growing to 50+ inline lines — move to `CRITICAL_RULES.md` or distribute into topic-specific sub-docs
- Same rule appearing in root and sub-doc — root wins, remove from sub-doc
- Sub-doc growing its own index of sub-sub-docs — flatten or restructure

---

## Security Note: Third-Party Hooks

Hook security rules moved to [`framework/safety.md` → Third-Party Hooks](../framework/safety.md#third-party-hooks-and-permission-settings) — they are safety policy, not authoring style.

---

## Cross-Reference

- [`framework/safety.md`](../framework/safety.md) — framework safety rules
- [`framework/reasoning-framework.md`](../framework/reasoning-framework.md) — how agents navigate code and switch providers
- [`providers/antigravity/GEMINI-template.md`](../providers/antigravity/GEMINI-template.md) — a validator provider's equivalent of this config

---
[← Docs index](README.md) · [README](../README.md)
