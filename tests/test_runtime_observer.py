import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime_observer import RuntimeObserver


class TestRuntimeObserver(unittest.TestCase):
    def load_action(self, path):
        with open(ROOT / path, "r", encoding="utf-8") as file:
            return json.load(file)

    def test_observer_records_events(self):
        observer = RuntimeObserver(policy_path=str(ROOT / "policy" / "strict_policy.json"))
        observer.observe(self.load_action("demo/demo_safe_action.json"), label="safe")
        observer.observe(self.load_action("demo/demo_prompt_injection_block.json"), label="block")
        summary = observer.summary()
        self.assertEqual(summary["total_events"], 2)
        self.assertGreaterEqual(summary["decision_counts"]["BLOCK"], 1)

    def test_export_json(self):
        observer = RuntimeObserver(policy_path=str(ROOT / "policy" / "strict_policy.json"))
        observer.observe(self.load_action("demo/demo_safe_action.json"), label="safe")
        out = ROOT / "runtime_observer" / "test_observation_results.json"
        data = observer.export_json(str(out))
        self.assertTrue(out.exists())
        self.assertEqual(data["summary"]["total_events"], 1)


if __name__ == "__main__":
    unittest.main()
