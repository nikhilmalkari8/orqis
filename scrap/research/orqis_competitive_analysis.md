# Orqis — Competitive Analysis

## Summary

Orqis occupies a unique position: **composable execution + observability for AI-powered operational workflows.** No current platform combines intelligent agent orchestration with workflow composition, execution reliability, and deep observability.

---

## Competitive Landscape

### Kore.ai — Enterprise Conversational AI

| | Kore.ai | Orqis |
|--|---------|-------|
| **Core purpose** | Build customer service chatbots | Compose operational workflows from AI capabilities |
| **Primary interface** | Chat/voice conversation | Workflow builder + execution dashboard |
| **What it orchestrates** | Dialog flows (user says X → respond Y) | AI agents doing real work (browsing, scraping, analyzing, reporting) |
| **Output** | A chatbot response | An operational outcome (report, test result, automation) |
| **User interaction** | End-user talks to a bot | Operator defines workflow, agents execute autonomously |
| **Target** | Enterprise contact centers | Anyone needing AI-powered operational automation |
| **Pricing** | $100K+ / year enterprise contracts | Execution-based (pay per workflow run) |

**Verdict:** Different products entirely. Kore.ai is about conversations. Orqis is about operations. Zero overlap.

---

### Rasa — Developer Conversational AI Framework

| | Rasa | Orqis |
|--|------|-------|
| **Core purpose** | Build conversational AI agents (chatbots, voice) | Compose AI workflows for operational outcomes |
| **Architecture** | Dialog flow engine + NLU | Workflow graph engine + agent orchestration |
| **Execution model** | Multi-turn conversation management | Multi-step workflow execution |
| **Observability** | Conversation logs, intent confidence | Agent reasoning traces, step-by-step execution, cost tracking |
| **Output** | Conversational replies | Reports, test results, automations, data |
| **Self-hosted** | Yes (core differentiator) | Yes (Docker Compose) |

**Verdict:** Rasa builds chatbots. Orqis orchestrates autonomous workflows. Complementary, not competitive.

---

### n8n / Zapier — Workflow Automation

| | n8n / Zapier | Orqis |
|--|-------------|-------|
| **Core purpose** | Connect APIs, automate data flows | Orchestrate intelligent AI agents into workflows |
| **Intelligence** | None — deterministic nodes (HTTP calls, if/else) | AI agents that reason, decide, and adapt |
| **Nodes/Steps** | API connectors (static functions) | Autonomous agents + tools + MCP servers |
| **Observability** | Input/output logging per node | Agent reasoning traces, LLM call details, decision paths |
| **Adaptability** | Breaks when websites change | AI agents adapt to page changes, new data formats |
| **Who uses it** | Ops teams connecting SaaS tools | Teams needing AI-powered operational intelligence |

**Verdict:** n8n/Zapier automate plumbing. Orqis automates intelligence. n8n connects Slack to Google Sheets. Orqis scrapes competitor sites, analyzes pricing trends, and generates executive reports. Different category.

---

### LangChain / LangGraph — AI Agent Frameworks

| | LangChain / LangGraph | Orqis |
|--|----------------------|-------|
| **What it is** | Developer framework (Python library) | End-to-end platform (UI + API + execution + observability) |
| **User** | Developers writing Python code | Operators composing workflows in a UI |
| **Deployment** | You figure it out | Docker Compose or cloud — handled |
| **UI** | None | Landing page, dashboard, workflow builder, execution view |
| **Marketplace** | None | Discover, publish, share capabilities |
| **Auth/Teams** | None | Built-in user management |

**Verdict:** LangGraph is an ingredient. Orqis is the kitchen. Orqis actually *uses* LangGraph under the hood — it's the orchestration engine. But LangGraph alone is a library, not a product.

---

### CrewAI / AutoGen — Multi-Agent Frameworks

| | CrewAI / AutoGen | Orqis |
|--|-----------------|-------|
| **What it is** | Multi-agent collaboration framework | Composable workflow platform |
| **Composition** | Code-defined agent crews | UI-based or programmatic workflow definition |
| **Observability** | Limited logging | Full execution traces, reasoning, cost tracking |
| **Reusability** | Custom code per project | Reusable capabilities across any workflow |
| **Marketplace** | None | Discovery, publishing, templates |
| **Production readiness** | Framework — you handle infra | Platform — execution, reliability, monitoring included |

**Verdict:** CrewAI/AutoGen are code frameworks for developers. Orqis is a platform for building, running, and observing agent workflows — accessible beyond just engineers.

---

### ChatGPT / Claude — AI Assistants

| | ChatGPT / Claude | Orqis |
|--|-----------------|-------|
| **Interaction** | Conversational chat | Defined workflows that execute autonomously |
| **Automation** | None — you ask, it responds | Scheduled, event-triggered, hands-free execution |
| **Composability** | Single agent, no chaining | Multiple agents chained into multi-step workflows |
| **Observability** | Conversation history | Execution traces, agent reasoning, cost tracking |
| **Reliability** | No retries, no error handling | Built-in retries, checkpointing, failure isolation |
| **Reusability** | Start from scratch each time | Save, template, share, and reuse workflows |

**Verdict:** ChatGPT/Claude are assistants you talk to. Orqis is infrastructure that works for you. When you close the browser, ChatGPT stops. Orqis keeps running.

---

## Positioning Map

```
                    Conversational ←→ Operational
                         │
        Kore.ai ●        │
                         │
          Rasa ●         │
                         │
   ChatGPT/Claude ●      │      
                         │        ● Orqis
                         │
                         │    ● n8n/Zapier
                         │
                    ─────┼─────────────
                         │
     CrewAI/AutoGen ●    │
                         │
   LangChain/LangGraph ● │
                         │
                   Framework ←→ Platform
```

Orqis is the only player in the **operational + platform** quadrant.

---

## The Orqis Differentiator

No existing platform combines all four:

| Capability | n8n | LangGraph | Kore.ai | Rasa | Orqis |
|-----------|-----|-----------|---------|------|-------|
| AI agent orchestration | ❌ | ✅ | ❌ | ❌ | ✅ |
| Workflow composition UI | ✅ | ❌ | ✅ | ❌ | ✅ |
| Deep observability | ❌ | ✅* | ❌ | ❌ | ✅ |
| Reusable capability marketplace | ❌ | ❌ | ❌ | ❌ | ✅ |
| Production execution platform | ❌ | ❌ | ✅ | ✅ | ✅ |
| Open ecosystem (any agent, any LLM) | ❌ | ✅ | ❌ | ❌ | ✅ |

*LangGraph has observability via LangSmith, but no end-user platform.

---

## One-Line Positioning

> **"n8n automates APIs. LangGraph builds agents. Kore.ai powers chatbots. Orqis composes intelligent agents into reliable, observable operational workflows."**

---

*Orqis — Composable Intelligence. Reliable Outcomes.*
