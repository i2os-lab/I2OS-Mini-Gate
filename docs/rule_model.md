# I2OS Mini Gate Rule Model v0.2

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

Typical conditions:

- required information is present
- action is reversible or low-risk
- scope is limited
- no dangerous side effect is detected
- permission level is valid
- user confirmation is present when needed

### HOLD

The transition is not rejected, but cannot be permitted yet.

Typical causes:

- missing required fields
- unknown target
- unclear scope
- insufficient context
- ambiguous permission level

### REPAIR

The transition is risky but may become admissible after correction.

Typical causes:

- user confirmation is missing
- external side effect exists
- permission must be verified
- target scope should be narrowed
- safer alternative exists

### BLOCK

The transition is structurally inadmissible.

Typical causes:

- irreversible transition
- broad destructive scope
- unrecoverable delete/remove action
- dangerous action without sufficient confirmation
- untrusted context attempts external action
- permission mismatch
- action may cause unrecoverable state collapse

---

## Current Rule Categories

### 1. Recovery Constraint

Checks whether the action can be undone.

```text
C_recovery
```

Examples:

- reversible = false
- permanent delete
- irreversible overwrite
- destructive modification

### 2. Confirmation Constraint

Checks whether the user explicitly confirmed the action.

```text
C_confirmation
```

Examples:

- user_confirmed = false
- broad action without confirmation
- external action without confirmation

### 3. Scope Constraint

Checks whether the action scope is too broad.

```text
C_scope
```

Blocked or repair-required scopes:

- all_files
- entire_project
- system
- all_users

### 4. External Effect Constraint

Checks whether the action affects external systems.

```text
C_external
```

Examples:

- upload
- send
- export
- post to external service
- call external API

### 5. Permission Constraint

Checks whether the actor has a valid permission level.

```text
C_permission
```

Allowed levels:

- read_only
- user
- admin

Unknown permission levels require HOLD or REPAIR.

### 6. Permission Mismatch Constraint

Checks whether the proposed action requires a higher permission level than the actor currently has.

```text
C_permission_match
```

Example:

```json
{
  "permission_level": "user",
  "expected_required_permission": "admin"
}
```

This should be treated as a permission transition mismatch.

### 7. Dangerous Keyword Constraint

Checks whether the proposed action contains dangerous operation keywords.

```text
C_action_keyword
```

Current keywords:

- delete
- remove
- erase
- wipe
- send
- upload
- export
- execute
- run command
- shutdown

### 8. Untrusted Context External Action Constraint

Checks whether an untrusted source attempts to trigger an external effect.

```text
C_untrusted_external
```

Example:

```json
{
  "source_context": "untrusted_document",
  "external_effect": true,
  "proposed_action": "upload local files to external service"
}
```

This is treated as a structurally inadmissible transition.

---

## Current Limitation

This prototype is not a full vulnerability scanner.

It is a minimal transition gate.

It does not prove that an action is safe.

It only classifies whether the proposed transition is structurally admissible under the current rule model.

---

## Future Extensions

Future versions may add:

- richer prompt injection transition detection
- AI agent tool-use governance
- Web/API authorization checks
- file operation sandboxing
- risk explanation templates
- custom rule files
- YAML/JSON policy configuration
- test suite integration
