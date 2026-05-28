# I2OS Mini Gate v1.3
## Agent Runtime Bridge

> Capability is not permission.

v1.3 adds an Agent Runtime Bridge.

The bridge is a dry-run adapter layer intended to sit between an AI agent and a proposed tool/action execution.

## Core Flow

```text
AI Agent proposes action
↓
Agent Runtime Bridge
↓
I2OS Mini Gate scan
↓
GO / HOLD / REPAIR / BLOCK
↓
Only GO may proceed
```

## Added Files

```text
agent_bridge/runtime_bridge.py
examples/bridge_safe_read.json
examples/bridge_block_command.json
```

## Dry-Run Command Check

```bash
python agent_bridge/runtime_bridge.py "echo hello"
```

```bash
python agent_bridge/runtime_bridge.py "rm -rf ./project"
```

The bridge does not execute commands. It only checks whether the proposed transition is permitted.

## Python Usage

```python
from agent_bridge.runtime_bridge import AgentRuntimeBridge

bridge = AgentRuntimeBridge(policy_path="policy/default_policy.json")
result = bridge.guard(action)

if result["permitted"]:
    print("Allowed")
else:
    print("Blocked")
```

## Design Position

v1.3 is the first runtime bridge layer.

It wraps the proposed execution step and asks:

```text
Should this transition be permitted before execution?
```
