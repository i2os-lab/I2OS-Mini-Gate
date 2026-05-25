# I2OS Mini Gate Rule Model v0.3

## Core Principle

> Capability is not permission.

I2OS Mini Gate does not ask only whether an action can be executed.

It asks whether the proposed transition should be permitted.

---

## Transition Model

A proposed action is treated as a transition.

```text
S_t → T → S_{t+1}
```

Where:

- `S_t` = current state
- `T` = proposed transition/action
- `S_{t+1}` = expected next state

The gate permits a transition only if it satisfies admissibility constraints.

```text
Permit(T) = 1 [ C(S_t, T, S_{t+1}) = 1 ]
```

---

## Decision Types

### GO

The transition is allowed.

### HOLD

The transition is not rejected, but cannot be permitted yet.

### REPAIR

The transition is risky but may become admissible after correction.

### BLOCK

The transition is structurally inadmissible.

---

## Rule Categories

### C_recovery

Checks whether the action can be undone.

### C_confirmation

Checks whether the user explicitly confirmed the action.

### C_scope

Checks whether the action scope is too broad.

### C_external

Checks whether the action affects external systems.

### C_permission

Checks whether the actor has a valid permission level.

### C_permission_match

Checks whether the proposed action requires a higher permission level than the actor currently has.

### C_action_keyword

Checks dangerous operation keywords.

### C_untrusted_external

Checks whether an untrusted source attempts to trigger an external effect.

### C_agent_action

Checks AI agent-specific fields such as action type, tool, side effect level, and sandbox requirement.

### C_tool_scope

Checks whether the selected tool and target scope are compatible.

---

## Current Limitation

This prototype is not a full vulnerability scanner.

It is a minimal transition gate.

It does not prove that an action is safe.

It only classifies whether the proposed transition is structurally admissible under the current rule model.
