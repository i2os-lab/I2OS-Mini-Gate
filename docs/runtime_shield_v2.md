# I2OS Mini Gate v2.0
## Product-grade Runtime Shield Prototype

> Capability is not permission.

v2.0 consolidates I2OS Mini Gate into a Product-grade Runtime Shield Prototype.

This is not a final commercial product.

It is a coherent public prototype showing how I2OS can govern proposed AI/software actions before execution.

---

## Core Function

```text
Proposed Action
↓
Runtime Shield
↓
Admissibility Scan
↓
GO / HOLD / REPAIR / BLOCK
↓
Human-verifiable explanation
```

---

## Added Files

```text
runtime_shield/shield.py
runtime_shield/__init__.py
docs/runtime_shield_v2.md
docs/release_v2_0.md
tests/test_runtime_shield.py
```

---

## Run

```bash
python runtime_shield/shield.py examples/audit_go_safe_summary.json
```

```bash
python runtime_shield/shield.py examples/audit_block_prompt_injection.json policy/strict_policy.json
```

---

## Python Usage

```python
from runtime_shield import RuntimeShield

shield = RuntimeShield(policy_path="policy/strict_policy.json")
result = shield.shield(action)

if result["permitted"]:
    print("Allowed")
else:
    print("Blocked")
```

---

## v2.0 Integrated Capabilities

- Runtime Admissibility Scanner
- AI Agent Action Checker
- Prompt Injection Transition Detector
- Audit / Logging / Explainability
- Policy Configuration
- Policy Profiles
- Unit Tests
- CLI Runtime Scanner
- Web/API Mode
- GitHub Action / CI Hook
- Agent Runtime Bridge
- Prompt Injection Lab
- Local Security Tool Prototype
- Dashboard Launcher
- Hardening / Error Handling

---

## Design Position

v2.0 represents the first consolidated Runtime Shield prototype.

It operationalizes the principle:

```text
Capability is not permission.
```

and the transition rule:

```text
Permit(T) = 1 [ C(S_t, T, S_{t+1}) = 1 ]
```

The system does not claim to prove safety.

It provides a structured pre-execution gate for admissibility checking.
