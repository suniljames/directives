# Engineering Directives

How I build software. Personas, processes, and templates for multi-agent software development.

This repo is the canonical source for engineering practices that apply across all projects. Individual project repos reference these directives and add their own project-specific context.

## Contents

### Personas

The engineering committee: 11 domain experts who review designs and code.

| # | Role | File |
|---|------|------|
| 1 | UX Designer | [`personas/01-ux-designer.md`](personas/01-ux-designer.md) |
| 2 | Software Engineer | [`personas/02-software-engineer.md`](personas/02-software-engineer.md) |
| 3 | System Architect | [`personas/03-system-architect.md`](personas/03-system-architect.md) |
| 4 | Data Engineer | [`personas/04-data-engineer.md`](personas/04-data-engineer.md) |
| 5 | AI/ML Engineer | [`personas/05-ai-ml-engineer.md`](personas/05-ai-ml-engineer.md) |
| 6 | Security Engineer | [`personas/06-security-engineer.md`](personas/06-security-engineer.md) |
| 7 | QA Engineer | [`personas/07-qa-engineer.md`](personas/07-qa-engineer.md) |
| 8 | SRE | [`personas/08-sre.md`](personas/08-sre.md) |
| 9 | Writer | [`personas/09-writer.md`](personas/09-writer.md) |
| 10 | Engineering Manager | [`personas/10-engineering-manager.md`](personas/10-engineering-manager.md) |
| 11 | PM | [`personas/11-pm.md`](personas/11-pm.md) |

Shared culture: [`personas/cross-cutting-traits.md`](personas/cross-cutting-traits.md)

### Process

| Doc | Description |
|-----|-------------|
| [`process/agent-architecture.md`](process/agent-architecture.md) | Builder/validator agent split — why and how |
| [`process/pipeline.md`](process/pipeline.md) | 6-stage autonomous pipeline: PM -> design -> implement -> review -> deploy -> summarize |
| [`process/committee-process.md`](process/committee-process.md) | Engineering committee review protocol |
| [`process/safety.md`](process/safety.md) | Universal safety guardrails |
| [`process/test-budget.md`](process/test-budget.md) | Test layer decision framework |
| [`process/code-review-framework.md`](process/code-review-framework.md) | Severity levels and review lens structure |
| [`process/prd-template.md`](process/prd-template.md) | Product requirements document format |

### Templates

Starter files for new project repos:

| Template | Description |
|----------|-------------|
| [`templates/CONTRIBUTING.md.template`](templates/CONTRIBUTING.md.template) | Universal entry point for all developers |
| [`templates/CLAUDE.md.template`](templates/CLAUDE.md.template) | Claude Code agent config |
| [`templates/GEMINI.md.template`](templates/GEMINI.md.template) | Gemini agent config |

### Domain Overlays

Optional additions for domain-specific projects:

| Overlay | Description |
|---------|-------------|
| [`overlays/healthcare/`](overlays/healthcare/) | HIPAA, PHI handling, patient safety |

## How to Use

1. **New project?** Copy files from `templates/` into your repo and customize.
2. **Reference personas** from your project's team docs — link, don't copy.
3. **Apply overlays** relevant to your domain (e.g., healthcare adds HIPAA requirements).
4. **Keep project-specific content in the project repo** — tech stack, architecture, test accounts, design system.

## Three-Tier Model

| Tier | Where | What |
|------|-------|------|
| **1. Directives** (this repo) | `suniljames/directives` | Engineering philosophy, personas, process, templates |
| **2. Organization** | `<org>/.github` or org-level repo | Domain compliance, org-specific workflows, shared CI |
| **3. Project** | Each project repo | Tech stack, architecture, environment, project-specific docs |
