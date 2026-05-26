# I2OS Mini Gate v1.8
## Local Dashboard Launcher

> Capability is not permission.

v1.8 adds a local dashboard launcher.

The launcher scans an action JSON, generates JSON / Markdown / HTML reports, and optionally opens the HTML dashboard in the browser.

---

## Added Files

```text
dashboard_launcher/launch_dashboard.py
dashboard_launcher/__init__.py
docs/dashboard_launcher.md
docs/release_v1_8.md
tests/test_dashboard_launcher.py
```

---

## Usage

Generate dashboard reports:

```bash
python dashboard_launcher/launch_dashboard.py --action examples/audit_block_prompt_injection.json --policy policy/strict_policy.json --report-prefix prompt_scan
```

Open in browser:

```bash
python dashboard_launcher/launch_dashboard.py --action examples/audit_block_prompt_injection.json --policy policy/strict_policy.json --report-prefix prompt_scan --open
```

JSON output:

```bash
python dashboard_launcher/launch_dashboard.py --action examples/audit_go_safe_summary.json --json
```

---

## Outputs

```text
reports/<prefix>.json
reports/<prefix>.md
dashboard/<prefix>.html
```

---

## Design Position

v1.8 improves human verification.

The flow becomes:

```text
Action JSON
↓
Policy Profile
↓
I2OS Gate
↓
JSON / Markdown / HTML
↓
Local Dashboard
```

This makes the project easier to demonstrate and review.
