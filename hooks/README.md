# Hooks

Git hooks kept in version control, so a fresh clone gets them. Git does not install them automatically. **Activate them once per clone:**

```
git config core.hooksPath hooks
```

| Hook | What it does |
|---|---|
| [`pre-commit`](pre-commit) | Runs [`scripts/check-personal-directives.py`](../scripts/check-personal-directives.py) when a commit touches [`AI.md`](../AI.md), [`people/`](../people/README.md), or the checker itself. Blocks the commit on any failure. |

Two design notes. The hook checks the **index**, not the working tree, by exporting the staged tree to a temporary directory and pointing the checker at it with `--root`, so what gets validated is exactly what is being committed. And it exits immediately when a commit touches none of those paths, so ordinary work in this repo pays nothing.

`git commit --no-verify` bypasses it, which is correct for the case where you know better. It should be rare enough to notice.

---
[← Back to README](../README.md)
