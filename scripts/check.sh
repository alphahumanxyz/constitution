#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf 'check failed: %s\n' "$1" >&2
  exit 1
}

[[ -f CONSTITUTION.md ]] || fail "CONSTITUTION.md is missing"
[[ -f README.md ]] || fail "README.md is missing"

grep -q '^# The Constitution$' CONSTITUTION.md || fail "CONSTITUTION.md must remain the canonical constitution document"
grep -q 'canonical governance document' README.md || fail "README.md must identify CONSTITUTION.md as canonical"
grep -q '\[CONSTITUTION.md\](CONSTITUTION.md)' README.md || fail "README.md must link to CONSTITUTION.md"

if grep -qiE 'must (interpret|refuse|not claim|be aware|follow)|overrides:|right to refuse|no role confusion' README.md; then
  fail "README.md must not duplicate constitutional rules; keep them in CONSTITUTION.md"
fi

printf 'constitution governance checks passed\n'
