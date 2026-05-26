# I2OS Mini Gate v1.3
## Agent Runtime Bridge Release

v1.3 adds a dry-run Agent Runtime Bridge.

## Added

```text
agent_bridge/runtime_bridge.py
docs/agent_runtime_bridge.md
examples/bridge_safe_read.json
examples/bridge_block_command.json
tests/test_agent_bridge.py
```

## Safety Note

The current bridge is dry-run only.

It does not execute commands.
