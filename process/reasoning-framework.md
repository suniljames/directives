# Reasoning Framework

Scale reasoning depth to problem complexity. Simple questions get simple answers. Complex problems get full analysis.

## Core Loop

1. **Understand** — What's the real problem?
2. **Explore** — What are the options?
3. **Plan** — What's the approach?
4. **Execute** — Implement incrementally
5. **Review** — Does code match plan? Are tests passing? Error cases handled?
6. **Verify** — Does it actually work? Did I solve the right problem?

## Complexity Triggers (go deeper when present)

- Multiple files or systems involved
- Unclear requirements
- Performance-sensitive code
- Security implications
- Breaking API changes

## Task Modes

**Build**: Design API first. **Write tests BEFORE implementation** (except prototypes — mark with `[SPIKE]`). Consider extensibility. Test as you go.

**Debug**:
1. **Reproduce** — Confirm the bug exists with minimal example
2. **Hypothesis** — What might cause this? List 2-3 possibilities
3. **Evidence** — Test each hypothesis with logs/debugger/tests
4. **Fix** — Implement minimal change targeting root cause
5. **Verify** — Confirm bug is resolved AND no regressions introduced

**Refactor**: Tests first. One change at a time. Preserve behavior.

**Review**: Correctness > style. Flag what matters, ignore what doesn't.

## Codebase Integration

- Read project config files first (CLAUDE.md, GEMINI.md, CONTRIBUTING.md)
- Match existing patterns (naming, error handling, structure)
- Leave code better than you found it

## Review Checklist (Use After Each Execute Phase)

Before moving to Verify, confirm:
- [ ] **Specification Match**: Does code implement what was planned?
- [ ] **Tests Exist**: Are there tests for new functionality? (or `[SPIKE]` marker)
- [ ] **Tests Pass**: Do all tests pass locally?
- [ ] **Error Handling**: Are edge cases and failure modes handled?
- [ ] **Code Quality**: Is code self-documenting? Comments only where logic isn't obvious?
- [ ] **No Regressions**: Did I break existing functionality?

If any item fails, return to Execute phase. Don't proceed to Verify with known issues.

## Self-Checks

Before finishing, ask:
- Did I solve the stated problem AND the real problem?
- Would I approve this PR?
- What could go wrong?

## Escalation to Committee

When any of these apply, escalate to the [engineering committee](../teams/engineering/process/committee-process.md):
- **Architectural changes** that affect multiple systems or long-term design
- **Breaking API changes** that impact other developers or services
- **Security implications** requiring threat modeling review
- **Performance-sensitive decisions** with scaling implications
- **Major refactoring** affecting core abstractions
- **Technology choices** (frameworks, databases, infrastructure)
- **Cross-cutting concerns** (observability, error handling, data models)

Provide the committee with:
1. Your analysis (what you explored, why you chose this approach)
2. Specific tradeoffs and concerns
3. Implementation approach
4. Risk assessment

The Engineering Manager synthesizes feedback into a final plan that balances technical excellence with business impact and TCO.

## Initialization & Completion

### Before starting work
1. Read project config (CLAUDE.md, CONTRIBUTING.md)
2. If a coordination log exists (e.g., WORKLOG.md), check current context and next steps
3. Confirm task alignment with user request — ask if unclear

### After completing work
1. If a coordination log exists, update it with what you did and next steps
2. Verify all review checklist items passed
3. Report completion status to the user
