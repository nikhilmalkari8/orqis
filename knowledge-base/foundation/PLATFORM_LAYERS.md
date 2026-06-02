# Platform layers (how systems like Orqis are built)

Orqis = **control plane** (define, register, trigger, observe) + **data plane** (execute agents/workflows) + **integrations** (LangGraph, LangSmith, LLMs).

Not a hosting company (Vercel). Not an agent framework (LangGraph). **Operational layer for workflows.**

## Essential layers (must have)

| # | Layer | Purpose | Orqis today |
|---|--------|---------|-------------|
| 1 | **Domain model** | Agents, workflows, executions, registry | ✅ Arango + KB schemas |
| 2 | **Agent contract** | How a step runs: inputs, outputs, config | ✅ `run(state)` + seed schemas |
| 3 | **Workflow contract** | Steps, versioning, validation | ✅ definition v1.0 + compiler |
| 4 | **Orchestration runtime** | Order steps, shared state | ✅ LangGraph (reused) |
| 5 | **Async execution** | Long runs off HTTP | ✅ Celery + Redis |
| 6 | **API (control plane)** | CRUD, run, list | ✅ FastAPI |
| 7 | **Persistence** | Metadata + run records | ✅ ArangoDB |
| 8 | **Observability (run)** | What happened, which step failed | ✅ executions + LangSmith URL |
| 9 | **Auth** | Who can trigger runs | ✅ JWT (single-user OK for now) |
| 10 | **Developer UX** | Find, debug, reuse agents | ✅ UI + agent detail API |
| 11 | **Documentation system** | Schemas, APIs, impact graph | ✅ knowledge-base |
| 12 | **Local dev** | One command up | ✅ Docker Compose + Make |

## Important (foundation phase — add before “big codebase”)

| # | Layer | Purpose | Priority |
|---|--------|---------|----------|
| 13 | **Operations runbook** | Worker down, seed, mock vs real agents | P0 |
| 14 | **Env catalog** | Every setting, secret, default | P0 |
| 15 | **Testing pyramid** | Compiler, API, one e2e run path | P0 |
| 16 | **CI** | lint + pytest on PR | P0 |
| 17 | **ADR log** | Why Arango, why Celery, why not no-code | P1 |
| 18 | **API versioning** | `/api/v1` prefix policy | P1 |
| 19 | **Migration strategy** | Arango schema/index changes | P1 |
| 20 | **Idempotency / run keys** | Safe re-trigger | P2 (reliability) |
| 21 | **Retries / timeouts** | Production trust | P2 |
| 22 | **Structured logging** | `execution_id` in every log line | P2 |
| 23 | **Contract tests** | OpenAPI or snapshot tests for APIs | P2 |

## Later (do not block foundation)

| Layer | When |
|-------|------|
| External agent onboarding | After dogfood F00 |
| Multi-tenant / teams / RBAC | After single-user loop works |
| Marketplace | After onboarding |
| Cron / webhooks | F02–F03 |
| Native trace UI | LangSmith enough for now |
| SDK package (`orqis-sdk` pip) | When developers outside repo integrate |
| K8s / multi-region | Enterprise |

## Reference architectures (market)

| Product | What they optimize | Orqis takeaway |
|---------|-------------------|----------------|
| **Temporal / Windmill** | Durable workflows, retries | Reliability patterns → Phase 2 |
| **LangSmith** | Trace LLM graphs | Reuse, don’t rebuild |
| **n8n** | Integrations + UI | We skip no-code; keep YAML/API |
| **Dify / Flowise** | Low-code AI apps | Different GTM; we’re code-first ops |
| **Hatchet / Trigger.dev** | Background jobs + DAG | Similar to our Celery + LangGraph split |

**Orqis wedge:** Agent registry + workflow composition + **agent-level** observability (not just run-level).
