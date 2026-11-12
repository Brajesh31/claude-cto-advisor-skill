# Engineering Metrics Framework

Metrics should help a team improve delivery and reliability. They should not be used as a simplistic ranking of individuals.

## Start with outcomes

Before selecting metrics, define the outcome to improve: delivery speed, service reliability, quality, customer value, or sustainable team capacity. Establish a baseline and measure trends over time.

## Delivery flow

Track a balanced set of flow measures:

- Lead time for changes: time from code being committed to running in production, with a clearly defined start and end.
- Deployment frequency: how often the service or product is deployed.
- Change failure rate: proportion of deployments that cause a production failure or require remediation.
- Time to restore service: time required to recover from a production failure.

Use consistent service boundaries and measurement windows. Avoid comparing services with fundamentally different release models without context.

## Quality and reliability

Useful measures include escaped defects, incident recurrence, service-level objective attainment, test reliability, and mean time to detect. Pair counts with severity and impact. A team that reports fewer incidents may simply be under-reporting them.

## Operational health

Track alert noise, toil, on-call load, deployment rollback frequency, and time spent on unplanned work. These reveal hidden costs that velocity metrics miss.

## Team sustainability

Use aggregate signals such as focus time, work-in-progress, interruption rate, onboarding time, and team confidence. Collect sensitive data only with a clear purpose, transparency, and appropriate access controls.

## Metric design checklist

For every metric, document:

| Field | Definition |
|---|---|
| Name | Short, unambiguous name |
| Purpose | Decision this metric informs |
| Formula | Exact calculation |
| Scope | Product, service, or team boundary |
| Source | System of record |
| Cadence | Review frequency |
| Owner | Person responsible for quality |
| Guardrail | What could be gamed or misinterpreted |

## Anti-patterns

- Do not use story points as a productivity score across teams.
- Do not rank engineers by commit count, lines changed, or tickets closed.
- Do not optimize deployment frequency while ignoring change failures.
- Do not set targets before validating data quality.
- Do not reward metric movement that harms customer outcomes or team health.

Review a small dashboard regularly, investigate meaningful changes, and retire measures that no longer drive decisions.
