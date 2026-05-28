import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from future_constraint import FutureConstraintLayer


class TestFutureConstraintLayer(unittest.TestCase):
    def load_action(self, path):
        with open(ROOT / path, "r", encoding="utf-8") as file:
            return json.load(file)

    def test_safe_action_future_low(self):
        layer = FutureConstraintLayer(policy_path=str(ROOT / "policy" / "balanced_policy.json"))
        result = layer.evaluate(self.load_action("demo/demo_safe_action.json"))
        self.assertEqual(result["future_constraint"]["future_constraint_level"], "LOW")
        self.assertTrue(result["future_constraint"]["future_compatible"])

    def test_delete_action_future_high_or_critical(self):
        layer = FutureConstraintLayer(policy_path=str(ROOT / "policy" / "strict_policy.json"))
        result = layer.evaluate(self.load_action("demo/demo_delete_block.json"))
        self.assertIn(result["future_constraint"]["future_constraint_level"], ["HIGH", "CRITICAL"])
        self.assertFalse(result["future_constraint"]["future_compatible"])


if __name__ == "__main__":
    unittest.main()
