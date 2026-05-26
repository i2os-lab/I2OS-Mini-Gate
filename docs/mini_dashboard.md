# I2OS Mini Gate v0.9
## Mini Dashboard / HTML Report

> Capability is not permission.

v0.9 adds a human-readable HTML dashboard report.

---

## Generate HTML Dashboard

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --html
```

With a custom report prefix:

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --html --report-prefix prompt_injection_scan
```

Generated output:

```text
dashboard/prompt_injection_scan.html
```

---

## Dashboard Contents

The HTML report includes:

- decision
- risk level
- policy name
- version
- human-verifiable explanation
- audit summary
- constraint results
- reason codes
- reasons
- repair suggestions
- input action JSON

---

## Design Position

v0.9 moves I2OS Mini Gate from CLI-only output into a visual audit report.

This improves human verification:

```text
CLI result
↓
Markdown report
↓
JSON report
↓
HTML dashboard
```

The system now becomes easier to show, audit, and publish.
