# I2OS Mini Gate v3.0
## Closed-Loop Runtime Governance Core

> Capability is not permission.  
> Permission is bounded by contract.  
> Recovery must be rechecked.

v3.0 integrates the v2.x layers into a closed-loop runtime governance core.

---

## Integrated Layers

```text
Human-Admissibility
↓
Recovery Path
↓
Recheck Loop
↓
Execution Contract
↓
Contract Enforcement
```

---

## Core Question

```text
Can the AI do this?
↓
Should this transition be permitted?
↓
Can the system recover if not?
↓
Was the recovery actually rechecked?
↓
Is the permitted execution bounded by contract?
↓
Does the actual execution remain inside that contract?
```

---

## Added

```text
governance_core/run_governance_core.py
governance_core/__init__.py
governance_core/sample_governance_package.json
governance_core/sample_governance_violation_package.json
docs/closed_loop_governance_core.md
docs/release_v3_0.md
tests/test_governance_core.py
```

---

## Run

```bash
python governance_core/run_governance_core.py governance_core/sample_governance_package.json
```

```bash
python governance_core/run_governance_core.py governance_core/sample_governance_violation_package.json
```

---

## Output

The core returns:

- final status
- initial decision
- recovery mode
- recheck status
- contract status
- enforcement decision
- complete nested governance trace

---

## Design Position

v3.0 is the first closed-loop runtime governance prototype.

It does not merely classify proposed actions.

It governs the transition lifecycle:

```text
propose
check
recover
recheck
contract
enforce
audit
```
