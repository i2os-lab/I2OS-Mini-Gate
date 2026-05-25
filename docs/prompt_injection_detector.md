# I2OS Mini Gate v0.4
## Prompt Injection Transition Detector

## Core Principle

> Capability is not permission.

Prompt injection is treated as an inadmissible state transition, not merely a dangerous string.

---

## Target Structure

```text
Untrusted Input
↓
Instruction Override
↓
Tool Permission Hijack
↓
External Side Effect
↓
Inadmissible Transition
```

---

## Fields

v0.4 checks:

- `source_context`
- `instruction_origin`
- `contains_instruction_override`
- `requests_tool_use`
- `requests_external_effect`
- `attempts_permission_escalation`
- `trusted_by_user`

---

## Detection Rules

### Instruction Override

If untrusted content attempts to override instructions:

```text
BLOCK
```

### Tool Use Request

If untrusted content requests tool use:

```text
BLOCK or REPAIR depending on side effect
```

### External Side Effect

If untrusted content requests upload, send, export, or external write:

```text
BLOCK
```

### Permission Escalation

If external content attempts to increase permissions:

```text
BLOCK
```

---

## Operational Definition

Prompt injection in I2OS is:

```text
An untrusted instruction attempting to create an inadmissible transition through an AI agent.
```
