import json
import sys
from datetime import datetime
from pathlib import Path


VERSION = "v0.2-complete"
REPORT_DIR = Path("reports")


def i2os_gate(action):
    """
    I2OS Mini Gate v0.2-complete

    Purpose:
    Classify a proposed action before execution.

    Output:
    - GO      : admissible transition
    - HOLD    : insufficient information
    - REPAIR  : admissible after correction
    - BLOCK   : inadmissible transition
    """

    reasons = []
    repairs = []

    proposed_action = action.get("proposed_action", "").lower()
    scope = action.get("scope", "unknown")
    reversible = action.get("reversible", None)
    user_confirmed = action.get("user_confirmed", None)
    external_effect = action.get("external_effect", None)
    permission_level = action.get("permission_level", "unknown")
    expected_required_permission = action.get("expected_required_permission", None)
    source_context = action.get("source_context", "trusted")

    required_fields = [
        "actor",
        "current_state",
        "proposed_action",
        "scope",
        "permission_level",
        "reversible",
        "external_effect",
        "user_confirmed"
    ]

    missing_fields = []
    for field in required_fields:
        if field not in action:
            missing_fields.append(field)

    if missing_fields:
        reasons.append(f"Missing required fields: {', '.join(missing_fields)}")

    # Recovery constraint
    if reversible is False:
        reasons.append("Irreversible transition")

    # Confirmation constraint
    if user_confirmed is False:
        reasons.append("User confirmation missing")
        repairs.append("Ask explicit user confirmation")

    # Scope constraint
    broad_scopes = ["all_files", "entire_project", "system", "all_users"]

    if scope in broad_scopes:
        reasons.append("Action scope too broad")
        repairs.append("Narrow the target scope")

    # External effect constraint
    if external_effect is True:
        reasons.append("External side effect detected")
        repairs.append("Require additional confirmation before external action")

    # Permission constraint
    allowed_permissions = ["read_only", "user", "admin"]

    if permission_level not in allowed_permissions:
        reasons.append("Unknown permission level")
        repairs.append("Verify actor permission level")

    # Permission mismatch constraint
    if expected_required_permission:
        if permission_rank(permission_level) < permission_rank(expected_required_permission):
            reasons.append(
                f"Permission transition mismatch: current={permission_level}, required={expected_required_permission}"
            )
            repairs.append("Require proper authorization before executing this transition")

    # Dangerous action keyword constraint
    dangerous_keywords = [
        "delete",
        "remove",
        "erase",
        "wipe",
        "send",
        "upload",
        "export",
        "execute",
        "run command",
        "shutdown"
    ]

    for keyword in dangerous_keywords:
        if keyword in proposed_action:
            reasons.append(f"Dangerous action keyword detected: {keyword}")
            break

    # Delete/remove-specific recovery check
    if "delete" in proposed_action or "remove" in proposed_action:
        if reversible is False:
            reasons.append("Delete/remove action is not recoverable")
            repairs.append("Move to trash instead of permanent deletion")

    # Untrusted context external action constraint
    if source_context in ["untrusted_document", "untrusted_input", "external_content"]:
        if external_effect is True:
            reasons.append("Untrusted context attempted to trigger external side effect")
            repairs.append("Ignore external action instructions from untrusted context")

    block_prefixes = [
        "Permission transition mismatch",
    ]

    block_signals = [
        "Irreversible transition",
        "Delete/remove action is not recoverable",
        "Action scope too broad",
        "Untrusted context attempted to trigger external side effect"
    ]

    has_block_signal = any(reason in block_signals for reason in reasons)
    has_block_prefix = any(any(reason.startswith(prefix) for prefix in block_prefixes) for reason in reasons)
    has_missing_info = any(reason.startswith("Missing required fields") for reason in reasons)
    has_repair_path = len(repairs) > 0

    if not reasons:
        decision = "GO"
    elif has_block_signal or has_block_prefix:
        decision = "BLOCK"
    elif has_missing_info:
        decision = "HOLD"
    elif has_repair_path:
        decision = "REPAIR"
    else:
        decision = "HOLD"

    summary = generate_summary(decision)

    return {
        "version": VERSION,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "decision": decision,
        "summary": summary,
        "reasons": reasons,
        "repairs": deduplicate(repairs),
        "input_action": action,
        "core_principle": "Capability is not permission.",
        "method": "State → Transition → Constraint Check → GO/HOLD/REPAIR/BLOCK"
    }


def permission_rank(level):
    ranks = {
        "unknown": -1,
        "read_only": 0,
        "user": 1,
        "admin": 2
    }
    return ranks.get(level, -1)


def deduplicate(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def generate_summary(decision):
    if decision == "GO":
        return "This transition is allowed because no inadmissible conditions were detected."
    if decision == "HOLD":
        return "This transition is held because required information is missing or insufficient."
    if decision == "REPAIR":
        return "This transition may become admissible after the suggested repairs are applied."
    if decision == "BLOCK":
        return "This transition is blocked because it contains structurally inadmissible conditions."
    return "This transition requires further review."


def save_json_report(result, filename):
    REPORT_DIR.mkdir(exist_ok=True)
    path = REPORT_DIR / filename
    with open(path, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)
    print(f"[I2OS] JSON report saved to: {path}")


def format_list(items):
    if not items:
        return "- None\n"
    return "".join(f"- {item}\n" for item in items)


def action_to_markdown(action):
    return "".join(f"- **{key}**: `{value}`\n" for key, value in action.items())


def generate_markdown_report(result, title="I2OS Mini Gate Report"):
    markdown = f"# {title}\n\n"
    markdown += "## Version\n\n"
    markdown += f"`{result['version']}`\n\n"
    markdown += "## Decision\n\n"
    markdown += f"**{result['decision']}**\n\n"
    markdown += "## Summary\n\n"
    markdown += f"{result['summary']}\n\n"
    markdown += "## Reasons\n\n"
    markdown += format_list(result.get("reasons", [])) + "\n"
    markdown += "## Repairs\n\n"
    markdown += format_list(result.get("repairs", [])) + "\n"
    markdown += "## Input Action\n\n"
    markdown += action_to_markdown(result.get("input_action", {})) + "\n"
    markdown += "## Core Principle\n\n"
    markdown += f"> {result['core_principle']}\n\n"
    markdown += "## Method\n\n"
    markdown += f"`{result['method']}`\n\n"
    markdown += "## Timestamp\n\n"
    markdown += f"`{result['timestamp']}`\n"
    return markdown


def save_markdown_report(result, filename):
    REPORT_DIR.mkdir(exist_ok=True)
    path = REPORT_DIR / filename
    markdown = generate_markdown_report(result)
    with open(path, "w", encoding="utf-8") as file:
        file.write(markdown)
    print(f"[I2OS] Markdown report saved to: {path}")


def run_sample_tests():
    samples = {
        "GO_sample_safe_summary": {
            "actor": "AI agent",
            "current_state": "User asked to summarize a local document",
            "proposed_action": "summarize the document",
            "target": "./docs/report.txt",
            "scope": "single_file",
            "permission_level": "read_only",
            "reversible": True,
            "external_effect": False,
            "user_confirmed": True
        },
        "HOLD_sample_missing_info": {
            "actor": "AI agent",
            "current_state": "User asked to process files",
            "proposed_action": "modify selected files"
        },
        "REPAIR_sample_external_upload": {
            "actor": "AI agent",
            "current_state": "User asked to share a report",
            "proposed_action": "upload report to external service",
            "target": "./docs/report.txt",
            "scope": "single_file",
            "permission_level": "user",
            "reversible": True,
            "external_effect": True,
            "user_confirmed": False
        },
        "BLOCK_sample_delete_all_files": {
            "actor": "AI agent",
            "current_state": "User asked to organize files",
            "proposed_action": "delete all files in ./downloads",
            "target": "./downloads",
            "scope": "all_files",
            "permission_level": "user",
            "reversible": False,
            "external_effect": False,
            "user_confirmed": False
        }
    }

    print(f"=== I2OS Mini Gate {VERSION} Sample Tests ===\n")
    all_results = {}

    for name, action in samples.items():
        print(f"--- {name} ---")
        result = i2os_gate(action)
        all_results[name] = result
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print()
        save_markdown_report(result, f"{name}.md")

    save_json_report(all_results, "i2os_sample_report.json")
    print("[I2OS] All sample tests completed.")


def load_action_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def safe_report_name(filename):
    stem = Path(filename).stem
    return f"{stem}_report"


def main():
    if len(sys.argv) < 2:
        print("[I2OS] No JSON file specified.")
        print("[I2OS] Running built-in 4 sample tests.\n")
        run_sample_tests()
    else:
        filename = sys.argv[1]
        print(f"[I2OS] Loading action file: {filename}\n")
        action = load_action_from_file(filename)
        result = i2os_gate(action)

        print("=== I2OS Mini Gate Result ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        base = safe_report_name(filename)
        save_json_report(result, f"{base}.json")
        save_markdown_report(result, f"{base}.md")


if __name__ == "__main__":
    main()
