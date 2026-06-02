# F00 — MVP baseline

**Status:** shipped

## Intent

Concept proof: first-party agents in Arango, workflows via LangGraph, async runs via Celery, thin UI, agent reuse across workflows.

## Agents (slugs)

`browser-agent` | `extractor` | `analyzer` | `reporter` | `qa-tester`

## Seed workflows

| slug | steps |
|------|-------|
| `competitor-intel` | browser-agent → extractor → analyzer |
| `qa-smoke` | qa-tester |

## Key schemas / APIs

- Schemas: [arango.md](../schemas/arango.md), [workflow-definition.md](../schemas/workflow-definition.md)
- APIs: [workflows.md](../apis/workflows.md) run → Celery
- Graph: [dependency-graph.md](../graph/dependency-graph.md)

## Not included

External onboarding, no-code builder, cron, marketplace.
