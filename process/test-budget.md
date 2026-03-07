# Test Budget Policy

## Principle

Every test should run at the **cheapest layer** that still validates the behavior.

## Test Layers

| Layer | When to Use | Relative Speed |
|-------|-------------|----------------|
| **Service / Unit** | Pure logic, models, services — no HTTP, no UI | Fastest |
| **API / Endpoint** | HTTP status, response shapes, auth checks | Fast |
| **Component** | UI component rendering, user interaction | Medium |
| **E2E / Browser** | Cross-page workflows, JS interaction, auth boundary testing | Slowest |

## Decision Checklist

1. **Does the test verify business logic with no HTTP?** -> Service layer
2. **Does the test check API response codes/shapes?** -> Endpoint layer
3. **Does the test check UI component behavior?** -> Component layer
4. **Does the test require a full browser (JS, navigation, viewport)?** -> E2E
5. **Does the test verify auth boundaries or access control?** -> E2E (marked `@security`)
6. **Does the test check responsive layout?** -> E2E

## Enforcement

- New E2E tests require justification (why can't this be a cheaper layer?).
- Layer decisions happen during committee review (QA Engineer assigns in Test Specification).
- The quality gate must stay fast. If the pipeline takes longer than 10 minutes, treat it as a blocking issue.
