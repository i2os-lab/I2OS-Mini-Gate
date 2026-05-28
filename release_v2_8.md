# I2OS Mini Gate v2.8
## Execution Contract Layer

> Capability is not permission.  
> Permission is not unlimited execution.

v2.8 adds an initial Execution Contract Layer.

The purpose is to convert a GO/permitted transition into a bounded execution contract.

---

## Core Question

```text
The transition is permitted.
↓
What exactly is permitted?
↓
What is not permitted?
↓
When must the system recheck?
```

---

## Added

```text
execution_contract/build_execution_contract.py
execution_contract/__init__.py
execution_contract/sample_contract_go.json
execution_contract/sample_contract_block.json
docs/execution_contract_layer.md
docs/release_v2_8.md
tests/test_execution_contract.py
```

---

## Run

```bash
python execution_contract/build_execution_contract.py execution_contract/sample_contract_go.json
```

```bash
python execution_contract/build_execution_contract.py recheck_loop/sample_recheck_rushed_send.json policy/balanced_policy.json
```

---

## Output

The layer returns:

- contract status
- contract ID
- allowed scope
- prohibited actions
- recheck triggers
- human visibility requirements
- audit requirements
- expiration rules

---

## Design Position

v2.8 prevents GO from becoming unlimited execution.

The system should not only decide that a transition is permitted.

It should define the boundary of that permission.
