# knowledge-base/

Token-efficient source of truth for **schemas**, **APIs**, and **dependency impact**.

## Folders

| Folder | Contents |
|--------|----------|
| [`schemas/`](./schemas/) | Arango, workflow definition/state, DTOs, [`env.md`](./schemas/env.md) |
| [`operations.md`](./operations.md) | Local runbook (make, mock, failures) |
| [`apis/`](./apis/) | HTTP routes, auth, request/response |
| [`graph/`](./graph/) | Dependency graph + “if you change X, update Y” |
| [`features/`](./features/) | One small file per shipped feature (delta only) |

## Rules

- **Do not** duplicate scrap docs — use `schemas/` + `apis/`; archive is `../scrap/`.
- **Do** update `graph/dependencies.yaml` when you add modules or coupling.
- **INDEX.md** stays short; detail lives in subfolders.

## Legacy

- `docs/kb/` removed → see `scrap/kb-v1/`
- Root `orqis_*.md` files → see `scrap/`
