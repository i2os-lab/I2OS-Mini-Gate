# I2OS Mini Gate v1.6
## Packaging / Install Mode

> Capability is not permission.

v1.6 adds a lightweight Python package layout.

The existing `i2os_gate.py` remains available.

A package facade is added:

```text
i2os_mini_gate/
├── __init__.py
├── __main__.py
├── gate.py
├── cli.py
├── policy.py
└── reports.py
```

---

## Run as a Module

```bash
python -m i2os_mini_gate --action examples/audit_block_prompt_injection.json
```

With policy:

```bash
python -m i2os_mini_gate --action examples/audit_block_prompt_injection.json --policy policy/default_policy.json
```

With HTML:

```bash
python -m i2os_mini_gate --action examples/audit_block_prompt_injection.json --html --report-prefix package_scan
```

---

## Install Locally

```bash
pip install -e .
```

Then run:

```bash
i2os-scan --action examples/audit_block_prompt_injection.json
```

---

## Why This Matters

Before v1.6, the main usage was:

```bash
python i2os_gate.py ...
```

From v1.6, the project can also be used as:

```bash
python -m i2os_mini_gate ...
```

or, after local install:

```bash
i2os-scan ...
```

This moves the project closer to a distributable tool without breaking the existing script-based workflow.
