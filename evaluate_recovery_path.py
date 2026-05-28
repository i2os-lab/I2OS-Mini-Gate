import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from human_admissibility import HumanAdmissibilityLayer
from recovery_path import RecoveryPathLayer


class RecheckLoopLayer:
    """
    I2OS Recheck Loop Layer.

    Runs an initial admissibility check, generates a recovery path if needed,
    then evaluates a repaired case and compares the transition state.

    Core principle:
    Recovery is not completion.
    Recovery must be rechecked.
    """

    def __init__(self, policy_path: Optional[str] = None):
        self.policy_path = policy_path
        self.human_layer = HumanAdmissibilityLayer(policy_path=policy_path)
        self.recovery_layer = RecoveryPathLayer(policy_path=policy_path)

    def evaluate_recheck(self, package: Dict[str, Any]) -> Dict[str, Any]:
        initial_case = package.get("initial_case", {})
        repaired_case = package.get("repaired_case", {})

        initial_result = self.human_layer.evaluate(initial_case)
        recovery_result = self.recovery_layer.evaluate_case(initial_result)["recovery_path"]
        repaired_result = self.human_layer.evaluate(repaired_case)

        initial_decision = initial_result.get("final_decision", "HOLD")
        repaired_decision = repaired_result.get("final_decision", "HOLD")

        decision_order = {"GO": 0, "HOLD": 1, "REPAIR": 2, "BLOCK": 3}

        improved = decision_order.get(repaired_decision, 3) < decision_order.get(initial_decision, 3)
        resolved_to_go = repaired_decision == "GO"

        if resolved_to_go:
            loop_status = "RESOLVED"
        elif improved:
            loop_status = "IMPROVED_BUT_NOT_RESOLVED"
        else:
            loop_status = "UNRESOLVED"

        return {
            "case_name": package.get("case_name", "unnamed_recheck_case"),
            "loop_status": loop_status,
            "initial_decision": initial_decision,
            "repaired_decision": repaired_decision,
            "improved": improved,
            "resolved_to_go": resolved_to_go,
            "initial_result": initial_result,
            "recovery_path": recovery_result,
            "repaired_result": repaired_result,
            "core_principle": "Recovery is not completion. Recovery must be rechecked.",
            "method": "Initial check → recovery path → repaired check → loop status"
        }


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python recheck_loop/evaluate_recheck_loop.py recheck_loop/sample_recheck_rushed_send.json")
        print("  python recheck_loop/evaluate_recheck_loop.py recheck_loop/sample_recheck_rushed_send.json policy/strict_policy.json")
        sys.exit(1)

    package_path = ROOT / sys.argv[1]
    policy_path = str(ROOT / sys.argv[2]) if len(sys.argv) >= 3 else str(ROOT / "policy" / "balanced_policy.json")

    package = load_json(package_path)
    layer = RecheckLoopLayer(policy_path=policy_path)
    result = layer.evaluate_recheck(package)

    out_path = ROOT / "recheck_loop" / f"{result['case_name']}_result.json"
    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"[I2OS] Recheck loop result saved to: {out_path}")

    sys.exit(0 if result["resolved_to_go"] else 2)


if __name__ == "__main__":
    main()
