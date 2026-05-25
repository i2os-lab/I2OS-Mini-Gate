# I2OS Mini Gate v0.3
## AI Agent Action Checker

## Core Principle

> Capability is not permission.

v0.3 extends I2OS Mini Gate toward AI agent action checking.

The purpose is to inspect proposed AI agent tool-use transitions before execution.

---

## AI Agent Transition

```text
S_t → T_agent → S_{t+1}
```

The transition is permitted only when it satisfies admissibility constraints.

```text
Permit(T_agent) = 1 [ C(S_t, T_agent, S_{t+1}) = 1 ]
```

---

## Agent Fields

v0.3 checks the following fields when present:

- `action_type`
- `tool_name`
- `side_effect_level`
- `target_scope`
- `requires_confirmation`
- `sandbox_required`
- `sandbox_enabled`

---

## Examples

### Safe Summary

Expected:

```text
GO
```

### Dangerous Command Execution

Expected:

```text
BLOCK
```

### External API Call

Expected:

```text
REPAIR
```

---

## Design Position

v0.3 moves I2OS Mini Gate from a generic action classifier toward a practical AI Agent Runtime Governance prototype.

The central question becomes:

```text
Should this AI agent transition be permitted before execution?
```

This is the operational form of:

> Capability is not permission.
