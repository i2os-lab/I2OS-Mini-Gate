# I2OS Mini Gate v2.2
## Runtime Observation Layer Release

v2.2 adds an initial Runtime Observation Layer.

## Added

```text
runtime_observer/observe_sequence.py
runtime_observer/__init__.py
docs/runtime_observation_layer.md
docs/release_v2_2.md
tests/test_runtime_observer.py
```

## Run

```bash
python runtime_observer/observe_sequence.py demo/demo_safe_action.json demo/demo_prompt_injection_block.json demo/demo_delete_block.json
```

## Position

v2.2 is the first step from pre-execution checking toward runtime decision observation.
