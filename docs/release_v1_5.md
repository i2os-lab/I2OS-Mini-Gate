# I2OS Mini Gate v1.5
## Local Security Tool Prototype Release

v1.5 adds a local security tool prototype.

## Added

```text
local_tool/i2os_local_security.py
docs/local_security_tool.md
tests/test_local_tool.py
```

## Run

```bash
python local_tool/i2os_local_security.py file --path ./README.md --operation read
```

```bash
python local_tool/i2os_local_security.py file --path ./project --operation delete
```

## Position

v1.5 makes I2OS Mini Gate usable as a lightweight local pre-execution checker.
