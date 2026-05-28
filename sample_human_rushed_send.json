import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from human_admissibility import HumanAdmissibilityLayer
from recovery_path import RecoveryPathLayer
from recheck_loop import RecheckLoopLayer
from execution_contract import ExecutionContractLayer
from contract_enforcement import ContractEnforcementLayer


class ClosedLoopGovernanceCore:
    """
    I2OS Closed-Loop Runtime Governance Core.

    Integrates:
    - Human-Admissibility
    - Recovery Path
    - Recheck Loop
    - Execution Contract
    - Contract Enforcement

    Core principle:
    Capability is not permission.
    Permission is bounded by contract.
    Recovery must be rechecked.
    """

    def __init__(self, policy_path: Optional[str] = None):
        self.policy_path = policy_path
        self.human_layer = HumanAdmissibilityLayer(policy_path=policy_path)
        self.recovery_layer = RecoveryPathLayer(policy_path=policy_path)
        self.recheck_layer = RecheckLoopLayer(policy_path=policy_path)
        self.contract_layer = ExecutionContractLayer(policy_path=policy_path)
        self.enforcement_layer = ContractEnforcementLayer()

    def run(self, package: Dict[str, Any]) -> Dict[str, Any]:
        case = package.get("case", {})
        repaired_case = package.get("repaired_case", {})
        attempted_execution = package.get("attempted_execution", {})

        initial_result = self.human_layer.evaluate(case)
        recovery_result = self.recovery_layer.evaluate_case(initial_result)

        recheck_package = {
            "case_name": package.get("package_name", "closed_loop_governance"),
            "initial_case": case,
            "repaired_case": repaired_case
        }
        recheck_result = self.recheck_layer.evaluate_recheck(recheck_package)

        contract_result = self.contract_layer.evaluate_input(recheck_result)
        contract = contract_result.get("execution_contract", {})

        enforcement_result = None
        if contract.get("contract_status") == "ISSUED" and attempted_execution:
            attempt = dict(attempted_execution)
            if "contract_id" not in attempt:
                attempt["contract_id"] = contract.get("contract_id")
            enforcement_result = self.enforcement_layer.enforce(contract, attempt)

        final_status = "UNRESOLVED"
        if enforcement_result:
            final_status = "EXECUTION_ALLOWED" if enforcement_result.get("within_contract") else "EXECUTION_BLOCKED_BY_CONTRACT"
        elif contract.get("contract_status") == "ISSUED":
            final_status = "CONTRACT_ISSUED_NO_EXECUTION_ATTEMPT"
        elif recheck_result.get("loop_status") == "RESOLVED":
            final_status = "RESOLVED_NO_CONTRACT"
        else:
            final_status = "NOT_RESOLVED"

        return {
            "package_name": package.get("package_name", "unnamed_governance_package"),
            "governance_version": "v3.0-complete",
            "final_status": final_status,
            "initial_decision": initial_result.get("final_decision"),
            "recovery_mode": recovery_result.get("recovery_path", {}).get("recovery_mode"),
            "recheck_status": recheck_result.get("loop_status"),
            "contract_status": contract.get("contract_status"),
            "enforcement_decision": enforcement_result.get("enforcement_decision") if enforcement_result else None,
            "within_contract": enforcement_result.get("within_contract") if enforcement_result else None,
            "initial_result": initial_result,
            "recovery_result": recovery_result,
            "recheck_result": recheck_result,
            "contract_result": contract_result,
            "enforcement_result": enforcement_result,
            "core_principles": [
                "Capability is not permission.",
                "Permission is bounded by contract.",
                "Recovery is not completion; recovery must be rechecked.",
                "Execution must remain inside the issued contract."
            ],
            "method": "Human-Admissibility → Recovery → Recheck → Contract → Enforcement"
        }


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python governance_core/run_governance_core.py governance_core/sample_governance_package.json")
        print("  python governance_core/run_governance_core.py governance_core/sample_governance_violation_package.json policy/strict_policy.json")
        sys.exit(1)

    package_path = ROOT / sys.argv[1]
    policy_path = str(ROOT / sys.argv[2]) if len(sys.argv) >= 3 else str(ROOT / "policy" / "balanced_policy.json")

    package = load_json(package_path)
    core = ClosedLoopGovernanceCore(policy_path=policy_path)
    result = core.run(package)

    out_path = ROOT / "governance_core" / f"{result['package_name']}_governance_result.json"
    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"[I2OS] Governance result saved to: {out_path}")

    allowed_statuses = {"EXECUTION_ALLOWED", "CONTRACT_ISSUED_NO_EXECUTION_ATTEMPT"}
    sys.exit(0 if result["final_status"] in allowed_statuses else 2)


if __name__ == "__main__":
    main()
