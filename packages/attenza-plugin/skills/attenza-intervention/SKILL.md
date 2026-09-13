---
name: attenza-intervention
description: Pause agent work for a durable human decision through Attenza, poll until the decision or deadline, and resume from the recorded result. Use when an action needs approval, selection, correction, missing input, or explicit human judgment and the Attenza MCP tools are connected.
---

# Attenza intervention

Use the connected `create_intervention`, `get_intervention`, and `cancel_intervention` tools. If they are unavailable, ask the user to connect or reconnect Attenza through the platform's OAuth flow. Never ask for an API key or private capability URL.

When the MCP tools are not exposed directly but the public `attenza` CLI is installed and already authorized, use `attenza create`, `attenza get`, `attenza wait`, or `attenza cancel` as the equivalent local transport. Do not initiate an interactive login during unattended work.

The connection needs `tasks:create` to post and `tasks:read` to wait for the answer; `tasks:cancel` is optional. If a call is denied by the connection's permissions, ask its owner to adjust or reconnect that connection in Attenza rather than seeking another credential or bypass.

This skill is **decide-only**. Treat missing-input `clarify` as the same wait-for-decision path until a dedicated skill exists. Do not invent notify UIs. `inform` is unavailable until in-product notify policy exists.

Read the `attenza` overview skill when choosing among modes.

## Create

Create an intervention only if **all** of these are true:

1. The next step is blocked on human judgment or missing input the agent cannot safely assume.
2. The consequence is irreversible, externally visible, spendy, or hard to undo — **or** the user explicitly asked to approve this class of action.
3. A clear decision artifact would let the agent resume without re-asking in chat.

Do not create an intervention for:

- Progress updates, status, or "still working"
- The agent's internal plan, hypotheses, chain-of-thought, or thought narration
- Routine confirmations the user already delegated in this session
- Nice-to-know FYIs (deploy notes, trivia, "heads up") — that is `inform`, which is disabled until notify policy exists in Attenza
- Questions that belong in the current chat because no durable handoff is needed

If unsure, prefer chat. Silence is better than spam. Never use create as a progress channel.

Put evidence and constraints in immutable `/context`; put only human-editable values under `/state`. Author only official A2UI v0.9/v0.9.1 Basic Catalog messages. Never supply HTML, JavaScript, CSS, URLs, classes, expressions, inline catalogs, or executable content.

Before authoring a surface, read:

- [references/a2ui-authoring.md](references/a2ui-authoring.md) for Attenza's accepted message shape, safe Basic Catalog subset, bindings, and component examples.
- [references/decision-design.md](references/decision-design.md) for choosing controls and actions that express the decision without ambiguity.

Use a stable, retry-safe `message_id`. Give the task a concise title, decision-oriented summary, recognizable source, and a `context_id` that groups related work. Make action names semantic, such as `approve_selected`, `revise`, or `reject`.

Never create a second intervention for the same `context_id` decision while an earlier task is still `TASK_STATE_INPUT_REQUIRED`. Poll that `task.id` instead.

Every decide has a deadline. Pass `expires_at` as an absolute timezone-aware ISO 8601 timestamp no more than seven days ahead, or `expires_in_seconds` from 60 to 604800, but never both. If neither is supplied, Attenza uses 24 hours. Record the returned `task.metadata.expiresAt`; it is the authoritative polling deadline. Do not teach or plan an indefinite wait.

## Protocol

Never wait forever.

- Honor `expiresAt` on every decide. Stop polling when it passes.
- On expiry, do **not** perform the gated action.
- If more time is needed, cancel and create a replacement with a later `expires_at`, or open a new decision after expiry. Do not keep waiting past the deadline.
- Do not invent an "open-ended" or "wait until whenever" path.

## Wait contract

Shared by every host. Mode is always `decide` (with `clarify` folded in). Only the wake strategy changes.

1. Immediately persist `task.id` and `expiresAt` across wakes (conversation state, PR/issue, agent state, or scheduled job metadata).
2. Stop the gated side effect until the task is terminal. Do not finish the run merely because creation succeeded.
3. Poll `get_intervention` with that exact id after 5 seconds, then bounded backoff up to 30 seconds. No tight loop.
4. If the human answers in chat first, `cancel_intervention` on that id and use the chat answer. Do not also wait for Attenza, and do not ask them to repeat the answer in the PWA.
5. Never duplicate create for the same `context_id` decision while one is still open. Cancel first if you must replace it to extend time.

Keep polling only while the host execution remains active, the task is `TASK_STATE_INPUT_REQUIRED`, and `expiresAt` has not passed. If the host must end first, keep the persisted id and deadline for a later wake — do not create a replacement.

## Host wait adapters

One decide mode. Pick the wait strategy for this host; do not invent a custom notification surface.

- **Grok Bot / long-lived:** create, persist `task.id` + `expiresAt`, end the turn, then schedule quiet cron or backoff wakes that poll `get_intervention` until terminal or expiry. Do not busy-wait the whole turn.
- **Cursor IDE:** if the user is present, a short in-turn poll with backoff is OK. Otherwise persist `task.id`, tell the user the decision is waiting in Attenza, and resume on the next user message. Do not spin the composer until they return.
- **Cursor Cloud Agent:** bounded poll while the VM is running. When the run must end, persist `task.id` and `expiresAt` in PR, issue, or agent state so a later agent can poll that task. Do not duplicate create.
- **Codex / ChatGPT one-shot:** create, report that work is blocked on Attenza, and end. The next turn or tool wake polls by `task.id`. Do not busy-wait the whole conversation.
- **Claude Code / CLI:** in an interactive terminal, `attenza wait TASK_ID` (or equivalent polling) is OK through expiry. Unattended, treat as one-shot: create, persist the id, and invoke later.
- **CI / headless:** create only if a human will actually see and answer the Attenza task. Fail closed on expiry; do not perform the gated action, and do not pretend CI will wait days.

## Resume

Resume only from a terminal task:

- `TASK_STATE_COMPLETED`: read the decision artifact, branch on `action.name`, and use the synchronized model plus `/state` patch.
- `TASK_STATE_CANCELED` with `metadata.resolution="expired"`: stop waiting because the deadline passed; do not perform the gated action.
- `TASK_STATE_CANCELED` with `metadata.resolution="canceled"`: stop the gated work.

A rejection action is a completed human decision, not a failed task. Never repeat a completed, canceled, or expired intervention as if it were still open. If polling fails transiently before the deadline, retry `get_intervention`. Create a new task only after cancel or expiry when more time is needed or the user asks for a new decision.
