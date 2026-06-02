# Dependency graph (visual)

Read with [`dependencies.yaml`](./dependencies.yaml) for file paths and impact lists.

## Layer 0 — Infrastructure

```mermaid
flowchart TB
  arango[(ArangoDB)]
  redis[(Redis)]
  ls[LangSmith optional]

  arango --> users[users]
  arango --> agents[agents]
  arango --> workflows[workflows]
  arango --> executions[executions]
  arango --> graph[graph edges]

  redis --> celery[Celery worker]
```

## Layer 1 — Core

```mermaid
flowchart TB
  agents_pkg[app/agents/*]
  registry[agent_registry]
  compiler[workflow_compiler]
  resolver[input_resolver]
  state[workflow_state]

  agents_pkg --> registry
  registry --> compiler
  resolver --> compiler
  state --> compiler
  state --> agents_pkg
```

## Layer 2 — Run path (critical)

```mermaid
flowchart LR
  API["POST /workflows/id/run"]
  ES[ExecutionService]
  EX[(executions)]
  Q[Redis queue]
  W[workflow_tasks]
  LG[LangGraph compile+invoke]
  AR[(agents collection)]

  API --> ES
  ES --> EX
  ES --> Q
  Q --> W
  W --> LG
  W --> EX
  LG --> agents_pkg[agent nodes]
  workflows[(workflows)] --> LG
```

## Layer 3 — API → UI

```mermaid
flowchart TB
  subgraph backend
    auth[api/auth]
    ag[api/agents]
    wf[api/workflows]
    ex[api/executions]
  end

  subgraph frontend
    UIauth[Login/Signup]
    UIag[Agent pages]
    UIwf[Workflow pages]
    UIex[Execution pages]
  end

  auth --> UIauth
  ag --> UIag
  wf --> UIwf
  ex --> UIex
  wf --> UIex
```

## Graph edges (Arango)

```mermaid
flowchart LR
  W[workflows] -->|workflow_uses_agent| A[agents]
  E[executions] -->|execution_of_workflow| W
```

**Changing `agents.slug`:** breaks workflow definitions, registry, graph edges, compiler validation.

**Changing `definition.steps`:** requires `workflow_edges` resync + compiler + worker.

## Hot paths (most coupled)

| Change here | Ripples to |
|-------------|------------|
| `workflow_compiler` | worker, workflow CRUD, all runs |
| `agent_registry` + new agent file | seed, compiler validate, graph edges, UI agent list |
| `executions` schema | worker, execution API, agent detail stats, UI execution page |
| `workflow_tasks` | run API, all execution status UX |
| `AuthService` / JWT | every protected route + UI |

Use [CHANGE_IMPACT.md](./CHANGE_IMPACT.md) for a checklist.
