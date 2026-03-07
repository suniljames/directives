# Healthcare PRD Addendum

When writing PRDs for healthcare projects, expand the base template's Section 7 and Section 8 with these domain-specific considerations.

## Section 7 Expansion: HIPAA Privacy & Compliance

Replace the generic "Privacy & Compliance" section with:

```markdown
### 7. HIPAA Privacy & Compliance Considerations

<ALWAYS include. Does this feature create, display, transmit, or store PHI?
Who can see what? Consent or access control implications? HIPAA logging?>

- **PHI involved?** Yes/No. If yes, list specific data elements.
- **Minimum necessary:** Is the feature exposing only the PHI needed for the task?
- **Access controls:** Which roles can access this data? How is access enforced?
- **Audit logging:** What PHI access events must be logged?
- **BAA impact:** Does this feature involve a third-party service? Is a BAA in place?
```

## Section 8 Expansion: Healthcare Multi-Tenancy

Replace the generic "Multi-Tenancy / Organizational Boundaries" section with:

```markdown
### 8. Multi-Tenancy Considerations

<How does this feature behave across agencies/tenants? Super-admin view vs
agency view? Data isolation requirements? Cross-tenant visibility rules?>

- **Tenant isolation:** How is data scoped to the agency? RLS policies?
- **Super-admin access:** What cross-tenant views are needed? With what audit trail?
- **Agency branding:** Does this feature surface agency-specific content or branding?
```

## Additional Persona Considerations

The PRD should address these healthcare-specific user types if relevant:

| Persona | Context |
|---------|---------|
| Caregiver (clinical) | On shift, mobile device, time-pressured |
| Caregiver (non-clinical) | Home health aide, limited clinical training |
| Family Member | Remote, anxious, checking in on loved one |
| Care Manager | Coordinating across caregivers and patients |
| Agency Admin | Compliance, staffing, billing |
| Super-Admin | Platform-wide oversight |
