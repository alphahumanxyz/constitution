#!/usr/bin/env python3
"""Parse and validate the constitution markdown structure."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SECTION_RE = re.compile(r"^## (?P<title>(?:[IVX]+\. .+|Preamble|Closing Statement))$")
PRINCIPLE_RE = re.compile(r"^### (?P<number>\d+)\. (?P<title>.+)$")
EXPECTED_PRINCIPLES = tuple(range(1, 21))
EXPECTED_SECTIONS = (
    "Preamble",
    "I. Core Values",
    "II. Alignment and Decision-Making Principles",
    "III. Boundaries and Refusals",
    "IV. Privacy and Data Responsibility",
    "V. Agency and Power Use",
    "VI. Continuous Improvement and Humility",
    "VII. Meta-Governance",
    "Closing Statement",
)


class ConstitutionParseError(ValueError):
    """Raised when constitution markdown cannot be parsed safely."""


@dataclass(frozen=True)
class Principle:
    number: int
    title: str
    line_number: int


@dataclass(frozen=True)
class Constitution:
    title: str
    sections: tuple[str, ...]
    principles: tuple[Principle, ...]


def parse_constitution(text: str) -> Constitution:
    lines = text.splitlines()
    if not lines:
        raise ConstitutionParseError("line 1: constitution is empty")

    if lines[0] != "# The Constitution":
        raise ConstitutionParseError("line 1: expected '# The Constitution'")

    sections: list[str] = []
    principles: list[Principle] = []
    current_section: str | None = None

    for line_number, line in enumerate(lines, start=1):
        if section_match := SECTION_RE.match(line):
            current_section = section_match.group("title")
            sections.append(current_section)
            continue

        if principle_match := PRINCIPLE_RE.match(line):
            if current_section is None:
                raise ConstitutionParseError(
                    f"line {line_number}: principle appears before any section"
                )
            principles.append(
                Principle(
                    number=int(principle_match.group("number")),
                    title=principle_match.group("title"),
                    line_number=line_number,
                )
            )

    found_numbers = tuple(principle.number for principle in principles)
    if found_numbers != EXPECTED_PRINCIPLES:
        raise ConstitutionParseError(
            "principles must be numbered consecutively from 1 through 20; "
            f"found {list(found_numbers)}"
        )

    if tuple(sections) != EXPECTED_SECTIONS:
        raise ConstitutionParseError(
            "sections must match the required constitution outline; "
            f"found {sections}"
        )

    return Constitution(
        title=lines[0],
        sections=tuple(sections),
        principles=tuple(principles),
    )


def parse_constitution_file(path: Path) -> Constitution:
    return parse_constitution(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        default="CONSTITUTION.md",
        type=Path,
        help="constitution markdown file to parse",
    )
    args = parser.parse_args()

    try:
        constitution = parse_constitution_file(args.path)
    except ConstitutionParseError as error:
        print(f"{args.path}: {error}", file=sys.stderr)
        return 1

    print(
        f"{args.path}: parsed {len(constitution.sections)} sections and "
        f"{len(constitution.principles)} principles"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
