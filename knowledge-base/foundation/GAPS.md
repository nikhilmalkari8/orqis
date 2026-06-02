# Foundation gaps — what to do now

Ordered by **leverage** (prevents losing track when codebase grows).

## P0 — Do in foundation phase (1–2 weeks)

| # | Item | Why | Output |
|---|------|-----|--------|
| G1 | **Dogfood loop** | Validates architecture | You run `competitor-intel` weekly |
| G2 | **`knowledge-base/operations.md`** | Onboarding future you | **Done** |
| G3 | **`knowledge-base/schemas/env.md`** | No secret confusion | **Done** |
| G4 | **CI: pytest + ruff** | Regressions caught early | `.github/workflows/ci.yml` |
| G5 | **Integration test** | API + mock run without Docker optional | `tests/test_run_mock.py` |
| G6 | **`foundation/decisions/ADR-001..003`** | Why key choices frozen | **Done** |
| G7 | **KB graph validation** | dependencies.yaml stays true | **Done** — `scripts/validate_dependencies.py` + PR template |

## P1 — Foundation polish (weeks 2–4)

| # | Item | Why |
|---|------|-----|
| G8 | API prefix `/api/v1` | Future breaking changes isolated |
| G9 | Arango migration note in `scripts/` | Index/collection changes documented |
| G10 | Structured logging (`execution_id`) | Debug at scale |
| G11 | OpenAPI export from FastAPI | `apis/` stays in sync |
| G12 | `CONTRIBUTING.md` | Feature + KB update ritual | **Done** |
| G13 | Retries + step timeout (F01) | Reliability minimum |

## P2 — After foundation (product features)

| Item | Feature ID suggestion |
|------|---------------------|
| Cron schedules | F02 |
| External agent onboard API | F03 |
| CLI `orqis run` | F04 |
| Branching workflows | F05 |
| Team / API keys | F06 |

## Anti-goals (foundation)

- No marketplace, no no-code canvas, no rewrite of LangGraph
- No second database
- No microservices split yet (monolith + worker is fine)
