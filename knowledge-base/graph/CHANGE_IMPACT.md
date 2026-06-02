# Change impact checklist

Before merging: find your component in [`dependencies.yaml`](./dependencies.yaml), then verify **all** `affects` nodes.

## By change type

### New agent (`app/agents/foo.py`)

- [ ] Register in `core/agent_registry.py`
- [ ] Seed in `seed/agents.py` (Arango + schemas)
- [ ] Document keys in `schemas/workflow-state.md`
- [ ] `dependencies.yaml` → `agent_implementations`, `agent_registry`
- [ ] Tests: registry + compiler accepts slug
- [ ] UI: appears in agents list automatically after seed

### Change workflow definition shape

- [ ] `schemas/workflow-definition.md`
- [ ] `WorkflowCompiler.validate()` + `schemas/workflow.py`
- [ ] `workflow_edges.sync_workflow_agent_edges`
- [ ] Seed templates + `workflows/examples/*.yaml`
- [ ] Frontend run form (WorkflowDetailPage) if inputs change

### Change execution document

- [ ] `schemas/arango.md`
- [ ] `execution_repository`, `workflow_tasks`
- [ ] `schemas/execution.py` + `ExecutionService`
- [ ] `ExecutionDetailPage`, agent `recent_executions`

### Change run / async behavior

- [ ] `workflow_tasks.py`, `execution_service.py`
- [ ] `docker-compose.yml` worker service
- [ ] `apis/workflows.md` run section
- [ ] Do **not** run LangGraph in API process

### New API route

- [ ] `api/*.py`, `schemas/*.py`, `services/*.py`
- [ ] `apis/INDEX.md` + module doc
- [ ] `dependencies.yaml` new node + edges
- [ ] Frontend `api/client` usage + page
- [ ] `map.md`

### Arango schema / index

- [ ] `scripts/init_arangodb.py`
- [ ] `schemas/arango.md`
- [ ] All repositories touching collection
- [ ] Re-run `make init` on fresh DB docs in README

## Quick lookup table

| If you edit… | Also check… |
|--------------|-------------|
| `browser.py` (agent) | registry, seed, workflow-state, worker |
| `workflow_compiler.py` | worker, workflow service, tests/test_compiler |
| `workflow_tasks.py` | run API, executions schema, LangSmith fields |
| `workflow_edges.py` | workflow create/update, agent detail `workflows_using` |
| `graph_repository.py` | AgentService only |
| `AuthService` | deps, all routers, AuthContext |
| `docker-compose.yml` | README, operations.md, stack.md, health endpoint |

## Graph file hygiene

- Use **repo-root paths** in every `files: [...]` entry (no bare `extractor.py`).
- Run `make validate-graph` before opening a PR.
- Globs (`backend/app/agents/*.py`) must match at least one file.
