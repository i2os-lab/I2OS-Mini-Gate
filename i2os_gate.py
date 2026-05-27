
import json
import sys
from datetime import datetime
from pathlib import Path

VERSION = "v2.4-complete"
REPORT_DIR = Path("reports")
AUDIT_DIR = Path("audit_logs")
AUDIT_FILE = AUDIT_DIR / "i2os_audit_log.jsonl"

DEFAULT_POLICY = {
    "policy_name": "I2OS Mini Gate Built-in Policy",
    "policy_version": "v0.6",
    "allowed_permission_levels": ["read_only", "user", "admin"],
    "permission_levels": {"unknown": -1, "read_only": 0, "user": 1, "admin": 2},
    "broad_scopes": ["all_files", "entire_project", "system", "all_users"],
    "dangerous_keywords": ["delete", "remove", "erase", "wipe", "send", "upload", "export", "execute", "run command", "shutdown", "rm -rf"],
    "untrusted_sources": ["untrusted_document", "untrusted_input", "external_content", "web_page", "email_body", "pdf_content"],
    "external_keywords": ["upload", "send", "export", "post", "external", "api"],
    "destructive_side_effect_levels": ["destructive", "irreversible"],
    "critical_reason_codes": ["PROMPT_INJECTION_TRANSITION", "PERMISSION_ESCALATION_ATTEMPT", "DESTRUCTIVE_TOOL_SCOPE_COMBINATION", "DELETE_NOT_RECOVERABLE"],
    "high_reason_codes": ["UNTRUSTED_EXTERNAL_SIDE_EFFECT_REQUEST", "UNTRUSTED_TOOL_USE_WITH_EXTERNAL_EFFECT", "COMMAND_EXECUTION_CONFIRMATION_MISSING", "EXTERNAL_WRITE_TRANSITION", "IRREVERSIBLE_TRANSITION"]
}

def load_policy(path=None):
    if not path:
        return DEFAULT_POLICY
    with open(path, "r", encoding="utf-8") as f:
        custom = json.load(f)
    merged = DEFAULT_POLICY.copy()
    merged.update(custom)
    return merged

def add(reasons, codes, reason, code):
    reasons.append(reason)
    codes.append(code)

def uniq(items):
    out = []
    for x in items:
        if x not in out:
            out.append(x)
    return out

def rank(level, policy):
    return policy.get("permission_levels", {}).get(level, -1)

def constraints():
    return {
        "context": "PASS",
        "recovery": "PASS",
        "confirmation": "PASS",
        "scope": "PASS",
        "external_effect": "PASS",
        "permission": "PASS",
        "action_keyword": "PASS",
        "agent_action": "PASS",
        "prompt_injection": "PASS",
        "auditability": "PASS"
    }

def i2os_gate(action, policy=None):
    policy = policy or DEFAULT_POLICY
    reasons, codes, repairs = [], [], []
    cr = constraints()

    proposed = str(action.get("proposed_action", "")).lower()
    scope = action.get("scope", action.get("target_scope", "unknown"))
    target_scope = action.get("target_scope", scope)
    reversible = action.get("reversible")
    user_confirmed = action.get("user_confirmed")
    external_effect = action.get("external_effect")
    permission_level = action.get("permission_level", "unknown")
    required_permission = action.get("expected_required_permission")

    source = action.get("source_context", "trusted")
    origin = action.get("instruction_origin", "user")
    override = action.get("contains_instruction_override", False)
    req_tool = action.get("requests_tool_use", False)
    req_external = action.get("requests_external_effect", False)
    escalation = action.get("attempts_permission_escalation", False)
    trusted = action.get("trusted_by_user", True)

    action_type = action.get("action_type")
    tool = action.get("tool_name")
    side = action.get("side_effect_level")
    requires_confirmation = action.get("requires_confirmation")
    sandbox_required = action.get("sandbox_required")
    sandbox_enabled = action.get("sandbox_enabled")

    missing = [f for f in ["actor","current_state","proposed_action","permission_level","reversible","external_effect","user_confirmed"] if f not in action]
    if "scope" not in action and "target_scope" not in action:
        missing.append("scope or target_scope")
    if missing:
        add(reasons, codes, "Missing required fields: " + ", ".join(missing), "MISSING_REQUIRED_FIELDS")
        cr["context"] = "FAIL"

    if reversible is False:
        add(reasons, codes, "Irreversible transition", "IRREVERSIBLE_TRANSITION")
        cr["recovery"] = "FAIL"

    if user_confirmed is False:
        add(reasons, codes, "User confirmation missing", "USER_CONFIRMATION_MISSING")
        repairs.append("Ask explicit user confirmation")
        cr["confirmation"] = "FAIL"

    if requires_confirmation is True and user_confirmed is False:
        add(reasons, codes, "Required confirmation is missing", "REQUIRED_CONFIRMATION_MISSING")
        repairs.append("Ask explicit user confirmation before execution")
        cr["confirmation"] = "FAIL"

    if scope in policy["broad_scopes"] or target_scope in policy["broad_scopes"]:
        add(reasons, codes, "Action scope too broad", "ACTION_SCOPE_TOO_BROAD")
        repairs.append("Narrow the target scope")
        cr["scope"] = "FAIL"

    if external_effect is True:
        add(reasons, codes, "External side effect detected", "EXTERNAL_SIDE_EFFECT")
        repairs.append("Require additional confirmation before external action")
        cr["external_effect"] = "FAIL"

    if permission_level not in policy["allowed_permission_levels"]:
        add(reasons, codes, "Unknown permission level", "UNKNOWN_PERMISSION_LEVEL")
        repairs.append("Verify actor permission level")
        cr["permission"] = "FAIL"

    if required_permission and rank(permission_level, policy) < rank(required_permission, policy):
        add(reasons, codes, f"Permission transition mismatch: current={permission_level}, required={required_permission}", "PERMISSION_TRANSITION_MISMATCH")
        repairs.append("Require proper authorization before executing this transition")
        cr["permission"] = "FAIL"

    for kw in policy["dangerous_keywords"]:
        if kw in proposed:
            add(reasons, codes, f"Dangerous action keyword detected: {kw}", "DANGEROUS_ACTION_KEYWORD")
            cr["action_keyword"] = "FAIL"
            break

    if any(x in proposed for x in ["delete", "remove", "rm -rf"]) and reversible is False:
        add(reasons, codes, "Delete/remove action is not recoverable", "DELETE_NOT_RECOVERABLE")
        repairs.append("Move to trash instead of permanent deletion")
        cr["recovery"] = "FAIL"

    destructive = policy["destructive_side_effect_levels"]
    if action_type:
        if side in destructive:
            add(reasons, codes, f"High side effect level detected: {side}", "HIGH_SIDE_EFFECT_LEVEL")
            add(reasons, codes, "Destructive agent action is not recoverable", "DESTRUCTIVE_AGENT_ACTION_NOT_RECOVERABLE")
            repairs.append("Use dry-run or sandbox before destructive action")
            cr["agent_action"] = "FAIL"; cr["recovery"] = "FAIL"
        if side in destructive and user_confirmed is False:
            add(reasons, codes, "Destructive agent action lacks confirmation", "DESTRUCTIVE_ACTION_CONFIRMATION_MISSING")
            repairs.append("Require explicit confirmation for destructive agent action")
        if action_type == "command_execution" and user_confirmed is False:
            add(reasons, codes, "Command execution without confirmation", "COMMAND_EXECUTION_CONFIRMATION_MISSING")
            repairs.append("Require explicit confirmation before command execution")
            cr["agent_action"] = "FAIL"
        if sandbox_required is True and sandbox_enabled is not True:
            add(reasons, codes, "Sandbox required but not enabled", "SANDBOX_REQUIRED_NOT_ENABLED")
            repairs.append("Enable sandbox or dry-run mode before execution")
            cr["agent_action"] = "FAIL"
        if tool in ["terminal", "filesystem"] and target_scope in ["entire_project", "system"] and side in destructive:
            add(reasons, codes, "Destructive tool-scope combination detected", "DESTRUCTIVE_TOOL_SCOPE_COMBINATION")
            repairs.append("Narrow scope or use a reversible operation")
            cr["scope"] = "FAIL"
        if external_effect is True and side == "external_write":
            add(reasons, codes, "External write transition detected", "EXTERNAL_WRITE_TRANSITION")
            repairs.append("Require explicit user confirmation and destination verification")
            cr["external_effect"] = "FAIL"

    untrusted = source in policy["untrusted_sources"] or origin == "external_content" or trusted is False
    proposed_external = any(k in proposed for k in policy["external_keywords"])

    if source in policy["untrusted_sources"] and external_effect is True:
        add(reasons, codes, "Untrusted context attempted to trigger external side effect", "UNTRUSTED_EXTERNAL_EFFECT")
        repairs.append("Ignore external action instructions from untrusted context")
        cr["prompt_injection"] = "FAIL"

    if untrusted and override:
        add(reasons, codes, "Instruction override detected from untrusted context", "UNTRUSTED_INSTRUCTION_OVERRIDE")
        repairs.append("Ignore instruction override from external content")
        cr["prompt_injection"] = "FAIL"
    if untrusted and req_tool:
        add(reasons, codes, "Untrusted context requested tool use", "UNTRUSTED_TOOL_USE_REQUEST")
        repairs.append("Require user confirmation before tool use")
        cr["prompt_injection"] = "FAIL"
    if untrusted and req_external:
        add(reasons, codes, "Untrusted context requested external side effect", "UNTRUSTED_EXTERNAL_SIDE_EFFECT_REQUEST")
        repairs.append("Block external side effects from untrusted content")
        cr["prompt_injection"] = "FAIL"
    if escalation:
        add(reasons, codes, "Permission escalation attempt detected", "PERMISSION_ESCALATION_ATTEMPT")
        repairs.append("Reject permission escalation from external instruction")
        cr["permission"] = "FAIL"
    if untrusted and req_tool and (req_external or external_effect is True or proposed_external):
        add(reasons, codes, "Prompt injection transition detected", "PROMPT_INJECTION_TRANSITION")
        repairs.append("Reject tool-use transition originating from untrusted content")
        cr["prompt_injection"] = "FAIL"
    if untrusted and req_tool and external_effect is True:
        add(reasons, codes, "Untrusted context requested tool use with external effect", "UNTRUSTED_TOOL_USE_WITH_EXTERNAL_EFFECT")
        repairs.append("Separate document content from executable tool instructions")
        cr["prompt_injection"] = "FAIL"

    block_signals = {
        "Irreversible transition",
        "Delete/remove action is not recoverable",
        "Action scope too broad",
        "Untrusted context attempted to trigger external side effect",
        "Destructive agent action is not recoverable",
        "Command execution without confirmation",
        "Destructive tool-scope combination detected",
        "Instruction override detected from untrusted context",
        "Untrusted context requested external side effect",
        "Permission escalation attempt detected",
        "Prompt injection transition detected",
        "Untrusted context requested tool use with external effect"
    }
    has_block = any(r in block_signals for r in reasons) or any(r.startswith("Permission transition mismatch") for r in reasons)
    has_missing = any(r.startswith("Missing required fields") for r in reasons)

    if not reasons:
        decision = "GO"
    elif has_block:
        decision = "BLOCK"
    elif has_missing:
        decision = "HOLD"
    elif repairs:
        decision = "REPAIR"
    else:
        decision = "HOLD"

    risk = risk_level(decision, codes, policy)
    result = {
        "version": VERSION,
        "policy_name": policy.get("policy_name", "unknown"),
        "policy_version": policy.get("policy_version", "unknown"),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "decision": decision,
        "risk_level": risk,
        "summary": summary(decision),
        "audit_summary": audit_summary(decision, codes),
        "human_verifiable_explanation": explanation(decision, reasons, repairs),
        "reasons": uniq(reasons),
        "reason_codes": uniq(codes),
        "constraint_results": cr,
        "repairs": uniq(repairs),
        "input_action": action,
        "core_principle": "Capability is not permission.",
        "method": "State → Transition → Constraint Check → GO/HOLD/REPAIR/BLOCK"
    }
    append_audit_log(result)
    return result

def risk_level(decision, codes, policy):
    if any(c in set(policy["critical_reason_codes"]) for c in codes):
        return "CRITICAL"
    if decision == "BLOCK":
        return "HIGH"
    if any(c in set(policy["high_reason_codes"]) for c in codes):
        return "HIGH"
    if decision in ["REPAIR", "HOLD"]:
        return "MEDIUM"
    return "LOW"

def summary(decision):
    return {
        "GO": "This transition is allowed because no inadmissible conditions were detected.",
        "HOLD": "This transition is held because required information is missing or insufficient.",
        "REPAIR": "This transition may become admissible after the suggested repairs are applied.",
        "BLOCK": "This transition is blocked because it contains structurally inadmissible conditions."
    }.get(decision, "This transition requires further review.")

def audit_summary(decision, codes):
    return f"Decision={decision}; ReasonCodes={', '.join(uniq(codes)) if codes else 'NO_RISK_CODES'}"

def explanation(decision, reasons, repairs):
    if decision == "GO":
        return "The proposed transition was permitted because no failing admissibility constraints were detected."
    txt = f"The proposed transition was classified as {decision} because the gate detected: "
    txt += "; ".join(uniq(reasons)) if reasons else "no explicit reason."
    if repairs:
        txt += " Suggested repair path: " + "; ".join(uniq(repairs))
    return txt

def append_audit_log(result):
    AUDIT_DIR.mkdir(exist_ok=True)
    entry = {
        "timestamp": result["timestamp"],
        "version": result["version"],
        "policy_name": result["policy_name"],
        "policy_version": result["policy_version"],
        "decision": result["decision"],
        "risk_level": result["risk_level"],
        "reason_codes": result["reason_codes"],
        "audit_summary": result["audit_summary"],
        "proposed_action": result.get("input_action", {}).get("proposed_action", "")
    }
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def save_json_report(result, filename):
    REPORT_DIR.mkdir(exist_ok=True)
    path = REPORT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[I2OS] JSON report saved to: {path}")

def md_list(items):
    return "- None\n" if not items else "".join(f"- {x}\n" for x in items)

def md_dict(d):
    return "- None\n" if not d else "".join(f"- **{k}**: `{v}`\n" for k, v in d.items())

def save_markdown_report(result, filename):
    REPORT_DIR.mkdir(exist_ok=True)
    path = REPORT_DIR / filename
    md = f"""# I2OS Mini Gate Report

## Version

`{result['version']}`

## Policy

- **Policy Name**: `{result['policy_name']}`
- **Policy Version**: `{result['policy_version']}`

## Decision

**{result['decision']}**

## Risk Level

**{result['risk_level']}**

## Summary

{result['summary']}

## Audit Summary

`{result['audit_summary']}`

## Human-Verifiable Explanation

{result['human_verifiable_explanation']}

## Reason Codes

{md_list(result.get('reason_codes', []))}
## Constraint Results

{md_dict(result.get('constraint_results', {}))}
## Reasons

{md_list(result.get('reasons', []))}
## Repairs

{md_list(result.get('repairs', []))}
## Core Principle

> {result['core_principle']}

## Method

`{result['method']}`

## Timestamp

`{result['timestamp']}`
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[I2OS] Markdown report saved to: {path}")

def load_action(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def sample_actions():
    return {
        "GO_policy_safe_summary": {
            "actor": "AI agent",
            "current_state": "User asked to summarize a report",
            "proposed_action": "read and summarize ./docs/report.txt",
            "action_type": "summary",
            "tool_name": "filesystem",
            "target": "./docs/report.txt",
            "target_scope": "single_file",
            "side_effect_level": "read_only",
            "permission_level": "read_only",
            "requires_confirmation": False,
            "user_confirmed": True,
            "reversible": True,
            "sandbox_required": False,
            "external_effect": False
        },
        "REPAIR_policy_external_api": {
            "actor": "AI agent",
            "current_state": "User asked to analyze local data",
            "proposed_action": "upload local data to external API",
            "action_type": "api_call",
            "tool_name": "api_client",
            "target": "https://api.example.test/upload",
            "target_scope": "external_service",
            "side_effect_level": "external_write",
            "permission_level": "user",
            "requires_confirmation": True,
            "user_confirmed": False,
            "reversible": True,
            "sandbox_required": False,
            "external_effect": True
        },
        "BLOCK_policy_prompt_injection": {
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
            "contains_instruction_override": True,
            "requests_tool_use": True,
            "requests_external_effect": True,
            "attempts_permission_escalation": True,
            "trusted_by_user": False,
            "user_confirmed": False,
            "reversible": True,
            "external_effect": True
        }
    }

def run_samples(policy):
    print(f"=== I2OS Mini Gate {VERSION} Sample Tests ===")
    print(f"[I2OS] Policy: {policy.get('policy_name')} ({policy.get('policy_version')})\n")
    all_results = {}
    for name, action in sample_actions().items():
        print(f"--- {name} ---")
        result = i2os_gate(action, policy)
        all_results[name] = result
        print(json.dumps(result, indent=2, ensure_ascii=False))
        save_json_report(result, f"{name}.json")
        save_markdown_report(result, f"{name}.md")
        print()
    save_json_report(all_results, "i2os_sample_report.json")



def html_escape(value):
    text = str(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_status_class(value):
    if value == "PASS":
        return "pass"
    if value == "FAIL":
        return "fail"
    return "neutral"


def generate_html_report(result, title="I2OS Mini Gate Dashboard Report"):
    constraints_html = ""
    for key, value in result.get("constraint_results", {}).items():
        constraints_html += f"""
        <tr>
          <td>{html_escape(key)}</td>
          <td><span class="badge {render_status_class(value)}">{html_escape(value)}</span></td>
        </tr>
        """

    reasons_html = "".join(f"<li>{html_escape(item)}</li>" for item in result.get("reasons", [])) or "<li>None</li>"
    repairs_html = "".join(f"<li>{html_escape(item)}</li>" for item in result.get("repairs", [])) or "<li>None</li>"
    codes_html = "".join(f"<li><code>{html_escape(item)}</code></li>" for item in result.get("reason_codes", [])) or "<li>None</li>"

    decision = result.get("decision", "UNKNOWN")
    risk = result.get("risk_level", "UNKNOWN")
    decision_class = decision.lower()
    risk_class = risk.lower()

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html_escape(title)}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{
      font-family: Arial, sans-serif;
      background: #0f172a;
      color: #e5e7eb;
      margin: 0;
      padding: 32px;
    }}
    .container {{
      max-width: 980px;
      margin: 0 auto;
    }}
    .card {{
      background: #111827;
      border: 1px solid #334155;
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 20px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }}
    h1, h2 {{
      margin-top: 0;
    }}
    .subtitle {{
      color: #94a3b8;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
    }}
    .metric {{
      background: #020617;
      border: 1px solid #1e293b;
      border-radius: 12px;
      padding: 16px;
    }}
    .label {{
      color: #94a3b8;
      font-size: 13px;
      margin-bottom: 6px;
    }}
    .value {{
      font-size: 24px;
      font-weight: bold;
    }}
    .go {{ color: #22c55e; }}
    .hold {{ color: #facc15; }}
    .repair {{ color: #fb923c; }}
    .block {{ color: #ef4444; }}
    .low {{ color: #22c55e; }}
    .medium {{ color: #facc15; }}
    .high {{ color: #fb923c; }}
    .critical {{ color: #ef4444; }}
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    td, th {{
      border-bottom: 1px solid #334155;
      padding: 10px;
      text-align: left;
    }}
    .badge {{
      border-radius: 999px;
      padding: 4px 10px;
      font-weight: bold;
      font-size: 12px;
    }}
    .pass {{
      background: rgba(34,197,94,0.15);
      color: #22c55e;
    }}
    .fail {{
      background: rgba(239,68,68,0.15);
      color: #ef4444;
    }}
    .neutral {{
      background: rgba(148,163,184,0.15);
      color: #cbd5e1;
    }}
    code {{
      background: #020617;
      border: 1px solid #1e293b;
      border-radius: 6px;
      padding: 2px 6px;
    }}
    pre {{
      background: #020617;
      border: 1px solid #1e293b;
      border-radius: 12px;
      padding: 16px;
      overflow-x: auto;
    }}
    .principle {{
      font-size: 20px;
      font-weight: bold;
      color: #f8fafc;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="card">
      <h1>I2OS Mini Gate Dashboard</h1>
      <p class="subtitle">Runtime Admissibility Scanner / Human-Verifiable Report</p>
      <p class="principle">Capability is not permission.</p>
    </div>

    <div class="grid">
      <div class="metric">
        <div class="label">Decision</div>
        <div class="value {decision_class}">{html_escape(decision)}</div>
      </div>
      <div class="metric">
        <div class="label">Risk Level</div>
        <div class="value {risk_class}">{html_escape(risk)}</div>
      </div>
      <div class="metric">
        <div class="label">Version</div>
        <div class="value">{html_escape(result.get("version"))}</div>
      </div>
      <div class="metric">
        <div class="label">Policy</div>
        <div class="value" style="font-size:16px;">{html_escape(result.get("policy_name"))}</div>
      </div>
    </div>

    <div class="card">
      <h2>Summary</h2>
      <p>{html_escape(result.get("summary"))}</p>
      <h2>Human-Verifiable Explanation</h2>
      <p>{html_escape(result.get("human_verifiable_explanation"))}</p>
      <h2>Audit Summary</h2>
      <p><code>{html_escape(result.get("audit_summary"))}</code></p>
    </div>

    <div class="card">
      <h2>Constraint Results</h2>
      <table>
        <thead>
          <tr><th>Constraint</th><th>Status</th></tr>
        </thead>
        <tbody>
          {constraints_html}
        </tbody>
      </table>
    </div>

    <div class="grid">
      <div class="card">
        <h2>Reason Codes</h2>
        <ul>{codes_html}</ul>
      </div>
      <div class="card">
        <h2>Reasons</h2>
        <ul>{reasons_html}</ul>
      </div>
    </div>

    <div class="card">
      <h2>Repair Suggestions</h2>
      <ul>{repairs_html}</ul>
    </div>

    <div class="card">
      <h2>Input Action</h2>
      <pre>{html_escape(json.dumps(result.get("input_action", {}), indent=2, ensure_ascii=False))}</pre>
    </div>

    <div class="card">
      <h2>Method</h2>
      <p><code>{html_escape(result.get("method"))}</code></p>
      <p class="subtitle">Generated at {html_escape(result.get("timestamp"))}</p>
    </div>
  </div>
</body>
</html>
"""


def save_html_report(result, filename):
    dashboard_dir = Path("dashboard")
    dashboard_dir.mkdir(exist_ok=True)
    path = dashboard_dir / filename
    html = generate_html_report(result)
    with open(path, "w", encoding="utf-8") as file:
        file.write(html)
    print(f"[I2OS] HTML dashboard report saved to: {path}")


def build_error_result(error_type, message, repair=None):
    return {
        "version": VERSION,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "decision": "HOLD",
        "risk_level": "MEDIUM",
        "summary": "The scan could not be completed because input validation failed.",
        "audit_summary": f"Decision=HOLD; ErrorType={error_type}",
        "human_verifiable_explanation": message,
        "reasons": [message],
        "reason_codes": [error_type],
        "constraint_results": {
            "context": "FAIL",
            "recovery": "PASS",
            "confirmation": "PASS",
            "scope": "PASS",
            "external_effect": "PASS",
            "permission": "PASS",
            "action_keyword": "PASS",
            "agent_action": "PASS",
            "prompt_injection": "PASS",
            "auditability": "FAIL"
        },
        "repairs": [repair] if repair else [],
        "input_action": {},
        "core_principle": "Capability is not permission.",
        "method": "Input Validation → HOLD"
    }


def validate_action_schema(action):
    if not isinstance(action, dict):
        return False, "Action input must be a JSON object."

    required_any = ["actor", "current_state", "proposed_action"]
    missing = [key for key in required_any if key not in action]
    if missing:
        return False, "Action input is missing core fields: " + ", ".join(missing)

    return True, "OK"


def safe_load_json_file(filename):
    path = Path(filename)

    if not path.exists():
        return None, build_error_result(
            "INPUT_FILE_NOT_FOUND",
            f"Input file not found: {filename}",
            "Check the file path and run again."
        )

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        return None, build_error_result(
            "INVALID_JSON",
            f"Invalid JSON in file {filename}: {exc}",
            "Fix JSON syntax and run again."
        )
    except OSError as exc:
        return None, build_error_result(
            "INPUT_FILE_READ_ERROR",
            f"Could not read input file {filename}: {exc}",
            "Check file permissions and run again."
        )

    ok, message = validate_action_schema(data)
    if not ok:
        return None, build_error_result(
            "INVALID_ACTION_SCHEMA",
            message,
            "Use a valid action JSON example as a template."
        )

    return data, None


def safe_load_policy_file(policy_file):
    if not policy_file:
        return load_policy(), None

    path = Path(policy_file)
    if not path.exists():
        return None, build_error_result(
            "POLICY_FILE_NOT_FOUND",
            f"Policy file not found: {policy_file}",
            "Check the policy path or omit --policy to use the default policy."
        )

    try:
        return load_policy(policy_file), None
    except json.JSONDecodeError as exc:
        return None, build_error_result(
            "INVALID_POLICY_JSON",
            f"Invalid policy JSON in file {policy_file}: {exc}",
            "Fix policy JSON syntax and run again."
        )
    except Exception as exc:
        return None, build_error_result(
            "POLICY_LOAD_ERROR",
            f"Policy could not be loaded: {exc}",
            "Check the policy file and run again."
        )

def parse_args(argv):
    config = {
        "action_file": None,
        "policy_file": None,
        "report_prefix": None,
        "quiet": False,
        "no_reports": False,
        "json_only": False,
        "html": False,
        "show_help": False
    }

    args = list(argv[1:])
    i = 0

    while i < len(args):
        arg = args[i]

        if arg in ["-h", "--help"]:
            config["show_help"] = True
            i += 1

        elif arg in ["--policy", "-p"]:
            if i + 1 >= len(args):
                raise ValueError("--policy requires a file path")
            config["policy_file"] = args[i + 1]
            i += 2

        elif arg in ["--action", "-a"]:
            if i + 1 >= len(args):
                raise ValueError("--action requires a file path")
            config["action_file"] = args[i + 1]
            i += 2

        elif arg == "--report-prefix":
            if i + 1 >= len(args):
                raise ValueError("--report-prefix requires a value")
            config["report_prefix"] = args[i + 1]
            i += 2

        elif arg == "--quiet":
            config["quiet"] = True
            i += 1

        elif arg == "--no-reports":
            config["no_reports"] = True
            i += 1

        elif arg == "--json-only":
            config["json_only"] = True
            i += 1

        elif arg == "--html":
            config["html"] = True
            i += 1

        else:
            if config["action_file"] is None:
                config["action_file"] = arg
            else:
                raise ValueError(f"Unknown extra argument: {arg}")
            i += 1

    return config


def print_help():
    help_text = """
I2OS Mini Gate v1.0-complete
Runtime Admissibility Scanner

Core principle:
  Capability is not permission.

Usage:
  python i2os_gate.py
  python i2os_gate.py examples/audit_block_prompt_injection.json
  python i2os_gate.py --action examples/audit_block_prompt_injection.json
  python i2os_gate.py --action examples/audit_block_prompt_injection.json --policy policy/default_policy.json

Options:
  --action, -a FILE        Action JSON file to scan
  --policy, -p FILE        Policy JSON file to load
  --report-prefix NAME     Prefix for generated report files
  --quiet                  Suppress non-essential messages
  --no-reports             Do not write JSON/Markdown reports
  --json-only              Print only result JSON
  --html                   Generate HTML dashboard report
  --help, -h               Show this help

Examples:
  python i2os_gate.py --action examples/audit_go_safe_summary.json
  python i2os_gate.py --action examples/audit_block_prompt_injection.json --policy policy/default_policy.json
  python i2os_gate.py --action examples/audit_block_prompt_injection.json --report-prefix scan_prompt_injection
  python i2os_gate.py --action examples/audit_block_prompt_injection.json --json-only --no-reports
  python i2os_gate.py --action examples/audit_block_prompt_injection.json --html
"""
    print(help_text.strip())


def main():
    try:
        config = parse_args(sys.argv)
    except Exception as exc:
        result = build_error_result(
            "CLI_ARGUMENT_ERROR",
            f"CLI argument error: {exc}",
            "Check --help and run again."
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if config["show_help"]:
        print_help()
        return

    policy, policy_error = safe_load_policy_file(config["policy_file"])
    if policy_error:
        print(json.dumps(policy_error, indent=2, ensure_ascii=False))
        return

    if not config["action_file"]:
        if not config["quiet"] and not config["json_only"]:
            print("[I2OS] No JSON file specified.")
            print("[I2OS] Running built-in sample tests.\n")
        run_samples(policy)
        return

    action_file = config["action_file"]

    if not config["quiet"] and not config["json_only"]:
        print(f"[I2OS] Loading action file: {action_file}")
        print(f"[I2OS] Using policy: {policy.get('policy_name')} ({policy.get('policy_version')})\n")

    action, action_error = safe_load_json_file(action_file)
    if action_error:
        if config["json_only"]:
            print(json.dumps(action_error, indent=2, ensure_ascii=False))
        else:
            print("=== I2OS Mini Gate Error ===")
            print(json.dumps(action_error, indent=2, ensure_ascii=False))
        return

    result = i2os_gate(action, policy)

    if config["json_only"]:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("=== I2OS Mini Gate Result ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    if not config["no_reports"]:
        if config["report_prefix"]:
            base = config["report_prefix"]
        else:
            base = Path(action_file).stem + "_report"

        save_json_report(result, f"{base}.json")
        save_markdown_report(result, f"{base}.md")
        if config.get("html"):
            save_html_report(result, f"{base}.html")


if __name__ == "__main__":
    main()
