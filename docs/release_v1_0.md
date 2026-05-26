# I2OS Mini Gate v1.0
## Runtime Admissibility Scanner

> Capability is not permission.

v1.0 is the first complete public prototype of I2OS Mini Gate as a Runtime Admissibility Scanner.

It checks proposed AI/software actions before execution and classifies them as:

```text
GO / HOLD / REPAIR / BLOCK
```

## Included Evolution

| Version | Focus |
|---|---|
| v0.1 | Mini Gate Prototype |
| v0.2 | Rule-Based Runtime Admissibility Gate |
| v0.3 | AI Agent Action Checker |
| v0.4 | Prompt Injection Transition Detector |
| v0.5 | Audit / Logging / Explainability |
| v0.6 | Policy Configuration Layer |
| v0.7 | Test Suite / Unit Tests |
| v0.8 | CLI Runtime Scanner |
| v0.9 | Mini Dashboard / HTML Report |
| v1.0 | Runtime Admissibility Scanner |

## Core Flow

```text
Action JSON
↓
Policy Configuration
↓
Runtime Admissibility Scanner
↓
Constraint Check
↓
GO / HOLD / REPAIR / BLOCK
↓
JSON / Markdown / HTML / Audit Log
```

## Core Principle

```text
Permit(T) = 1 [ C(S_t, T, S_{t+1}) = 1 ]
```

A transition is permitted only when the movement from the current state to the next state satisfies admissibility constraints.

## Example

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --policy policy/default_policy.json --html --report-prefix prompt_injection_scan
```

Generated outputs:

```text
reports/prompt_injection_scan.json
reports/prompt_injection_scan.md
dashboard/prompt_injection_scan.html
audit_logs/i2os_audit_log.jsonl
```

## Design Position

I2OS Mini Gate v1.0 is a minimal, inspectable prototype for AI agent runtime governance.

It demonstrates the I2OS principle:

```text
AI safety should govern transitions before they become actions.
```
