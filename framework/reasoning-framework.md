# Reasoning Framework

Scale reasoning depth to problem complexity. Simple questions get simple answers. Complex problems get full analysis.

## Core Loop

1. **Understand** — What's the real problem?
2. **Explore** — What are the options?
3. **Plan** — What's the approach?
4. **Execute** — Implement incrementally
5. **Review** — Does the output match the plan? Quality checks passing? Edge cases handled?
6. **Verify** — Does it actually work? Did I solve the right problem?

## Complexity Triggers (go deeper when present)

- Multiple files, systems, or stakeholders involved
- Unclear requirements
- Performance-sensitive work
- Security or compliance implications
- Breaking changes to existing contracts or interfaces

## Task Modes

Teams instantiate these modes for their domain. The pattern is universal; the specifics change.

**Create**: Define requirements first. **Verify quality BEFORE finalizing** (except exploratory work — mark with `[SPIKE]`). Consider extensibility. Validate as you go.

**Diagnose**:
1. **Reproduce** — Confirm the problem exists with a minimal example
2. **Hypothesis** — What might cause this? List 2-3 possibilities
3. **Evidence** — Test each hypothesis against available data
4. **Fix** — Implement minimal change targeting root cause
5. **Verify** — Confirm the problem is resolved AND no regressions introduced

**Restructure**: Validate first. One change at a time. Preserve behavior.

**Review**: Correctness > style. Flag what matters, ignore what doesn't.

## Project Integration

- Read project config files first (CLAUDE.md, GEMINI.md, CONTRIBUTING.md)
- Match existing patterns (naming, conventions, structure)
- Leave things better than you found them

### LSP-First Code Navigation

When a symbol's location is known (a class name, function, import), prefer semantic lookups over exploratory file reads:

- Use `goToDefinition`, `findReferences`, `hover` via the LSP integration rather than reading whole files to locate a symbol
- For Python projects: install [Pyright](https://github.com/microsoft/pyright) as the LSP server; also install [`django-stubs`](https://github.com/typeddjango/django-stubs) for full Django ORM and view type coverage — without it, Pyright gives partial benefit on Django codebases
- For TypeScript/JavaScript: `typescript-language-server` covers the same lookups
- LSP server config goes in `dotfiles/.claude/settings.json` — see your dotfiles repo for setup instructions

A chain of exploratory file reads to trace a call path costs more tokens than one `goToDefinition`. Reach for LSP first when navigating unfamiliar code.

### GEMINI.md Equivalence

> **Note to Claude Code:** This guidance is addressed to the Gemini CLI agent. When configuring a Gemini session, include this instruction in the session primer or in `GEMINI.md` itself.

If a project contains a `GEMINI.md` at its root, treat it as equivalent context authority to `CLAUDE.md` — it defines identity, pipeline commands, session isolation rules, and role scope for the Gemini CLI agent. Read it before starting work the same way a Claude Code session reads `CLAUDE.md`.

See [`providers/gemini/GEMINI-template.md`](../providers/gemini/GEMINI-template.md) for the canonical template.

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
