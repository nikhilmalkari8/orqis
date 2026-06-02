# Orqis — Invariants (do not break)

## Product

- **Workflows** chain **agents** by `slug` in `definition.steps[]`.
- MVP agents are **first-party only** (seed + `app/agents/`); no public agent registration API unless a feature adds it.
- **Developer-first** — YAML/JSON definitions; no drag-and-drop builder unless requested.

## Runtime

- `POST /workflows/{id}/run` **must** enqueue Celery `execute_workflow` — do not run LangGraph inline in API (long jobs).
- **Redis required** for Celery broker/backend in current architecture.
- **ArangoDB** holds metadata + executions; **not** full LangSmith spans.
- Set `failed_step_id` + `failed_agent_slug` on step failure.

## Code conventions

- New agent: `backend/app/agents/{name}.py` exports `async def run(state) -> state`, register in `core/agent_registry.py`, seed in `app/seed/agents.py`.
- New workflow step field: update `WorkflowCompiler.validate()` if needed.
- Graph edges: call `sync_workflow_agent_edges()` on workflow create/update.
- Pydantic schemas in `schemas/`; logic in `services/`; Arango in `repositories/`.

## Config

- Secrets in **env** only — never in workflow/agent documents in Arango.
- `MOCK_AGENTS=true` — agents use `agents/_mock.py` (no external API keys).

## UI

- Operational pages only: agents, workflows, executions, auth.
- Agent detail must show: definition, `workflows_using`, stats, recent executions.
