# I2OS Mini Gate v2.9
## Contract Enforcement Layer Release

v2.9 adds an initial Contract Enforcement Layer.

## Added

```text
contract_enforcement/enforce_contract.py
contract_enforcement/__init__.py
contract_enforcement/sample_contract.json
contract_enforcement/sample_attempt_allowed.json
contract_enforcement/sample_attempt_violation.json
docs/contract_enforcement_layer.md
docs/release_v2_9.md
tests/test_contract_enforcement.py
```

## Run

```bash
python contract_enforcement/enforce_contract.py contract_enforcement/sample_contract.json contract_enforcement/sample_attempt_allowed.json
```

## Position

v2.9 checks whether attempted execution remains inside the issued contract.
