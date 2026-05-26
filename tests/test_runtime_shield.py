import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime_shield import RuntimeShield


class TestRuntimeShield(unittest.TestCase):
    def setUp(self):
        self.shield = RuntimeShield(policy_path=str(ROOT / "policy" / "strict_policy.json"))

    def load_action(self, filename):
        with open(ROOT / "examples" / filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def test_safe_summary_permitted(self):
        action = self.load_action("audit_go_safe_summary.json")
        result = self.shield.shield(action)
        self.assertTrue(result["permitted"])
        self.assertEqual(result["decision"], "GO")

    def test_prompt_injection_blocked(self):
        action = self.load_action("audit_block_prompt_injection.json")
        result = self.shield.shield(action)
        self.assertFalse(result["permitted"])
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("PROMPT_INJECTION_TRANSITION", result["reason_codes"])

    def test_explain_returns_text(self):
        action = self.load_action("audit_block_prompt_injection.json")
        explanation = self.shield.explain(action)
        self.assertIsInstance(explanation, str)
        self.assertTrue(len(explanation) > 0)


if __name__ == "__main__":
    unittest.main()
