{
  "case_name": "safe_local_draft_contract",
  "final_decision": "GO",
  "final_permitted": true,
  "action": {
    "actor": "AI agent",
    "current_state": "User confirmed local draft creation",
    "proposed_action": "create local markdown draft for human review",
    "action_type": "file_operation",
    "tool_name": "filesystem",
    "target": "./drafts/message_preview.md",
    "target_scope": "single_file",
    "side_effect_level": "local_write",
    "permission_level": "user",
    "requires_confirmation": true,
    "user_confirmed": true,
    "reversible": true,
    "sandbox_required": false,
    "external_effect": false
  },
  "human_admissibility": {
    "human_admissibility_level": "LOW",
    "human_decision": "GO",
    "human_admissible": true,
    "human_signals": []
  },
  "transition_result": {
    "future_constraint": {
      "future_constraint_level": "LOW",
      "future_compatible": true,
      "future_signals": []
    }
  }
}