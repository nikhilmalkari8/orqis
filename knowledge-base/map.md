# Orqis — Code map

See also [`graph/dependencies.yaml`](./graph/dependencies.yaml) for coupling.

## Backend (`backend/app/`)

| Path | Role |
|------|------|
| `main.py` | FastAPI app, routers, CORS |
| `config.py` | `Settings` env |
| `db/arango.py` | DB connection |
| `api/auth.py` | JWT |
| `api/agents.py` | Agent list/detail |
| `api/workflows.py` | Workflow CRUD + run |
| `api/executions.py` | Execution read |
| `api/deps.py` | DI, `get_current_user_id` |
| `services/*_service.py` | Business logic |
| `services/workflow_edges.py` | Arango `workflow_uses_agent` sync |
| `repositories/*.py` | Arango CRUD + AQL |
| `repositories/graph_repository.py` | Agent↔workflow queries |
| `core/workflow_compiler.py` | Definition → LangGraph |
| `core/agent_registry.py` | slug → `run()` |
| `core/input_resolver.py` | `{{ state.x }}` templates |
| `agents/*.py` | Agent nodes (Layer 2) |
| `tasks/workflow_tasks.py` | Celery `execute_workflow` |
| `tasks/celery_app.py` | Celery config |
| `seed/agents.py` | `AGENT_SEED_DATA`, `WORKFLOW_SEED_TEMPLATES` |

## Scripts

| Path | Role |
|------|------|
| `scripts/init_arangodb.py` | Collections, graph, indexes |
| `scripts/seed_data.py` | Agents, dev user, workflows |

## Frontend (`frontend/src/`)

| Path | Role |
|------|------|
| `App.jsx` | Routes |
| `api/client.js` | Axios + JWT |
| `pages/AgentDetailPage.jsx` | “Everything about agent” |
| `pages/WorkflowDetailPage.jsx` | Run workflow |
| `pages/ExecutionDetailPage.jsx` | Steps + LangSmith link |

## Infra

| Path | Role |
|------|------|
| `docker-compose.yml` | arangodb, redis, api, worker, frontend |
| `Makefile` | up, init, seed, test |
