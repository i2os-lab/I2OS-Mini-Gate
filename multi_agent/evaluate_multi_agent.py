import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from future_constraint import FutureConstraintLayer


class MultiAgentGovernanceLayer:
    """
    I2OS Multi-Agent Governance Layer.

    Evaluates whether a sequence of agent/tool transitions remains admissible
    as a chain.

    Core question:
    Can individually acceptable actions become inadmissible as a sequence?
    """

    def __init__(self, policy_path: Optional[str] = None):
        self.policy_path = policy_path
        self.future_layer = FutureConstraintLayer(policy_path=policy_path)

    def evaluate_chain(self, chain: Dict[str, Any]) -> Dict[str, Any]:
        agents = chain.get("agents", [])
        events: List[Dict[str, Any]] = []

        chain_risk_points = 0
        external_effect_count = 0
        not_permitted_count = 0
        high_future_count = 0

        for index, agent in enumerate(agents):
            action = agent.get("action", {})
            result = self.future_layer.evaluate(action)
            future = result.get("future_constraint", {})

            if action.get("external_effect") is True:
                external_effect_count += 1

            if not result.get("final_permitted", False):
                not_permitted_count += 1

            if future.get("future_constraint_level") in ["HIGH", "CRITICAL"]:
                high_future_count += 1

            if result.get("final_decision") == "BLOCK":
                chain_risk_points += 4
            elif result.get("final_decision") == "REPAIR":
                chain_risk_points += 2
            elif result.get("final_decision") == "HOLD":
                chain_risk_points += 1

            if action.get("external_effect") is True:
                chain_risk_points += 2

            if action.get("reversible") is False:
                chain_risk_points += 2

            events.append({
                "index": index,
                "agent_id": agent.get("agent_id", f"agent_{index}"),
                "role": agent.get("role", ""),
                "final_decision": result.get("final_decision"),
                "final_permitted": result.get("final_permitted"),
                "shield_decision": result.get("shield_decision"),
                "future_constraint_level": future.get("future_constraint_level"),
                "future_signals": future.get("future_signals", []),
                "reason_codes": result.get("reason_codes", []),
            })

        if chain_risk_points >= 8 or not_permitted_count >= 2:
            chain_decision = "BLOCK"
        elif chain_risk_points >= 4 or not_permitted_count == 1 or high_future_count >= 1:
            chain_decision = "REPAIR"
        else:
            chain_decision = "GO"

        return {
            "chain_name": chain.get("chain_name", "unnamed_chain"),
            "chain_decision": chain_decision,
            "chain_permitted": chain_decision == "GO",
            "chain_risk_points": chain_risk_points,
            "agent_count": len(agents),
            "not_permitted_count": not_permitted_count,
            "external_effect_count": external_effect_count,
            "high_future_count": high_future_count,
            "events": events,
            "core_principle": "Capability is not permission.",
            "method": "Agent sequence → Runtime Shield → Future Constraint → Chain Governance"
        }


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python multi_agent/evaluate_multi_agent.py multi_agent/sample_chain_upload_risk.json")
        print("  python multi_agent/evaluate_multi_agent.py multi_agent/sample_chain_safe_local.json policy/balanced_policy.json")
        sys.exit(1)

    chain_path = ROOT / sys.argv[1]
    policy_path = str(ROOT / sys.argv[2]) if len(sys.argv) >= 3 else str(ROOT / "policy" / "balanced_policy.json")

    chain = load_json(chain_path)
    layer = MultiAgentGovernanceLayer(policy_path=policy_path)
    result = layer.evaluate_chain(chain)

    out_path = ROOT / "multi_agent" / f"{result['chain_name']}_result.json"
    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"[I2OS] Multi-agent result saved to: {out_path}")

    sys.exit(0 if result["chain_permitted"] else 2)


if __name__ == "__main__":
    main()
