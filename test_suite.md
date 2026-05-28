# I2OS Mini Gate v0.6
## Policy Configuration Layer

v0.6 introduces external policy configuration.

Before v0.6, many rules were fixed inside `i2os_gate.py`.

From v0.6, key rule sets can be loaded from:

```text
policy/default_policy.json
```

## Configurable Items

- allowed permission levels
- permission ranks
- broad scopes
- dangerous keywords
- untrusted sources
- external keywords
- destructive side-effect levels
- critical reason codes
- high risk reason codes

## Usage

```bash
python i2os_gate.py examples/audit_block_prompt_injection.json --policy policy/default_policy.json
```

## Design Position

This moves I2OS Mini Gate from a hard-coded prototype toward a configurable Runtime Admissibility Scanner.
