# I2OS Mini Gate v2.8
## Execution Contract Layer Release

v2.8 adds an initial Execution Contract Layer.

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

## Run

```bash
python execution_contract/build_execution_contract.py execution_contract/sample_contract_go.json
```

## Position

v2.8 turns GO into a bounded, auditable execution contract.
