# Code Review Framework

Each engineering committee member reviews the PR diff through a role-specific lens.

## Severity Levels

| Severity | Meaning | Blocks merge? |
|----------|---------|---------------|
| **MUST-FIX** | Correctness bug, security vulnerability, data loss risk, or broken contract | Yes |
| **SHOULD-FIX** | Code quality issue, missing edge case, poor naming, or maintainability concern | Yes (in current round) |
| **NIT** | Style preference, minor suggestion, optional improvement | No |

## Review Lenses by Role

Each project provides its own technology-specific review checklists. Below is the generic focus area for each role.

### 1. UX Designer
**Skip if:** No frontend files in the diff.
- Accessibility compliance (contrast, alt text, ARIA, focus management)
- Semantic HTML, form UX, tab order, keyboard navigation
- Responsive behavior (mobile-first, touch targets)
- Design system compliance (component library tokens, no hardcoded values)
- Visual hierarchy, motion with reduced-motion respect

### 2. Software Engineer
- Code quality: DRY, dead code, complexity
- Naming clarity, readability (functions under 30 lines)
- API framework patterns: schema validation, dependency injection, proper status codes
- Frontend patterns: server vs client rendering, proper data fetching
- Edge cases: empty inputs, null handling, error states

### 3. System Architect
- Service layer separation (routing -> business logic -> data access)
- Multi-tenancy enforcement, tenant context propagation
- Coupling and cohesion, circular dependencies
- Frontend routing patterns: layouts, error boundaries

### 4. Data Engineer
- Migration safety: reversible, separate data from schema migrations
- Query performance: N+1, missing indexes, eager loading
- ORM patterns: relationships, async sessions, transaction boundaries
- Data isolation policy correctness

### 5. AI/ML Engineer
**Skip if:** No AI/LLM code in the diff.
- API integration: retry logic, timeout handling, cost tracking
- Prompt injection risks, sensitive data in prompts
- Fallback behavior when AI service unavailable
- Token/cost management

### 6. Security Engineer
- Injection vectors (SQL, XSS, template injection)
- Auth bypass: missing middleware, role checks
- Sensitive data exposure in logs, errors, URLs, API responses
- CSRF, secret handling, input validation
- Multi-tenant data leakage

### 7. QA Engineer
- Test coverage for changed/added code
- Edge cases, assertion quality, fixture adequacy
- Test isolation, mock boundaries
- Correct test layer per test budget (cheapest layer that gives confidence)

### 8. SRE
- Error handling: graceful degradation for external services
- Structured logging with context
- Health checks, container resource usage
- Connection handling: timeouts, pool awareness

### 9. Writer
- User-facing copy: helpful errors, clear labels
- API response messages: clear, no sensitive data
- Code comments: explain *why*, not *what*
- Commit message conventions
