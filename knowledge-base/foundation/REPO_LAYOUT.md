# Repo layout — where new things go

Keep this stable. If you need a new top-level folder, write an ADR first.

```
orqis/
├── backend/                 # Python: API + worker (same image)
│   ├── app/
│   │   ├── api/             # HTTP only — thin
│   │   ├── services/        # Business rules
│   │   ├── repositories/    # Arango only
│   │   ├── core/            # Compiler, registry, security
│   │   ├── agents/          # One file per agent slug
│   │   ├── tasks/           # Celery only
│   │   ├── schemas/         # Pydantic DTOs
│   │   └── seed/            # Seed data definitions
│   ├── scripts/             # init DB, seed, future migrations
│   └── tests/               # pytest
│
├── frontend/                # React SPA
│   └── src/
│       ├── pages/           # One page per route
│       ├── api/             # API client modules (optional split)
│       └── components/
│
├── workflows/examples/      # Reference YAML (not auto-loaded)
│
├── knowledge-base/          # CANONICAL docs
│   ├── schemas/ apis/ graph/ features/
│   └── foundation/          # Phase plans, ADRs, layout
│
├── scrap/                   # ARCHIVE — never implement from
│
├── .cursor/rules/           # Short pointers only
├── AGENTS.md
├── docker-compose.yml
└── Makefile
```

## Boundaries (do not blur)

| Layer | May call | Must not |
|-------|----------|----------|
| `api/` | `services/` | Arango directly, LangGraph |
| `services/` | `repositories/`, enqueue Celery | LangGraph invoke |
| `tasks/` | `core/compiler`, agents, repos | FastAPI request context |
| `repositories/` | Arango | Business rules |
| `agents/` | external libs, state dict | HTTP, Arango |

## Naming

- Agent slug: `kebab-case` — matches filename `browser.py` → `browser-agent`
- Feature KB: `F{nn}-{kebab-name}.md`
- ADR: `ADR-{nnn}-{kebab-title}.md`

## Forbidden without ADR

- `packages/` monorepo split
- `services/worker/` separate repo
- Second UI framework
- MongoDB alongside Arango
