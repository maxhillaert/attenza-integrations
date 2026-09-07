---
name: attenza-intervention
description: Pause agent work for a durable human decision through Attenza, poll until the decision or deadline, and resume from the recorded result. Use when an action needs approval, selection, correction, missing input, or explicit human judgment and the Attenza MCP tools are connected.
---

# Attenza intervention

Use the connected `create_intervention`, `get_intervention`, and `cancel_intervention` tools. If they are unavailable, ask the user to connect or reconnect Attenza through the platform's OAuth flow. Never ask for an API key or private capability URL.

When the MCP tools are not exposed directly but the public `attenza` CLI is installed and already authorized, use `attenza create`, `attenza get`, `attenza wait`, or `attenza cancel` as the equivalent local transport. Do not initiate an interactive login during unattended work.

The connection needs `tasks:create` to post and `tasks:read` to wait for the answer; `tasks:cancel` is optional. If a call is denied by the connection's permissions, ask its owner to adjust or reconnect that connection in Attenza rather than seeking another credential or bypass.

## Create

Create an intervention only when work is genuinely blocked on a human decision. Put evidence and constraints in immutable `/context`; put only human-editable values under `/state`. Author only official A2UI v0.9/v0.9.1 Basic Catalog messages. Never supply HTML, JavaScript, CSS, URLs, classes, expressions, inline catalogs, or executable content.

Use a stable, retry-safe `message_id`. Give the task a concise title, decision-oriented summary, recognizable source, and a `context_id` that groups related work. Make action names semantic, such as `approve_selected`, `revise`, or `reject`.

For time-sensitive input, pass `expires_at` as an absolute timezone-aware ISO 8601 timestamp no more than seven days ahead. Alternatively pass `expires_in_seconds` from 60 to 604800, but never pass both. If neither is supplied, Attenza uses 24 hours. Record the returned `task.metadata.expiresAt`; it is the authoritative polling deadline.

## Wait and resume

Immediately after a successful create, preserve the returned `task.id` and `task.metadata.expiresAt`, stop the gated action, and start polling `get_intervention` with that exact id. Do not finish the agent run merely because creation succeeded, and do not ask the human to repeat their answer in chat.

Poll after 5 seconds, then use bounded backoff up to 30 seconds. Do not busy-loop. Keep polling while the host execution remains active, the task is `TASK_STATE_INPUT_REQUIRED`, and the expiry deadline has not passed. If the host must end before the task is terminal, preserve the existing `task.id` and deadline so a later or scheduled wake can poll that task instead of creating a duplicate.

Resume only from a terminal task:

- `TASK_STATE_COMPLETED`: read the decision artifact, branch on `action.name`, and use the synchronized model plus `/state` patch.
- `TASK_STATE_CANCELED` with `metadata.resolution="expired"`: stop waiting because the deadline passed; do not perform the gated action.
- `TASK_STATE_CANCELED` with `metadata.resolution="canceled"`: stop the gated work.

A rejection action is a completed human decision, not a failed task. Never repeat a completed, canceled, or expired intervention. If polling fails transiently before the deadline, retry `get_intervention`; never create a replacement unless the user explicitly asks for a new decision.
