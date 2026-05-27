# I2OS Mini Gate v2.4
## Multi-Agent Governance Layer

> Capability is not permission.

v2.4 adds an initial Multi-Agent Governance Layer.

The purpose is to evaluate whether a sequence of agent/tool transitions remains admissible as a chain.

---

## Core Question

```text
Can individually acceptable actions become inadmissible as a sequence?
```

---

## Added

```text
multi_agent/evaluate_multi_agent.py
multi_agent/__init__.py
multi_agent/sample_chain_upload_risk.json
multi_agent/sample_chain_safe_local.json
docs/multi_agent_governance.md
docs/release_v2_4.md
tests/test_multi_agent.py
```

---

## Run

```bash
python multi_agent/evaluate_multi_agent.py multi_agent/sample_chain_upload_risk.json
```

```bash
python multi_agent/evaluate_multi_agent.py multi_agent/sample_chain_safe_local.json policy/balanced_policy.json
```

---

## Design Position

v2.4 moves from single-agent transition governance toward chain-level governance.

The flow becomes:

```text
Agent sequence
↓
Runtime Shield
↓
Future Constraint Layer
↓
Multi-Agent Governance
↓
Chain decision
```

This is the first step toward governing tool chains and multi-agent systems.
