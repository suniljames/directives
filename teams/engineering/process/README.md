# Engineering Process

The procedures the engineering team runs. Reading order for a first pass: pipeline → committee → acceptance. The rest are contracts you'll reach when you need them.

| Doc | What it governs |
|---|---|
| [Pipeline](pipeline.md) | The 6-stage lifecycle end to end — stages, labels, PR slicing, session isolation. Read first. |
| [Committee Process](committee-process.md) | How the personas review a design — order, synthesis, fresh-eyes validation, authorization. |
| [Acceptance & Close](acceptance-and-close.md) | How "done" is written (criteria with falsifiers) and verified (the close gate). |
| [Code Review Framework](code-review-framework.md) | Severity levels and review rules for the PR diff (the Review stage's counterpart to the committee's design review). |
| [PRD Template](prd-template.md) | The structure `/define` produces. |
| [Test Budget](test-budget.md) | Which test layer each behavior gets. |
| [Scope Classification](scope-classification.md) | How commands decide trivial vs full-committee treatment. |
| [Coordination Contracts](coordination-contracts.md) | Comment guards, label state machines, machine-readable verdicts. |
| [Knowledge Pruning](knowledge-pruning.md) | Keeping configs, memory, and docs current without losing hard-won rules. |

Team-agnostic rules these docs lean on live in [`framework/`](../../../framework/README.md).

---
[← Back to engineering](../README.md) · [README](../../../README.md)
