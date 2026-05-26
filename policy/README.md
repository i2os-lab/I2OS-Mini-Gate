# I2OS Mini Gate Policy Profiles

v1.7 adds policy profiles.

## Profiles

| File | Profile | Purpose |
|---|---|---|
| strict_policy.json | strict | high-safety environments |
| balanced_policy.json | balanced | default practical use |
| permissive_policy.json | permissive | local sandbox experiments |

## Usage

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --policy policy/strict_policy.json
```

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --policy policy/balanced_policy.json
```

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --policy policy/permissive_policy.json
```
