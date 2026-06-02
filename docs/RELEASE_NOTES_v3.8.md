# I2OS Mini Gate v3.8

## Runtime Governance Refinement

## Release Type

Refinement / Documentation / Runtime Governance Clarification

## Status

Planned / In Progress

## Core Principle

```text
Capability is not permission.
```

I2OS Mini Gate v3.8 continues the transition from simple action classification toward runtime transition governance.

The system does not only ask:

```text
Can the AI or software perform this action?
```

It asks:

```text
Should this proposed transition be permitted before execution?
```

---

## 1. Purpose of v3.8

I2OS Mini Gate v3.8 refines the runtime governance structure after the v3.7-complete release.

v3.7 focused on repository stabilization and public release packaging.

v3.8 focuses on making the runtime governance model easier to understand, verify, and extend.

Main purpose:

```text
Clarify how proposed AI/software actions are checked
as state transitions before execution.
```

---

## 2. What v3.8 Adds

v3.8 adds documentation and conceptual refinement for:

- runtime governance flow
- GO / HOLD / REPAIR / BLOCK classification
- example cases
- admissibility constraints
- human-verifiable explanations
- transition governance vs output filtering
- path toward v4.0 stable closed-loop governance

---

## 3. Main Documents

### docs/runtime_governance_v3_8.md

Explains the runtime governance model.

Includes:

- public definition
- runtime governance flow
- classification logic
- core equation
- admissibility constraints
- human-verifiable governance
- v4.0 direction

### docs/example_cases_v3_8.md

Provides concrete examples for each classification.

Includes:

- GO examples
- HOLD examples
- REPAIR examples
- BLOCK examples
- comparison table
- design principle

---

## 4. Runtime Output

I2OS Mini Gate classifies proposed transitions as:

```text
GO / HOLD / REPAIR / BLOCK
```

### GO

The transition is admissible and may proceed.

### HOLD

The transition requires confirmation, clarification, or additional context.

### REPAIR

The transition is not currently admissible, but it may become admissible if corrected.

### BLOCK

The transition is inadmissible and should not proceed.

---

## 5. Core Equation

The conceptual kernel remains:

```text
Permit(T) = 1 [ C(S_t, T, S_{t+1}) = 1 ]
```

Where:

- S_t = current state
- T = proposed transition
- S_{t+1} = next state
- C = admissibility constraint

A transition is permitted only when it satisfies the admissibility constraint.

---

## 6. Admissibility Constraint

The admissibility constraint may include:

```text
C =
C_context
∧ C_safety
∧ C_recovery
∧ C_sync
∧ C_future
```

Meaning:

- context-valid
- safety-compatible
- recoverable
- synchronized with user intent and task scope
- future-compatible

---

## 7. Why v3.8 Matters

Modern AI systems increasingly perform actions, not only generate text.

These actions may include:

- file operations
- shell commands
- tool calls
- email sending
- API access
- code execution
- memory writes
- agent-to-agent delegation

For such systems, output filtering is not enough.

The proposed action must be checked before execution.

I2OS Mini Gate v3.8 clarifies this pre-execution transition governance layer.

---

## 8. Difference from v3.7

### v3.7-complete

Focused on:

- repository stabilization
- clean release packaging
- README update
- release ZIP publication
- public announcement

### v3.8

Focuses on:

- runtime governance refinement
- clearer documentation
- example cases
- human-verifiable explanations
- v4.0 preparation

---

## 9. Path Toward v4.0

v3.8 prepares the project for:

```text
I2OS Mini Gate v4.0
Stable Closed-Loop Runtime Governance Prototype
```

Expected v4.0 direction:

```text
Proposed Action
↓
Human-Admissibility
↓
Recovery Path
↓
Recheck Loop
↓
Execution Contract
↓
Contract Enforcement
↓
Final Governance Report
```

v3.8 is the refinement layer before that stable closed-loop release.

---

## 10. Public Positioning

I2OS Mini Gate is a minimal runtime admissibility gate for AI or software actions before execution.

It is not only an output filter.

It is a transition governance prototype.

Public summary:

```text
I2OS Mini Gate checks proposed AI/software actions
as state transitions before execution
and classifies them as GO / HOLD / REPAIR / BLOCK.
```

---

## 11. Repository

```text
https://github.com/i2os-lab/I2OS-Mini-Gate
```

---

## 12. Final Principle

```text
Capability is not permission.
```

A system should not execute an action simply because it can.

It should execute only when the proposed transition is admissible.
