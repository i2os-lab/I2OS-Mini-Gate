# I2OS Mini Gate v2.5
## Human-Admissibility Layer Release

v2.5 adds an initial Human-Admissibility Layer.

## Added

```text
human_admissibility/evaluate_human_admissibility.py
human_admissibility/__init__.py
human_admissibility/sample_human_confirmed_safe_action.json
human_admissibility/sample_human_rushed_send.json
human_admissibility/sample_emotional_escalation_block.json
docs/human_admissibility_layer.md
docs/release_v2_5.md
tests/test_human_admissibility.py
```

## Run

```bash
python human_admissibility/evaluate_human_admissibility.py human_admissibility/sample_human_rushed_send.json
```

## Position

v2.5 begins human-AI coupled-state admissibility checking.
