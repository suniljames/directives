# Engineering Team

The first fully-built team: 11 reviewer personas, a 6-stage pipeline, and the process contracts that hold it together. Everything is driven by [`manifest.yml`](manifest.yml) — roles, stages, labels, and vocabularies live there, and docs point at it rather than restating it.

| Start with… | When |
|---|---|
| [`manifest.yml`](manifest.yml) | You want the canonical config — who's on the team, the pipeline stages, the labels. |
| [`personas/`](personas/README.md) | You want the reviewer profiles (the "who"). |
| [`process/`](process/README.md) | You want the procedures — pipeline, committee protocol, review rules, close gate (the "how"). |

How the pieces fit: a task moves through the [pipeline](process/pipeline.md); at the Design and Review stages the [committee](process/committee-process.md) of personas reviews it; the [close gate](process/acceptance-and-close.md) decides when it's done.

---
[← Back to teams](../README.md) · [README](../../README.md)
