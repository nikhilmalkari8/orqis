# Environment variables

Canonical reference for `.env` (repo root). **Never commit real secrets.** Copy from `.env.example`.

Pydantic Settings (`backend/app/config.py`) reads these (case-insensitive). Docker Compose overrides hostnames for `api`/`worker` (see `docker-compose.yml`).

## Application

| Variable | Default | Secret | Required | Used by |
|----------|---------|--------|----------|---------|
| `DEBUG` | `false` | no | no | API logging |
| `JWT_SECRET` | (dev placeholder) | **yes** | prod | Auth tokens |
| `JWT_ALGORITHM` | `HS256` | no | no | Auth (code default) |
| `JWT_EXPIRE_MINUTES` | `10080` | no | no | Auth (code default) |
| `CORS_ORIGINS` | `http://localhost:5173,...` | no | no | API CORS (code default) |

## ArangoDB

| Variable | Default | Secret | Required | Used by |
|----------|---------|--------|----------|---------|
| `ARANGO_URL` | `http://localhost:8529` | no | yes | API, worker, scripts |
| `ARANGO_DB` | `orqis` | no | yes | All repos |
| `ARANGO_USER` | `root` | no | yes | Connection |
| `ARANGO_PASSWORD` | `orqis_dev_password` | **yes** | yes | Connection, compose |

## Redis / Celery

| Variable | Default | Secret | Required | Used by |
|----------|---------|--------|----------|---------|
| `REDIS_URL` | `redis://localhost:6379/0` | no | yes | Health, Celery |
| `CELERY_BROKER_URL` | same as Redis /0 | no | yes | Worker enqueue |
| `CELERY_RESULT_BACKEND` | `redis://.../1` | no | yes | Task results |

## Agents & LLM

| Variable | Default | Secret | Required | Used by |
|----------|---------|--------|----------|---------|
| `MOCK_AGENTS` | `true` | no | no | All agent `run()` paths |
| `OPENAI_API_KEY` | empty | **yes** | if `MOCK_AGENTS=false` | LiteLLM agents |
| `EXECUTION_OUTPUT_MAX_BYTES` | `262144` | no | no | Worker truncation (code default) |

## LangSmith

| Variable | Default | Secret | Required | Used by |
|----------|---------|--------|----------|---------|
| `LANGSMITH_TRACING` | `false` | no | no | Worker traces |
| `LANGSMITH_API_KEY` | empty | **yes** | if tracing on | LangSmith |
| `LANGSMITH_PROJECT` | `orqis-mvp` | no | no | Trace project name |

## Seed / dev user

| Variable | Default | Secret | Required | Used by |
|----------|---------|--------|----------|---------|
| `SEED_DEV_USER` | `false` in code / `true` in `.env.example` | no | no | `seed_data.py` |
| `DEV_USER_EMAIL` | `dev@orqis.local` | no | no | Seed only |
| `DEV_USER_PASSWORD` | `devpassword` | **yes** | no | Seed only; dev only |

## Frontend (build-time)

| Variable | Default | Secret | Required | Used by |
|----------|---------|--------|----------|---------|
| `VITE_API_URL` | `http://localhost:8000/api` | no | yes | React API client |

Set in `docker-compose.yml` for the `frontend` service; rebuild/restart frontend if changed.

## Production notes

- Rotate `JWT_SECRET` and `ARANGO_PASSWORD`; do not use `.env.example` values.
- Set `MOCK_AGENTS=false` only when keys and observability are configured.
- Prefer secrets manager / CI vars over committing `.env`.
