# I2OS Mini Gate v2.7
## Recheck Loop Layer Release

v2.7 adds an initial Recheck Loop Layer.

## Added

```text
recheck_loop/evaluate_recheck_loop.py
recheck_loop/__init__.py
recheck_loop/sample_recheck_rushed_send.json
docs/recheck_loop_layer.md
docs/release_v2_7.md
tests/test_recheck_loop.py
```

## Run

```bash
python recheck_loop/evaluate_recheck_loop.py recheck_loop/sample_recheck_rushed_send.json
```

## Position

v2.7 connects recovery path generation to re-evaluation.
