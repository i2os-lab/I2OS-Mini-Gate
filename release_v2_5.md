# I2OS Mini Gate v2.5
## Human-Admissibility Layer

> Capability is not permission.

v2.5 adds an initial Human-Admissibility Layer.

The purpose is to evaluate whether the human side is stable, explicit, and human-verifiable enough to authorize an AI/software transition.

## Core Question

```text
Can the AI do this?
↓
Should this transition be permitted?
↓
Does this chain remain admissible?
↓
Is the human side stable enough to authorize it?
```

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
python human_admissibility/evaluate_human_admissibility.py human_admissibility/sample_human_confirmed_safe_action.json
```

```bash
python human_admissibility/evaluate_human_admissibility.py human_admissibility/sample_emotional_escalation_block.json policy/strict_policy.json
```

## Signals

The initial layer checks:

- human confirmation
- emotional pressure
- urgency level
- cooldown state
- human verifiability
- explicit intent
- external pressure
- irreversibility
- external side effects

## Design Position

v2.5 expands runtime governance from AI/tool transition safety to human-AI coupled-state admissibility.

The system should not ask only whether an AI can act.

It should ask whether the human-AI state is stable enough for the action to be authorized.
