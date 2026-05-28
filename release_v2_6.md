# I2OS Mini Gate v2.6
## Recovery Path Layer

> Capability is not permission.

v2.6 adds an initial Recovery Path Layer.

The purpose is to convert HOLD / REPAIR / BLOCK decisions into human-verifiable recovery paths.

---

## Core Question

```text
The transition is not admissible.
↓
Can the system recover?
↓
What must change before rechecking?
```

---

## Added

```text
recovery_path/evaluate_recovery_path.py
recovery_path/__init__.py
recovery_path/sample_recovery_hold.json
recovery_path/sample_recovery_repair.json
recovery_path/sample_recovery_block.json
docs/recovery_path_layer.md
docs/release_v2_6.md
tests/test_recovery_path.py
```

---

## Run

```bash
python recovery_path/evaluate_recovery_path.py recovery_path/sample_recovery_block.json
```

```bash
python recovery_path/evaluate_recovery_path.py human_admissibility/sample_emotional_escalation_block.json policy/strict_policy.json
```

---

## Output

The layer returns:

- recovery mode
- recovery steps
- signals
- required conditions for recheck

---

## Design Position

v2.6 moves I2OS Mini Gate from blocking into recoverable runtime governance.

The system should not only stop inadmissible transitions.

It should show how to return to an admissible state.
