# Orqis MVP — Implementation Plan (v4: Concept MVP)

> Aligns with [`../product/orqis.md`](../product/orqis.md). **Phase 1** proves the concept with **your agents only**. **Phase 2** adds external agent onboarding.

---

## MVP Goal (Concept Proof)

Prove that Orqis can:

1. **Host your agents** — register, version, inspect metadata and schemas  
2. **Orchestrate agents in workflows** — chain agents; pass state between steps  
3. **Observe two layers** — workflow runs **and** each agent’s internal work (LLM calls, browser steps, etc.)  
4. **Reuse agents** — same agent slug in multiple workflows without duplicating code  

**Out of scope for this MVP:** onboarding third-party / external agents, marketplace, no-code builder, enterprise features.

---

## Two Layers of Orchestration (Yes — Both Are in Scope)

Orqis orchestrates at **two levels**. Both matter for the concept.

### Layer 1 — Workflow orchestration (Orqis + LangGraph)

**What:** Order agents in a workflow, pass shared state, handle failures at step boundaries.

```
Workflow:  scrape → extract → analyze → deliver
           (node)   (node)    (node)     (node)
```

- **LangGraph** compiles workflow definitions into a `StateGraph`  
- Each **node** = one of **your** registered agents (`browser-agent`, `extractor`, …)  
- **Edges** = data flow (workflow state: `urls`, `raw_content`, `structured_data`, …)  
- **Celery** runs the compiled graph asynchronously  

**Orqis builds:** workflow compiler, run API, execution records, step-level failure attribution.

### Layer 2 — Agent internal orchestration (inside each node)

**What:** What happens *inside* a single agent when the workflow invokes it.

| Agent | Internal engine | What LangSmith shows |
|-------|-----------------|----------------------|
| Browser / QA | **Browser Use** (own agent loop on Playwright) | Sub-traces: navigation, clicks, LLM decisions |
| Extractor | **Instructor** + **LiteLLM** | Structured extraction calls, retries |
| Analyzer / Reporter | **LiteLLM** | Prompts, tokens, latency |
| Scraper | **Firecrawl** | API calls, extracted content |

You **do not** reimplement these loops. You **wrap** them as LangGraph node functions. LangSmith (via LangGraph) captures **nested** activity when configured.

```
┌─────────────────────────────────────────────────────────┐
│  WORKFLOW (LangGraph)          ← Orqis orchestrates      │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐              │
│  │ Agent A │ → │ Agent B │ → │ Agent C │              │
│  └────┬────┘   └────┬────┘   └────┬────┘              │
│       │             │             │                    │
│       ▼             ▼             ▼                    │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐              │
│  │ Browser │   │Instructor│  │ LiteLLM │  ← internal  │
│  │ Use loop│   │ + LLM    │  │  calls  │    orchestration│
│  └─────────┘   └─────────┘   └─────────┘              │
└─────────────────────────────────────────────────────────┘
         LangSmith trace: workflow graph + per-node detail
```

> [!IMPORTANT]
> **MVP delivers both:** workflows chain agents (Layer 1), and LangSmith lets you drill into each agent’s internal run (Layer 2). Orqis surfaces workflow + agent metadata in its API/UI; deep dive stays LangSmith until a native viewer is worth building.

---

## Philosophy: Tie the Knots, Don't Build the Thread

| What we need | Build custom? | Reuse |
|-------------|---------------|--------|
| Workflow + agent orchestration | Compiler + registry glue only | **LangGraph** |
| Agent internals (browser, extract, analyze) | Thin wrappers (~20–40 lines each) | **Browser Use**, **Instructor**, **LiteLLM**, **Firecrawl** |
| Traces (workflow + agent internals) | Store trace URL + step errors | **LangSmith** |
| Async runs | Task enqueue | **Celery + Redis** |
| LLM access inside agents | — | **LiteLLM** |
| External agent onboarding | **Phase 2** | — |
| MCP / many connectors | Optional in MVP | **Phase 2** |

**What Orqis builds:** agent registry (yours), workflow definitions (YAML/API), workflow compiler, run worker, execution + agent observability API, thin UI.

---

## MVP Scope

### In scope

| Area | Detail |
|------|--------|
| **Your agents** | 2–4 agents you implement in `backend/app/agents/`; seeded into registry |
| **Agent registry** | List/detail: schemas, config, framework, version, entrypoint |
| **Agent observability** | Per-agent: workflows using it, execution history, last status/error, LangSmith links |
| **Workflows** | YAML or JSON definitions referencing agents by `slug`; stored in MongoDB |
| **Orchestration** | LangGraph sequential graph (branching later) |
| **Runs** | API + Celery worker; manual trigger (cron optional stretch) |
| **Reuse** | Same `slug` in ≥2 workflows |
| **Auth** | Minimal JWT (single-user dogfood OK) |

### Out of scope (MVP)

- External / third-party agent onboarding (`POST /agents` from others)  
- Form-based or drag-and-drop workflow builder  
- Marketplace, billing, teams/SSO  
- Custom trace UI replacing LangSmith  

### Phase 2 (after concept proved)

- Onboarding API for external agents (contract validation, sandbox)  
- MCP catalog, more connectors  
- Cron, retries/timeouts as platform features  
- CLI/SDK polish, production hardening  

---

## The Reusable Threads

*(Unchanged technically — see previous sections for LiteLLM, LangGraph, LangSmith, Browser Use, Instructor, Firecrawl examples.)*

### LangGraph — workflow orchestration

- Nodes = your agents  
- State = workflow-level shared dict  
- Compile per run from stored definition  

### LangSmith — workflow + internal agent traces

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY="your-key"
```

- Full workflow graph  
- Per-node inputs/outputs  
- Nested spans for Browser Use / LLM calls where supported  

### Agent wrappers (your code)

Each file in `app/agents/` exports a LangGraph-compatible `async def run(state) -> state` that delegates to Browser Use, Instructor, etc.

---

## What Orqis Builds (The Knots)

### 1. Agent registry (first-party only)

- Seed from `app/agents/` + `seed/agents.py`  
- MongoDB `agents` collection: slug, schemas, config, `implementation` metadata  
- **No** public registration API in MVP — agents added via code + seed  

### 2. Workflow definition & storage

- YAML files in `workflows/examples/` + CRUD via API  
- Steps: `{ id, agent: "<slug>", config, inputs }`  
- Compiler → LangGraph  

### 3. Platform API (FastAPI)

- Auth, agents (read), workflows CRUD, run, executions  
- **Agent detail enrichment:** used-by workflows, recent runs, aggregate success/fail  

### 4. Glue layer

- `workflow_compiler.py` — definition → `StateGraph`  
- `agent_registry.py` — slug → `run` function (from your agents package)  
- Celery task — compile + `ainvoke` + persist execution + LangSmith URL  

### 5. Frontend (thin, operational)

- Login, dashboard  
- **Agents list + agent detail** (definition, usage, runs, trace links)  
- Workflows list + detail (read definition; edit via YAML/API for MVP)  
- Executions list + detail (status, `failed_step_id`, LangSmith link)  
- **No** form-based workflow builder  

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  React UI (thin)                                          │
│  Agents · Workflows · Executions · LangSmith links        │
└────────────────────────┬─────────────────────────────────┘
                         │ REST
┌────────────────────────▼─────────────────────────────────┐
│  FastAPI                                                  │
│  Agent registry (read) · Workflows CRUD · Runs · Auth     │
│  Workflow compiler (definition → LangGraph)               │
└────────────────────────┬─────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────┐
│  Celery worker                                            │
│  ┌────────────────────────────────────────────────────┐  │
│  │ LangGraph workflow (Layer 1)                        │  │
│  │   node: your browser-agent  → Browser Use (Layer 2) │  │
│  │   node: your extractor      → Instructor (Layer 2) │  │
│  │   node: your analyzer       → LiteLLM (Layer 2)     │  │
│  └────────────────────────────────────────────────────┘  │
│  LangSmith ← traces workflow + agent internals              │
└────────────────────────┬─────────────────────────────────┘
           ┌─────────────┴─────────────┐
      MongoDB                      Redis
```

---

## Database (MongoDB)

### `users`

```json
{ "_id": "ObjectId", "email": "string", "password_hash": "string", "created_at": "datetime" }
```

### `agents` (first-party registry)

```json
{
  "_id": "ObjectId",
  "name": "Browser Agent",
  "slug": "browser-agent",
  "version": "1.0.0",
  "description": "string",
  "framework": "browser-use | instructor | litellm | firecrawl",
  "entrypoint": "app.agents.browser:run",
  "input_schema": {},
  "output_schema": {},
  "config_schema": {},
  "default_config": {},
  "category": "automation | extraction | analysis | delivery",
  "created_at": "datetime"
}
```

### `workflows`

```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "name": "string",
  "slug": "competitor-intel",
  "description": "string",
  "definition": {
    "inputs": { "urls": { "type": "array", "items": "string" } },
    "steps": [
      { "id": "scrape", "agent": "browser-agent", "config": {}, "inputs": { "urls": "{{ inputs.urls }}" } },
      { "id": "extract", "agent": "extractor", "config": {}, "inputs": {} }
    ]
  },
  "is_template": true,
  "created_at": "datetime"
}
```

### `executions`

```json
{
  "_id": "ObjectId",
  "workflow_id": "ObjectId",
  "user_id": "ObjectId",
  "status": "pending | running | completed | failed",
  "started_at": "datetime",
  "completed_at": "datetime",
  "input_data": {},
  "output_data": {},
  "langsmith_trace_url": "string",
  "failed_step_id": "string | null",
  "failed_agent_slug": "string | null",
  "duration_ms": 0,
  "error": "string | null",
  "step_summaries": [
    { "step_id": "scrape", "agent": "browser-agent", "status": "completed", "duration_ms": 12000 }
  ]
}
```

> Step-level **reasoning and LLM internals** live in **LangSmith**. Orqis stores enough to attribute failure to **step + agent** without opening LangSmith for every triage.

---

## Project Structure

```
orqis/
├── docker-compose.yml
├── .env.example
├── Makefile
├── workflows/
│   └── examples/
│       ├── competitor-intel.yaml
│       └── qa-smoke.yaml
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── agent.py
│   │   │   ├── workflow.py
│   │   │   └── execution.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── agent.py
│   │   │   ├── workflow.py
│   │   │   └── execution.py
│   │   │
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── agents.py          # list, detail (+ usage & runs)
│   │   │   ├── workflows.py
│   │   │   └── executions.py
│   │   │
│   │   ├── core/
│   │   │   ├── auth.py
│   │   │   ├── workflow_compiler.py
│   │   │   └── agent_registry.py   # slug → run(); loads YOUR agents only
│   │   │
│   │   ├── agents/                 # YOU build these (internal orchestration inside)
│   │   │   ├── __init__.py
│   │   │   ├── browser.py          # wraps Browser Use
│   │   │   ├── extractor.py        # wraps Instructor
│   │   │   ├── scraper.py          # wraps Firecrawl (optional)
│   │   │   ├── analyzer.py         # wraps LiteLLM
│   │   │   ├── reporter.py
│   │   │   └── qa_tester.py        # wraps Browser Use (different config)
│   │   │
│   │   ├── tasks/
│   │   │   ├── celery_app.py
│   │   │   └── workflow_tasks.py
│   │   │
│   │   └── seed/
│   │       └── agents.py
│   │
│   └── tests/
│
└── frontend/
    └── src/
        └── pages/
            ├── Dashboard.jsx
            ├── AgentsList.jsx
            ├── AgentDetail.jsx      # everything about one agent
            ├── WorkflowsList.jsx
            ├── WorkflowDetail.jsx
            ├── ExecutionsList.jsx
            └── ExecutionDetail.jsx
```

---

## Workflow Compiler (`core/workflow_compiler.py`)

Maps stored steps to **your** agents only (MVP):

```python
from langgraph.graph import StateGraph
from app.core.agent_registry import get_agent_runner

async def compile_workflow(definition: dict):
    graph = StateGraph(WorkflowState)
    steps = definition["steps"]

    for step in steps:
        runner = get_agent_runner(step["agent"])  # slug → your run()
        graph.add_node(step["id"], runner)

    graph.set_entry_point(steps[0]["id"])
    for i in range(len(steps) - 1):
        graph.add_edge(steps[i]["id"], steps[i + 1]["id"])
    graph.set_finish_point(steps[-1]["id"])

    return graph.compile()
```

### Example agent wrapper (Layer 2 inside Layer 1)

```python
# app/agents/browser.py
from browser_use import Agent as BrowserUseAgent
from langchain_openai import ChatOpenAI

async def run(state: dict) -> dict:
    """LangGraph node — internal loop is Browser Use."""
    bu_agent = BrowserUseAgent(
        task=state.get("browser_task") or f"Extract content from: {state['urls']}",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await bu_agent.run()
    return {**state, "raw_content": result}
```

---

## Your Agents (MVP set)

Build only what you need to prove reuse (suggested minimum):

| Slug | Wraps | Role in workflows |
|------|-------|-------------------|
| `browser-agent` | Browser Use | Collect / navigate |
| `extractor` | Instructor | Structure raw content |
| `analyzer` | LiteLLM | Reason over data |
| `reporter` | LiteLLM | Format output (optional for v1) |

**QA demo:** reuse `browser-agent` with different `config` in a second workflow — proves reuse without new code.

---

## Agent Detail API (“everything about the agent”)

`GET /api/agents/:slug` returns:

```json
{
  "agent": { "slug", "name", "schemas", "config", "framework", "version", "entrypoint" },
  "workflows_using": [{ "id", "name", "slug" }],
  "stats": {
    "total_runs": 42,
    "success_rate": 0.86,
    "last_run_at": "...",
    "last_status": "failed",
    "last_error": "..."
  },
  "recent_executions": [
    { "execution_id", "workflow_slug", "status", "failed_step_id", "langsmith_trace_url", "started_at" }
  ]
}
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Create account |
| POST | `/api/auth/login` | Login → JWT |
| GET | `/api/auth/me` | Current user |
| GET | `/api/agents` | List **your** registered agents |
| GET | `/api/agents/:slug` | Agent detail + usage + run stats + recent executions |
| GET | `/api/workflows` | List workflows |
| POST | `/api/workflows` | Create workflow (YAML/JSON body) |
| GET | `/api/workflows/:id` | Workflow detail |
| PUT | `/api/workflows/:id` | Update workflow |
| DELETE | `/api/workflows/:id` | Delete workflow |
| POST | `/api/workflows/:id/run` | Execute → `execution_id` |
| GET | `/api/executions` | List executions (filter `?agent=browser-agent`) |
| GET | `/api/executions/:id` | Execution + trace URL + step summaries |

**Phase 2:** `POST /api/agents` for external onboarding.

---

## Example Workflow YAML

```yaml
name: competitor-intel
inputs:
  urls: { type: array, items: string }
  email: { type: string }
steps:
  - id: scrape
    agent: browser-agent
    config:
      model: gpt-4o
  - id: extract
    agent: extractor
  - id: analyze
    agent: analyzer
```

---

## Observability

| Layer | Where |
|-------|--------|
| Workflow run (status, steps, failure) | Orqis `executions` + UI |
| Agent-level history | Orqis `GET /api/agents/:slug` |
| Workflow graph + agent internals | LangSmith (link from execution + agent detail) |

### MVP UI

- Execution row: status, duration, failed step/agent, **Open in LangSmith**  
- Agent page: definition, which workflows use it, last N runs  

---

## Dependencies

### Backend (`requirements.txt`)

```
fastapi
uvicorn
motor
beanie
pydantic-settings
python-jose[cryptography]
passlib[bcrypt]
celery
redis
pyyaml

litellm
langgraph
langsmith
langchain-openai
browser-use
instructor
firecrawl-py
playwright
```

---

## Build Order

### Phase 1 — Foundation (~3 days)

1. Docker Compose (MongoDB, Redis, API, worker)  
2. Beanie models: `users`, `agents`, `workflows`, `executions`  
3. Auth (JWT)  
4. `app/agents/` — first agent wrapper + `agent_registry.py`  
5. Seed 2 agents (`browser-agent`, `extractor`)  

### Phase 2 — Orchestration (~4 days)

1. Remaining agent wrappers (`analyzer`, optional `scraper`, `qa_tester`)  
2. `workflow_compiler.py` + `WorkflowState`  
3. Celery `execute_workflow` task  
4. LangSmith trace URL + `step_summaries` + `failed_step_id` / `failed_agent_slug`  
5. Workflow + execution APIs  
6. Example YAML workflows in repo  

### Phase 3 — Agent & run visibility (~3 days)

1. `GET /api/agents/:slug` with workflows-using + stats + recent runs  
2. Execution list filter by agent  
3. Thin React: Agents list/detail, Workflows list/detail, Executions list/detail  

### Phase 4 — Prove reuse (~2 days)

1. Second workflow reusing `browser-agent` (e.g. QA smoke)  
2. `pytest` for compiler + registry  
3. Manual E2E: run both workflows, verify agent detail page shows cross-workflow usage  
4. README: define agent, define YAML workflow, run, debug via LangSmith  

**Total: ~12–14 days** for concept MVP (demo-ready). Production hardening (cron, retries, rate limits) = Phase 2 platform work.

---

## Verification Plan

### Concept proof checklist

- [ ] 2+ **your** agents registered and visible on agent detail page  
- [ ] Workflow runs through LangGraph with ≥2 steps  
- [ ] LangSmith shows **workflow graph** and **internal** activity for at least one agent (e.g. browser)  
- [ ] Same agent `slug` used in **two** workflows — agent detail lists both  
- [ ] Failed run sets `failed_step_id` + `failed_agent_slug`  
- [ ] Agent detail shows run history and link to latest LangSmith trace  

### Automated

- `pytest`: `agent_registry`, `workflow_compiler`, auth, execution status transitions  

---

## Phase 2 Preview (After Concept Proved)

| Feature | Purpose |
|---------|---------|
| `POST /api/agents` onboard | External agents with validated schemas |
| MCP integration catalog | Plug-in tools without custom code per integration |
| Cron / webhooks | Scheduled workflows |
| Retries, timeouts | Safer production runs |
| CLI `orqis run` | Developer ergonomics |

---

> **Summary:** MVP = **your agents** in a registry, **LangGraph** orchestrates them in workflows, **Browser Use / Instructor / LiteLLM** orchestrate internals inside each node, **LangSmith** exposes both layers, Orqis ties it together and shows **everything about each agent** — then onboarding others comes later.
