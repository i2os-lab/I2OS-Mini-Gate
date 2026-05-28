# I2OS Mini Gate v2.3
## Future Constraint Layer Release

v2.3 adds an initial Future Constraint Layer.

## Added

```text
future_constraint/evaluate_future.py
future_constraint/__init__.py
docs/future_constraint_layer.md
docs/release_v2_3.md
tests/test_future_constraint.py
```

## Run

```bash
python future_constraint/evaluate_future.py demo/demo_safe_action.json
python future_constraint/evaluate_future.py demo/demo_delete_block.json policy/strict_policy.json
```

## Position

v2.3 introduces future compatibility checks as a bridge toward dynamic runtime governance.
