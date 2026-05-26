import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestPromptInjectionLabArtifacts(unittest.TestCase):
    def test_lab_files_exist(self):
        lab = ROOT / "prompt_injection_lab"
        self.assertTrue((lab / "run_lab.py").exists())
        self.assertTrue((lab / "hidden_upload.json").exists())
        self.assertTrue((lab / "tool_hijack_webpage.json").exists())
        self.assertTrue((lab / "email_permission_escalation.json").exists())
        self.assertTrue((lab / "safe_untrusted_summary.json").exists())
        self.assertTrue((lab / "memory_poisoning_attempt.json").exists())

    def test_lab_doc_exists(self):
        self.assertTrue((ROOT / "docs" / "prompt_injection_lab.md").exists())

    def test_runner_contains_expected_cases(self):
        text = (ROOT / "prompt_injection_lab" / "run_lab.py").read_text(encoding="utf-8")
        self.assertIn("hidden_upload.json", text)
        self.assertIn("memory_poisoning_attempt.json", text)


if __name__ == "__main__":
    unittest.main()
