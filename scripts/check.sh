#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

required_files=(
  "README.md"
  "CONSTITUTION.md"
  "LICENSE"
)

for path in "${required_files[@]}"; do
  if [[ ! -f "$path" ]]; then
    echo "missing required file: $path" >&2
    exit 1
  fi
done

grep -q "^# " README.md
grep -q "^# " CONSTITUTION.md
grep -q "safe" README.md

echo "constitution check ok"
