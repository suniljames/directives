# Healthcare PRD Addendum

When writing PRDs for healthcare projects, replace Section 7 and Section 8 of the [base PRD template](../../teams/engineering/process/prd-template.md) with the healthcare versions below. (Not legal advice — see the [overlay README](README.md).)

## Section 7 Replacement: HIPAA Privacy & Compliance

```markdown
### 7. HIPAA Privacy & Compliance Considerations

<ALWAYS include. Does this feature create, display, transmit, or store PHI
(Protected Health Information)? Who can see what? Consent or access-control
implications? Logging requirements?>

- **PHI involved?** Yes/No. If yes, list specific data elements.
- **Minimum necessary:** Does the feature expose only the PHI needed for the task? (A core HIPAA principle.)
- **Access controls:** Which roles can access this data? How is access enforced?
- **Audit logging:** What PHI access events must be logged?
- **BAA impact:** Does this feature involve a third-party service? Is a BAA (Business Associate Agreement — the contract HIPAA requires with vendors that handle PHI) in place?
```

## Section 8 Replacement: Healthcare Multi-Tenancy

```markdown
### 8. Multi-Tenancy Considerations

<How does this feature behave across tenant organizations? Platform-admin view
vs tenant view? Data isolation requirements? Cross-tenant visibility rules?>

- **Tenant isolation:** How is data scoped to the tenant organization? Enforced at which layer (e.g., database row-level security)?
- **Platform-admin access:** What cross-tenant views are needed? With what audit trail?
- **Tenant branding:** Does this feature surface tenant-specific content or branding?
```

## Additional Persona Considerations

The PRD should address the healthcare user types your product actually serves. **Worked example — one home-care platform's persona set** (replace with your vertical's own):

| Persona | Context |
|---------|---------|
| Caregiver (clinical) | On shift, mobile device, time-pressured |
| Caregiver (non-clinical) | Limited clinical training |
| Family Member | Remote, anxious, checking in on a loved one |
| Care Manager | Coordinating across caregivers and patients |
| Tenant Admin | Compliance, staffing, billing |
| Platform Admin | Cross-tenant oversight |

---
[← Overlay index](README.md) · [README](../../README.md)
