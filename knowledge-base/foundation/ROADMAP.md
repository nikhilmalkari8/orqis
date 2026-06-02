# Foundation & product roadmap

## Phase 0 — Concept (done)

**F00 mvp-baseline:** Agents in registry, workflows, Celery runs, UI, KB + Cursor rules.

**Exit:** E2E mock run + agent reuse visible in UI.

---

## Phase 1 — Foundation hardening (you are here)

**Theme:** Same product, **trustworthy process** — won’t lose track when code grows.

| Week | Focus | Deliverables |
|------|--------|--------------|
| 1 | Prove + document ops | G1–G3 in GAPS.md, operations.md, env.md |
| 2 | CI + tests | G4–G5, CONTRIBUTING.md |
| 3 | Decisions frozen | G6 ADRs, validate dependencies.yaml |
| 4 | Reliability slice | F01 timeouts/retries, update graph |

**Exit criteria:**

- CI green on main
- KB complete for env + ops + testing
- ADR-001..003 written
- You still use platform for real task without fear

---

## Phase 2 — Operate (features)

| ID | Feature | Depends on |
|----|---------|------------|
| F01 | Step/workflow timeouts + 1 retry | Foundation |
| F02 | Cron (Celery Beat) | F01 |
| F03 | `POST /agents` onboard (contract validation) | F01 |
| F04 | CLI for run/list | API stable |
| F05 | Workflow branches (compiler v2) | F01 |
| F06 | API keys + workspaces | Auth model |

Each feature = one `features/Fxx.md` + graph YAML update only.

---

## Phase 3 — Scale (later)

Teams, marketplace, enterprise SSO, partner deploy hooks (Vercel/Railway), native trace viewer.

**Rule:** Phase 3 items never start until Phase 2 exit criteria met.

---

## How to append (butter smooth)

```
New idea → Is it Fxx or ADR?
  → Feature: features/Fxx.md + INDEX row + dependencies.yaml + code
  → Decision: foundation/decisions/ADR-NNN-title.md (1 page)
  → Big milestone: bump CURRENT_STATE.md only
```

Never expand `scrap/`. Never add long prose to Cursor rules.
