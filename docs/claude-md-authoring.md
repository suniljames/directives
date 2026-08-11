# CLAUDE.md Authoring Guide

How to write `CLAUDE.md` files that stay lean, load the right context, and don't accumulate clutter over time.

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
- Rule lists that exceed ~10 bullets
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

## Security Note: Third-Party Hooks and Permission Settings

Before enabling third-party tools as Claude Code hooks, consider the interaction with your settings:

**The compound risk:** `skipDangerousModePermissionPrompt: true` removes the confirmation gate for destructive operations. Adding a third-party hook (such as an output interceptor) on top of an already-permissive configuration means both layers trust each other without independent verification.

**When wiring a new hook:**
1. Read the hook source before installing — especially for tools that intercept all shell output
2. Verify provenance: pinned version + checksum, ideally with a published release on a known-good registry
3. Make hooks fail-open (`exec hook-binary || exit 0`) so a crashed hook binary doesn't block agent execution
4. Understand the scope: a `PostToolUse` hook on Bash receives output from **every** shell command in the session — not just the specific tool that triggered it. This includes commands that surface environment variables, API responses, file contents, or data query results. Scope your hook's processing accordingly.
5. Document the tradeoff in your project's `SAFETY.md` or equivalent: what you gave up and why it was worth it

See [`framework/safety.md`](../framework/safety.md) for the framework-level safety rules this doc extends.

---

## Cross-Reference

- [`framework/safety.md`](../framework/safety.md) — framework safety rules
- [`framework/reasoning-framework.md`](../framework/reasoning-framework.md) — how agents navigate code and switch providers
- [`providers/gemini/GEMINI-template.md`](../providers/gemini/GEMINI-template.md) — a validator provider's equivalent of this config (Gemini example)
