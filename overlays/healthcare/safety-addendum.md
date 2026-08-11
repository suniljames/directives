# Healthcare Safety Addendum

These rules extend [`framework/safety.md`](../../framework/safety.md) for HIPAA-regulated projects. (Not legal advice — see the [overlay README](README.md).)

## PHI Handling

- **Never** expose Protected Health Information (PHI) in logs, error messages, or API responses.
- **Never** include PHI in AI/LLM prompts without explicit justification and audit logging.
- **Never** commit PHI to version control.
- Apply the **minimum necessary** principle: only access, display, or transmit the PHI required for the task.

## Audit & Compliance

- All access to PHI must be audit-logged with: who, what, when, and why.
- BAA (Business Associate Agreement) tracking is required for all third-party services that handle PHI.
- Audit trails are not optional features — they are compliance requirements.

## Multi-Tenancy (Healthcare)

- All queries must run under enforced tenant isolation — e.g., database row-level security (RLS) — so one organization's data can never reach another's session.
- Never bypass tenant isolation except for platform-admin operations with explicit audit logging.
- Test tenant isolation in every data-access service test.
- Log all cross-tenant access attempts.

## Deployment Safety (Healthcare)

- Ensure encrypted connections for all services handling PHI.
- Back up data stores before any destructive operation, and require confirmation for commands that destroy data volumes — generic data-destruction rules live in [`framework/safety.md`](../../framework/safety.md) and [`framework/data-safety.md`](../../framework/data-safety.md); PHI raises their stakes from "lost work" to "breach notification".

---
[← Overlay index](README.md) · [README](../../README.md)
