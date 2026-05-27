# I2OS Mini Gate v2.1 Demo Showcase

> Capability is not permission.

This demo package provides simple cases to show how I2OS Mini Gate works as a Runtime Shield Prototype.

## Demo Cases

| File | Expected Direction |
|---|---|
| demo_safe_action.json | GO |
| demo_prompt_injection_block.json | BLOCK |
| demo_delete_block.json | BLOCK |
| demo_external_upload_repair.json | REPAIR or BLOCK |

## Run

```bash
python demo/run_demo.py
```

## Purpose

The demo is designed for quick review:

```text
Proposed action
↓
Runtime Shield
↓
GO / HOLD / REPAIR / BLOCK
```
