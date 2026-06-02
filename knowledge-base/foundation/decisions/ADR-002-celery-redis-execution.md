# ADR-002: Celery + Redis for workflow execution

**Status:** accepted  
**Date:** 2026-06-01

## Context

Workflow runs invoke LangGraph + agents (minutes, LLM calls). HTTP must return quickly.

## Decision

`POST /workflows/{id}/run` creates execution → **`execute_workflow.delay()`** via Celery; Redis broker + result backend.

## Consequences

- **Pros:** Standard pattern; API stays responsive; worker scales separately
- **Cons:** Redis required in every environment; must run worker process
- **Invariant:** Never `ainvoke` full workflow inside FastAPI route

## Alternatives rejected

- Sync run in API — timeouts, blocks server  
- FastAPI BackgroundTasks only — no persistence across restarts, harder scale  
- Temporal — powerful but heavy for concept MVP
