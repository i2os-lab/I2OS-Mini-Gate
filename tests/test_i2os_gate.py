import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from i2os_gate import i2os_gate, load_policy


def load_json(relative_path):
    with open(ROOT / relative_path, "r", encoding="utf-8") as file:
        return json.load(file)


class TestI2OSMiniGate(unittest.TestCase):
    def setUp(self):
        self.policy = load_policy(str(ROOT / "policy" / "default_policy.json"))

    def test_go_safe_summary(self):
        action = load_json("examples/audit_go_safe_summary.json")
        result = i2os_gate(action, policy=self.policy)
        self.assertEqual(result["decision"], "GO")
        self.assertEqual(result["risk_level"], "LOW")

    def test_repair_external_api(self):
        action = load_json("examples/audit_repair_external_api.json")
        result = i2os_gate(action, policy=self.policy)
        self.assertIn(result["decision"], ["REPAIR", "BLOCK"])
        self.assertIn("EXTERNAL_SIDE_EFFECT", result["reason_codes"])
        self.assertIn("USER_CONFIRMATION_MISSING", result["reason_codes"])

    def test_block_prompt_injection(self):
        action = load_json("examples/audit_block_prompt_injection.json")
        result = i2os_gate(action, policy=self.policy)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(result["risk_level"], "CRITICAL")
        self.assertIn("PROMPT_INJECTION_TRANSITION", result["reason_codes"])

    def test_missing_fields_hold(self):
        action = {"actor": "AI agent", "proposed_action": "modify selected files"}
        result = i2os_gate(action, policy=self.policy)
        self.assertEqual(result["decision"], "HOLD")
        self.assertIn("MISSING_REQUIRED_FIELDS", result["reason_codes"])

    def test_destructive_command_block(self):
        action = {
            "actor": "AI agent",
            "current_state": "User asked to clean temporary files",
            "proposed_action": "execute rm -rf ./project",
            "action_type": "command_execution",
            "tool_name": "terminal",
            "target": "./project",
            "target_scope": "entire_project",
            "side_effect_level": "destructive",
            "permission_level": "user",
            "requires_confirmation": True,
            "user_confirmed": False,
            "reversible": False,
            "sandbox_required": True,
            "sandbox_enabled": False,
            "external_effect": False
        }
        result = i2os_gate(action, policy=self.policy)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("COMMAND_EXECUTION_CONFIRMATION_MISSING", result["reason_codes"])
        self.assertIn("DESTRUCTIVE_TOOL_SCOPE_COMBINATION", result["reason_codes"])


if __name__ == "__main__":
    unittest.main()
