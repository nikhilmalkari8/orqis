# Schemas — Pydantic API DTOs

**Location:** `backend/app/schemas/`

## Auth (`auth.py`)

| Model | Fields |
|-------|--------|
| `SignupRequest` | `email`, `password` (min 8) |
| `LoginRequest` | `email`, `password` |
| `UserOut` | `id`, `email`, `display_name?` |
| `TokenResponse` | `access_token`, `token_type`, `user` |

## Agent (`agent.py`)

| Model | Purpose |
|-------|---------|
| `AgentSummary` | list item |
| `AgentListResponse` | `{ items: AgentSummary[] }` |
| `AgentDetail` | full agent metadata |
| `AgentDetailResponse` | `agent`, `workflows_using`, `stats`, `recent_executions` |

## Workflow (`workflow.py`)

| Model | Purpose |
|-------|---------|
| `WorkflowDefinition` | nested in create/update |
| `WorkflowCreate` | `slug`, `name`, `description?`, `is_template`, `definition` |
| `WorkflowUpdate` | partial fields |
| `WorkflowSummary` | list row |
| `WorkflowResponse` | full document |
| `RunWorkflowRequest` | `input_data` |
| `RunWorkflowResponse` | `execution_id`, `status`, `celery_task_id?` |

## Execution (`execution.py`)

| Model | Purpose |
|-------|---------|
| `ExecutionSummary` | list row |
| `StepSummary` | step in detail view |
| `ExecutionResponse` | full execution |
