# Orqis Knowledge Base (KB)

**Purpose:** Let AI (and you) implement small features fast with **minimal tokens**.

## How to use (humans)

1. **Always start from** [`INDEX.md`](./INDEX.md) — it is the only required read for most tasks.
2. When you ship a feature, append **one small file** under `features/` using [`feature-template.md`](./feature-template.md).
3. Add **one line** to `INDEX.md` feature table + **3–5 lines** to `changelog.md`.
4. Do **not** duplicate long specs — link to `orqis_mvp_design.md` §sections instead.

## Token rules (for maintainers)

| Do | Don't |
|----|--------|
| Tables, paths, invariants | Paste full design doc into KB |
| One feature = one `features/Fxx-*.md` (~40 lines max) | Grow a single mega doc |
| Update INDEX row + changelog only | Rewrite architecture each time |
| Mark **deprecated** in changelog | Delete history |

## Doc hierarchy

```
INDEX.md          ← read first (always)
invariants.md     ← hard rules
map.md            ← where code lives
stack.md          ← dependencies
features/F*.md    ← incremental deltas
changelog.md      ← dated one-liners
```

Deep reference (read only if INDEX points you there): `orqis.md`, `orqis_mvp_design.md`.
