#!/usr/bin/env bash
set -euo pipefail

python3 -m unittest discover -s tests
python3 scripts/constitution_contract.py CONSTITUTION.md
