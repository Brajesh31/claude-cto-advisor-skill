# Architecture Decision Records

An architecture decision record (ADR) captures a consequential technical choice, the context that made it necessary, and the trade-offs accepted.

## When to write an ADR

Use an ADR for decisions that are costly to reverse or affect multiple teams, services, security boundaries, operational responsibilities, or long-term maintainability. Do not create one for every small implementation detail.

## Template

```markdown
# ADR-NNN: [Decision title]

- Status: Proposed | Accepted | Superseded | Deprecated
- Date: YYYY-MM-DD
- Owners: [team or roles]

## Context
What problem or constraint requires a decision? Include relevant requirements,
scale, security, operational constraints, and existing system behavior.

## Decision drivers
- [Requirement or constraint]
- [Requirement or constraint]

## Options considered
1. [Option A]
2. [Option B]
3. [Option C]

## Decision
State the selected option clearly.

## Consequences
### Positive
- [Benefit]

### Negative and risks
- [Trade-off, migration cost, or new operational burden]

## Rollout and validation
How will the choice be introduced, measured, and rolled back?

## References
[Designs, issues, benchmarks, or related ADRs]
```

## Review rules

- Record the decision, not a transcript of the discussion.
- Separate verified facts from assumptions.
- Include alternatives that were seriously considered.
- Make consequences explicit, including ongoing ownership and cost.
- Link superseding decisions rather than rewriting history.
- Revisit the decision when its assumptions materially change.

## Lightweight decision log

For reversible decisions, a short dated entry may be enough: context, choice, owner, and revisit trigger.
