# Orqis MVP

Developer-first platform to **register your agents**, **compose workflows**, **run** them via LangGraph, and **observe** executions (with LangSmith for deep traces).

## Quick start

```bash
cp .env.example .env
make up
# wait ~30s for services
make init
make seed
```

- **API:** http://localhost:8000/docs  
- **UI:** http://localhost:5173  
- **ArangoDB:** http://localhost:8529  

**Dev login (after seed):** `dev@orqis.local` / `devpassword`

## Run a workflow

1. Open UI → **Workflows** → **Competitor Intelligence** → **Run now**  
2. Or API: `POST /api/workflows/{id}/run` with `{"input_data": {"urls": ["https://example.com"]}}`  
3. View **Executions** → open run → **LangSmith** link (if tracing enabled)

## Mock agents (default)

`MOCK_AGENTS=true` in `.env` runs agents without OpenAI/Browser Use. Set `MOCK_AGENTS=false` and provide `OPENAI_API_KEY` for real LLM/browser runs.

## Project layout

```
backend/     FastAPI + Celery + LangGraph
frontend/    React operational UI
workflows/   Example YAML definitions
```

## Commands

| Command | Description |
|---------|-------------|
| `make up` | Start Docker stack |
| `make init` | Create ArangoDB collections & graph |
| `make seed` | Seed agents + dev user + template workflows |
| `make test` | Run pytest |
| `make down` | Stop stack |

## Contributing

See [`CONTRIBUTING.md`](./CONTRIBUTING.md). Validate the dependency graph: `make validate-graph`.

## Knowledge base (schemas, APIs, dependency graph)

**Start here:** [`knowledge-base/INDEX.md`](./knowledge-base/INDEX.md) · **Runbook:** [`knowledge-base/operations.md`](./knowledge-base/operations.md)

| Folder | Purpose |
|--------|---------|
| `knowledge-base/schemas/` | Arango, workflow definition, state, DTOs |
| `knowledge-base/apis/` | Every HTTP route |
| `knowledge-base/graph/` | `dependencies.yaml` + impact checklist |
| `knowledge-base/features/` | One file per shipped feature |

## Archived docs

Older markdown lives under [`scrap/`](./scrap/README.md) (product, design, planning, research, vision). **Do not use for implementation.**

## Active docs

- [`knowledge-base/`](./knowledge-base/INDEX.md) — schemas, APIs, dependency graph (canonical)

## Architecture

- **ArangoDB** — agent & workflow metadata, executions, graph edges (`workflow_uses_agent`)  
- **Redis** — Celery queue  
- **LangGraph** — workflow orchestration (Layer 1)  
- **Browser Use / Instructor / LiteLLM** — agent internals (Layer 2)  
- **LangSmith** — trace storage (optional)
