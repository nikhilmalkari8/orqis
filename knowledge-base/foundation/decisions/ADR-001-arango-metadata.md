# ADR-001: ArangoDB for platform metadata

**Status:** accepted  
**Date:** 2026-06-01

## Context

Need store for users, agents, workflows, executions, and **graph** queries (“workflows using agent X”).

## Decision

Use **ArangoDB** for all MVP platform documents + `workflow_uses_agent` / `execution_of_workflow` edges.

## Consequences

- **Pros:** Document + graph in one DB; reuse queries in `graph_repository.py`
- **Cons:** Team must know AQL; migrations manual via `scripts/init_arangodb.py`
- **Not in Arango:** LangSmith spans, Celery queue bodies, secrets

## Alternatives rejected

- MongoDB only — weaker first-class graph edges  
- Postgres — more setup for MVP; revisit at multi-tenant scale
