# I2OS Mini Gate

## Latest Release

**I2OS Mini Gate v3.8** is now available.

This release refines the runtime governance layer and clarifies how proposed AI/software actions are checked as state transitions before execution.

Download:

[Download v3.8](https://github.com/i2os-lab/I2OS-Mini-Gate/releases/tag/v3.8)

---

## Overview

**Runtime Admissibility Scanner for AI Agent Actions**

> Capability is not permission.

I2OS Mini Gate is a minimal runtime gate that checks proposed AI/software actions before execution.

It classifies each proposed transition as:

```text
GO / HOLD / REPAIR / BLOCK
```

---

## Current Version

```text
v3.8
```

---

## Core Idea

AI safety should not only filter outputs.

It should govern transitions before they become actions.

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

---

## Core Principle

```text
Permit(T) = 1 [ C(S_t, T, S_{t+1}) = 1 ]
```

A transition is permitted only when the movement from the current state to the next state satisfies admissibility constraints.

---

## Roadmap: v3.8 Runtime Governance Refinement

The current phase of I2OS Mini Gate is **v3.8 Runtime Governance Refinement**.

v3.7-complete stabilized the public release package and repository structure.

v3.8 focuses on making the runtime governance model clearer, more verifiable, and easier to understand for external users.

### v3.8 Core Principle

```text
Capability is not permission.
```

I2OS Mini Gate does not only ask:

```text
Can the AI or software perform this action?
```

It asks:

```text
Should this proposed transition be permitted before execution?
```

### v3.8 Focus

- Clarify the runtime governance model
- Explain GO / HOLD / REPAIR / BLOCK classifications
- Add concrete example cases
- Improve human-verifiable explanations
- Strengthen documentation for transition governance
- Prepare the path toward v4.0 Stable Closed-Loop Runtime Governance Prototype

### Main v3.8 Documents

```text
docs/runtime_governance_v3_8.md
docs/example_cases_v3_8.md
docs/RELEASE_NOTES_v3.8.md
```

### v3.8 Runtime Governance Direction

```text
Proposed Action
↓
State Extraction
↓
Admissibility Check
↓
Recovery / Confirmation Check
↓
Runtime Classification
↓
Human-Verifiable Explanation
↓
Audit / Report Output
```

### Toward v4.0

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

---

## Features

- GO / HOLD / REPAIR / BLOCK classification
- AI agent action checking
- prompt injection transition detection
- external policy configuration
- audit logging
- JSON reports
- Markdown reports
- HTML dashboard reports
- CLI execution
- unit tests
- runtime governance documentation
- example transition cases
- human-verifiable explanation structure

---

## Quickstart

```bash
python i2os_gate.py
```

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --policy policy/default_policy.json
```

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --html --report-prefix prompt_injection_scan
```

```bash
python run_tests.py
```

---

## CLI Options

```text
--action, -a FILE        Action JSON file to scan
--policy, -p FILE        Policy JSON file to load
--report-prefix NAME     Prefix for generated report files
--quiet                  Suppress non-essential messages
--no-reports             Do not write JSON/Markdown reports
--json-only              Print only result JSON
--html                   Generate HTML dashboard report
--help, -h               Show help
```

---

## Version Path

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
| v1.1 | Web/API Mode |
| v1.2 | GitHub Action / CI Hook |
| v1.3 | Agent Runtime Bridge |
| v1.4 | Prompt Injection Lab |
| v1.5 | Local Security Tool Prototype |
| v1.6 | Packaging / Install Mode |
| v1.7 | Policy Profiles |
| v1.8 | Local Dashboard Launcher |
| v1.9 | Hardening / Error Handling |
| v2.0 | Product-grade Runtime Shield Prototype |
| v2.1 | Demo / Showcase Package |
| v2.2 | Runtime Observation Layer |
| v2.3 | Future Constraint Layer |
| v2.4 | Multi-Agent Governance Layer |
| v2.5 | Human-Admissibility Layer |
| v2.6 | Recovery Path Layer |
| v2.7 | Recheck Loop Layer |
| v2.8 | Execution Contract Layer |
| v2.9 | Contract Enforcement Layer |
| v3.0 | Closed-Loop Runtime Governance Core |
| v3.7-complete | Repository Stabilization Release |
| v3.8 | Runtime Governance Refinement |

---

## Documentation

### v3.8 Runtime Governance

```text
docs/runtime_governance_v3_8.md
docs/example_cases_v3_8.md
docs/RELEASE_NOTES_v3.8.md
```

### Core Runtime Shield

```text
docs/runtime_shield_v2.md
PRODUCT_POSITIONING.md
```

### Closed-Loop Governance

```text
docs/closed_loop_governance_core.md
docs/human_admissibility_layer.md
docs/recovery_path_layer.md
docs/recheck_loop_layer.md
docs/execution_contract_layer.md
docs/contract_enforcement_layer.md
```

---

## v1.1 Web/API Mode

Optional FastAPI mode is included.

Install dependencies:

```bash
pip install -r requirements-api.txt
```

Start API server:

```bash
uvicorn i2os_api:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Main endpoint:

```text
POST /scan
```

See:

```text
docs/web_api_mode.md
```

---

## v1.2 GitHub Action / CI Hook

v1.2 adds CI integration.

Run locally:

```bash
python ci/i2os_ci_scan.py --policy policy/default_policy.json --fail-on BLOCK
```

GitHub Actions workflow:

```text
.github/workflows/i2os-mini-gate.yml
```

See:

```text
docs/github_action_ci.md
```

---

## v1.3 Agent Runtime Bridge

v1.3 adds a dry-run runtime bridge for AI agent actions.

```bash
python agent_bridge/runtime_bridge.py "echo hello"
```

```bash
python agent_bridge/runtime_bridge.py "rm -rf ./project"
```

The bridge does not execute commands. It only checks whether the proposed transition is permitted.

See:

```text
docs/agent_runtime_bridge.md
```

---

## v1.4 Prompt Injection Lab

v1.4 adds repeatable prompt-injection transition tests.

```bash
python prompt_injection_lab/run_lab.py --policy policy/default_policy.json
```

See:

```text
docs/prompt_injection_lab.md
```

---

## v1.5 Local Security Tool Prototype

v1.5 adds a lightweight local security tool.

```bash
python local_tool/i2os_local_security.py file --path ./README.md --operation read
```

```bash
python local_tool/i2os_local_security.py file --path ./project --operation delete
```

```bash
python local_tool/i2os_local_security.py url --url https://example.com/upload --operation upload
```

See:

```text
docs/local_security_tool.md
```

---

## v1.6 Packaging / Install Mode

v1.6 adds package-style execution.

```bash
python -m i2os_mini_gate --action examples/audit_block_prompt_injection.json
```

Optional local install:

```bash
pip install -e .
i2os-scan --action examples/audit_block_prompt_injection.json
```

See:

```text
docs/packaging_install.md
```

---

## v1.7 Policy Profiles

v1.7 adds three policy profiles:

```text
policy/strict_policy.json
policy/balanced_policy.json
policy/permissive_policy.json
```

Example:

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --policy policy/strict_policy.json
```

See:

```text
docs/policy_profiles.md
```

---

## v1.8 Local Dashboard Launcher

v1.8 adds a dashboard launcher.

```bash
python dashboard_launcher/launch_dashboard.py --action examples/audit_block_prompt_injection.json --policy policy/strict_policy.json --report-prefix prompt_scan
```

Open generated HTML in browser:

```bash
python dashboard_launcher/launch_dashboard.py --action examples/audit_block_prompt_injection.json --policy policy/strict_policy.json --report-prefix prompt_scan --open
```

See:

```text
docs/dashboard_launcher.md
```

---

## v1.9 Hardening / Error Handling

v1.9 adds fail-safe error handling.

Examples:

```bash
python i2os_gate.py --action examples/not_found.json
```

```bash
python i2os_gate.py --action examples/invalid_action_missing_fields.json
```

```bash
python i2os_gate.py --action examples/invalid_json_example.json
```

See:

```text
docs/hardening_error_handling.md
```

---

## v2.0 Product-grade Runtime Shield Prototype

v2.0 consolidates the system into a Runtime Shield prototype.

```bash
python runtime_shield/shield.py examples/audit_block_prompt_injection.json policy/strict_policy.json
```

Python usage:

```python
from runtime_shield import RuntimeShield

shield = RuntimeShield(policy_path="policy/strict_policy.json")
result = shield.shield(action)
```

See:

```text
docs/runtime_shield_v2.md
PRODUCT_POSITIONING.md
```

---

## v2.1 Demo / Showcase Package

v2.1 adds a simple demo package.

```bash
python demo/run_demo.py
```

Demo cases:

```text
safe action → GO
prompt injection → BLOCK
delete all files → BLOCK
external upload → REPAIR or BLOCK
```

See:

```text
docs/demo_showcase.md
```

---

## v2.2 Runtime Observation Layer

v2.2 adds sequence-level runtime observation.

```bash
python runtime_observer/observe_sequence.py demo/demo_safe_action.json demo/demo_prompt_injection_block.json demo/demo_delete_block.json
```

See:

```text
docs/runtime_observation_layer.md
```

---

## v2.3 Future Constraint Layer

v2.3 adds future compatibility checks.

```bash
python future_constraint/evaluate_future.py demo/demo_safe_action.json
```

```bash
python future_constraint/evaluate_future.py demo/demo_delete_block.json policy/strict_policy.json
```

See:

```text
docs/future_constraint_layer.md
```

---

## v2.4 Multi-Agent Governance Layer

v2.4 adds chain-level governance for multi-agent/tool sequences.

```bash
python multi_agent/evaluate_multi_agent.py multi_agent/sample_chain_upload_risk.json
```

```bash
python multi_agent/evaluate_multi_agent.py multi_agent/sample_chain_safe_local.json policy/balanced_policy.json
```

See:

```text
docs/multi_agent_governance.md
```

---

## v2.5 Human-Admissibility Layer

v2.5 adds human-side authorization stability checks.

```bash
python human_admissibility/evaluate_human_admissibility.py human_admissibility/sample_human_confirmed_safe_action.json
```

```bash
python human_admissibility/evaluate_human_admissibility.py human_admissibility/sample_emotional_escalation_block.json policy/strict_policy.json
```

See:

```text
docs/human_admissibility_layer.md
```

---

## v2.6 Recovery Path Layer

v2.6 converts HOLD / REPAIR / BLOCK into recovery paths.

```bash
python recovery_path/evaluate_recovery_path.py recovery_path/sample_recovery_block.json
```

```bash
python recovery_path/evaluate_recovery_path.py human_admissibility/sample_emotional_escalation_block.json policy/strict_policy.json
```

See:

```text
docs/recovery_path_layer.md
```

---

## v2.7 Recheck Loop Layer

v2.7 connects recovery paths to a second admissibility check.

```bash
python recheck_loop/evaluate_recheck_loop.py recheck_loop/sample_recheck_rushed_send.json
```

See:

```text
docs/recheck_loop_layer.md
```

---

## v2.8 Execution Contract Layer

v2.8 converts GO into a bounded execution contract.

```bash
python execution_contract/build_execution_contract.py execution_contract/sample_contract_go.json
```

```bash
python execution_contract/build_execution_contract.py recheck_loop/sample_recheck_rushed_send.json policy/balanced_policy.json
```

See:

```text
docs/execution_contract_layer.md
```

---

## v2.9 Contract Enforcement Layer

v2.9 checks whether attempted execution remains inside the issued contract.

```bash
python contract_enforcement/enforce_contract.py contract_enforcement/sample_contract.json contract_enforcement/sample_attempt_allowed.json
```

```bash
python contract_enforcement/enforce_contract.py contract_enforcement/sample_contract.json contract_enforcement/sample_attempt_violation.json
```

See:

```text
docs/contract_enforcement_layer.md
```

---

## v3.0 Closed-Loop Runtime Governance Core

v3.0 integrates the v2.x layers into a closed-loop governance pipeline.

```bash
python governance_core/run_governance_core.py governance_core/sample_governance_package.json
```

```bash
python governance_core/run_governance_core.py governance_core/sample_governance_violation_package.json
```

See:

```text
docs/closed_loop_governance_core.md
```

---

## Author

Masayuki Ando / ANDOM

Project:

```text
I2OS
Infinity Intelligence Operating System
```

---

## License

MIT License
