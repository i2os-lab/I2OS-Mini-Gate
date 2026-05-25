import json
import sys
from datetime import datetime
from pathlib import Path


VERSION = "v0.4-complete"
REPORT_DIR = Path("reports")


def i2os_gate(action):
    """
    I2OS Mini Gate v0.4-complete

    Purpose:
    Classify a proposed AI/software action before execution.

    Output:
    - GO      : admissible transition
    - HOLD    : insufficient information
    - REPAIR  : admissible after correction
    - BLOCK   : inadmissible transition
    """

    reasons = []
    repairs = []

    proposed_action = str(action.get("proposed_action", "")).lower()
    scope = action.get("scope", action.get("target_scope", "unknown"))
    target_scope = action.get("target_scope", scope)
    reversible = action.get("reversible", None)
    user_confirmed = action.get("user_confirmed", None)
    external_effect = action.get("external_effect", None)
    permission_level = action.get("permission_level", "unknown")
    expected_required_permission = action.get("expected_required_permission", None)

    # Important:
    # These variables are defined here before use to avoid NameError.
    source_context = action.get("source_context", "trusted")
    instruction_origin = action.get("instruction_origin", "user")
    contains_instruction_override = action.get("contains_instruction_override", False)
    requests_tool_use = action.get("requests_tool_use", False)
    requests_external_effect = action.get("requests_external_effect", False)
    attempts_permission_escalation = action.get("attempts_permission_escalation", False)
    trusted_by_user = action.get("trusted_by_user", True)

    action_type = action.get("action_type", None)
    tool_name = action.get("tool_name", None)
    side_effect_level = action.get("side_effect_level", None)
    requires_confirmation = action.get("requires_confirmation", None)
    sandbox_required = action.get("sandbox_required", None)
    sandbox_enabled = action.get("sandbox_enabled", None)

    required_fields = [
        "actor",
        "current_state",
        "proposed_action",
        "permission_level",
        "reversible",
        "external_effect",
        "user_confirmed"
    ]

    missing_fields = []
    for field in required_fields:
        if field not in action:
            missing_fields.append(field)

    if "scope" not in action and "target_scope" not in action:
        missing_fields.append("scope or target_scope")

    if missing_fields:
        reasons.append(f"Missing required fields: {', '.join(missing_fields)}")

    # Recovery constraint
    if reversible is False:
        reasons.append("Irreversible transition")

    # Confirmation constraint
    if user_confirmed is False:
        reasons.append("User confirmation missing")
        repairs.append("Ask explicit user confirmation")

    if requires_confirmation is True and user_confirmed is False:
        reasons.append("Required confirmation is missing")
        repairs.append("Ask explicit user confirmation before execution")

    # Scope constraint
    broad_scopes = ["all_files", "entire_project", "system", "all_users"]

    if scope in broad_scopes or target_scope in broad_scopes:
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
        "shutdown",
        "rm -rf"
    ]

    for keyword in dangerous_keywords:
        if keyword in proposed_action:
            reasons.append(f"Dangerous action keyword detected: {keyword}")
            break

    # Delete/remove-specific recovery check
    if "delete" in proposed_action or "remove" in proposed_action or "rm -rf" in proposed_action:
        if reversible is False:
            reasons.append("Delete/remove action is not recoverable")
            repairs.append("Move to trash instead of permanent deletion")

    # Untrusted context external action constraint
    if source_context in ["untrusted_document", "untrusted_input", "external_content", "web_page", "email_body", "pdf_content"]:
        if external_effect is True:
            reasons.append("Untrusted context attempted to trigger external side effect")
            repairs.append("Ignore external action instructions from untrusted context")

    # v0.3 Agent action checks
    if action_type:
        check_agent_action(
            reasons=reasons,
            repairs=repairs,
            action_type=action_type,
            tool_name=tool_name,
            side_effect_level=side_effect_level,
            target_scope=target_scope,
            sandbox_required=sandbox_required,
            sandbox_enabled=sandbox_enabled,
            user_confirmed=user_confirmed,
            external_effect=external_effect,
        )

    # v0.4 Prompt injection transition checks
    check_prompt_injection_transition(
        action=action,
        reasons=reasons,
        repairs=repairs,
        source_context=source_context,
        instruction_origin=instruction_origin,
        contains_instruction_override=contains_instruction_override,
        requests_tool_use=requests_tool_use,
        requests_external_effect=requests_external_effect,
        attempts_permission_escalation=attempts_permission_escalation,
        trusted_by_user=trusted_by_user,
        external_effect=external_effect,
        proposed_action=proposed_action,
    )

    block_prefixes = [
        "Permission transition mismatch",
    ]

    block_signals = [
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
        "Untrusted context requested tool use with external effect",
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
        "reasons": deduplicate(reasons),
        "repairs": deduplicate(repairs),
        "input_action": action,
        "core_principle": "Capability is not permission.",
        "method": "State → Transition → Constraint Check → GO/HOLD/REPAIR/BLOCK"
    }


def check_agent_action(
    reasons,
    repairs,
    action_type,
    tool_name,
    side_effect_level,
    target_scope,
    sandbox_required,
    sandbox_enabled,
    user_confirmed,
    external_effect,
):
    destructive_levels = ["destructive", "irreversible"]

    if side_effect_level in destructive_levels:
        reasons.append(f"High side effect level detected: {side_effect_level}")

    if side_effect_level in destructive_levels and user_confirmed is False:
        reasons.append("Destructive agent action lacks confirmation")
        repairs.append("Require explicit confirmation for destructive agent action")

    if side_effect_level in destructive_levels:
        reasons.append("Destructive agent action is not recoverable")
        repairs.append("Use dry-run or sandbox before destructive action")

    if action_type == "command_execution" and user_confirmed is False:
        reasons.append("Command execution without confirmation")
        repairs.append("Require explicit confirmation before command execution")

    if sandbox_required is True and sandbox_enabled is not True:
        reasons.append("Sandbox required but not enabled")
        repairs.append("Enable sandbox or dry-run mode before execution")

    if tool_name in ["terminal", "filesystem"] and target_scope in ["entire_project", "system"]:
        if side_effect_level in destructive_levels:
            reasons.append("Destructive tool-scope combination detected")
            repairs.append("Narrow scope or use a reversible operation")

    if external_effect is True and side_effect_level == "external_write":
        reasons.append("External write transition detected")
        repairs.append("Require explicit user confirmation and destination verification")


def check_prompt_injection_transition(
    action,
    reasons,
    repairs,
    source_context,
    instruction_origin,
    contains_instruction_override,
    requests_tool_use,
    requests_external_effect,
    attempts_permission_escalation,
    trusted_by_user,
    external_effect,
    proposed_action,
):
    untrusted_sources = [
        "untrusted_document",
        "untrusted_input",
        "external_content",
        "web_page",
        "email_body",
        "pdf_content"
    ]

    untrusted = (
        source_context in untrusted_sources
        or instruction_origin == "external_content"
        or trusted_by_user is False
    )

    external_keywords = ["upload", "send", "export", "post", "external", "api"]

    proposed_external = any(keyword in proposed_action for keyword in external_keywords)

    if untrusted and contains_instruction_override:
        reasons.append("Instruction override detected from untrusted context")
        repairs.append("Ignore instruction override from external content")

    if untrusted and requests_tool_use:
        reasons.append("Untrusted context requested tool use")
        repairs.append("Require user confirmation before tool use")

    if untrusted and requests_external_effect:
        reasons.append("Untrusted context requested external side effect")
        repairs.append("Block external side effects from untrusted content")

    if attempts_permission_escalation:
        reasons.append("Permission escalation attempt detected")
        repairs.append("Reject permission escalation from external instruction")

    if untrusted and requests_tool_use and (requests_external_effect or external_effect is True or proposed_external):
        reasons.append("Prompt injection transition detected")
        repairs.append("Reject tool-use transition originating from untrusted content")

    if untrusted and requests_tool_use and external_effect is True:
        reasons.append("Untrusted context requested tool use with external effect")
        repairs.append("Separate document content from executable tool instructions")


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
        "REPAIR_sample_external_api_call": {
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
        "BLOCK_sample_prompt_injection": {
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
        print("[I2OS] Running built-in sample tests.\n")
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
