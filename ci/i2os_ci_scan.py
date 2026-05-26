import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from i2os_gate import i2os_gate, load_policy


DEFAULT_EXAMPLES = [
    "examples/audit_go_safe_summary.json",
    "examples/audit_repair_external_api.json",
    "examples/audit_block_prompt_injection.json"
]


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    parser = argparse.ArgumentParser(
        description="I2OS Mini Gate CI scanner"
    )
    parser.add_argument(
        "--policy",
        default=None,
        help="Policy JSON path"
    )
    parser.add_argument(
        "--actions",
        nargs="*",
        default=DEFAULT_EXAMPLES,
        help="Action JSON files to scan"
    )
    parser.add_argument(
        "--fail-on",
        choices=["NONE", "BLOCK", "REPAIR", "HOLD"],
        default="BLOCK",
        help="Fail CI when this decision or higher severity appears"
    )
    args = parser.parse_args()

    policy = load_policy(args.policy)
    severity = {"GO": 0, "HOLD": 1, "REPAIR": 2, "BLOCK": 3, "NONE": 99}
    fail_threshold = severity[args.fail_on]

    print("=== I2OS Mini Gate CI Scan ===")
    print(f"Policy: {policy.get('policy_name', 'unknown')} ({policy.get('policy_version', 'unknown')})")
    print(f"Fail on: {args.fail_on}")
    print()

    failed = False
    summary = []

    for action_path in args.actions:
        action_file = ROOT / action_path
        action = load_json(action_file)
        result = i2os_gate(action, policy=policy)

        decision = result["decision"]
        risk = result["risk_level"]
        codes = ",".join(result.get("reason_codes", [])) or "NO_RISK_CODES"

        summary.append({
            "file": action_path,
            "decision": decision,
            "risk_level": risk,
            "reason_codes": result.get("reason_codes", [])
        })

        print(f"[{decision}] {action_path} | risk={risk} | codes={codes}")

        if severity[decision] >= fail_threshold:
            failed = True

    print()
    print("=== Summary JSON ===")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if failed:
        print()
        print("[I2OS] CI scan failed due to configured fail-on threshold.")
        sys.exit(1)

    print()
    print("[I2OS] CI scan passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
