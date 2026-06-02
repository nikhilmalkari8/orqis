# Best practices — docs, knowledge base, rules & AI context

General patterns for any growing platform (Orqis included). **Append** new sections here; don’t duplicate into Cursor rules.

---

## 1. Documentation system (industry standard)

### Diátaxis — four types (never mix in one page)

| Type | User need | Example | Updates when |
|------|-----------|---------|--------------|
| **Tutorial** | Learning by doing | “First workflow in 15 min” | UX changes |
| **How-to** | Solve one task | “Add a new agent” | Process changes |
| **Reference** | Lookup contracts | Schemas, APIs, env vars | Code changes |
| **Explanation** | Why / tradeoffs | ADRs, architecture | Decisions change |

**Orqis mapping:**

- Tutorial → `README.md` quick start  
- How-to → `features/Fxx.md`, `CHANGE_IMPACT.md`  
- Reference → `knowledge-base/schemas/`, `apis/`  
- Explanation → `foundation/decisions/ADR-*`, `PLATFORM_LAYERS.md`

### Single source of truth (SSOT)

| Rule | Practice |
|------|----------|
| One canonical home per fact | API path lives in `apis/` — not README, not rules |
| Generated > hand-copied | Prefer OpenAPI from code, typed schemas from Pydantic |
| Archive, don’t delete history | `scrap/` or git — never “silent rewrite” |
| Link, don’t copy | Rules/KB index point to reference docs |

### Docs live with code

- Docs PR in **same PR** as behavior change (or immediately after).  
- PR checklist: “KB / graph / ADR updated?”  
- Broken links in CI (optional: `markdown-link-check`).

### C4 / architecture (lightweight)

| Level | Audience | Orqis |
|-------|----------|-------|
| Context | Everyone | `PLATFORM_LAYERS.md` |
| Container | Devs | `dependency-graph.md` |
| Component | Implementers | `dependencies.yaml` + `map.md` |
| Code | IDE | Code itself |

Don’t draw diagrams you won’t maintain — **one** container diagram + **YAML graph** is enough for most startups.

---

## 2. Knowledge base design (token-efficient + scalable)

### Layer model (best practice)

```
INDEX.md          (~50–100 lines)     — table of contents only
├── reference/    (schemas, apis)     — lookup tables, changes with code
├── graph/        (deps + impact)     — coupling, not prose
├── features/     (Fxx deltas)        — one file per shipped unit of work
├── foundation/   (phases, ADRs)     — slow-changing
└── archive/      (dead docs)        — never read by default
```

### Token rules for AI-assisted dev

| Do | Don’t |
|----|--------|
| Short INDEX + pointers | 50-page “platform bible” in every chat |
| Per-feature delta (~40 lines) | Re-document entire system per task |
| Machine-readable graph (YAML) | Only prose architecture |
| `@` specific files in prompts | `@` entire repo or scrap |
| Update graph when coupling changes | Hope agent discovers side effects |

### Append-only workflow (butter smooth)

```
Ship feature X
  → features/Fxx.md      (what/why/touch list)
  → INDEX.md             (+1 table row)
  → changelog.md         (+1 bullet)
  → dependencies.yaml  (nodes/edges if needed)
  → schemas/ or apis/    (if contract changed)
```

**Never:** edit F00 for new work; never grow INDEX into a spec.

### What belongs in KB vs code vs rules

| Content | KB | Code comments | Cursor rules |
|---------|----|--------------|--------------|
| API request/response shapes | ✅ | — | pointer only |
| “Must use Celery for runs” | ✅ invariants | — | ✅ 1 line |
| Why Arango vs Postgres | ✅ ADR | — | — |
| How to parse one function | — | rare | — |
| Read order for agents | ✅ INDEX | — | ✅ minimal |

**Rule of thumb:** Rules < 50 lines each; KB holds truth; rules hold **protocol**.

---

## 3. Architecture Decision Records (ADRs)

**Format:** `ADR-NNN-title.md` — 1 page max.

```markdown
# ADR-NNN: Title
Status: proposed | accepted | deprecated | superseded by ADR-XXX
## Context
## Decision
## Consequences (pros/cons)
## Alternatives considered
```

| When to write | When to skip |
|---------------|--------------|
| Hard to reverse (DB, queue, auth model) | Rename a variable |
| Explains “why not X” | Obvious library choice |
| Team will ask in 6 months | One-line local fix |

**Never** edit accepted ADRs — supersede with new number.

---

## 4. Dependency & impact tracking

### Two complementary artifacts

| Artifact | Human | Machine/AI |
|----------|-------|------------|
| Mermaid diagram | Mental model | Optional |
| `dependencies.yaml` | Review in PR | “affects” blast radius |

Each component:

```yaml
component_id:
  files: [paths]
  depends_on: [other_ids]   # must not break
  affects: [other_ids]      # retest/update when this changes
```

### CHANGE_IMPACT checklists

“If you change X, also update Y” — by **change type** (new agent, new API, schema migration). Faster than re-deriving graph every time.

### Validate graph (mature teams)

Script in CI: every `files:` path exists; every `depends_on` id exists; optional: API routes match `apis/INDEX.md`.

---

## 5. Cursor / AI rules (max potential)

### Split rules by concern + scope

| Rule | `alwaysApply` | `globs` |
|------|---------------|---------|
| Project protocol (read INDEX, KB first) | ✅ true | — |
| Backend conventions | false | `backend/**` |
| Frontend conventions | false | `frontend/**` |
| KB maintenance | false | `knowledge-base/**` |

**Anti-pattern:** one 300-line `alwaysApply` rule (burns tokens every chat, drifts).

### Rules are pointers, not encyclopedias

```markdown
# Good
Read knowledge-base/INDEX.md. Before edits: dependencies.yaml node for touched component.

# Bad
[Paste entire Arango schema here]
```

### AGENTS.md + rules + KB

| File | Role |
|------|------|
| `AGENTS.md` | Repo entry for any agent |
| `.cursor/rules/*.mdc` | Cursor-specific injection |
| `knowledge-base/INDEX.md` | Canonical read order |

Keep them **synchronized** (same read order, same invariants).

### Prompt patterns (user habit)

```
@knowledge-base/INDEX.md
@knowledge-base/graph/dependencies.yaml
@knowledge-base/apis/workflows.md
Task: <one concrete outcome>
After ship: update Fxx + graph
```

### User Rules vs Project Rules

| | User Rules (Cursor settings) | Project Rules (`.cursor/rules/`) |
|--|------------------------------|----------------------------------|
| Scope | All your projects | This repo only |
| Use for | Tone, “don’t commit unless asked” | Orqis architecture, KB protocol |

---

## 6. Repository & code organization

### Bounded contexts (folders = boundaries)

- `api/` — HTTP only, thin  
- `services/` — business logic  
- `repositories/` or `db/` — persistence only  
- `tasks/` or `worker/` — async execution only  

**Lint/import rules** (later): api must not import agent implementations directly.

### Monorepo docs at root

```
README.md           — 5 min to first run
CONTRIBUTING.md     — how to PR + doc ritual
AGENTS.md           — AI entry
knowledge-base/     — SSOT reference
.github/            — CI, PR template
```

### CONTRIBUTING.md essentials

- Branch naming (optional)  
- “Run `make test` before PR”  
- **Doc checklist:** feature file, INDEX, changelog, dependencies.yaml  
- No secrets in PRs  

### PR template (`.github/pull_request_template.md`)

```markdown
## KB
- [ ] features/Fxx or N/A
- [ ] dependencies.yaml if coupling changed
- [ ] schemas/apis if contract changed
```

---

## 7. Testing & quality docs

| Layer | Doc where | Purpose |
|-------|-----------|---------|
| Unit | Near code / `tests/` | Compiler, pure functions |
| Integration | `tests/` + one KB line | API + DB + queue |
| E2E | README or operations.md | Full docker path |
| Contract | `apis/` vs OpenAPI | Drift detection |

Document **what to run after change type X** in `CHANGE_IMPACT.md` — not only “run all tests”.

---

## 8. Operations & environment

| Doc | Contents |
|-----|----------|
| `operations.md` | up/down, seed, logs, common failures |
| `schemas/env.md` | var, default, secret?, required? |
| `stack.md` | versions of major deps |

**Never** document secrets’ values — names only.

---

## 9. Maturity ladder (self-assessment)

| Level | Docs & process |
|-------|----------------|
| **0** | README only |
| **1** | README + random markdown |
| **2** | KB with INDEX + schemas/apis |
| **3** | + feature deltas + dependency graph |
| **4** | + ADRs + CI doc checks + Cursor rules |
| **5** | + generated OpenAPI, graph validation, ops/runbooks |

**Orqis today:** ~2.5–3. Foundation target: **solid 4**.

---

## 10. Anti-patterns (avoid)

- Wiki that duplicates code and drifts  
- “Read everything in /docs before coding”  
- ADRs for every PR  
- Diagrams in PowerPoint not in repo  
- Scrap mixed with canonical KB  
- Changing architecture without `affects` review  
- No-code docs for a code-first product (or vice versa)  
- LLM-generated 200-line rule files  

---

## 11. Minimal “perfect enough” stack (any platform)

1. `INDEX.md` + `invariants.md`  
2. `reference/` (schemas + APIs)  
3. `features/Fxx.md` + `changelog.md`  
4. `graph/dependencies.yaml` + `CHANGE_IMPACT.md`  
5. `decisions/ADR-*`  
6. `operations.md` + `env.md`  
7. `CONTRIBUTING.md` + PR template  
8. Cursor: 1 always rule + globs per major area  
9. CI: test + optional link check  
10. Same PR updates code + reference docs  

---

*General reference — not Orqis-exclusive. Link from foundation/README.md.*
