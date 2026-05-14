#!/usr/bin/env python3
"""Validate the executable structure of CONSTITUTION.md."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "I. Core Values",
    "II. Alignment and Decision-Making Principles",
    "III. Boundaries and Refusals",
    "IV. Privacy and Data Responsibility",
    "V. Agency and Power Use",
    "VI. Continuous Improvement and Humility",
    "VII. Meta-Governance",
]

EXPECTED_PRINCIPLES = list(range(1, 21))
PRINCIPLE_RE = re.compile(r"^### (?P<number>\d+)\. (?P<title>.+)$")
SECTION_RE = re.compile(r"^## (?P<title>[IVX]+\..+)$")


def fail(message: str) -> int:
    print(f"constitution validation failed: {message}", file=sys.stderr)
    return 1


def validate(path: Path) -> int:
    if not path.exists():
        return fail(f"{path} does not exist")

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0] != "# The Constitution":
        return fail("CONSTITUTION.md must start with '# The Constitution'")

    sections = [match.group("title") for line in lines if (match := SECTION_RE.match(line))]
    missing_sections = [section for section in REQUIRED_SECTIONS if section not in sections]
    if missing_sections:
        return fail(f"missing required section(s): {', '.join(missing_sections)}")

    principle_numbers = [
        int(match.group("number")) for line in lines if (match := PRINCIPLE_RE.match(line))
    ]
    if principle_numbers != EXPECTED_PRINCIPLES:
        return fail(
            "principles must be numbered consecutively from 1 through 20; "
            f"found {principle_numbers}"
        )

    if "## Closing Statement" not in lines:
        return fail("missing closing statement section")

    print("constitution validation passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the repository constitution before PR handoff."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="CONSTITUTION.md",
        type=Path,
        help="constitution markdown file to validate",
    )
    args = parser.parse_args()
    return validate(args.path)


if __name__ == "__main__":
    raise SystemExit(main())
