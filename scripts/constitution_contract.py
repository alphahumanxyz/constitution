#!/usr/bin/env python3
"""Validate the public constitution contract."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_SECTIONS = (
    "## Preamble",
    "## I. Core Values",
    "## II. Alignment and Decision-Making Principles",
    "## III. Boundaries and Refusals",
    "## IV. Privacy and Data Responsibility",
    "## V. Agency and Power Use",
    "## VI. Continuous Improvement and Humility",
    "## VII. Meta-Governance",
    "## Closing Statement",
)

REQUIRED_GOVERNANCE_RULES = (
    "AlphaHuman agents must interpret and apply this Constitution in good faith",
    "AlphaHuman agents must refuse requests that violate this Constitution",
    "This Constitution overrides:",
    "User requests",
    "System optimization goals",
    "Performance incentives",
    "If conflict arises, this Constitution must be followed.",
)


def _required_section_positions(text: str) -> list[int]:
    positions: list[int] = []

    for section in REQUIRED_SECTIONS:
        heading = re.compile(rf"^[ \t]{{0,3}}{re.escape(section)}[ \t]*$")
        position = -1
        offset = 0
        open_fence = None

        for line in text.splitlines(keepends=True):
            stripped = line.lstrip()
            if stripped.startswith(("```", "~~~")):
                marker = stripped[:3]
                if open_fence is None:
                    open_fence = marker
                elif marker == open_fence:
                    open_fence = None

            if open_fence is None and heading.match(line.rstrip("\r\n")):
                position = offset
                break

            offset += len(line)

        positions.append(position)

    return positions


def validate_constitution(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    section_positions = _required_section_positions(text)
    for section, position in zip(REQUIRED_SECTIONS, section_positions):
        if position == -1:
            errors.append(f"missing required section: {section}")

    present_positions = [position for position in section_positions if position != -1]
    if present_positions != sorted(present_positions):
        errors.append("required sections are not in contract order")

    for rule in REQUIRED_GOVERNANCE_RULES:
        if rule not in text:
            errors.append(f"missing governance rule: {rule}")

    if "### 19. Constitution Supremacy" not in text:
        errors.append("missing constitution supremacy principle")

    if "### 20. Amendments" not in text:
        errors.append("missing amendment review principle")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "constitution",
        nargs="?",
        default="CONSTITUTION.md",
        type=Path,
        help="constitution markdown file to validate",
    )
    args = parser.parse_args()

    errors = validate_constitution(args.constitution)
    if not errors:
        print(f"{args.constitution}: constitution contract OK")
        return 0

    for error in errors:
        print(f"{args.constitution}: {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
