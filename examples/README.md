# I2OS Mini Gate Examples

This directory contains action examples for testing transition admissibility.

## Files

- `safe_summary.json` → expected `GO`
- `ai_agent_file_delete.json` → expected `BLOCK`
- `prompt_injection_upload.json` → expected `BLOCK`
- `api_auth_bypass.json` → expected `BLOCK`
- `agent_safe_summary.json` → expected `GO`
- `agent_dangerous_command.json` → expected `BLOCK`
- `agent_external_api_call.json` → expected `REPAIR`

## Usage

```bash
python i2os_gate.py examples/safe_summary.json
python i2os_gate.py examples/ai_agent_file_delete.json
python i2os_gate.py examples/prompt_injection_upload.json
python i2os_gate.py examples/api_auth_bypass.json
python i2os_gate.py examples/agent_safe_summary.json
python i2os_gate.py examples/agent_dangerous_command.json
python i2os_gate.py examples/agent_external_api_call.json
```
