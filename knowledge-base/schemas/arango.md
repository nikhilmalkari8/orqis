# Schemas — ArangoDB

**DB:** `orqis` · **Graph:** `orqis_graph`

## Document collections

### `users`

| Field | Type | Notes |
|-------|------|-------|
| `_key` | string | UUID |
| `email` | string | unique index |
| `password_hash` | string | bcrypt |
| `display_name` | string? | |
| `is_active` | bool | |
| `created_at` / `updated_at` | ISO8601 | |

### `agents`

| Field | Type | Notes |
|-------|------|-------|
| `_key` | string | UUID |
| `slug` | string | **unique** — referenced by workflow steps |
| `name`, `version`, `description` | string | |
| `status` | string | `active` |
| `owner` | string | MVP: `system` |
| `implementation` | object | `type`, `entrypoint`, `framework`, `module?` |
| `category`, `tags` | string / string[] | |
| `input_schema`, `output_schema`, `config_schema` | JSON Schema | |
| `default_config` | object | |
| `created_at` / `updated_at` | ISO8601 | |

### `workflows`

| Field | Type | Notes |
|-------|------|-------|
| `_key` | string | UUID |
| `user_id` | string | owner |
| `slug` | string | unique per `user_id` |
| `name`, `description` | string | |
| `version` | int | default 1 |
| `status` | string | `active` |
| `is_template` | bool | |
| `definition` | object | see [workflow-definition.md](./workflow-definition.md) |
| `created_at` / `updated_at` | ISO8601 | |

### `executions`

| Field | Type | Notes |
|-------|------|-------|
| `_key` | string | UUID |
| `user_id`, `workflow_id` | string | |
| `workflow_slug`, `workflow_version` | string / int | denormalized |
| `status` | enum | `pending` \| `running` \| `completed` \| `failed` \| `cancelled` |
| `trigger` | string | MVP: `api` |
| `input_data`, `output_data` | object | output may be truncated |
| `langsmith` | object | `trace_url`, `run_id?`, `project` |
| `failed_step_id`, `failed_agent_slug` | string? | |
| `error` | string? | |
| `step_summaries` | array | see below |
| `started_at`, `completed_at` | ISO8601? | |
| `duration_ms` | int? | |
| `celery_task_id` | string? | |
| `created_at` / `updated_at` | ISO8601 | |

**`step_summaries[]` item:**

| Field | Type |
|-------|------|
| `step_id`, `agent` | string |
| `status` | `running` \| `completed` \| `failed` |
| `started_at`, `completed_at` | ISO8601? |
| `duration_ms` | int? |
| `error` | string? |

## Edge collections

### `workflow_uses_agent`

| From | To | Edge fields |
|------|-----|-------------|
| `workflows/{id}` | `agents/{id}` | `step_id`, `step_order`, `agent_slug`, `config_snapshot` |

Synced by `services/workflow_edges.sync_workflow_agent_edges` on workflow create/update.

### `execution_of_workflow`

| From | To |
|------|-----|
| `executions/{id}` | `workflows/{id}` |

Created on run trigger.

## Indexes (MVP)

- `users.email` unique  
- `agents.slug` unique  
- `workflows.[user_id, slug]` unique  
- `executions.workflow_id`, `user_id`, `status`, `created_at`

## Not stored in Arango

- LangSmith span bodies  
- LLM API keys  
- Celery queue payloads (Redis)
