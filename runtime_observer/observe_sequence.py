import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime_shield import RuntimeShield


class RuntimeObserver:
    """
    I2OS Runtime Observation Layer.

    Observes a sequence of proposed actions and records transition decisions.

    Core principle:
    Capability is not permission.
    """

    def __init__(self, policy_path: Optional[str] = None):
        self.policy_path = policy_path
        self.shield = RuntimeShield(policy_path=policy_path)
        self.events: List[Dict[str, Any]] = []

    def observe(self, action: Dict[str, Any], label: Optional[str] = None) -> Dict[str, Any]:
        result = self.shield.shield(action)
        event = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "label": label or action.get("proposed_action", "unlabeled_action"),
            "decision": result["decision"],
            "permitted": result["permitted"],
            "risk_level": result["risk_level"],
            "reason_codes": result.get("reason_codes", []),
            "repairs": result.get("repairs", []),
            "explanation": result.get("explanation", ""),
        }
        self.events.append(event)
        return event

    def summary(self) -> Dict[str, Any]:
        counts = {"GO": 0, "HOLD": 0, "REPAIR": 0, "BLOCK": 0}
        risks = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}

        for event in self.events:
            counts[event["decision"]] = counts.get(event["decision"], 0) + 1
            risks[event["risk_level"]] = risks.get(event["risk_level"], 0) + 1

        return {
            "total_events": len(self.events),
            "decision_counts": counts,
            "risk_counts": risks,
            "blocked_or_not_permitted": sum(1 for e in self.events if not e["permitted"]),
            "core_principle": "Capability is not permission."
        }

    def export_json(self, path: str) -> Dict[str, Any]:
        output = {
            "observer": "I2OS Runtime Observation Layer",
            "policy_path": self.policy_path,
            "summary": self.summary(),
            "events": self.events,
        }
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=2, ensure_ascii=False)
        return output


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python runtime_observer/observe_sequence.py demo/demo_safe_action.json demo/demo_prompt_injection_block.json")
        sys.exit(1)

    observer = RuntimeObserver(policy_path=str(ROOT / "policy" / "strict_policy.json"))

    for item in sys.argv[1:]:
        action_path = ROOT / item
        action = load_json(action_path)
        event = observer.observe(action, label=item)
        print(f"[{event['decision']}] {item} | permitted={event['permitted']} | risk={event['risk_level']}")

    output_path = ROOT / "runtime_observer" / "observation_results.json"
    observer.export_json(str(output_path))

    print()
    print("=== Runtime Observation Summary ===")
    print(json.dumps(observer.summary(), indent=2, ensure_ascii=False))
    print(f"[I2OS] Observation results saved to: {output_path}")


if __name__ == "__main__":
    main()
