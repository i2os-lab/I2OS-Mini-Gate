# I2OS Mini Gate Rule Model v0.4

## Core Principle

> Capability is not permission.

I2OS Mini Gate asks whether a proposed transition should be permitted before execution.

---

## Transition Model

```text
S_t → T → S_{t+1}
```

```text
Permit(T) = 1 [ C(S_t, T, S_{t+1}) = 1 ]
```

---

## Rule Categories

- C_recovery
- C_confirmation
- C_scope
- C_external
- C_permission
- C_permission_match
- C_action_keyword
- C_untrusted_external
- C_agent_action
- C_tool_scope
- C_instruction_origin
- C_tool_hijack
- C_external_instruction
- C_permission_escalation
- C_untrusted_tool_use

---

## v0.4 Addition

v0.4 adds rule-based prompt injection transition checks.

It treats prompt injection as an inadmissible transition where an untrusted instruction source attempts to alter tool use, permissions, or external side effects.
