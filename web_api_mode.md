# Quickstart

## Run Built-in Samples

```bash
python i2os_gate.py
```

## Scan an Action JSON

```bash
python i2os_gate.py --action examples/audit_go_safe_summary.json
```

## Use External Policy

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --policy policy/default_policy.json
```

## Generate HTML Dashboard

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --html --report-prefix prompt_injection_scan
```

## Run Tests

```bash
python run_tests.py
```

## JSON-only Integration Mode

```bash
python i2os_gate.py --action examples/audit_go_safe_summary.json --json-only --no-reports
```
