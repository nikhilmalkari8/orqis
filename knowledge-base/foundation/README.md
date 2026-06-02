# Foundation phase — Orqis platform

**Goal:** Arrange repo + docs + process so the codebase can grow without losing track.  
**Status:** Foundation (post-MVP scaffold, pre-scale).  
**Canonical ops doc:** append here; do not duplicate in `scrap/`.

## Read order

1. [BEST_PRACTICES_DOCS_AND_AI.md](./BEST_PRACTICES_DOCS_AND_AI.md) — **general** docs, KB, rules, ADRs (any platform)  
2. [PLATFORM_LAYERS.md](./PLATFORM_LAYERS.md) — what a platform like Orqis must have  
3. [CURRENT_STATE.md](./CURRENT_STATE.md) — what exists today  
4. [GAPS.md](./GAPS.md) — what to build in foundation phase  
5. [ROADMAP.md](./ROADMAP.md) — phased F01+ and repo conventions  
6. [REPO_LAYOUT.md](./REPO_LAYOUT.md) — where new code goes  

## Append-only discipline

| When you… | Update… |
|-----------|---------|
| Ship feature | `../features/Fxx.md` + `../INDEX.md` + `../changelog.md` + `../graph/dependencies.yaml` |
| Change architecture | `../graph/*` + optional `decisions/ADR-NNN.md` |
| New env var | `../schemas/env.md` |
| New runbook step | `../operations.md` |
| PR / coupling | `../../CONTRIBUTING.md` + `make validate-graph` |
