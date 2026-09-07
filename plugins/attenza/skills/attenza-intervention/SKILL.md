---
name: attenza-intervention
description: Pause an agent for a durable human decision through Attenza. Use when an action needs approval, selection, correction, missing input, or explicit human judgment and the Attenza MCP tools are connected.
---

# Attenza intervention

Use the connected `create_intervention`, `get_intervention`, and `cancel_intervention` tools. If they are unavailable, ask the user to connect or reconnect Attenza through the platform's OAuth flow. Never ask for an API key or private capability URL.

The connection needs `tasks:create` to post and `tasks:read` to wait for the answer; `tasks:cancel` is optional. If a call is denied by the connection's permissions, ask its owner to adjust or reconnect that connection in Attenza rather than seeking another credential or bypass.

## Create

Create an intervention only when work is genuinely blocked on a human decision. Put evidence and constraints in immutable `/context`; put only human-editable values under `/state`. Author only official A2UI v0.9/v0.9.1 Basic Catalog messages. Never supply HTML, JavaScript, CSS, URLs, classes, expressions, inline catalogs, or executable content.

Use a stable, retry-safe `message_id`. Give the task a concise title, decision-oriented summary, recognizable source, and a `context_id` that groups related work. Make action names semantic, such as `approve_selected`, `revise`, or `reject`.

## Wait and resume

Preserve the returned task id and stop the gated action. Poll `get_intervention` at a reasonable interval; do not invent or infer the human's answer. Resume only from a terminal task:

- `TASK_STATE_COMPLETED`: read the decision artifact, branch on `action.name`, and use the synchronized model plus `/state` patch.
- `TASK_STATE_CANCELED`: stop the gated work. `expired` and `canceled` are not approval.

A rejection action is a completed human decision, not a failed task. Never repeat a completed or canceled intervention.
