# Engineering Directives

How I build software. Personas, processes, and templates for multi-agent software development.

This repo is the canonical source for engineering practices that apply across all projects. Individual project repos reference these directives and add their own project-specific context.

## Architecture

Three config files drive the entire system:

| File | Scope | What it controls |
|------|-------|-----------------|
| [`agents.yml`](agents.yml) | Global | Agent types, LLM providers, default assignments, fallback chains |
| [`teams/engineering/manifest.yml`](teams/engineering/manifest.yml) | Per-team | Role roster, pipeline stages, labels, controlled vocabularies |
| Per-project `CONTRIBUTING.md` | Per-project | Team reference, pipeline mode, provider overrides |

## Teams

### Engineering

> **Manifest:** [`teams/engineering/manifest.yml`](teams/engineering/manifest.yml)

**Personas** — [`teams/engineering/personas/`](teams/engineering/personas/)

| Role | Agent | Persona |
|------|-------|---------|
| UX Designer | Builder | [`ux-designer.md`](teams/engineering/personas/ux-designer.md) |
| Software Engineer | Builder | [`software-engineer.md`](teams/engineering/personas/software-engineer.md) |
| System Architect | Builder | [`system-architect.md`](teams/engineering/personas/system-architect.md) |
| Data Engineer | Builder | [`data-engineer.md`](teams/engineering/personas/data-engineer.md) |
| AI/ML Engineer | Builder | [`ai-ml-engineer.md`](teams/engineering/personas/ai-ml-engineer.md) |
| Security Engineer | Validator | [`security-engineer.md`](teams/engineering/personas/security-engineer.md) |
| QA Engineer | Validator | [`qa-engineer.md`](teams/engineering/personas/qa-engineer.md) |
| SRE | Builder | [`sre.md`](teams/engineering/personas/sre.md) |
| Writer | Validator | [`writer.md`](teams/engineering/personas/writer.md) |
| Engineering Manager | Builder | [`engineering-manager.md`](teams/engineering/personas/engineering-manager.md) |
| PM | Validator | [`pm.md`](teams/engineering/personas/pm.md) |

Shared culture: [`cross-cutting-traits.md`](teams/engineering/personas/cross-cutting-traits.md)

**Process** — [`teams/engineering/process/`](teams/engineering/process/)

| Doc | Description |
|-----|-------------|
| [`pipeline.md`](teams/engineering/process/pipeline.md) | 6-stage pipeline, ad-hoc work gate, label lifecycle |
| [`committee-process.md`](teams/engineering/process/committee-process.md) | Committee review protocol, fresh-eyes validation, UX mockups |
| [`code-review-framework.md`](teams/engineering/process/code-review-framework.md) | Severity levels and review lens structure |
| [`test-budget.md`](teams/engineering/process/test-budget.md) | Test layer decision framework |
| [`prd-template.md`](teams/engineering/process/prd-template.md) | Product requirements document format |

## Adding a New Team

Copy `teams/TEMPLATE/` to `teams/<your-team-name>/` and customize the manifest, personas, and cross-cutting traits. See the [template manifest](teams/TEMPLATE/manifest.yml) for field documentation.

## Global Process

Applies across all teams.

| Doc | Description |
|-----|-------------|
| [`process/agent-architecture.md`](process/agent-architecture.md) | Agent types, provider assignments, single-provider fallback |
| [`process/orchestration.md`](process/orchestration.md) | How orchestrators consume config files to route work |
| [`process/reasoning-framework.md`](process/reasoning-framework.md) | AI reasoning loop, task modes, complexity triggers, review checklist |
| [`process/safety.md`](process/safety.md) | Universal safety guardrails |

## Templates

Starter files for new project repos:

| Template | Description |
|----------|-------------|
| [`CONTRIBUTING.md.template`](templates/CONTRIBUTING.md.template) | Universal entry point for all developers |
| [`CLAUDE.md.template`](templates/CLAUDE.md.template) | Claude Code agent config |
| [`GEMINI.md.template`](templates/GEMINI.md.template) | Gemini/validator agent config |
| [`worklog.md.template`](templates/worklog.md.template) | Multi-agent coordination log |
| [`pm-context.md.template`](templates/pm-context.md.template) | Domain context for PM persona |

## Domain Overlays

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
