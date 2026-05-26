# I2OS Mini Gate v1.2
## GitHub Action / CI Hook Release

v1.2 adds CI-based transition governance.

## Added

```text
.github/workflows/i2os-mini-gate.yml
ci/i2os_ci_scan.py
docs/github_action_ci.md
tests/test_ci.py
```

## Local Run

```bash
python ci/i2os_ci_scan.py --policy policy/default_policy.json --fail-on BLOCK
```

## Position

v1.2 connects I2OS Mini Gate to automated development workflows.
