# I2OS Mini Gate v2.7
## Recheck Loop Layer

> Capability is not permission.

v2.7 adds an initial Recheck Loop Layer.

The purpose is to connect recovery paths to a second admissibility check.

---

## Core Question

```text
The transition was inadmissible.
↓
A recovery path was generated.
↓
The action was repaired.
↓
Does the repaired transition now become admissible?
```

---

## Added

```text
recheck_loop/evaluate_recheck_loop.py
recheck_loop/__init__.py
recheck_loop/sample_recheck_rushed_send.json
docs/recheck_loop_layer.md
docs/release_v2_7.md
tests/test_recheck_loop.py
```

---

## Run

```bash
python recheck_loop/evaluate_recheck_loop.py recheck_loop/sample_recheck_rushed_send.json
```

---

## Output

The layer returns:

- initial decision
- recovery path
- repaired decision
- loop status
- whether the repaired case resolved to GO

---

## Design Position

v2.7 turns recovery into a closed verification loop.

The system should not only provide a recovery path.

It should recheck whether the repaired transition is actually admissible.
