# I2OS Mini Gate v0.7
## Test Suite / Unit Tests

> Capability is not permission.

v0.7 adds a basic unit test suite to verify stable decision behavior.

## Run Tests

```bash
python run_tests.py
```

or:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Tested Cases

| Test | Expected |
|---|---|
| safe summary | GO |
| external API call | REPAIR or BLOCK |
| prompt injection | BLOCK |
| missing fields | HOLD |
| destructive command | BLOCK |

## Design Position

v0.7 moves I2OS Mini Gate from a working prototype toward a verifiable runtime governance component.
