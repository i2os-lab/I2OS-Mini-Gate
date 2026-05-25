# I2OS Mini Gate

**I2OS Mini Gate** is a minimal runtime admissibility gate for checking proposed AI or software actions before execution.

Core principle:

> Capability is not permission.

I2OS Mini Gate classifies proposed actions as:

- **GO**: admissible transition
- **HOLD**: insufficient information
- **REPAIR**: admissible after correction
- **BLOCK**: inadmissible transition

---

## Current Version

```text
v0.4-complete
```

## v0.4 Focus

**Prompt Injection Transition Detector**

v0.4 adds rule-based detection for cases where untrusted content attempts to influence AI agent tool use, external actions, or permission boundaries.

I2OS treats prompt injection not only as a malicious string, but as an inadmissible state transition:

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

## Usage

Run built-in sample tests:

```bash
python i2os_gate.py
```

Run specific examples:

```bash
python i2os_gate.py examples/prompt_injection_hidden_upload.json
python i2os_gate.py examples/prompt_injection_tool_hijack.json
python i2os_gate.py examples/prompt_injection_permission_escalation.json
python i2os_gate.py examples/prompt_injection_safe_summary.json
```

Generated reports:

```text
reports/i2os_sample_report.json
reports/*.md
```

---

## Core Method

```text
Permit(T) = 1 [ C(S_t, T, S_{t+1}) = 1 ]
```

A transition is permitted only when the movement from the current state to the next state satisfies admissibility constraints.

---

## Documentation

```text
docs/rule_model.md
docs/agent_action_checker.md
docs/prompt_injection_detector.md
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
├── agent_external_api_call.json
├── prompt_injection_hidden_upload.json
├── prompt_injection_tool_hijack.json
├── prompt_injection_permission_escalation.json
└── prompt_injection_safe_summary.json
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
