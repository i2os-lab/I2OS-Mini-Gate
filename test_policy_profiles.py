import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from local_tool.i2os_local_security import build_file_action, build_url_action
from i2os_gate import i2os_gate, load_policy


class TestLocalSecurityTool(unittest.TestCase):
    def setUp(self):
        self.policy = load_policy(str(ROOT / "policy" / "default_policy.json"))

    def test_build_file_read_go(self):
        action = build_file_action("./README.md", "read")
        result = i2os_gate(action, policy=self.policy)
        self.assertEqual(result["decision"], "GO")

    def test_build_file_delete_block(self):
        action = build_file_action("./project", "delete")
        result = i2os_gate(action, policy=self.policy)
        self.assertEqual(result["decision"], "BLOCK")

    def test_build_url_get(self):
        action = build_url_action("https://example.com", "get")
        result = i2os_gate(action, policy=self.policy)
        self.assertIn(result["decision"], ["GO", "REPAIR"])

    def test_build_url_upload_not_go(self):
        action = build_url_action("https://example.com/upload", "upload")
        result = i2os_gate(action, policy=self.policy)
        self.assertIn(result["decision"], ["REPAIR", "BLOCK"])


if __name__ == "__main__":
    unittest.main()
