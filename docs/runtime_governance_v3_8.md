# I2OS Mini Gate v3.8
## Runtime Governance Refinement

## Release Type

Refinement / Documentation / Runtime Governance Clarification

## Status

Planned / In Progress

## Core Principle

```text
Capability is not permission.

An AI or software system may be capable of performing an action, but capability alone does not mean that the action should be permitted.

1. Purpose

I2OS Mini Gate v3.8 refines the runtime governance layer introduced in the previous releases.

The purpose of this phase is to make the project easier to understand, verify, and extend as a public runtime transition governance prototype.

I2OS Mini Gate is not only an output filter.

It is a pre-execution transition gate for AI or software actions.

2. Public Definition

I2OS Mini Gate is a minimal runtime admissibility gate that checks proposed AI or software actions as state transitions before execution.

It classifies proposed transitions as:

GO / HOLD / REPAIR / BLOCK

The core question is not:

Can the AI do this?

The core question is:

Should this transition be permitted before execution?
3. Runtime Governance Model

The v3.8 runtime governance model is based on the following flow:

Proposed Action
↓
State Extraction
↓
Admissibility Check
↓
Recovery / Confirmation Check
↓
Runtime Classification
↓
Human-Verifiable Explanation
↓
Audit / Report Output

The goal is to prevent inadmissible transitions before they become real-world actions.

4. Classification
GO

The proposed transition is permitted.

Typical conditions:

context is valid
action is recoverable
no dangerous external side effect
no prompt injection pattern detected
human confirmation is not required or already satisfied

Example:

Action:
Read a local document and summarize it.

Result:
GO
HOLD

The proposed transition is not immediately rejected, but it requires additional context, confirmation, or clarification.

Typical conditions:

missing user confirmation
ambiguous action target
unclear scope
incomplete context
potentially sensitive operation

Example:

Action:
Send an email to a client.

Result:
HOLD

Reason:
Recipient and final content require confirmation.
REPAIR

The proposed transition is not currently admissible, but it may become admissible if corrected.

Typical conditions:

unsafe parameters
excessive scope
missing constraints
recoverability problem
action should be reframed into a safer form

Example:

Action:
Delete all temporary files.

Result:
REPAIR

Suggested repair:
Limit deletion to a specific confirmed folder and create a backup first.
BLOCK

The proposed transition is rejected.

Typical conditions:

irreversible destructive action
prompt injection attempt
unsafe external effect
credential exposure
unauthorized access
unrecoverable state change

Example:

Action:
Delete the entire project directory.

Result:
BLOCK

Reason:
Irrecoverable destructive transition.
5. Core Equation

The conceptual kernel is:

Permit(T) = 1 [ C(S_t, T, S_{t+1}) = 1 ]

Where:

S_t = current state
T = proposed transition
S_{t+1} = next state after transition
C = admissibility constraint

A transition is permitted only when the transition from the current state to the next state satisfies the admissibility constraint.

6. Admissibility Constraints

The admissibility constraint may include:

C =
C_context
∧ C_safety
∧ C_recovery
∧ C_sync
∧ C_future
C_context

Checks whether the action makes sense in the current context.

C_safety

Checks whether the action avoids unsafe or harmful effects.

C_recovery

Checks whether the system can recover if the action fails.

C_sync

Checks whether the action remains synchronized with the user intent, environment, and task scope.

C_future

Checks whether the transition may create future instability or unrecoverable consequences.

7. Why Transition Governance Matters

Traditional AI safety often focuses on output filtering.

Output filtering asks:

Is this output acceptable?

Runtime transition governance asks:

Should this action become real?

This distinction is important because some unsafe actions are not merely text outputs.

They may involve:

file operations
tool calls
shell commands
external API calls
memory writes
email sending
code execution
agent-to-agent delegation

For such systems, safety must occur before execution.

8. Difference from Output Filtering
Output Filtering	Runtime Governance
Checks generated text	Checks proposed transitions
Happens after generation	Happens before execution
Focuses on harmful content	Focuses on inadmissible state change
Often rule-based	Constraint and recovery aware
Output-level safety	Action-level safety

I2OS Mini Gate focuses on action-level safety.

9. Human-Verifiable Governance

I2OS Mini Gate should not only return a classification.

It should also provide a human-verifiable explanation.

A useful report should include:

classification
reason codes
constraint results
risk level
recommended repair
audit log

This allows humans to understand why a transition was permitted, delayed, repaired, or blocked.

10. v3.8 Refinement Goals

v3.8 focuses on refinement rather than major expansion.

Main goals:

clarify runtime governance model
improve public readability
organize example cases
strengthen README explanation
prepare v4.0 stable closed-loop governance direction
make GO / HOLD / REPAIR / BLOCK easier to understand
connect runtime governance with human-verifiable explanation
11. Path Toward v4.0

v3.8 prepares the project for:

I2OS Mini Gate v4.0
Stable Closed-Loop Runtime Governance Prototype

Expected v4.0 direction:

Proposed Action
↓
Human-Admissibility
↓
Recovery Path
↓
Recheck Loop
↓
Execution Contract
↓
Contract Enforcement
↓
Final Governance Report

v3.8 is the refinement layer before that stable closed-loop release.

12. Final Principle
Capability is not permission.

The future of AI safety is not only about making models more capable.

It is also about deciding which state transitions should be permitted before execution.

I2OS Mini Gate is a small prototype for that transition governance layer.
