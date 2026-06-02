# Branch promotion policy

## Flow

```text
dev  ──PR──►  stage  ──PR──►  prod
```

| Target | Allowed source | Blocked |
|--------|----------------|---------|
| `stage` | `dev` only | Direct push, PR from `main`, `prod`, feature branches |
| `prod` | `stage` only | Direct push, PR from `dev` (skips stage) |

## Enforcement

1. **GitHub Actions** — [`.github/workflows/enforce-branch-flow.yml`](./workflows/enforce-branch-flow.yml) fails PRs with the wrong head branch.
2. **Branch protection** — `stage` and `prod` require PRs + the workflow check (see setup script).

## One-time setup (repo owner)

Private repos need **GitHub Pro** *or* a **public** repo for branch protection on GitHub Free.

```bash
# 1) Allow pushing workflow files (if push was rejected)
gh auth refresh -h github.com -s repo,workflow
git push origin dev

# 2) Run workflow once on dev (Actions tab) so the check name exists

# 3) Apply protection (after Pro upgrade OR: gh repo edit --visibility public)
./scripts/setup-branch-protection.sh
```

If the required check name differs, open a PR to `stage`, see the failed/pending check label in the PR UI, then update `STATUS_CONTEXT` in the script.

## Day-to-day

```bash
# Promote dev → stage
gh pr create --base stage --head dev --title "Promote dev to stage"

# Promote stage → prod
gh pr create --base prod --head stage --title "Promote stage to prod"
```

Develop on **dev** only; do not commit directly to `stage` or `prod`.
