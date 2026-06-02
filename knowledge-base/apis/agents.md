# API — Agents (read-only MVP)

| Method | Path | Response |
|--------|------|----------|
| GET | `/api/agents` | `{ items: AgentSummary[] }` |
| GET | `/api/agents/{slug}` | `AgentDetailResponse` |

**`AgentDetailResponse` includes:**

- `agent` — schemas, implementation, config  
- `workflows_using` — from graph AQL (`graph_repository`)  
- `stats` — 30d aggregates  
- `recent_executions` — filtered by `step_summaries[].agent`

**Service:** `AgentService` · **Repos:** `AgentRepository`, `GraphRepository`, `ExecutionRepository`

**Affects if changed:** `AgentDetailPage.jsx`, seed `agents.py`, workflow validation (unknown slug)

**Not in MVP:** `POST /agents` (onboarding)
