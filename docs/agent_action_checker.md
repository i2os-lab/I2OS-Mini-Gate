# I2OS Mini Gate v0.3 Design
## AI Agent Action Checker

## Core Principle

> Capability is not permission.

I2OS Mini Gate v0.3 extends the current Runtime Admissibility Gate toward AI agent action checking.

The purpose is not only to classify generic actions, but to inspect proposed AI agent tool-use transitions before execution.

---

## Purpose

AI agents may propose actions such as:

- reading files
- deleting files
- executing commands
- calling APIs
- uploading data
- sending messages
- modifying repositories
- writing or overwriting files

In I2OS, each proposed action is treated as a state transition.

```text
S_t → T_agent → S_{t+1}
```

The transition is permitted only when it satisfies admissibility constraints.

```text
Permit(T_agent) = 1 [ C(S_t, T_agent, S_{t+1}) = 1 ]
```

---

## v0.3 Target

v0.3 introduces explicit AI agent action fields.

```json
{
  "actor": "AI agent",
  "current_state": "User asked to clean old files",
  "proposed_action": "delete files in ./old_project",
  "action_type": "file_operation",
  "tool_name": "filesystem",
  "target": "./old_project",
  "target_scope": "entire_project",
  "side_effect_level": "destructive",
  "permission_level": "user",
  "requires_confirmation": true,
  "user_confirmed": false,
  "reversible": false,
  "sandbox_required": true,
  "external_effect": false
}
```

---

## New Fields

### action_type

Classifies the type of proposed action.

```text
file_operation
command_execution
api_call
network_request
message_send
repository_write
data_export
summary
```

### tool_name

Identifies the tool the agent intends to use.

```text
filesystem
terminal
browser
email
github
api_client
database
```

### side_effect_level

Classifies the possible side effect of the action.

```text
none
read_only
local_write
external_write
destructive
irreversible
```

### target_scope

Clarifies the affected range.

```text
single_file
selected_files
directory
entire_project
system
all_users
external_service
```

### requires_confirmation

Indicates whether explicit user confirmation is required before execution.

### sandbox_required

Indicates whether the action should be executed only in a sandbox or dry-run environment.

---

## Decision Logic Extension

### GO

Allowed when:

- action is read-only or low-risk
- all required fields are present
- no external side effect exists
- no destructive effect exists
- permission is sufficient
- confirmation is present if required

### HOLD

Used when:

- action_type is missing
- tool_name is missing
- target_scope is unclear
- side_effect_level is unknown
- permission requirement is ambiguous

### REPAIR

Used when:

- confirmation is required but missing
- sandbox is required but not specified
- action can become safe after scope narrowing
- external side effect requires additional confirmation

### BLOCK

Used when:

- destructive action is irreversible
- command execution is proposed without confirmation
- untrusted context attempts tool use
- permission mismatch exists
- target_scope is entire_project/system/all_users with destructive effect
- external write occurs from untrusted context

---

## New Rule Categories

### C_tool

Checks whether the selected tool is appropriate for the requested action.

### C_side_effect

Checks whether the action creates local, external, destructive, or irreversible effects.

### C_confirmation_required

Checks whether explicit confirmation is required and present.

### C_sandbox

Checks whether high-risk actions require dry-run or sandbox execution.

### C_tool_scope

Checks whether the selected tool and target scope are compatible.

---

## v0.3 Implementation Plan

### Step 1

Add the new fields to examples.

### Step 2

Add rule checks for:

- action_type
- tool_name
- side_effect_level
- target_scope
- requires_confirmation
- sandbox_required
- sandbox_enabled

### Step 3

Update Markdown reports to show agent-specific fields.

### Step 4

Add examples for:

- safe read-only summary
- dangerous command execution
- external API call
- repository write
- email send

### Step 5

Prepare v0.3 release as:

```text
I2OS Mini Gate v0.3
AI Agent Action Checker
```

---

## Design Position

v0.3 moves I2OS Mini Gate from a generic action classifier toward a practical AI Agent Runtime Governance prototype.

The central question becomes:

```text
Should this AI agent transition be permitted before execution?
```

This is the operational form of:

> Capability is not permission.
