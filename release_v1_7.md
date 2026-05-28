# I2OS Mini Gate v1.7
## Policy Profiles

> Capability is not permission.

v1.7 adds policy profiles.

The purpose is to switch runtime strictness depending on the operating environment.

---

## Profiles

```text
policy/strict_policy.json
policy/balanced_policy.json
policy/permissive_policy.json
```

---

## Strict Policy

For high-safety environments.

Characteristics:

- more broad scopes are blocked
- more keywords are treated as dangerous
- more untrusted sources are recognized
- more reason codes are escalated to critical

Example:

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --policy policy/strict_policy.json
```

---

## Balanced Policy

Default practical profile.

Example:

```bash
python i2os_gate.py --action examples/audit_block_prompt_injection.json --policy policy/balanced_policy.json
```

---

## Permissive Policy

For low-risk local sandbox experiments.

Example:

```bash
python i2os_gate.py --action examples/audit_go_safe_summary.json --policy policy/permissive_policy.json
```

---

## Design Position

v1.7 makes I2OS Mini Gate adaptable.

The same action can be evaluated under different operating assumptions:

```text
strict
balanced
permissive
```

This moves the project closer to real-world deployment, where different environments require different safety levels.
