import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestCIArtifacts(unittest.TestCase):
    def test_workflow_exists(self):
        self.assertTrue((ROOT / ".github" / "workflows" / "i2os-mini-gate.yml").exists())

    def test_ci_scanner_exists(self):
        self.assertTrue((ROOT / "ci" / "i2os_ci_scan.py").exists())

    def test_ci_scan_go_only_passes(self):
        result = subprocess.run(
            [
                sys.executable,
                "ci/i2os_ci_scan.py",
                "--policy", "policy/default_policy.json",
                "--actions", "examples/audit_go_safe_summary.json",
                "--fail-on", "BLOCK"
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("[GO]", result.stdout)

    def test_ci_scan_block_fails(self):
        result = subprocess.run(
            [
                sys.executable,
                "ci/i2os_ci_scan.py",
                "--policy", "policy/default_policy.json",
                "--actions", "examples/audit_block_prompt_injection.json",
                "--fail-on", "BLOCK"
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("[BLOCK]", result.stdout)


if __name__ == "__main__":
    unittest.main()
