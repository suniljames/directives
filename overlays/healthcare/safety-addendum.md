# Healthcare Safety Addendum

These rules extend [`framework/safety.md`](../../framework/safety.md) for HIPAA-regulated projects.

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

- All queries must go through tenant-isolation-enforced sessions (e.g., RLS).
- Never bypass tenant isolation except for super-admin operations with explicit audit logging.
- Test tenant isolation in every data-access service test.
- Log all cross-tenant access attempts.

## Docker / Deployment Safety (Healthcare)

- Never `docker compose down -v` without confirmation (destroys data volumes).
- Back up database volumes before destructive operations.
- Ensure encrypted connections for all services handling PHI.
