# I2OS Mini Gate v0.8
## CLI Runtime Scanner

> Capability is not permission.

v0.8 improves the command-line interface so I2OS Mini Gate can be used as a lightweight runtime scanner.

---

## Basic Usage

Run built-in sample scans:

```bash
python i2os_gate.py
```

Scan a specific action file:

```bash
python i2os_gate.py examples/audit_block_prompt_injection.json
```

or:

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json
```

---

## Policy File

Use an external policy:

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --policy policy/default_policy.json
```

---

## Report Prefix

Set custom report names:

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --report-prefix scan_prompt_injection
```

This generates:

```text
reports/scan_prompt_injection.json
reports/scan_prompt_injection.md
```

---

## JSON-Only Mode

Useful for integration with other tools:

```bash
python i2os_gate.py --action examples/audit_go_safe_summary.json --json-only --no-reports
```

---

## Quiet Mode

Suppress non-essential messages:

```bash
python i2os_gate.py --action examples/audit_go_safe_summary.json --quiet
```

---

## Help

```bash
python i2os_gate.py --help
```

---

## Design Position

v0.8 moves I2OS Mini Gate from a Python script into a minimal CLI Runtime Scanner.

The flow becomes:

```text
Action JSON
↓
Policy
↓
CLI Runtime Scanner
↓
GO / HOLD / REPAIR / BLOCK
↓
Reports / Audit Logs
```
