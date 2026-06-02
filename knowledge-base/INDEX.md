# Orqis Knowledge Base — START HERE

**Path:** `knowledge-base/` (repo root)

## Read order (minimize tokens)

| Step | File | When |
|------|------|------|
| 1 | This file | Always |
| 2 | [`invariants.md`](./invariants.md) | Always |
| 3 | [`graph/dependency-graph.md`](./graph/dependency-graph.md) | Before any change — what else is affected |
| 4 | [`graph/dependencies.yaml`](./graph/dependencies.yaml) | Same (machine-readable impact lookup) |
| 5 | `schemas/*` or `apis/*` | Only if task touches data or HTTP |
| 6 | `features/Fxx-*.md` | Only if row below matches task |

## Foundation phase (arrange before scale)

| Doc | Purpose |
|-----|---------|
| [`foundation/README.md`](./foundation/README.md) | Start here for “how we build without losing track” |
| [`foundation/PLATFORM_LAYERS.md`](./foundation/PLATFORM_LAYERS.md) | Essential vs later layers |
| [`foundation/GAPS.md`](./foundation/GAPS.md) | What to do now (P0/P1/P2) |
| [`foundation/ROADMAP.md`](./foundation/ROADMAP.md) | Phases F01+ |
| [`foundation/BEST_PRACTICES_DOCS_AND_AI.md`](./foundation/BEST_PRACTICES_DOCS_AND_AI.md) | General docs, KB, Cursor rules (any platform) |

## Quick links

| Need | Go to |
|------|--------|
| Run / debug locally | [`operations.md`](./operations.md) |
| Env variables | [`schemas/env.md`](./schemas/env.md) |
| ArangoDB shapes | [`schemas/arango.md`](./schemas/arango.md) |
| Workflow YAML/JSON | [`schemas/workflow-definition.md`](./schemas/workflow-definition.md) |
| API contracts | [`apis/INDEX.md`](./apis/INDEX.md) |
| Code locations | [`map.md`](./map.md) |
| Stack | [`stack.md`](./stack.md) |
| Change impact | [`graph/CHANGE_IMPACT.md`](./graph/CHANGE_IMPACT.md) |

## Features

| ID | Slug | File |
|----|------|------|
| F00 | mvp-baseline | [features/F00-mvp-baseline.md](./features/F00-mvp-baseline.md) |

## After shipping a feature

1. `features/Fxx-name.md` from [`feature-template.md`](./feature-template.md)
2. One row above + [`changelog.md`](./changelog.md)
3. Update `graph/dependencies.yaml` if new component or edges

## Archive (do not implement from)

Historical docs: [`../scrap/README.md`](../scrap/README.md)

## Cursor rules

| Rule | When |
|------|------|
| `.cursor/rules/orqis-knowledge-base.mdc` | Every chat |
| `orqis-backend.mdc` | `backend/**` |
| `orqis-frontend.mdc` | `frontend/**` |
| `orqis-kb-maintenance.mdc` | `knowledge-base/**` |
