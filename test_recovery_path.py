import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from multi_agent import MultiAgentGovernanceLayer


class TestMultiAgentGovernanceLayer(unittest.TestCase):
    def load_chain(self, path):
        with open(ROOT / path, "r", encoding="utf-8") as file:
            return json.load(file)

    def test_upload_risk_chain_not_go(self):
        layer = MultiAgentGovernanceLayer(policy_path=str(ROOT / "policy" / "balanced_policy.json"))
        result = layer.evaluate_chain(self.load_chain("multi_agent/sample_chain_upload_risk.json"))
        self.assertIn(result["chain_decision"], ["REPAIR", "BLOCK"])
        self.assertFalse(result["chain_permitted"])

    def test_safe_local_chain_evaluates(self):
        layer = MultiAgentGovernanceLayer(policy_path=str(ROOT / "policy" / "balanced_policy.json"))
        result = layer.evaluate_chain(self.load_chain("multi_agent/sample_chain_safe_local.json"))
        self.assertIn("chain_decision", result)
        self.assertEqual(result["agent_count"], 3)


if __name__ == "__main__":
    unittest.main()
