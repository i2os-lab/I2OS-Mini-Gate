import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class ContractEnforcementLayer:
    """
    I2OS Contract Enforcement Layer.

    Checks whether an attempted execution remains within the issued
    Execution Contract.

    Core principle:
    Permission is bounded by contract.
    """

    def enforce(self, contract: Dict[str, Any], attempt: Dict[str, Any]) -> Dict[str, Any]:
        violations: List[str] = []
        recheck_triggers: List[str] = []

        if contract.get("contract_status") != "ISSUED" or not contract.get("permitted", False):
            violations.append("contract_not_issued_or_not_permitted")

        contract_id = contract.get("contract_id")
        attempt_contract_id = attempt.get("contract_id")
        if contract_id and attempt_contract_id and contract_id != attempt_contract_id:
            violations.append("contract_id_mismatch")

        allowed = contract.get("allowed_scope", {}) or {}
        action = attempt.get("attempted_action", {}) or {}

        def compare(field: str, violation_code: str, trigger_code: str):
            expected = allowed.get(field)
            actual = action.get(field)
            if expected is not None and actual != expected:
                violations.append(violation_code)
                recheck_triggers.append(trigger_code)

        compare("target", "target_changed_outside_contract", "target_changed")
        compare("target_scope", "scope_changed_outside_contract", "scope_expanded")
        compare("tool_name", "tool_changed_outside_contract", "new_agent_or_tool_added")
        compare("action_type", "action_type_changed_outside_contract", "new_agent_or_tool_added")

        expected_external = bool(allowed.get("external_effect_allowed", False))
        actual_external = bool(action.get("external_effect", False))
        if actual_external and not expected_external:
            violations.append("external_effect_added_outside_contract")
            recheck_triggers.append("external_effect_added")

        expected_side_effect = allowed.get("side_effect_level")
        actual_side_effect = action.get("side_effect_level")
        side_effect_order = {
            "read_only": 0,
            "local_write": 1,
            "external_write": 2,
            "destructive": 3,
            "irreversible": 4
        }
        if expected_side_effect in side_effect_order and actual_side_effect in side_effect_order:
            if side_effect_order[actual_side_effect] > side_effect_order[expected_side_effect]:
                violations.append("side_effect_level_increased")
                recheck_triggers.append("side_effect_level_increased")

        prohibited = [str(x).lower() for x in contract.get("prohibited_actions", []) or []]
        proposed = str(action.get("proposed_action", "")).lower()

        if "external_upload_or_send" in prohibited and ("send" in proposed or "upload" in proposed or actual_external):
            violations.append("prohibited_external_send_or_upload")

        if "execute_destructive_action_without_new_contract" in prohibited and actual_side_effect in ["destructive", "irreversible"]:
            violations.append("prohibited_destructive_execution")

        decision = "GO" if not violations else "BLOCK"

        if violations and set(recheck_triggers):
            decision = "HOLD" if "target_changed" in recheck_triggers or "new_agent_or_tool_added" in recheck_triggers else "BLOCK"

        return {
            "enforcement_timestamp": datetime.now().isoformat(timespec="seconds"),
            "contract_id": contract_id,
            "attempt_name": attempt.get("attempt_name", "unnamed_attempt"),
            "enforcement_decision": decision,
            "within_contract": not violations,
            "violations": sorted(set(violations)),
            "recheck_triggers": sorted(set(recheck_triggers)),
            "attempted_action": action,
            "core_principle": "Permission is bounded by contract.",
            "method": "Execution contract + attempted action → contract enforcement decision"
        }


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python contract_enforcement/enforce_contract.py contract_enforcement/sample_contract.json contract_enforcement/sample_attempt_allowed.json")
        print("  python contract_enforcement/enforce_contract.py contract_enforcement/sample_contract.json contract_enforcement/sample_attempt_violation.json")
        sys.exit(1)

    contract_path = ROOT / sys.argv[1]
    attempt_path = ROOT / sys.argv[2]

    contract = load_json(contract_path)
    attempt = load_json(attempt_path)

    layer = ContractEnforcementLayer()
    result = layer.enforce(contract, attempt)

    out_path = ROOT / "contract_enforcement" / f"{result['attempt_name']}_enforcement_result.json"
    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"[I2OS] Contract enforcement result saved to: {out_path}")

    sys.exit(0 if result["within_contract"] else 2)


if __name__ == "__main__":
    main()
