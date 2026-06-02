# Orqis

> **Agents are easy to build. Workflows are how they get used.**

Orqis is a developer-first platform for **composing, running, and operating agents in production workflows** — without rebuilding the AI stack or competing with deploy platforms.

---

## The Problem

Teams build agents constantly (LangGraph, CrewAI, custom Python, MCP tools) but most never make it to real use:

| Gap | What happens today |
|-----|-------------------|
| **Deployment** | Agents live in repos; wiring them to schedules, APIs, and secrets is ad hoc |
| **Composition** | Multi-step automations are glue scripts, not a durable model |
| **Observability** | Failures are hard to debug — no clear step-level traces or cost view |
| **Maintenance** | Model/API/site changes break runs; no versioning or operational habit |

Intelligence exists. **Operational use** does not.

---

## What Orqis Is

Orqis is the **workflow layer** for agents.

- **Workflows** are the main product — the unit of automation (inputs, steps, outputs, triggers, failures).
- **Agents and tools** are steps inside workflows — either **yours** or **reused** from a registry.
- **Runs** are observable and repeatable — you can see what failed, fix it, and run again.

Developers define workflows in **code** (Python, YAML, or SDK) — not in a no-code canvas. Control and accuracy matter more than drag-and-drop accessibility.

```
Your agents + shared capabilities
            ↓
      Orqis workflows
   (define → run → observe → maintain)
            ↓
    Outcomes in production
```

---

## What Orqis Does (Core)

### 1. Register capabilities

Onboard agents and tools your team already built, or reuse built-in / shared capabilities (browser, extraction, notifications, MCP connectors, etc.).

Each capability has a clear contract: inputs, outputs, config, version.

### 2. Compose workflows

Chain capabilities into workflows — sequential steps today; branching, parallelism, and human-in-the-loop later.

Workflows are how agents are **actually used**: scheduled reports, post-deploy QA, research pipelines, internal ops — not one-off chat sessions.

### 3. Execute reliably

Trigger runs via API, CLI, webhooks, or schedules. Orqis orchestrates execution using proven runtimes (see [Built on](#built-on-not-from-scratch)) — it does not reinvent graph engines or LLM clients.

### 4. Observe and maintain

Every run should answer: *What ran? Which step failed? What did it cost? Can I replay or fix it?*

Observability is first-class — integrated with industry tooling and surfaced in context of **your workflow**, not scattered across logs and notebooks.

---

## What Orqis Is Not

| Orqis is not… | Why |
|---------------|-----|
| **A no-code / visual automation product** | That space is crowded; efficiency and accuracy for developers come first |
| **Vercel (or generic hosting)** | Deploy apps and workers where you already deploy; integrate with those platforms when useful |
| **An agent framework** | We don’t teach you how to write agents — we help you **run and operate** them in workflows |
| **Built from scratch** | LangGraph, LangSmith, LiteLLM, MCP, and other market tools are reused; Orqis owns the product layer on top |

---

## Philosophy

1. **Workflows over agents** — A lone agent in a repo is not a product outcome; a workflow is.
2. **Composition over construction** — Reuse intelligence and infra that already exist; build the knots, not the threads.
3. **Developers first** — Code-first definitions, testable runs, clear contracts — not a canvas for everyone.
4. **Operational truth** — If you can’t run it weekly and debug a failure in minutes, it’s not done.
5. **Integrate, don’t replace** — Partner with deploy and framework ecosystems; own the workflow operational layer.

---

## Who It’s For

**Primary:** Developers and platform engineers who:

- Already have (or are building) agents
- Need them in **production automations**, not demos
- Are tired of stitching Celery, auth, tracing, and secrets by hand

**Not primary (V1):** Non-technical operators building automations without code.

---

## V1 — What We Ship First

V1 proves one loop end to end:

```
Define workflow (code/YAML)
  → Register your agents + reuse a small set of built-ins
  → Run (API / CLI + at least one trigger, e.g. manual or cron)
  → Observe (execution list + step-level trace / LangSmith integration)
  → Fix and re-run
```

### In scope

- Workflow definition and storage
- Capability / agent registry (onboard + reuse)
- Workflow compiler → LangGraph (or equivalent) at runtime
- Run API and execution records
- Basic auth and project/workspace model (minimal)
- Observability: per-run status, errors, trace links or embedded views
- Reuse: LangGraph, LangSmith, LiteLLM, MCP, selected agent libraries (e.g. Browser Use, Instructor)

### Out of scope (V1)

- No-code / drag-and-drop workflow builder
- Natural language workflow generation
- Marketplace, payments, revenue share
- Enterprise SSO, on-prem, compliance packs
- Full hosting platform (Vercel-like deploy is integrate later, not build)

### V1 success criteria

- **You** run at least one real workflow on a recurring basis
- A failed step is identifiable without digging through unrelated logs
- The same registered agent is reused across more than one workflow

---

## Later Versions (Same Direction, More Depth)

These extend V1 — they are not pivots.

| Phase | Focus |
|-------|--------|
| **V2 — Reliability** | Retries, timeouts, checkpointing, dead-letter queues, alerts |
| **V2 — Maintenance** | Workflow/agent versioning, health checks, regression runs |
| **V2 — Teams** | Shared registry, secrets per env, roles, audit |
| **V3 — Triggers & integrations** | Webhooks, event buses, deeper deploy partner hooks (Vercel, Railway, K8s) |
| **V3 — Vertical templates** | Packaged workflows (competitive intel, QA, support ops) on the same engine |
| **V4 — Ecosystem** | Publish/share capabilities, marketplace, community templates |
| **V4+ — Enterprise** | SSO, private registries, data residency, SLAs |

---

## Built On (Not From Scratch)

Orqis reuses production-ready components and productizes the layer above them:

| Need | Typical reuse |
|------|----------------|
| Graph execution | LangGraph |
| LLM access | LiteLLM |
| Tracing | LangSmith |
| Tools & integrations | MCP servers |
| Browser / extraction / scrape | Browser Use, Instructor, Firecrawl, etc. |
| Async jobs | Celery + Redis |
| API & data | FastAPI, MongoDB (or equivalent) |

**Orqis builds:** workflow model, registry, compiler/glue, run API, execution product UI, auth, and the experience that makes the stack **usable as one platform**.

---

## Architecture (Conceptual)

```
┌─────────────────────────────────────────┐
│  Developer surface                       │
│  SDK / YAML / Python · CLI · Run UI      │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  Orqis platform                          │
│  Registry · Workflows · Runs · Auth      │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  Orchestration (reused)                  │
│  LangGraph · Queue · LangSmith             │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│  Capabilities (yours + built-ins + MCP)  │
└─────────────────────────────────────────┘
                   │
         Deploy elsewhere (Vercel, Docker, …)
```

---

## One-Line Summary

> **Orqis is where developers turn agents into production workflows — register or reuse capabilities, run and observe them in one place, built on the tools you already use.**

---

## Positioning (vs the market)

- **LangGraph / CrewAI** — How you *build* agents. Orqis is how you *run* them in workflows.
- **n8n / Zapier** — Deterministic app plumbing. Orqis is *intelligent* multi-step automation with agent steps.
- **LangSmith alone** — Traces for graphs you already run. Orqis adds registry, workflow product, triggers, and team operational model.
- **Vercel** — Where your service lives. Orqis is *what* executes and *how* you operate agent workflows.

---

*Orqis — Workflows for agents. Production by default.*
