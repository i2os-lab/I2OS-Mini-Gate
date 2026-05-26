# I2OS Mini Gate v1.7
## Policy Profiles Release

v1.7 adds policy profiles.

## Added

```text
policy/strict_policy.json
policy/balanced_policy.json
policy/permissive_policy.json
policy/README.md
docs/policy_profiles.md
i2os_mini_gate/profiles.py
tests/test_policy_profiles.py
```

## Run

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --policy policy/strict_policy.json
```

## Position

v1.7 makes the gate adaptable for strict, balanced, and permissive environments.
