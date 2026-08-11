# Teams

Each team is a self-contained package: a roster of personas, a pipeline, and process docs, all driven by one `manifest.yml`. The structure is identical across teams; only the expertise changes.

| Directory | What it is |
|---|---|
| [`engineering/`](engineering/README.md) | The first fully-built team — 11 personas, a 6-stage pipeline, and the process contracts. Use it as-is or as the worked example. |
| [`new-team-template/`](new-team-template/manifest.yml) | Copy this to create a new team (sales, marketing, ops…). The manifest is annotated field-by-field. |

To create a team: `cp -r teams/new-team-template teams/<your-team>`, fill in the manifest and personas, and declare `<!-- team: <your-team> -->` in your project's `CONTRIBUTING.md`. Setup walkthrough: [Getting Started → Adapting to other teams](../docs/getting-started.md).

---
[← Back to README](../README.md)
