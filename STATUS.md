# I2OS Mini Gate Status

```text
Current Version: v2.0-complete
Status: Public Prototype
Category: Runtime Admissibility Scanner
```

## Stable Capabilities

- GO / HOLD / REPAIR / BLOCK classification
- AI agent action checking
- prompt injection transition detection
- external policy configuration
- audit logging
- JSON reports
- Markdown reports
- HTML dashboard reports
- CLI execution
- unit tests

## Next Possible Versions

| Version | Direction |
|---|---|
| v1.1 | Web/API Mode |
| v1.2 | GitHub Action / CI Hook |
| v1.3 | Agent Runtime Bridge |
| v1.4 | Prompt Injection Lab |
| v1.5 | Local Security Tool Prototype |
| v2.0 | Product-grade Runtime Shield |
```


## v1.1 Added

- Optional FastAPI web/API mode
- `i2os_api.py`
- `requirements-api.txt`
- `/scan` endpoint documentation


## v1.2 Added

- GitHub Action / CI Hook
- `ci/i2os_ci_scan.py`
- `.github/workflows/i2os-mini-gate.yml`


## v1.3 Added

- Agent Runtime Bridge
- Dry-run command guard
- Bridge examples
- Bridge tests


## v1.4 Added

- Prompt Injection Lab
- Repeatable prompt injection cases
- Lab runner
- Lab artifact tests


## v1.5 Added

- Local Security Tool Prototype
- File operation pre-check
- URL/network operation pre-check
- Local tool tests


## v1.6 Added

- Python package facade
- Module execution
- pyproject.toml
- optional console script `i2os-scan`


## v1.7 Added

- Strict / Balanced / Permissive policy profiles
- Policy profile documentation
- Policy profile tests


## v1.8 Added

- Local Dashboard Launcher
- JSON / Markdown / HTML one-shot report generation
- Optional browser open
- Dashboard launcher tests


## v1.9 Added

- Fail-safe input validation
- JSON error handling
- Policy loading error handling
- Structured HOLD error results


## v2.0 Added

- Runtime Shield facade
- Product positioning document
- Runtime Shield tests
- Consolidated v2.0 release documentation
