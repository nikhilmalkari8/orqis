## Summary

<!-- What changed and why (1–3 sentences) -->

## Type

- [ ] Feature (new Fxx — link file below)
- [ ] Bug fix
- [ ] Docs / KB only
- [ ] Refactor (no behavior change)

## Knowledge base & graph

- [ ] Read `knowledge-base/graph/dependencies.yaml` for touched nodes
- [ ] `make validate-graph` (or `python scripts/validate_dependencies.py`) passes
- [ ] Updated `knowledge-base/apis/` and/or `schemas/` if contracts changed
- [ ] Updated `knowledge-base/schemas/env.md` if env vars changed
- [ ] Updated `graph/dependencies.yaml` if new module or coupling
- [ ] Feature doc: `knowledge-base/features/Fxx-*.md` + INDEX + changelog (if shipping feature)

## Tests

- [ ] `make test` or `pytest` from `backend/` passes

## Feature doc (if applicable)

**Fxx file:** <!-- e.g. knowledge-base/features/F01-timeouts.md -->
