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

Both tie to graph edges for `browser-agent` reuse proof.

## Execution fields (Arango `executions`)

`status`, `step_summaries[]`, `failed_step_id`, `failed_agent_slug`, `langsmith.trace_url`, `output_data` (truncated if huge).

## Compiler

- `schema_version: "1.0"`
- Sequential edges only
- `on_step_event` updates summaries in worker

## Not included

See `INDEX.md` out-of-scope list.

## Deep spec

`orqis_mvp_design.md` §5 (Arango), §10 (API), §11 (Celery).
