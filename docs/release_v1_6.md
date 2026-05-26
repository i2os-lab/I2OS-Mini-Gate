# I2OS Mini Gate v1.6
## Packaging / Install Mode Release

v1.6 adds package-style execution.

## Added

```text
i2os_mini_gate/
pyproject.toml
docs/packaging_install.md
tests/test_package_mode.py
```

## Run

```bash
python -m i2os_mini_gate --action examples/audit_go_safe_summary.json --json-only --no-reports
```

## Optional local install

```bash
pip install -e .
i2os-scan --action examples/audit_go_safe_summary.json
```

## Position

v1.6 makes I2OS Mini Gate easier to run, install, and distribute.
