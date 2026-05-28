import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from recovery_path import RecoveryPathLayer


class TestRecoveryPathLayer(unittest.TestCase):
    def load_case(self, path):
        with open(ROOT / path, "r", encoding="utf-8") as file:
            return json.load(file)

    def test_hold_returns_clarify(self):
        layer = RecoveryPathLayer(policy_path=str(ROOT / "policy" / "balanced_policy.json"))
        result = layer.evaluate_case(self.load_case("recovery_path/sample_recovery_hold.json"))
        self.assertEqual(result["recovery_path"]["recovery_mode"], "CLARIFY")

    def test_repair_returns_repair_steps(self):
        layer = RecoveryPathLayer(policy_path=str(ROOT / "policy" / "balanced_policy.json"))
        result = layer.evaluate_case(self.load_case("recovery_path/sample_recovery_repair.json"))
        self.assertEqual(result["recovery_path"]["recovery_mode"], "REPAIR")
        self.assertGreater(len(result["recovery_path"]["recovery_steps"]), 0)

    def test_block_returns_block_and_reframe(self):
        layer = RecoveryPathLayer(policy_path=str(ROOT / "policy" / "strict_policy.json"))
        result = layer.evaluate_case(self.load_case("recovery_path/sample_recovery_block.json"))
        self.assertEqual(result["recovery_path"]["recovery_mode"], "BLOCK_AND_REFRAME")


if __name__ == "__main__":
    unittest.main()
