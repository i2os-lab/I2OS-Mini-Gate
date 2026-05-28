import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from execution_contract import ExecutionContractLayer


class TestExecutionContractLayer(unittest.TestCase):
    def load_case(self, path):
        with open(ROOT / path, "r", encoding="utf-8") as file:
            return json.load(file)

    def test_go_issues_contract(self):
        layer = ExecutionContractLayer(policy_path=str(ROOT / "policy" / "balanced_policy.json"))
        result = layer.evaluate_input(self.load_case("execution_contract/sample_contract_go.json"))
        contract = result["execution_contract"]
        self.assertEqual(contract["contract_status"], "ISSUED")
        self.assertIn("allowed_scope", contract)
        self.assertIn("recheck_triggers", contract)

    def test_block_does_not_issue_contract(self):
        layer = ExecutionContractLayer(policy_path=str(ROOT / "policy" / "strict_policy.json"))
        result = layer.evaluate_input(self.load_case("execution_contract/sample_contract_block.json"))
        contract = result["execution_contract"]
        self.assertEqual(contract["contract_status"], "NOT_ISSUED")


if __name__ == "__main__":
    unittest.main()
