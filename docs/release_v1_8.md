# I2OS Mini Gate v1.8
## Local Dashboard Launcher Release

v1.8 adds a local dashboard launcher.

## Added

```text
dashboard_launcher/launch_dashboard.py
dashboard_launcher/__init__.py
i2os_mini_gate/dashboard.py
docs/dashboard_launcher.md
tests/test_dashboard_launcher.py
```

## Run

```bash
python dashboard_launcher/launch_dashboard.py --action examples/audit_block_prompt_injection.json --policy policy/strict_policy.json --report-prefix prompt_scan
```

## Position

v1.8 strengthens the visual review layer by making HTML dashboard creation easier.
