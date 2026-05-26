import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from i2os_gate import i2os_gate, load_policy


class TestPolicyProfiles(unittest.TestCase):
    def test_profile_files_exist(self):
        self.assertTrue((ROOT / "policy" / "strict_policy.json").exists())
        self.assertTrue((ROOT / "policy" / "balanced_policy.json").exists())
        self.assertTrue((ROOT / "policy" / "permissive_policy.json").exists())

    def test_profiles_load(self):
        for name in ["strict_policy.json", "balanced_policy.json", "permissive_policy.json"]:
            policy = load_policy(str(ROOT / "policy" / name))
            self.assertIn("policy_name", policy)
            self.assertIn("profile", policy)

    def test_strict_profile_blocks_prompt_injection(self):
        policy = load_policy(str(ROOT / "policy" / "strict_policy.json"))
        with open(ROOT / "examples" / "audit_block_prompt_injection.json", "r", encoding="utf-8") as file:
            action = json.load(file)
        result = i2os_gate(action, policy=policy)
        self.assertEqual(result["decision"], "BLOCK")

    def test_balanced_profile_safe_summary_go(self):
        policy = load_policy(str(ROOT / "policy" / "balanced_policy.json"))
        with open(ROOT / "examples" / "audit_go_safe_summary.json", "r", encoding="utf-8") as file:
            action = json.load(file)
        result = i2os_gate(action, policy=policy)
        self.assertEqual(result["decision"], "GO")


if __name__ == "__main__":
    unittest.main()
