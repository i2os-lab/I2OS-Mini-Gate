# I2OS Mini Gate v1.2
## GitHub Action / CI Hook

> Capability is not permission.

v1.2 adds GitHub Actions / CI integration.

This allows I2OS Mini Gate to run automatically on:

- push
- pull request
- manual workflow dispatch

---

## Added Files

```text
.github/workflows/i2os-mini-gate.yml
ci/i2os_ci_scan.py
```

---

## GitHub Actions Workflow

```yaml
name: I2OS Mini Gate CI
```

The workflow:

1. checks out the repository
2. sets up Python
3. runs unit tests
4. runs CI scan examples

---

## Local CI Scan

```bash
python ci/i2os_ci_scan.py --policy policy/default_policy.json --fail-on BLOCK
```

Scan selected files:

```bash
python ci/i2os_ci_scan.py --policy policy/default_policy.json --actions examples/audit_go_safe_summary.json examples/audit_repair_external_api.json --fail-on BLOCK
```

---

## Fail-On Levels

```text
NONE
HOLD
REPAIR
BLOCK
```

Default:

```text
BLOCK
```

---

## Design Position

v1.2 moves I2OS Mini Gate from local/API execution into automated repository verification.

The flow becomes:

```text
GitHub Push / Pull Request
↓
Unit Tests
↓
I2OS CI Scan
↓
GO / HOLD / REPAIR / BLOCK
↓
Pass / Fail
```

This is the first step toward CI-based transition governance.
