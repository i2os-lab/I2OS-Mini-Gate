import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from i2os_gate import i2os_gate, load_policy, VERSION


class RuntimeShield:
    """
    I2OS Runtime Shield Prototype.

    Product-grade direction prototype:
    - scan proposed actions
    - return GO / HOLD / REPAIR / BLOCK
    - keep execution separated from permission
    - expose human-verifiable decision records

    Core principle:
    Capability is not permission.
    """

    def __init__(self, policy_path: Optional[str] = None):
        self.policy_path = policy_path
        self.policy = load_policy(policy_path)

    def scan(self, action: Dict[str, Any]) -> Dict[str, Any]:
        return i2os_gate(action, policy=self.policy)

    def permit(self, action: Dict[str, Any]) -> bool:
        return self.scan(action).get("decision") == "GO"

    def explain(self, action: Dict[str, Any]) -> str:
        result = self.scan(action)
        return result.get("human_verifiable_explanation", "")

    def shield(self, action: Dict[str, Any]) -> Dict[str, Any]:
        result = self.scan(action)
        return {
            "shield_version": VERSION,
            "permitted": result.get("decision") == "GO",
            "decision": result.get("decision"),
            "risk_level": result.get("risk_level"),
            "reason_codes": result.get("reason_codes", []),
            "repairs": result.get("repairs", []),
            "explanation": result.get("human_verifiable_explanation"),
            "raw_result": result
        }


def load_action_file(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python runtime_shield/shield.py examples/audit_block_prompt_injection.json")
        print("  python runtime_shield/shield.py examples/audit_go_safe_summary.json policy/strict_policy.json")
        sys.exit(1)

    action_path = sys.argv[1]
    policy_path = sys.argv[2] if len(sys.argv) >= 3 else None

    shield = RuntimeShield(policy_path=policy_path)
    action = load_action_file(action_path)
    result = shield.shield(action)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    sys.exit(0 if result["permitted"] else 2)


if __name__ == "__main__":
    main()
