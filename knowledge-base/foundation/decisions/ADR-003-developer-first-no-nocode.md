# ADR-003: Developer-first workflows (no no-code builder)

**Status:** accepted  
**Date:** 2026-06-01

## Context

Workflow platforms often ship visual builders (n8n-style). Orqis targets developers who need accuracy and reuse of their own agents.

## Decision

Workflows defined via **JSON/YAML/API**; UI is **operational** (list, run, observe) — not a drag-and-drop composer in MVP or foundation phase.

## Consequences

- **Pros:** Faster MVP; matches “agents in production” thesis; smaller UI surface
- **Cons:** Non-devs cannot self-serve; GTM is engineer-led initially
- **UI may add:** run form from `definition.inputs`, YAML viewer — not node canvas

## Alternatives rejected

- Form-based step editor (old plan) — removed from implementation path  
- NL workflow generator — Phase 3+ only if ever
