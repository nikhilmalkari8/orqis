# Current state (foundation baseline)

Snapshot after **F00 mvp-baseline**. Update this file only on major milestones (F05, F10…), not every small PR.

## Repo map

| Area | Path | Maturity |
|------|------|----------|
| Backend API + worker | `backend/app/` | Runnable scaffold |
| Frontend UI | `frontend/src/` | Operational pages |
| Infra | `docker-compose.yml`, `Makefile` | Dev-ready |
| KB | `knowledge-base/` | Active canonical docs |
| Archive | `scrap/` | Historical only |
| Cursor | `.cursor/rules/`, `AGENTS.md` | 4 rules |
| Examples | `workflows/examples/*.yaml` | Reference only |

## Domain objects (implemented)

- **Agent** — metadata in Arango; code in `app/agents/`; read API
- **Workflow** — definition JSON; graph edges to agents; CRUD + run
- **Execution** — async via Celery; step_summaries; LangSmith link

## Not implemented (product / infra)

- External agent registration API
- Cron / webhooks
- Workflow branching in compiler
- `/api/v1` versioning
- CI pipeline (pytest/ruff workflow)

## Documentation & process (done)

- KB: `operations.md`, `schemas/env.md`, graph validation script, PR template
- ADRs: [`decisions/ADR-001..003`](./decisions/)
- Repo: [`CONTRIBUTING.md`](../../CONTRIBUTING.md)

## Proof required before leaving foundation

- [ ] `make up && make seed` works on clean machine
- [ ] One workflow runs E2E with `MOCK_AGENTS=true`
- [ ] Agent detail shows 2+ workflows using `browser-agent`
- [ ] You run same workflow 3 days in a row without manual fixes
