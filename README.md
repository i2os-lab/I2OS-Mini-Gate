# I2OS Mini Gate

**I2OS Mini Gate** is a minimal runtime admissibility gate for checking proposed AI or software actions before execution.

Core principle:

> Capability is not permission.

I2OS Mini Gate classifies proposed actions as:

- **GO**: admissible transition
- **HOLD**: insufficient information
- **REPAIR**: admissible after correction
- **BLOCK**: inadmissible transition

This prototype is derived from the I2OS concepts of **Runtime Admissibility**, **Transition Governance**, and **Structural Admissibility**.

---

## Concept

Modern AI agents and software systems can perform increasingly powerful actions.

However:

```text
Capability does not mean permission.
```

Before an action becomes executable, the system should check whether the proposed transition is structurally admissible.

I2OS Mini Gate follows this process:

```text
State
↓
Transition
↓
Constraint Check
↓
GO / HOLD / REPAIR / BLOCK
```

---

## Core Method

```text
Permit(T) = 1 [ C(S_t, T, S_{t+1}) = 1 ]
```

Meaning:

A transition is permitted only when the movement from the current state to the next state satisfies admissibility constraints.

---

## v0.3 Focus

**v0.3-complete** extends I2OS Mini Gate into an early **AI Agent Action Checker**.

It now checks agent-specific fields such as:

- `action_type`
- `tool_name`
- `side_effect_level`
- `target_scope`
- `requires_confirmation`
- `sandbox_required`
- `sandbox_enabled`

This makes the gate closer to an AI agent runtime governance prototype.

---

## Usage

Run built-in sample tests:

```bash
python i2os_gate.py
```

Run a specific example:

```bash
python i2os_gate.py examples/agent_safe_summary.json
python i2os_gate.py examples/agent_dangerous_command.json
python i2os_gate.py examples/agent_external_api_call.json
python i2os_gate.py examples/prompt_injection_upload.json
python i2os_gate.py examples/api_auth_bypass.json
```

Generated reports:

```text
reports/i2os_sample_report.json
reports/*.md
```

---

## Examples

```text
examples/
├── safe_summary.json
├── ai_agent_file_delete.json
├── prompt_injection_upload.json
├── api_auth_bypass.json
├── agent_safe_summary.json
├── agent_dangerous_command.json
└── agent_external_api_call.json
```

Expected decisions:

| Example | Expected |
|---|---|
| safe_summary.json | GO |
| ai_agent_file_delete.json | BLOCK |
| prompt_injection_upload.json | BLOCK |
| api_auth_bypass.json | BLOCK |
| agent_safe_summary.json | GO |
| agent_dangerous_command.json | BLOCK |
| agent_external_api_call.json | REPAIR |

---

## Documentation

```text
docs/rule_model.md
docs/agent_action_checker.md
```

---

## Philosophy

Traditional security tools often ask:

```text
Where is the vulnerability?
```

I2OS asks:

```text
Why is this transition inadmissible?
```

The goal is not only to detect dangerous outputs, but to prevent structurally unsafe transitions before they become real-world actions.

---

## Status

Current version:

```text
v0.3-complete
```

Implemented features:

- GO / HOLD / REPAIR / BLOCK output
- JSON / Markdown report generation
- documented rule model
- AI agent action fields
- basic prompt injection transition handling
- basic authorization mismatch handling
- basic sandbox requirement handling
- basic destructive tool-use detection

---

## Author

Masayuki Ando / ANDOM

Project:

```text
I2OS
Infinity Intelligence Operating System
```

---

## Core Principle

> Capability is not permission.
