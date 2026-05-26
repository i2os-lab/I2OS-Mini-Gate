import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from i2os_gate import build_error_result, safe_load_json_file, safe_load_policy_file


class TestHardening(unittest.TestCase):
    def test_build_error_result_hold(self):
        result = build_error_result("TEST_ERROR", "test message", "repair it")
        self.assertEqual(result["decision"], "HOLD")
        self.assertIn("TEST_ERROR", result["reason_codes"])

    def test_missing_file_returns_error(self):
        data, err = safe_load_json_file(str(ROOT / "examples" / "not_found.json"))
        self.assertIsNone(data)
        self.assertEqual(err["decision"], "HOLD")
        self.assertIn("INPUT_FILE_NOT_FOUND", err["reason_codes"])

    def test_invalid_json_returns_error(self):
        data, err = safe_load_json_file(str(ROOT / "examples" / "invalid_json_example.json"))
        self.assertIsNone(data)
        self.assertEqual(err["decision"], "HOLD")
        self.assertIn("INVALID_JSON", err["reason_codes"])

    def test_missing_policy_returns_error(self):
        policy, err = safe_load_policy_file(str(ROOT / "policy" / "not_found_policy.json"))
        self.assertIsNone(policy)
        self.assertEqual(err["decision"], "HOLD")
        self.assertIn("POLICY_FILE_NOT_FOUND", err["reason_codes"])


if __name__ == "__main__":
    unittest.main()
