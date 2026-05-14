import textwrap
import unittest

from scripts.constitution_parser import ConstitutionParseError, parse_constitution


VALID_CONSTITUTION = """
# The Constitution

## Preamble

## I. Core Values
### 1. Human-Centeredness
### 2. Safety First
### 3. Beneficence
### 4. Non-Maleficence
### 5. Respect and Dignity
### 6. Honesty and Integrity

## II. Alignment and Decision-Making Principles
### 7. Intent Interpretation
### 8. Proportionality
### 9. Least Harm Principle
### 10. Long-Term Impact Awareness

## III. Boundaries and Refusals
### 11. Right to Refuse
### 12. No Role Confusion

## IV. Privacy and Data Responsibility
### 13. Privacy Respect
### 14. Confidentiality by Default

## V. Agency and Power Use
### 15. Power Awareness
### 16. No Hidden Objectives

## VI. Continuous Improvement and Humility
### 17. Epistemic Humility
### 18. Learning Orientation

## VII. Meta-Governance
### 19. Constitution Supremacy
### 20. Amendments

## Closing Statement
"""


class ConstitutionParserTests(unittest.TestCase):
    def test_valid_constitution_parses_all_principles(self) -> None:
        constitution = parse_constitution(textwrap.dedent(VALID_CONSTITUTION).strip())

        self.assertEqual("# The Constitution", constitution.title)
        self.assertEqual(20, len(constitution.principles))
        self.assertEqual(
            (
                "Preamble",
                "I. Core Values",
                "II. Alignment and Decision-Making Principles",
                "III. Boundaries and Refusals",
                "IV. Privacy and Data Responsibility",
                "V. Agency and Power Use",
                "VI. Continuous Improvement and Humility",
                "VII. Meta-Governance",
                "Closing Statement",
            ),
            constitution.sections,
        )
        self.assertEqual("Closing Statement", constitution.sections[-1])

    def test_duplicate_principle_number_is_rejected(self) -> None:
        malformed = textwrap.dedent(VALID_CONSTITUTION).strip().replace(
            "### 12. No Role Confusion",
            "### 11. No Role Confusion",
        )

        with self.assertRaisesRegex(
            ConstitutionParseError,
            r"principles must be numbered consecutively from 1 through 20",
        ):
            parse_constitution(malformed)

    def test_missing_closing_statement_is_rejected(self) -> None:
        malformed = textwrap.dedent(VALID_CONSTITUTION).strip().replace(
            "\n## Closing Statement",
            "",
        )

        with self.assertRaisesRegex(
            ConstitutionParseError,
            "sections must match the required constitution outline",
        ):
            parse_constitution(malformed)

    def test_missing_required_outline_sections_are_rejected(self) -> None:
        malformed = textwrap.dedent(VALID_CONSTITUTION).strip()
        for section in (
            "\n## I. Core Values",
            "\n## II. Alignment and Decision-Making Principles",
            "\n## III. Boundaries and Refusals",
            "\n## IV. Privacy and Data Responsibility",
            "\n## V. Agency and Power Use",
            "\n## VI. Continuous Improvement and Humility",
            "\n## VII. Meta-Governance",
        ):
            malformed = malformed.replace(section, "")

        with self.assertRaisesRegex(
            ConstitutionParseError,
            "sections must match the required constitution outline",
        ):
            parse_constitution(malformed)


if __name__ == "__main__":
    unittest.main()
