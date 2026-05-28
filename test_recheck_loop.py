import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from human_admissibility import HumanAdmissibilityLayer


class TestHumanAdmissibilityLayer(unittest.TestCase):
    def load_case(self, path):
        with open(ROOT / path, "r", encoding="utf-8") as file:
            return json.load(file)

    def test_confirmed_safe_action_go(self):
        layer = HumanAdmissibilityLayer(policy_path=str(ROOT / "policy" / "balanced_policy.json"))
        result = layer.evaluate(self.load_case("human_admissibility/sample_human_confirmed_safe_action.json"))
        self.assertEqual(result["human_decision"], "GO")

    def test_emotional_escalation_not_go(self):
        layer = HumanAdmissibilityLayer(policy_path=str(ROOT / "policy" / "strict_policy.json"))
        result = layer.evaluate(self.load_case("human_admissibility/sample_emotional_escalation_block.json"))
        self.assertIn(result["human_decision"], ["REPAIR", "BLOCK"])
        self.assertFalse(result["human_admissible"])

    def test_rushed_send_hold_or_repair_or_block(self):
        layer = HumanAdmissibilityLayer(policy_path=str(ROOT / "policy" / "balanced_policy.json"))
        result = layer.evaluate(self.load_case("human_admissibility/sample_human_rushed_send.json"))
        self.assertIn(result["human_decision"], ["HOLD", "REPAIR", "BLOCK"])


if __name__ == "__main__":
    unittest.main()
