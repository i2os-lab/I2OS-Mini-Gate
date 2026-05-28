import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_bridge.runtime_bridge import AgentRuntimeBridge, build_command_action, guarded_dry_run


class TestAgentRuntimeBridge(unittest.TestCase):
    def setUp(self):
        self.bridge = AgentRuntimeBridge(policy_path=str(ROOT / "policy" / "default_policy.json"))

    def test_bridge_safe_read_permitted(self):
        with open(ROOT / "examples" / "bridge_safe_read.json", "r", encoding="utf-8") as file:
            action = json.load(file)
        result = self.bridge.guard(action)
        self.assertTrue(result["permitted"])
        self.assertEqual(result["decision"], "GO")

    def test_bridge_block_command(self):
        with open(ROOT / "examples" / "bridge_block_command.json", "r", encoding="utf-8") as file:
            action = json.load(file)
        result = self.bridge.guard(action)
        self.assertFalse(result["permitted"])
        self.assertEqual(result["decision"], "BLOCK")

    def test_build_command_action_dangerous(self):
        action = build_command_action("rm -rf ./project")
        self.assertEqual(action["action_type"], "command_execution")
        self.assertEqual(action["side_effect_level"], "destructive")
        self.assertFalse(action["reversible"])

    def test_guarded_dry_run_blocks_rm_rf(self):
        result = guarded_dry_run("rm -rf ./project", policy_path=str(ROOT / "policy" / "default_policy.json"))
        self.assertFalse(result["permitted"])
        self.assertEqual(result["decision"], "BLOCK")


if __name__ == "__main__":
    unittest.main()
