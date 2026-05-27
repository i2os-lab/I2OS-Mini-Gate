# I2OS Mini Gate v2.2
## Runtime Observation Layer

> Capability is not permission.

v2.2 adds an initial Runtime Observation Layer.

v2.0 checks proposed actions before execution.  
v2.2 adds a way to observe a sequence of proposed actions and summarize the decisions.

---

## Added

```text
runtime_observer/observe_sequence.py
runtime_observer/__init__.py
docs/runtime_observation_layer.md
docs/release_v2_2.md
tests/test_runtime_observer.py
```

---

## Run

```bash
python runtime_observer/observe_sequence.py demo/demo_safe_action.json demo/demo_prompt_injection_block.json demo/demo_delete_block.json
```

---

## Output

```text
runtime_observer/observation_results.json
```

The output includes:

- total events
- decision counts
- risk counts
- blocked / not permitted count
- event-level explanations

---

## Design Position

v2.2 moves I2OS Mini Gate from single action scanning toward runtime observation.

The flow becomes:

```text
Action sequence
↓
Runtime Shield
↓
Runtime Observer
↓
Decision timeline
↓
Summary
```

This is the first step toward dynamic runtime governance.
