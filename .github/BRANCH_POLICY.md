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

Repo is **public** — branch protection is enabled on `stage` and `prod` (PR required, no direct push).

**Push the workflow** (needs `workflow` scope on your `gh` token once):

```bash
gh auth refresh -h github.com -s repo,workflow
# Complete the browser device login when prompted
git push origin dev
```

**Re-enable the CI gate** after the workflow exists on `dev`:

```bash
./scripts/setup-branch-protection.sh
```

The first `dev → stage` PR can merge without the `enforce` check (workflow must land on `stage` first). Later PRs use the check once the workflow is on the base branch.

If the required check name differs, open a PR to `stage`, see the failed/pending check label in the PR UI, then update `STATUS_CONTEXT` in the script.

## Day-to-day

```bash
# Promote dev → stage
gh pr create --base stage --head dev --title "Promote dev to stage"

# Promote stage → prod
gh pr create --base prod --head stage --title "Promote stage to prod"
```

Develop on **dev** only; do not commit directly to `stage` or `prod`.
