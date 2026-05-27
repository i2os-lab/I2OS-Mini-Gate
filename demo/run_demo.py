import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime_shield import RuntimeShield

DEMO_CASES = [
    ("Safe read-only action", "demo/demo_safe_action.json", "policy/balanced_policy.json"),
    ("Prompt injection block", "demo/demo_prompt_injection_block.json", "policy/strict_policy.json"),
    ("Irreversible delete block", "demo/demo_delete_block.json", "policy/strict_policy.json"),
    ("External upload repair/block", "demo/demo_external_upload_repair.json", "policy/balanced_policy.json"),
]


def load_json(path):
    with open(ROOT / path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    print("=== I2OS Mini Gate v2.1 Demo Showcase ===")
    print("Core principle: Capability is not permission.")
    print()

    rows = []

    for title, action_path, policy_path in DEMO_CASES:
        action = load_json(action_path)
        shield = RuntimeShield(policy_path=str(ROOT / policy_path))
        result = shield.shield(action)

        row = {
            "title": title,
            "action": action_path,
            "policy": policy_path,
            "decision": result["decision"],
            "permitted": result["permitted"],
            "risk_level": result["risk_level"],
            "reason_codes": result["reason_codes"],
        }
        rows.append(row)

        print(f"## {title}")
        print(f"Action: {action_path}")
        print(f"Policy: {policy_path}")
        print(f"Decision: {result['decision']}")
        print(f"Permitted: {result['permitted']}")
        print(f"Risk: {result['risk_level']}")
        print(f"Reason Codes: {', '.join(result['reason_codes']) if result['reason_codes'] else 'NO_RISK_CODES'}")
        print()

    out_path = ROOT / "demo" / "demo_results.json"
    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2, ensure_ascii=False)

    print(f"[I2OS] Demo results saved to: {out_path}")


if __name__ == "__main__":
    main()
