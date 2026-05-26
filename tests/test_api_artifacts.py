import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestAPIArtifacts(unittest.TestCase):
    def test_api_file_exists(self):
        self.assertTrue((ROOT / "i2os_api.py").exists())

    def test_requirements_api_exists(self):
        self.assertTrue((ROOT / "requirements-api.txt").exists())

    def test_api_doc_exists(self):
        self.assertTrue((ROOT / "docs" / "web_api_mode.md").exists())

    def test_api_contains_scan_endpoint(self):
        text = (ROOT / "i2os_api.py").read_text(encoding="utf-8")
        self.assertIn('@app.post("/scan")', text)
        self.assertIn("Capability is not permission.", text)


if __name__ == "__main__":
    unittest.main()
