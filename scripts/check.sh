#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

python3 scripts/validate_constitution.py CONSTITUTION.md
git diff --check
