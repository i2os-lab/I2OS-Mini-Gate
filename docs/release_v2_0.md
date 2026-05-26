# I2OS Mini Gate v2.0
## Product-grade Runtime Shield Prototype Release

v2.0 consolidates the v1.x line into the first Runtime Shield Prototype.

## Added

```text
runtime_shield/shield.py
runtime_shield/__init__.py
i2os_mini_gate/shield.py
docs/runtime_shield_v2.md
docs/release_v2_0.md
tests/test_runtime_shield.py
```

## Run

```bash
python runtime_shield/shield.py examples/audit_block_prompt_injection.json policy/strict_policy.json
```

## Position

v2.0 is the first coherent public Runtime Shield prototype.

It is suitable for:

- GitHub demonstration
- local dry-run security checks
- AI agent runtime governance research
- prompt injection transition testing
- future product-grade development
