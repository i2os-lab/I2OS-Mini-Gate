# I2OS Mini Gate

Runtime Admissibility Scanner for AI Agent Actions

> Capability is not permission.

I2OS Mini Gate is a public implementation layer derived from the broader I2OS research line, focusing specifically on Runtime Admissibility and Transition Governance.

I2OS Mini Gate は、I2OS全体構造のうち、Runtime Admissibility と Transition Governance に焦点を当てた公開実装層です。

I2OS Mini Gate is a minimal runtime gate that checks proposed AI/software actions before execution.
I2OS Mini Gate は、I2OS全体構造のうち、Runtime Admissibility と Transition Governance に焦点を当てた公開実装層です。

It classifies each proposed transition as:

```text
GO / HOLD / REPAIR / BLOCK
```

## Current Version

```text
v2.0-complete
```

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

## Core Principle

```text
Permit(T) = 1 [ C(S_t, T, S_{t+1}) = 1 ]
```

A transition is permitted only when the movement from the current state to the next state satisfies admissibility constraints.

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

## Author

Masayuki Ando / ANDOM

Project:

```text
I2OS
Infinity Intelligence Operating System
```

## License

MIT License


---

## v1.1 Web/API Mode

Optional FastAPI mode is now included.

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
Original concept and architecture by Masayuki Ando / ANDOM.
I2OS Mini Gate is part of the I2OS research line: Runtime Admissibility, Transition Governance, and the principle “Capability is not permission.”

See:

```text
docs/runtime_shield_v2.md
PRODUCT_POSITIONING.md
```
