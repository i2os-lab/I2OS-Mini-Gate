import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from future_constraint import FutureConstraintLayer


class HumanAdmissibilityLayer:
    """
    I2OS Human-Admissibility Layer.

    Evaluates whether the human side is stable, explicit, and human-verifiable
    enough to authorize an AI/software transition.

    Core principle:
    Capability is not permission.
    """

    def __init__(self, policy_path: Optional[str] = None):
        self.policy_path = policy_path
        self.future_layer = FutureConstraintLayer(policy_path=policy_path)

    def human_admissibility_score(self, human_state: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, Any]:
        points = 0
        signals: List[str] = []

        emotional_pressure = str(human_state.get("emotional_pressure", "unknown")).lower()
        urgency_level = str(human_state.get("urgency_level", "unknown")).lower()
        human_verifiability = str(human_state.get("human_verifiability", "unknown")).lower()

        human_confirmed = bool(human_state.get("human_confirmed", False))
        cooldown_taken = bool(human_state.get("cooldown_taken", False))
        explicit_intent = bool(human_state.get("explicit_intent", False))
        external_pressure = bool(human_state.get("external_pressure", False))

        irreversible = action.get("reversible", True) is False
        external_effect = action.get("external_effect", False) is True
        side_effect = action.get("side_effect_level", "unknown")

        if not human_confirmed and side_effect != "read_only":
            points += 2
            signals.append("human_confirmation_missing")

        if emotional_pressure == "high":
            points += 3
            signals.append("emotional_escalation_high")
        elif emotional_pressure == "medium":
            points += 1
            signals.append("emotional_pressure_medium")

        if urgency_level == "high":
            points += 2
            signals.append("urgency_high")
        elif urgency_level == "medium":
            points += 1
            signals.append("urgency_medium")

        if not cooldown_taken and (emotional_pressure in ["medium", "high"] or urgency_level == "high"):
            points += 2
            signals.append("cooldown_not_taken")

        if human_verifiability == "low":
            points += 3
            signals.append("human_verifiability_low")
        elif human_verifiability == "medium":
            points += 1
            signals.append("human_verifiability_medium")

        if not explicit_intent and side_effect != "read_only":
            points += 2
            signals.append("explicit_intent_missing")

        if external_pressure:
            points += 1
            signals.append("external_pressure_detected")

        if irreversible:
            points += 2
            signals.append("irreversible_action")

        if external_effect:
            points += 2
            signals.append("external_effect_action")

        if side_effect in ["external_write", "destructive", "irreversible"]:
            points += 2
            signals.append("high_side_effect_action")

        if points >= 10:
            level = "CRITICAL"
            decision = "BLOCK"
        elif points >= 7:
            level = "HIGH"
            decision = "REPAIR"
        elif points >= 4:
            level = "MEDIUM"
            decision = "HOLD"
        else:
            level = "LOW"
            decision = "GO"

        return {
            "human_admissibility_level": level,
            "human_decision": decision,
            "human_admissible": decision == "GO",
            "human_risk_points": points,
            "human_signals": signals,
            "principle": "Human authorization must be stable, explicit, and human-verifiable."
        }

    def evaluate(self, case: Dict[str, Any]) -> Dict[str, Any]:
        human_state = case.get("human_state", {})
        action = case.get("action", {})

        transition_result = self.future_layer.evaluate(action)
        human_result = self.human_admissibility_score(human_state, action)

        decision_order = {"GO": 0, "HOLD": 1, "REPAIR": 2, "BLOCK": 3}
        transition_decision = transition_result.get("final_decision", "HOLD")
        human_decision = human_result.get("human_decision", "HOLD")

        final_decision = max([transition_decision, human_decision], key=lambda d: decision_order.get(d, 1))
        final_permitted = final_decision == "GO"

        return {
            "case_name": case.get("case_name", "unnamed_case"),
            "final_decision": final_decision,
            "final_permitted": final_permitted,
            "transition_decision": transition_decision,
            "transition_permitted": transition_result.get("final_permitted", False),
            "human_decision": human_decision,
            "human_admissible": human_result.get("human_admissible", False),
            "human_admissibility": human_result,
            "transition_result": transition_result,
            "core_principle": "Capability is not permission.",
            "method": "Action transition + future constraint + human admissibility"
        }


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python human_admissibility/evaluate_human_admissibility.py human_admissibility/sample_human_confirmed_safe_action.json")
        print("  python human_admissibility/evaluate_human_admissibility.py human_admissibility/sample_emotional_escalation_block.json policy/strict_policy.json")
        sys.exit(1)

    case_path = ROOT / sys.argv[1]
    policy_path = str(ROOT / sys.argv[2]) if len(sys.argv) >= 3 else str(ROOT / "policy" / "balanced_policy.json")

    case = load_json(case_path)
    layer = HumanAdmissibilityLayer(policy_path=policy_path)
    result = layer.evaluate(case)

    out_path = ROOT / "human_admissibility" / f"{result['case_name']}_result.json"
    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"[I2OS] Human-admissibility result saved to: {out_path}")

    sys.exit(0 if result["final_permitted"] else 2)


if __name__ == "__main__":
    main()
