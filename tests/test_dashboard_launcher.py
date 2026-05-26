import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dashboard_launcher.launch_dashboard import launch_dashboard


class TestDashboardLauncher(unittest.TestCase):
    def test_launcher_file_exists(self):
        self.assertTrue((ROOT / "dashboard_launcher" / "launch_dashboard.py").exists())

    def test_launch_dashboard_go(self):
        output = launch_dashboard(
            action_path=str(ROOT / "examples" / "audit_go_safe_summary.json"),
            policy_path=str(ROOT / "policy" / "balanced_policy.json"),
            report_prefix="test_dashboard_launcher_go",
            open_browser=False,
        )
        self.assertEqual(output["decision"], "GO")
        self.assertTrue((ROOT / "dashboard" / "test_dashboard_launcher_go.html").exists())

    def test_launch_dashboard_block(self):
        output = launch_dashboard(
            action_path=str(ROOT / "examples" / "audit_block_prompt_injection.json"),
            policy_path=str(ROOT / "policy" / "strict_policy.json"),
            report_prefix="test_dashboard_launcher_block",
            open_browser=False,
        )
        self.assertEqual(output["decision"], "BLOCK")
        self.assertTrue((ROOT / "dashboard" / "test_dashboard_launcher_block.html").exists())


if __name__ == "__main__":
    unittest.main()
