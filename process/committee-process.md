# Engineering Committee Process

The engineering committee convenes for critical review of issues requiring cross-functional analysis.

## Core Principles

1. **Sequential, iterative review** — Members post in strict order. Each reads all prior comments.
2. **Overwrite-to-final-consensus** — After deliberation, members whose positions changed overwrite their comments.
3. **Shared component reuse** — Every design must seek reuse opportunities across templates, components, services, and utilities.

## Committee Members

Full persona definitions with backgrounds, expertise, and review lenses are in [`personas/`](../personas/). Shared team culture: [`cross-cutting-traits.md`](../personas/cross-cutting-traits.md).

| # | Role | Agent | Persona |
|---|------|-------|---------|
| 1 | UX Designer (15y) | Builder | [`01-ux-designer.md`](../personas/01-ux-designer.md) |
| 2 | Senior Software Engineer (15y) | Builder | [`02-software-engineer.md`](../personas/02-software-engineer.md) |
| 3 | System Architect (15y) | Builder | [`03-system-architect.md`](../personas/03-system-architect.md) |
| 4 | Principal Data Engineer (15y) | Builder | [`04-data-engineer.md`](../personas/04-data-engineer.md) |
| 5 | Principal AI/ML Engineer (15y) | Builder | [`05-ai-ml-engineer.md`](../personas/05-ai-ml-engineer.md) |
| 6 | Principal Security Engineer (15y) | Validator | [`06-security-engineer.md`](../personas/06-security-engineer.md) |
| 7 | Principal QA Engineer (15y) | Validator | [`07-qa-engineer.md`](../personas/07-qa-engineer.md) |
| 8 | Senior SRE (15y) | Builder | [`08-sre.md`](../personas/08-sre.md) |
| 9 | Principal Writer (15y) | Validator | [`09-writer.md`](../personas/09-writer.md) |
| 10 | Engineering Manager (20y) | Builder | [`10-engineering-manager.md`](../personas/10-engineering-manager.md) |
| 11 | Senior PM (15y) | Validator | [`11-pm.md`](../personas/11-pm.md) |

## UX Mockup Generation (UI/UX Changes Only)

- **When:** User-facing UI changes. Skip for backend/API/infra.
- **Design Direction:** Purpose, tone, design system alignment, typography, motion, anti-patterns.
- **Format:** SVG in `docs/mockups/<issue-number>/`
- **Responsive viewports:** Mobile (<=480px), Tablet (481-1024px), Desktop (>1024px)
- **Multiple states:** Default, error, success, loading for each viewport where they differ.

## Test Specification Format

Used during design review to define what must be tested.

```markdown
## Test Specification

### Service Layer
- GIVEN <precondition>
  WHEN <service method call>
  THEN <expected result/side effect>

### API/Endpoint Layer
- GIVEN <auth state>
  WHEN <HTTP method + path>
  THEN <status code, response body>

### Component Layer
- GIVEN <component props/state>
  WHEN <user interaction>
  THEN <rendered output>

### E2E / Browser
- GIVEN <user role, viewport, page state>
  WHEN <user interaction>
  THEN <visible feedback, navigation>
  MARKERS: @smoke | @security | (none)
```
