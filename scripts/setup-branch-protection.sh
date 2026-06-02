#!/usr/bin/env bash
# Apply branch protection for stage and prod on nikhilmalkari8/orqis
# Requires: gh CLI, repo Pro OR public (see BRANCH_POLICY.md)

set -euo pipefail

REPO="${GITHUB_REPO:-nikhilmalkari8/orqis}"
# After first workflow run, confirm name in PR checks; override if needed.
STATUS_CONTEXT="${STATUS_CONTEXT:-enforce}"

protect_branch() {
  local branch="$1"
  echo "Protecting branch: $branch"
  gh api -X PUT "repos/${REPO}/branches/${branch}/protection" \
    --input - <<EOF
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["${STATUS_CONTEXT}"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0,
    "dismiss_stale_reviews": false
  },
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": false,
  "lock_branch": false,
  "allow_fork_syncing": false
}
EOF
}

echo "Repository: ${REPO}"
echo "Required status check: ${STATUS_CONTEXT}"
echo ""

if ! gh api "repos/${REPO}" --jq .private | grep -q false; then
  if gh api "repos/${REPO}" --jq .private | grep -q true; then
    echo "Note: Private repo on GitHub Free cannot use branch protection."
    echo "  Option A: Upgrade to GitHub Pro"
    echo "  Option B: gh repo edit ${REPO} --visibility public"
    echo ""
  fi
fi

protect_branch stage
protect_branch prod

echo ""
echo "Done. stage and prod now require PRs + status check '${STATUS_CONTEXT}'."
echo "Promotion: dev → stage → prod (enforced by enforce-branch-flow workflow)."
