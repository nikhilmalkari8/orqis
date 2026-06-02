# API — Workflows

| Method | Path | Status | Response |
|--------|------|--------|----------|
| GET | `/api/workflows` | 200 | `WorkflowSummary[]` |
| POST | `/api/workflows` | 201 | `WorkflowResponse` |
| GET | `/api/workflows/{id}` | 200 | `WorkflowResponse` |
| PUT | `/api/workflows/{id}` | 200 | `WorkflowResponse` |
| DELETE | `/api/workflows/{id}` | 204 | — |
| POST | `/api/workflows/{id}/run` | 202 | `RunWorkflowResponse` |

**Create/update body:** `WorkflowCreate` / `WorkflowUpdate` — see [schemas/workflow-definition.md](../schemas/workflow-definition.md)

**Run body:** `{ "input_data": { ... } }` — keys should match `definition.inputs`

**Service:** `WorkflowService` (CRUD), `ExecutionService` (run)

**Run side effects:**

1. Insert `executions` (`pending`)  
2. Edge `execution_of_workflow`  
3. `execute_workflow.delay(execution_id)` → Redis → worker  

**Affects if changed:** compiler, worker, all workflow pages, graph edges sync
