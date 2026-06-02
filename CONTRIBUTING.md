# Contributing to Orqis

Thanks for helping. This repo treats **knowledge-base** as the source of truth for contracts and coupling; **code** and **KB** change together.

## Before you code

1. Read [`knowledge-base/INDEX.md`](knowledge-base/INDEX.md) → [`invariants.md`](knowledge-base/invariants.md)
2. Find your touch point in [`knowledge-base/graph/dependencies.yaml`](knowledge-base/graph/dependencies.yaml)
3. Check [`knowledge-base/graph/CHANGE_IMPACT.md`](knowledge-base/graph/CHANGE_IMPACT.md) for your change type

**Do not implement from** [`scrap/`](scrap/README.md) — archive only.

## Pull request checklist

Use the [PR template](.github/pull_request_template.md). At minimum:

- [ ] Behavior matches [`knowledge-base/apis/`](knowledge-base/apis/) or APIs updated in same PR
- [ ] Schemas/env updated if data shape or env vars changed ([`schemas/`](knowledge-base/schemas/), [`schemas/env.md`](knowledge-base/schemas/env.md))
- [ ] `make validate-graph` passes (or `python scripts/validate_dependencies.py`)
- [ ] `make test` or `pytest` from `backend/` passes for touched areas
- [ ] New coupling → `knowledge-base/graph/dependencies.yaml` updated
- [ ] Shipped feature → `knowledge-base/features/Fxx-*.md` + INDEX row + [`changelog.md`](knowledge-base/changelog.md)

## New feature (Fxx)

1. Copy [`knowledge-base/feature-template.md`](knowledge-base/feature-template.md) → `features/Fxx-slug.md`
2. Add one row to [`knowledge-base/INDEX.md`](knowledge-base/INDEX.md) features table
3. One bullet in [`knowledge-base/changelog.md`](knowledge-base/changelog.md)
4. Update `graph/dependencies.yaml` (new node or `files` / `depends_on` / `affects`)
5. Do **not** rewrite [`features/F00-mvp-baseline.md`](knowledge-base/features/F00-mvp-baseline.md) for unrelated work

## Architecture decisions

Non-trivial tradeoffs → one page under [`knowledge-base/foundation/decisions/`](knowledge-base/foundation/decisions/) (`ADR-NNN-title.md`). Supersede with a new ADR; do not edit accepted ADR history.

## New agent

Follow [`.cursor/rules/orqis-backend.mdc`](.cursor/rules/orqis-backend.mdc) checklist:

- `backend/app/agents/{name}.py` + mock path if needed
- `AgentRegistry.load_builtin_agents()`
- `backend/app/seed/agents.py`
- `knowledge-base/schemas/workflow-state.md`
- `dependencies.yaml` → `agent_implementations`

## New env variable

1. Add to `backend/app/config.py` and `.env.example`
2. Document in [`knowledge-base/schemas/env.md`](knowledge-base/schemas/env.md)
3. Mention in [`knowledge-base/operations.md`](knowledge-base/operations.md) if it affects run/debug

## Local setup

See [`README.md`](README.md) and [`knowledge-base/operations.md`](knowledge-base/operations.md).

## Cursor / AI

[`AGENTS.md`](AGENTS.md) and [`.cursor/rules/`](.cursor/rules/) mirror the same read order. Prefer `@knowledge-base/INDEX.md` + one schema/api file over pasting large docs.

## General doc practices

[`knowledge-base/foundation/BEST_PRACTICES_DOCS_AND_AI.md`](knowledge-base/foundation/BEST_PRACTICES_DOCS_AND_AI.md)
