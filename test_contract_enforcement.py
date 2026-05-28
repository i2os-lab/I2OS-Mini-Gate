import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from recheck_loop import RecheckLoopLayer


class TestRecheckLoopLayer(unittest.TestCase):
    def load_package(self, path):
        with open(ROOT / path, "r", encoding="utf-8") as file:
            return json.load(file)

    def test_recheck_loop_resolves_or_improves(self):
        layer = RecheckLoopLayer(policy_path=str(ROOT / "policy" / "balanced_policy.json"))
        result = layer.evaluate_recheck(self.load_package("recheck_loop/sample_recheck_rushed_send.json"))
        self.assertIn(result["loop_status"], ["RESOLVED", "IMPROVED_BUT_NOT_RESOLVED", "UNRESOLVED"])
        self.assertTrue(result["improved"] or result["resolved_to_go"])


if __name__ == "__main__":
    unittest.main()
