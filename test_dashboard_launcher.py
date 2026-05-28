import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestPackageMode(unittest.TestCase):
    def test_package_files_exist(self):
        self.assertTrue((ROOT / "i2os_mini_gate" / "__init__.py").exists())
        self.assertTrue((ROOT / "i2os_mini_gate" / "__main__.py").exists())
        self.assertTrue((ROOT / "pyproject.toml").exists())

    def test_module_json_only_go(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "i2os_mini_gate",
                "--action",
                "examples/audit_go_safe_summary.json",
                "--json-only",
                "--no-reports"
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(data["decision"], "GO")


if __name__ == "__main__":
    unittest.main()
