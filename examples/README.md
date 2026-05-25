# I2OS Mini Gate Examples

This directory contains additional action examples for testing transition admissibility.

## Files

- `safe_summary.json`
  - Read-only local summarization action.
  - Expected decision: `GO`

- `ai_agent_file_delete.json`
  - AI agent proposes deleting an entire project directory.
  - Expected decision: `BLOCK`

- `prompt_injection_upload.json`
  - Untrusted document attempts to trigger an external upload.
  - Expected decision: `BLOCK`

- `api_auth_bypass.json`
  - Normal user attempts to access an admin-level export transition.
  - Expected decision: `BLOCK`

## Usage

```bash
python i2os_gate.py examples/safe_summary.json
python i2os_gate.py examples/ai_agent_file_delete.json
python i2os_gate.py examples/prompt_injection_upload.json
python i2os_gate.py examples/api_auth_bypass.json
```
