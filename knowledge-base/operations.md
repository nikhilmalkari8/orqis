# Operations — runbook

How-to for local dev and debugging. **Env reference:** [`schemas/env.md`](./schemas/env.md).

## Prerequisites

- Docker Desktop (or Docker Engine) running
- `cp .env.example .env` at repo root

## First-time setup

```bash
make up      # build + start arangodb, redis, api, worker, frontend
# wait ~30s for healthchecks
make init    # Arango collections + graph
make seed    # agents, dev user, template workflows
```

| URL | Service |
|-----|---------|
| http://localhost:8000/docs | API (OpenAPI) |
| http://localhost:5173 | UI |
| http://localhost:8529 | ArangoDB UI |

**Dev login (after seed):** `dev@orqis.local` / `devpassword` (see `DEV_USER_*` in env).

## Daily commands

| Command | Purpose |
|---------|---------|
| `make up` | Start stack |
| `make down` | Stop stack (data volume persists) |
| `make init` | Re-run Arango schema (safe to repeat) |
| `make seed` | Re-seed agents/workflows/user |
| `make test` | `pytest` inside API container |
| `make logs-api` | Follow API logs |
| `make logs-worker` | Follow Celery worker logs |

## Run a workflow

**UI:** Workflows → **Competitor Intelligence** or **QA Smoke** → **Run now** → Executions.

**API:**

```bash
# Get workflow id from GET /api/workflows, then:
curl -X POST "http://localhost:8000/api/workflows/{id}/run" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"input_data": {"urls": ["https://example.com"]}}'
```

Login: `POST /api/auth/login` with email/password from seed.

## Mock vs real agents

| Mode | Setting | Behavior |
|------|---------|----------|
| Mock (default) | `MOCK_AGENTS=true` | Agents return fixture data; no OpenAI/Browser Use |
| Real | `MOCK_AGENTS=false` + `OPENAI_API_KEY` | LLM/browser agents call external APIs |

Restart worker after env change: `docker compose restart worker api`.

## LangSmith

Set `LANGSMITH_TRACING=true`, `LANGSMITH_API_KEY`, and `LANGSMITH_PROJECT`. Execution detail may show a trace URL when tracing is enabled.

## Common failures

| Symptom | Check |
|---------|--------|
| `make up` fails | Docker daemon running |
| API 503 / DB errors | `make init`; Arango healthy on :8529 |
| Run stays `pending` | Worker up: `make logs-worker`; Redis on :6379 |
| Run fails immediately | `MOCK_AGENTS` vs keys; compiler errors in worker log |
| UI can’t reach API | `VITE_API_URL` matches API (`http://localhost:8000/api`) |
| Auth fails after re-seed | `SEED_DEV_USER=true` and run `make seed` |

## Reset data

```bash
make down
docker volume rm orqis_arangodb_data   # name may vary: docker volume ls
make up && make init && make seed
```

## Validate dependency graph (PR / local)

```bash
make validate-graph
```

See [`graph/dependencies.yaml`](./graph/dependencies.yaml) and [`graph/CHANGE_IMPACT.md`](./graph/CHANGE_IMPACT.md).

## Tests without full stack

From `backend/` with venv:

```bash
pytest -q
```

Integration tests (when present) may use in-process mocks; Docker optional.
