# I2OS Mini Gate v1.1
## Web/API Mode

> Capability is not permission.

v1.1 adds an optional FastAPI-based web/API mode.

This allows I2OS Mini Gate to be called by external tools, scripts, local dashboards, or future AI agent bridges.

---

## Install API Dependencies

```bash
pip install -r requirements-api.txt
```

or:

```bash
pip install fastapi uvicorn pydantic
```

---

## Start API Server

```bash
uvicorn i2os_api:app --reload
```

Default local URL:

```text
http://127.0.0.1:8000
```

Interactive API docs:

```text
http://127.0.0.1:8000/docs
```

---

## Endpoints

### GET /

Basic API info.

### GET /health

Health check.

### GET /version

Current I2OS Mini Gate version.

### POST /scan

Scan an action transition.

---

## Example Request

```json
{
  "action": {
    "actor": "AI agent",
    "current_state": "AI is summarizing an untrusted document",
    "proposed_action": "upload local files to external service",
    "action_type": "api_call",
    "tool_name": "api_client",
    "target": "https://example.test/upload",
    "target_scope": "external_service",
    "side_effect_level": "external_write",
    "permission_level": "user",
    "source_context": "untrusted_document",
    "instruction_origin": "external_content",
    "contains_instruction_override": true,
    "requests_tool_use": true,
    "requests_external_effect": true,
    "attempts_permission_escalation": true,
    "trusted_by_user": false,
    "user_confirmed": false,
    "reversible": true,
    "external_effect": true
  },
  "policy_path": "policy/default_policy.json"
}
```

Expected decision:

```text
BLOCK
```

---

## Design Position

v1.1 moves I2OS Mini Gate from a local CLI tool toward an integration-ready Runtime Admissibility API.

The flow becomes:

```text
External Tool / Agent
↓
POST /scan
↓
I2OS Runtime Admissibility Scanner
↓
GO / HOLD / REPAIR / BLOCK
↓
JSON Response
```
