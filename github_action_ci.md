# I2OS Mini Gate v1.1
## Web/API Mode Release

v1.1 adds optional Web/API mode.

This is the first step from local CLI usage toward external integration.

## Added

```text
i2os_api.py
requirements-api.txt
docs/web_api_mode.md
```

## Run

```bash
pip install -r requirements-api.txt
uvicorn i2os_api:app --reload
```

## Main Endpoint

```text
POST /scan
```

## Position

v1.1 prepares the path toward:

```text
v1.2 GitHub Action / CI Hook
v1.3 Agent Runtime Bridge
```
