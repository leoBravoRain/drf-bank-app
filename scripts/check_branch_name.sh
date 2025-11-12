#!/bin/bash
set -e

# Get current branch name
branch_name=$(git rev-parse --abbrev-ref HEAD)

# Regex pattern for allowed branch names
# Matches e.g. feature/NX-123, fix/NX-99-description, hotfix/NX-2, release/NX-400
pattern='^(feature|fix|hotfix|release)\/[A-Z]+-[0-9]+(-[a-z0-9._-]+)?$'

if [[ ! $branch_name =~ $pattern ]]; then
  echo "❌ Invalid branch name: '$branch_name'"
  echo ""
  echo "Branch names must follow this pattern:"
  echo "  ^(feature|fix|hotfix|release)/[A-Z]+-[0-9]+(-[a-z0-9._-]+)?$"
  echo ""
  echo "Examples of valid branch names:"
  echo "  ✅ feature/NX-123-add-login-endpoint"
  echo "  ✅ fix/NX-45-balance-bug"
  echo "  ✅ hotfix/NX-99"
  echo "  ✅ release/NX-400"
  echo ""
  echo "Examples of invalid branch names:"
  echo "  ❌ feature/login"
  echo "  ❌ feature/123-login"
  echo "  ❌ bugfix/NX123"
  echo ""
  exit 1
fi

echo "✅ Branch name '$branch_name' is valid."
