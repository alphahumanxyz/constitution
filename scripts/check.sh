#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

python3 -m unittest discover -s tests
python3 scripts/constitution_parser.py CONSTITUTION.md
git diff --check
