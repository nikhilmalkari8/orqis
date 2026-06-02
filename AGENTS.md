# Orqis — Agent instructions

**Start:** [`knowledge-base/INDEX.md`](knowledge-base/INDEX.md) → [`invariants.md`](knowledge-base/invariants.md)

**Cursor rules:** `.cursor/rules/orqis-knowledge-base.mdc` (always) + layer rules for `backend/`, `frontend/`, `knowledge-base/`

Before coding: [`graph/dependencies.yaml`](knowledge-base/graph/dependencies.yaml) + [`CHANGE_IMPACT.md`](knowledge-base/graph/CHANGE_IMPACT.md)

Detail on demand: [`schemas/`](knowledge-base/schemas/) · [`apis/`](knowledge-base/apis/) · [`features/`](knowledge-base/features/)

Archive: [`scrap/`](scrap/README.md) — not for implementation

After shipping: `features/Fxx-*.md` + INDEX row + changelog + `dependencies.yaml` if coupling changed.

**Contributing:** [`CONTRIBUTING.md`](CONTRIBUTING.md) · **Runbook:** [`knowledge-base/operations.md`](knowledge-base/operations.md) · **Validate graph:** `make validate-graph`
