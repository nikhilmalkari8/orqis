# APIs — Index

**Base:** `http://localhost:8000`  
**Prefix:** `/api` (except health)  
**Auth:** `Authorization: Bearer <jwt>` on all except auth + health

| Module | File | Doc |
|--------|------|-----|
| Auth | `api/auth.py` | [auth.md](./auth.md) |
| Agents | `api/agents.py` | [agents.md](./agents.md) |
| Workflows | `api/workflows.py` | [workflows.md](./workflows.md) |
| Executions | `api/executions.py` | [executions.md](./executions.md) |
| Health | `api/health.py` | below |

## Health (no /api prefix)

| Method | Path | Response |
|--------|------|----------|
| GET | `/health` | `{ status, arango, redis }` |

## Error body (all modules)

```json
{ "error": { "code": "VALIDATION_ERROR", "message": "...", "details": {} } }
```

| Code | HTTP |
|------|------|
| `UNAUTHORIZED` | 401 |
| `NOT_FOUND`, `AGENT_NOT_FOUND` | 404 |
| `VALIDATION_ERROR` | 422 |

## Side effects chain

| Endpoint | Triggers |
|----------|----------|
| `POST /workflows` | Arango insert + `workflow_uses_agent` edges |
| `PUT /workflows` | Arango update + edge resync |
| `POST /workflows/{id}/run` | execution doc + edge + **Celery** `execute_workflow` |

See [graph/dependency-graph.md](../graph/dependency-graph.md).
