import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from i2os_gate import i2os_gate, load_policy


def build_file_action(path: str, operation: str, confirmed: bool = False):
    operation = operation.lower()
    destructive = operation in ["delete", "remove", "wipe", "erase"]
    write_op = operation in ["write", "modify", "overwrite", "delete", "remove", "wipe", "erase"]

    if destructive:
        side_effect = "destructive"
        reversible = False
    elif write_op:
        side_effect = "local_write"
        reversible = True
    else:
        side_effect = "read_only"
        reversible = True

    scope = "single_file"
    if path in [".", "./", "*", "./*", "/"]:
        scope = "system"
    elif path.endswith("/") or path.endswith("/*"):
        scope = "directory"

    return {
        "actor": "local_user_or_ai_agent",
        "current_state": "Local security pre-check",
        "proposed_action": f"{operation} local path {path}",
        "action_type": "file_operation",
        "tool_name": "filesystem",
        "target": path,
        "target_scope": scope,
        "side_effect_level": side_effect,
        "permission_level": "user" if side_effect != "read_only" else "read_only",
        "requires_confirmation": destructive or write_op,
        "user_confirmed": confirmed,
        "reversible": reversible,
        "sandbox_required": destructive,
        "sandbox_enabled": False,
        "external_effect": False
    }


def build_url_action(url: str, operation: str, confirmed: bool = False):
    operation = operation.lower()
    external_write = operation in ["post", "upload", "send", "submit", "export"]

    return {
        "actor": "local_user_or_ai_agent",
        "current_state": "Local network pre-check",
        "proposed_action": f"{operation} request to {url}",
        "action_type": "network_request",
        "tool_name": "browser",
        "target": url,
        "target_scope": "external_service",
        "side_effect_level": "external_write" if external_write else "read_only",
        "permission_level": "user" if external_write else "read_only",
        "requires_confirmation": external_write,
        "user_confirmed": confirmed,
        "reversible": True,
        "sandbox_required": False,
        "external_effect": True
    }


def print_result(result, json_only=False):
    if json_only:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print("=== I2OS Local Security Tool Result ===")
    print(f"Decision: {result['decision']}")
    print(f"Risk: {result['risk_level']}")
    print(f"Summary: {result['summary']}")
    print()
    print("Reason Codes:")
    for code in result.get("reason_codes", []):
        print(f"- {code}")
    if not result.get("reason_codes"):
        print("- None")
    print()
    print("Explanation:")
    print(result.get("human_verifiable_explanation"))


def main():
    parser = argparse.ArgumentParser(description="I2OS Local Security Tool Prototype")
    sub = parser.add_subparsers(dest="command")

    file_parser = sub.add_parser("file", help="Check local file operation")
    file_parser.add_argument("--path", required=True)
    file_parser.add_argument("--operation", default="read")
    file_parser.add_argument("--confirmed", action="store_true")
    file_parser.add_argument("--policy", default=None)
    file_parser.add_argument("--json", action="store_true")

    url_parser = sub.add_parser("url", help="Check URL/network operation")
    url_parser.add_argument("--url", required=True)
    url_parser.add_argument("--operation", default="get")
    url_parser.add_argument("--confirmed", action="store_true")
    url_parser.add_argument("--policy", default=None)
    url_parser.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    policy = load_policy(args.policy)

    if args.command == "file":
        action = build_file_action(args.path, args.operation, args.confirmed)
        result = i2os_gate(action, policy=policy)
        print_result(result, json_only=args.json)
        sys.exit(0 if result["decision"] == "GO" else 2)

    if args.command == "url":
        action = build_url_action(args.url, args.operation, args.confirmed)
        result = i2os_gate(action, policy=policy)
        print_result(result, json_only=args.json)
        sys.exit(0 if result["decision"] == "GO" else 2)


if __name__ == "__main__":
    main()
