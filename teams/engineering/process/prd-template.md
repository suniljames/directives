# PRD Template

Use this template when composing a Product Requirements Document. Every section is **required** — use "N/A" with a brief rationale if a section does not apply.

For domain-specific addenda (e.g., HIPAA for healthcare), see the relevant overlay in [`overlays/`](../../../overlays/).

---

```markdown
## Product Requirements Document

**Issue:** #<number>
**PM Review Date:** <YYYY-MM-DD>
**Status:** Draft

---

### 1. Problem Statement

<What user problem does this solve? Who feels the pain? How severe is it?
Frame from the end-user's perspective, not the engineering team's.>

### 2. User Personas Affected

<Which user types are impacted? For each persona, describe their relationship
to this problem:>

| Persona | Impact | Context |
|---------|--------|---------|
| e.g., End User | Primary | ... |
| e.g., Admin | Operational | ... |

### 3. User Stories / Jobs to Be Done

1. ...
2. ...
3. ...

### 4. Success Criteria

<Measurable, observable outcomes. Write as testable statements.>

- [ ] ...
- [ ] ...
- [ ] ...

### 5. Scope

**In scope:**
- ...

**Out of scope (and why):**
- ...

### 6. User Experience Requirements

<Expected user flow. What does the user see, tap, read? What feedback?
What error states? Keep it behavioral, not technical.>

### 7. Privacy & Compliance Considerations

<Does this feature create, display, transmit, or store sensitive data?
Who can see what? Consent or access control implications? Audit logging?>

### 8. Multi-Tenancy / Organizational Boundaries

<How does this feature behave across organizational boundaries? Admin vs
standard user views? Data isolation requirements?>

### 9. Documentation & Audit Requirements

<What should be logged? What user-facing help text or documentation is needed?>

### 10. Related Issues

| Issue | Relationship | Summary |
|-------|-------------|---------|
| #... | Prerequisite / Related / Follow-up | ... |

### 11. Open Questions

1. ...

### 12. Recommendation

<Overall product recommendation. Build as described? With modifications? Priority?>
```
