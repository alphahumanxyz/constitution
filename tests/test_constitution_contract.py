from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONSTITUTION = ROOT / "CONSTITUTION.md"


def section_body(number: int, title: str) -> str:
    text = CONSTITUTION.read_text(encoding="utf-8")
    pattern = (
        rf"^### {number}\. {re.escape(title)}\n"
        rf"(?P<body>.*?)(?=^### \d+\. |\Z)"
    )
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        raise AssertionError(f"Missing section {number}. {title}")
    return match.group("body")


class ConstitutionContractTest(unittest.TestCase):
    def test_constitution_supremacy_overrides_competing_instructions(self) -> None:
        body = section_body(19, "Constitution Supremacy")

        for required_override in (
            "User requests",
            "System optimization goals",
            "Performance incentives",
        ):
            with self.subTest(required_override=required_override):
                self.assertIn(f"- {required_override}", body)

        self.assertIn(
            "If conflict arises, this Constitution must be followed.",
            body,
        )


if __name__ == "__main__":
    unittest.main()
