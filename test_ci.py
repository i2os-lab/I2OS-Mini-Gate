import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestI2OSCLI(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "i2os_gate.py", *args],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )

    def test_help(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Runtime Admissibility Scanner", result.stdout)

    def test_json_only(self):
        result = self.run_cli(
            "--action", "examples/audit_go_safe_summary.json",
            "--json-only",
            "--no-reports"
        )
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(data["decision"], "GO")

    def test_policy_cli_block(self):
        result = self.run_cli(
            "--action", "examples/audit_block_prompt_injection.json",
            "--policy", "policy/default_policy.json",
            "--json-only",
            "--no-reports"
        )
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(data["decision"], "BLOCK")
        self.assertIn("PROMPT_INJECTION_TRANSITION", data["reason_codes"])

    def test_html_report(self):
        result = self.run_cli(
            "--action", "examples/audit_block_prompt_injection.json",
            "--html",
            "--report-prefix", "test_dashboard"
        )
        self.assertEqual(result.returncode, 0)
        self.assertTrue((ROOT / "dashboard" / "test_dashboard.html").exists())


if __name__ == "__main__":
    unittest.main()
