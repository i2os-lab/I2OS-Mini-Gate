import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from i2os_gate import i2os_gate, load_policy


class AgentRuntimeBridge:
    """
    I2OS Agent Runtime Bridge.

    Dry-run only. It does not execute commands.
    Core principle: Capability is not permission.
    """

    def __init__(self, policy_path: Optional[str] = None):
        self.policy = load_policy(policy_path)

    def scan(self, action: Dict[str, Any]) -> Dict[str, Any]:
        return i2os_gate(action, policy=self.policy)

    def guard(self, action: Dict[str, Any]) -> Dict[str, Any]:
        result = self.scan(action)
        return {
            "permitted": result.get("decision") == "GO",
            "decision": result.get("decision"),
            "risk_level": result.get("risk_level"),
            "reason_codes": result.get("reason_codes", []),
            "human_verifiable_explanation": result.get("human_verifiable_explanation"),
            "raw_result": result
        }


def build_command_action(command: str, target: str = "local_shell", user_confirmed: bool = False) -> Dict[str, Any]:
    destructive_keywords = ["rm -rf", "delete", "remove", "erase", "wipe", "shutdown"]
    destructive = any(keyword in command.lower() for keyword in destructive_keywords)

    return {
        "actor": "AI agent",
        "current_state": "AI agent proposes command execution",
        "proposed_action": f"execute command: {command}",
        "action_type": "command_execution",
        "tool_name": "terminal",
        "target": target,
        "target_scope": "system" if destructive else "single_command",
        "side_effect_level": "destructive" if destructive else "local_write",
        "permission_level": "user",
        "requires_confirmation": True,
        "user_confirmed": user_confirmed,
        "reversible": False if destructive else True,
        "sandbox_required": True,
        "sandbox_enabled": False,
        "external_effect": False
    }


def guarded_dry_run(command: str, policy_path: Optional[str] = None) -> Dict[str, Any]:
    bridge = AgentRuntimeBridge(policy_path=policy_path)
    action = build_command_action(command)
    return bridge.guard(action)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python agent_bridge/runtime_bridge.py \"echo hello\"")
        print("  python agent_bridge/runtime_bridge.py \"rm -rf ./project\"")
        sys.exit(1)

    command = " ".join(sys.argv[1:])
    result = guarded_dry_run(command)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["permitted"]:
        print("[I2OS] DRY-RUN ONLY: command would be permitted.")
        sys.exit(0)

    print("[I2OS] Command is not permitted by runtime bridge.")
    sys.exit(2)


if __name__ == "__main__":
    main()
