import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime_shield import RuntimeShield


FUTURE_RISK_KEYWORDS = [
    "delete",
    "remove",
    "wipe",
    "erase",
    "export",
    "upload",
    "send",
    "persistent",
    "memory",
    "admin",
    "all users",
    "external",
]


class FutureConstraintLayer:
    """
    I2OS Future Constraint Layer.

    This layer estimates whether a proposed transition may create
    future irrecoverability, escalation, or continuity collapse.

    It does not predict the future.
    It checks future compatibility constraints.

    Core principle:
    Capability is not permission.
    """

    def __init__(self, policy_path: Optional[str] = None):
        self.shield = RuntimeShield(policy_path=policy_path)

    def future_constraint_score(self, action: Dict[str, Any]) -> Dict[str, Any]:
        proposed = str(action.get("proposed_action", "")).lower()
        side_effect = action.get("side_effect_level", "unknown")
        reversible = action.get("reversible", True)
        external_effect = action.get("external_effect", False)
        target_scope = action.get("target_scope", action.get("scope", "unknown"))
        user_confirmed = action.get("user_confirmed", False)

        risk_points = 0
        signals: List[str] = []

        if reversible is False:
            risk_points += 3
            signals.append("future_irrecoverability")

        if external_effect is True:
            risk_points += 2
            signals.append("external_future_dependency")

        if side_effect in ["destructive", "irreversible", "external_write"]:
            risk_points += 3
            signals.append("high_future_side_effect")

        if target_scope in ["system", "all_files", "all_users", "entire_project"]:
            risk_points += 2
            signals.append("broad_future_scope")

        if user_confirmed is False and side_effect != "read_only":
            risk_points += 1
            signals.append("future_confirmation_gap")

        keyword_hits = [kw for kw in FUTURE_RISK_KEYWORDS if kw in proposed]
        if keyword_hits:
            risk_points += min(3, len(keyword_hits))
            signals.append("future_risk_keywords:" + ",".join(keyword_hits[:5]))

        if risk_points >= 7:
            level = "CRITICAL"
        elif risk_points >= 5:
            level = "HIGH"
        elif risk_points >= 3:
            level = "MEDIUM"
        else:
            level = "LOW"

        future_compatible = level in ["LOW", "MEDIUM"]

        return {
            "future_constraint_level": level,
            "future_compatible": future_compatible,
            "future_risk_points": risk_points,
            "future_signals": signals,
            "principle": "Future compatibility is not prediction; it is constraint checking."
        }

    def evaluate(self, action: Dict[str, Any]) -> Dict[str, Any]:
        shield_result = self.shield.shield(action)
        future_result = self.future_constraint_score(action)

        final_permitted = shield_result["permitted"] and future_result["future_compatible"]

        if not future_result["future_compatible"] and shield_result["decision"] == "GO":
            final_decision = "HOLD"
        else:
            final_decision = shield_result["decision"]

        return {
            "final_permitted": final_permitted,
            "final_decision": final_decision,
            "shield_decision": shield_result["decision"],
            "shield_permitted": shield_result["permitted"],
            "shield_risk_level": shield_result["risk_level"],
            "future_constraint": future_result,
            "reason_codes": shield_result.get("reason_codes", []),
            "explanation": shield_result.get("explanation", ""),
            "core_principle": "Capability is not permission."
        }


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python future_constraint/evaluate_future.py demo/demo_safe_action.json")
        print("  python future_constraint/evaluate_future.py demo/demo_delete_block.json policy/strict_policy.json")
        sys.exit(1)

    action_path = ROOT / sys.argv[1]
    policy_path = str(ROOT / sys.argv[2]) if len(sys.argv) >= 3 else str(ROOT / "policy" / "balanced_policy.json")

    action = load_json(action_path)
    layer = FutureConstraintLayer(policy_path=policy_path)
    result = layer.evaluate(action)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["final_permitted"] else 2)


if __name__ == "__main__":
    main()
