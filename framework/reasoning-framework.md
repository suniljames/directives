# Reasoning Framework

Scale reasoning depth to problem complexity. Simple questions get simple answers. Complex problems get full analysis.

## Core Loop

1. **Understand** — What's the real problem?
2. **Explore** — What are the options?
3. **Plan** — What's the approach?
4. **Execute** — Implement incrementally
5. **Review** — Does the output match the plan? Quality checks passing? Edge cases handled?
6. **Verify** — Does it actually work? Did I solve the right problem? Use independent instruments, not re-reads of your own reasoning ([`verification.md`](verification.md)). Two rules with no exceptions: run the environment rather than reasoning about it when correctness depends on an external system's behavior, and treat comments/docs as claims to verify, not evidence.

## Complexity Triggers (go deeper when present)

- Multiple files, systems, or stakeholders involved
- Unclear requirements
- Performance-sensitive work
- Security or compliance implications
- Breaking changes to existing contracts or interfaces

## Task Modes

Teams instantiate these modes for their domain. The pattern is universal; the specifics change.

**Create**: Define requirements first. **Verify quality BEFORE finalizing** (except exploratory work — mark with `[SPIKE]`). Consider extensibility. Validate as you go.

**Diagnose**: follow [`diagnosis.md`](diagnosis.md) — the core rule is *no red-capable check, no theorizing*:
1. **Rule out known impostors** — environment failures that look like code bugs (keep a repo-local list)
2. **Reproduce** — one already-run command that goes red on the exact symptom, green when fixed
3. **Hypotheses** — 3-5 ranked, each with a falsifiable prediction; no prediction = discard
4. **Evidence** — one variable at a time, each probe mapped to a prediction
5. **Fix & force red** — minimal root-cause change; reintroduce the bug, watch it fail, restore
6. **Retrospective** — name the missing verification layer and the check that would have caught it earlier

**Restructure**: Validate first. One change at a time. Preserve behavior.

**Review**: Correctness > style. Flag what matters, ignore what doesn't.

## Project Integration

- Read project config files first (CLAUDE.md, any counterpart provider context files, CONTRIBUTING.md)
- Match existing patterns (naming, conventions, structure)
- Leave things better than you found them

### LSP-First Code Navigation

When a symbol's location is known (a class name, function, import), prefer semantic lookups over exploratory file reads:

- Use `goToDefinition`, `findReferences`, `hover` via the LSP integration rather than reading whole files to locate a symbol
- For Python projects: install [Pyright](https://github.com/microsoft/pyright) as the LSP server; also install [`django-stubs`](https://github.com/typeddjango/django-stubs) for full Django ORM and view type coverage — without it, Pyright gives partial benefit on Django codebases
- For TypeScript/JavaScript: `typescript-language-server` covers the same lookups
- LSP server config goes in `dotfiles/.claude/settings.json` — see your dotfiles repo for setup instructions

A chain of exploratory file reads to trace a call path costs more tokens than one `goToDefinition`. Reach for LSP first when navigating unfamiliar code.

### Counterpart Context File Equivalence

Each provider reads its own root context file (example: Claude Code reads `CLAUDE.md`; Gemini CLI reads `GEMINI.md`). If a project contains a counterpart provider's context file at its root, treat it as equivalent context authority to your own — it defines identity, pipeline commands, session isolation rules, and role scope for that agent. When configuring a counterpart session, include this equivalence instruction in the session primer or in that provider's context file itself.

See [`providers/antigravity/GEMINI-template.md`](../providers/antigravity/GEMINI-template.md) for a worked template.

### Model Selection

Match model capability to task complexity:

| Task type | Model guidance |
|-----------|---------------|
| Planning, architecture, synthesis, complex debugging | Highest-capability model in your subscription |
| Mechanical execution — formatting, repetitive edits, log parsing, simple lookups | Cost-efficient model |
| Validator / review pass | Highest-capability model in your subscription; independent model preferred |

This is a heuristic for when paying for full capability is worth the cost, not a rule about which model to use. A session that starts on a capable model for planning and switches to a smaller model for execution passes the cheaper work to the cheaper tool without sacrificing decision quality.

## Review Checklist (Use After Each Execute Phase)

Before moving to Verify, confirm:
- [ ] **Specification Match**: Does the output match what was planned?
- [ ] **Quality Verified**: Has quality been validated? (or `[SPIKE]` marker)
- [ ] **Checks Pass**: Do all quality checks pass?
- [ ] **Edge Cases**: Are boundary conditions and failure modes handled?
- [ ] **Clarity**: Is the work self-explanatory? Annotations only where logic isn't obvious?
- [ ] **No Regressions**: Did I break existing functionality?

If any item fails, return to Execute phase. Don't proceed to Verify with known issues.

## Self-Checks

Before finishing, ask:
- Did I solve the stated problem AND the real problem?
- Would I approve this work?
- What could go wrong?

## Escalation to Committee

When any of these apply, escalate to the team's [committee](../docs/glossary.md):
- **Structural changes** that affect multiple systems or long-term design
- **Breaking changes** that impact other teams or downstream consumers
- **Security or compliance implications** requiring specialist review
- **High-stakes decisions** with significant resource or reputation impact
- **Major restructuring** affecting core processes or abstractions
- **Tool or platform choices** with long-term commitment
- **Cross-cutting concerns** that span multiple roles or domains

Provide the committee with:
1. Your analysis (what you explored, why you chose this approach)
2. Specific tradeoffs and concerns
3. Implementation approach
4. Risk assessment

The committee lead synthesizes feedback into a final plan that balances quality with business impact.

## Initialization & Completion

### Before starting work
1. Read project config (CLAUDE.md, CONTRIBUTING.md)
2. If a coordination log exists (e.g., WORKLOG.md), check current context and next steps
3. Confirm task alignment with user request — ask if unclear

### After completing work
1. If a coordination log exists, update it with what you did and next steps
2. Verify all review checklist items passed
3. Report completion status to the user

---
[← Framework index](README.md) · [README](../README.md)
