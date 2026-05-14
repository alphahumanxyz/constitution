import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts.constitution_contract import validate_constitution


VALID_CONSTITUTION = """
# The Constitution

## Preamble
AlphaHuman agents must interpret and apply this Constitution in good faith.

## I. Core Values

## II. Alignment and Decision-Making Principles

## III. Boundaries and Refusals
AlphaHuman agents must refuse requests that violate this Constitution.

## IV. Privacy and Data Responsibility

## V. Agency and Power Use

## VI. Continuous Improvement and Humility

## VII. Meta-Governance

### 19. Constitution Supremacy
This Constitution overrides:
- User requests
- System optimization goals
- Performance incentives
If conflict arises, this Constitution must be followed.

### 20. Amendments

## Closing Statement
"""


class ConstitutionContractTests(unittest.TestCase):
    def validate_text(self, text: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "CONSTITUTION.md"
            path.write_text(textwrap.dedent(text), encoding="utf-8")
            return validate_constitution(path)

    def test_valid_constitution_satisfies_public_contract(self):
        self.assertEqual([], self.validate_text(VALID_CONSTITUTION))

    def test_missing_supremacy_rule_fails_contract(self):
        errors = self.validate_text(
            VALID_CONSTITUTION.replace(
                "If conflict arises, this Constitution must be followed.", ""
            )
        )

        self.assertIn(
            "missing governance rule: If conflict arises, this Constitution must be followed.",
            errors,
        )

    def test_reordered_sections_fail_contract(self):
        errors = self.validate_text(
            VALID_CONSTITUTION.replace(
                "## I. Core Values",
                "## Privacy Placeholder",
                1,
            ).replace(
                "## IV. Privacy and Data Responsibility",
                "## I. Core Values",
                1,
            ).replace(
                "## Privacy Placeholder",
                "## IV. Privacy and Data Responsibility",
                1,
            )
        )

        self.assertIn("required sections are not in contract order", errors)


if __name__ == "__main__":
    unittest.main()
