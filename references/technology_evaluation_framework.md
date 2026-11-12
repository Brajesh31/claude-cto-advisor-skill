# Technology Evaluation Framework

Use this framework to compare technologies, vendors, platforms, or architectural approaches against explicit requirements.

## 1. Define the decision

Write down the problem, expected lifetime, users, workload, scale, compliance constraints, and what happens if no change is made. Separate required capabilities from preferences.

## 2. Establish hard constraints

Examples:

- Security, privacy, and regulatory requirements
- Deployment region and data residency
- Supported languages and runtime versions
- Availability and recovery objectives
- Integration with existing systems
- Exit and data portability requirements

Reject options that fail a genuine hard constraint before scoring preferences.

## 3. Score viable options

Use a 1 to 5 scale and assign weights before scoring. A practical starting model:

| Criterion | Example weight |
|---|---:|
| Functional fit | 20% |
| Security and compliance | 20% |
| Reliability and operability | 15% |
| Total cost of ownership | 15% |
| Integration and migration effort | 10% |
| Performance and scalability | 10% |
| Skills, support, and ecosystem | 5% |
| Portability and exit cost | 5% |

Weighted score = sum(weight × rating) divided by sum(weights). Document evidence and uncertainty for each rating. A score is a decision aid, not an objective truth.

## 4. Estimate total cost

Include license or subscription fees, infrastructure, data transfer, support, training, migration, maintenance, observability, staffing, and exit costs. Model expected growth and a downside scenario.

## 5. Validate with a proof of concept

Choose a representative workload. Define measurable acceptance criteria in advance. Test failure behavior, security controls, performance, deployment, upgrades, and operational workflows. Do not accept a vendor demo as a production proof.

## 6. Decide and record

Record the selected option, rejected alternatives, evidence, assumptions, risks, owner, rollout plan, and review date in an ADR.

## Questions to ask vendors

- Can data be exported in a usable format?
- What happens during a regional or provider outage?
- How are vulnerabilities disclosed and remediated?
- What support response commitments are contractual?
- Which features require higher pricing tiers?
- Can the product be operated and monitored with our existing systems?
- What are the practical migration and termination costs?

## Red flags

Unclear data ownership, no credible exit path, unsupported compliance claims, opaque pricing, weak incident communication, and performance claims without reproducible test conditions.
