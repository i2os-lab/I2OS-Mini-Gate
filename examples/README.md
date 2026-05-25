# I2OS Mini Gate Examples

This directory contains action examples for testing transition admissibility.

## v0.4 Prompt Injection Examples

- `prompt_injection_hidden_upload.json` → expected `BLOCK`
- `prompt_injection_tool_hijack.json` → expected `BLOCK`
- `prompt_injection_permission_escalation.json` → expected `BLOCK`
- `prompt_injection_safe_summary.json` → expected `GO`

## Usage

```bash
python i2os_gate.py examples/prompt_injection_hidden_upload.json
python i2os_gate.py examples/prompt_injection_tool_hijack.json
python i2os_gate.py examples/prompt_injection_permission_escalation.json
python i2os_gate.py examples/prompt_injection_safe_summary.json
```
