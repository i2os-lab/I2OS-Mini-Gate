# I2OS Mini Gate v1.5
## Local Security Tool Prototype

> Capability is not permission.

v1.5 adds a lightweight local security tool prototype.

The goal is to make I2OS Mini Gate usable as a small command-line safety checker for local actions.

## Added Files

```text
local_tool/i2os_local_security.py
docs/local_security_tool.md
tests/test_local_tool.py
```

## File Operation Check

```bash
python local_tool/i2os_local_security.py file --path ./README.md --operation read
```

```bash
python local_tool/i2os_local_security.py file --path ./project --operation delete
```

## URL / Network Operation Check

```bash
python local_tool/i2os_local_security.py url --url https://example.com --operation get
```

```bash
python local_tool/i2os_local_security.py url --url https://example.com/upload --operation upload
```

## JSON Output

```bash
python local_tool/i2os_local_security.py file --path ./README.md --operation read --json
```

## Design Position

v1.5 turns I2OS Mini Gate into a local security tool prototype.

This is still a pre-execution dry-run checker.

It does not execute file or network operations.
