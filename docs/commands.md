# Slash Commands

What the `/define`-style commands in the pipeline diagram are, and how to get them. Read this when you reach the Standard setup path.

## What they are

A slash command is a saved prompt file. Typing `/define 42` in your AI tool loads the file named `define.md` and runs it with `42` as the argument. The commands are not software — they're instructions your AI reads, one file per pipeline stage:

| Command | Stage | Starter file |
|---|---|---|
| `/define` | Requirements → PRD | [`templates/commands/define.md`](../templates/commands/define.md) |
| `/design` | Committee design review | [`templates/commands/design.md`](../templates/commands/design.md) |
| `/implement` | Test-first build | [`templates/commands/implement.md`](../templates/commands/implement.md) |
| `/review` | Code review & merge | [`templates/commands/review.md`](../templates/commands/review.md) |
| `/summarize` | Stakeholder summary (optional) | [`templates/commands/summarize.md`](../templates/commands/summarize.md) |

## Install

1. Copy the five starter files into your project, in the directory your AI tool reads commands from. Example — Claude Code reads `.claude/commands/`:
   ```bash
   cp templates/commands/{define,design,implement,review,summarize}.md  your-project/.claude/commands/
   ```
   (Other tools: check where yours loads prompt/command files; the file contents are tool-agnostic.)
2. Open `implement.md` and fill in the one marked slot: your project's quality-gate command (lint/test/build).
3. Done — `/define <issue number>` in your next session runs the first stage.

## How they relate to the process docs

Each starter is a distillation. The full contracts — what each stage produces, the label lifecycle, the committee protocol, the close rules — live in [`teams/engineering/process/`](../teams/engineering/process/README.md). The starters point there; customize them for your project, but keep the label actions matching the [pipeline](../teams/engineering/process/pipeline.md) or the stage tracking breaks.

---
[← Docs index](README.md) · [README](../README.md)
