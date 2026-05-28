import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestDemoShowcase(unittest.TestCase):
    def test_demo_files_exist(self):
        demo = ROOT / "demo"
        self.assertTrue((demo / "run_demo.py").exists())
        self.assertTrue((demo / "demo_safe_action.json").exists())
        self.assertTrue((demo / "demo_prompt_injection_block.json").exists())
        self.assertTrue((demo / "demo_delete_block.json").exists())
        self.assertTrue((demo / "demo_external_upload_repair.json").exists())

    def test_demo_docs_exist(self):
        self.assertTrue((ROOT / "docs" / "demo_showcase.md").exists())
        self.assertTrue((ROOT / "docs" / "release_v2_1.md").exists())


if __name__ == "__main__":
    unittest.main()
