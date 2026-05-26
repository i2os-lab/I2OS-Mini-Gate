import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from i2os_gate import i2os_gate, load_policy

LAB_DIR = Path(__file__).resolve().parent

EXPECTED = {
    "hidden_upload.json": "BLOCK",
    "tool_hijack_webpage.json": "BLOCK",
    "email_permission_escalation.json": "BLOCK",
    "safe_untrusted_summary.json": "GO",
    "memory_poisoning_attempt.json": "BLOCK"
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    parser = argparse.ArgumentParser(description="I2OS Prompt Injection Lab Runner")
    parser.add_argument("--policy", default=None, help="Policy JSON path")
    parser.add_argument("--json", action="store_true", help="Print JSON summary")
    args = parser.parse_args()

    policy = load_policy(args.policy)
    results = []
    failed = False

    print("=== I2OS Prompt Injection Lab ===")
    print(f"Policy: {policy.get('policy_name', 'unknown')} ({policy.get('policy_version', 'unknown')})")
    print()

    for filename, expected in EXPECTED.items():
        path = LAB_DIR / filename
        action = load_json(path)
        result = i2os_gate(action, policy=policy)
        decision = result["decision"]
        ok = decision == expected
        failed = failed or not ok
        row = {
            "case": filename,
            "expected": expected,
            "decision": decision,
            "risk_level": result.get("risk_level"),
            "ok": ok,
            "reason_codes": result.get("reason_codes", [])
        }
        results.append(row)
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {filename}: expected={expected}, decision={decision}, risk={result.get('risk_level')}")

    print()
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))

    if failed:
        print("[I2OS] Prompt Injection Lab failed.")
        sys.exit(1)

    print("[I2OS] Prompt Injection Lab passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
