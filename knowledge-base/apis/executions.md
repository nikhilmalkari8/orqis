# API — Executions

| Method | Path | Query | Response |
|--------|------|-------|----------|
| GET | `/api/executions` | `workflow_id`, `agent`, `status`, `limit` (≤100) | `ExecutionSummary[]` |
| GET | `/api/executions/{id}` | — | `ExecutionResponse` |

**Written by:** Celery `workflow_tasks.execute_workflow` (not API)

**Service:** `ExecutionService` (read + trigger only)

**Affects if changed:** `ExecutionDetailPage.jsx`, `AgentService` recent list, worker task
