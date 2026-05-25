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

## What This Prototype Detects

This prototype checks simple but important transition risks:

- irreversible actions
- missing user confirmation
- overly broad action scope
- external side effects
- unknown permission level
- dangerous action keywords
- unrecoverable delete/remove operations
- permission mismatch indicators
- untrusted-context external actions

---

## Usage

Run built-in sample tests:

```bash
python i2os_gate.py
```

Run a specific example:

```bash
python i2os_gate.py examples/ai_agent_file_delete.json
python i2os_gate.py examples/prompt_injection_upload.json
python i2os_gate.py examples/api_auth_bypass.json
```

Generated reports:

```text
reports/i2os_sample_report.json
reports/*.md
```

---

## Additional Examples

The `examples/` directory contains transition cases.

```text
examples/
├── ai_agent_file_delete.json
├── prompt_injection_upload.json
├── api_auth_bypass.json
└── safe_summary.json
```

### AI Agent File Delete

A proposed file deletion action over an entire project.

Expected decision:

```text
BLOCK
```

### Prompt Injection Upload

An untrusted document attempts to trigger an external upload.

Expected decision:

```text
BLOCK
```

### API Authorization Bypass

A normal user attempts to access an admin-level export transition.

Expected decision:

```text
BLOCK
```

### Safe Summary

A read-only local summarization action.

Expected decision:

```text
GO
```

---

## Rule Model

See:

```text
docs/rule_model.md
```

---

---

## v0.3 Design: AI Agent Action Checker

The next design step is documented here:

```text
docs/agent_action_checker.md
```

v0.3 extends I2OS Mini Gate toward AI agent runtime governance by adding agent-specific action fields:

- `action_type`
- `tool_name`
- `side_effect_level`
- `target_scope`
- `requires_confirmation`
- `sandbox_required`

Additional v0.3 design examples:

```text
examples/agent_safe_summary.json
examples/agent_dangerous_command.json
examples/agent_external_api_call.json
```

## Roadmap

### v0.1.4 - Mini Gate Prototype

Implemented:

- GO / HOLD / REPAIR / BLOCK classification
- built-in sample tests
- JSON report generation
- Markdown report generation
- basic transition risk detection

### v0.2 - Rule-Based Runtime Admissibility Gate

Implemented in this complete package:

- documented rule model
- examples directory
- additional transition examples
- prompt injection / untrusted context rule
- permission mismatch rule
- reports directory

### v0.3 - AI Agent Action Checker

Planned direction:

- classify AI agent file operations, command execution, uploads, and external API calls
- add structured tool-use transition fields

### v0.4 - Prompt Injection Transition Detector

Planned direction:

- detect external instructions attempting to change tool permissions
- identify untrusted context attempting to trigger external side effects

### v0.5 - Web/API Authorization Transition Checker

Planned direction:

- inspect proposed API transitions
- detect permission mismatch
- detect user-to-admin transition anomalies

### v1.0 - Runtime Admissibility Scanner

Long-term target:

- AI agent runtime security
- LLM tool-use governance
- prompt injection transition detection
- irreversible action prevention
- Web/API authorization transition checks
- structural bug hunting

---

## Project Position

This is a minimal prototype of:

```text
I2OS Runtime Admissibility Scanner
```

It is not a full security scanner.

It is a small experimental gate for detecting inadmissible state transitions before execution.

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
v0.2-complete
```

Implemented features:

- four-way decision output
- JSON / Markdown report generation
- documented rule model
- additional example actions
- basic prompt injection transition handling
- basic authorization mismatch handling

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
