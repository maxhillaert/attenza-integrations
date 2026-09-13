---
name: attenza
description: >-
  Explain when to use Attenza MCP for durable human decisions (and when not to).
  Use before creating an intervention, when unsure whether to escalate to the
  human, or when choosing among Attenza modes.
---

# Attenza

Attenza is the durable human-decision layer for agents. The human owns judgment;
the agent owns execution. The MCP does not exist to narrate thinking, stream
progress, or invent one-off notification UIs.

## Why it exists

Chat is ephemeral and host-specific. Attenza stores a decision task the human
can answer in the Attenza PWA (or compatible surface), then the agent resumes
from the recorded result — across restarts, minutes, or days.

Use Attenza when work must **stop** until a human decides, and must **resume
correctly** from that decision later.

## Modes

Agents pick a **mode**, not a custom layout.

| Mode | Meaning | Agent waits? | Status |
| --- | --- | --- | --- |
| `decide` | Approval, selection, correction, or explicit judgment gates irreversible or externally visible work | Yes, until decision, cancel, or expiry | **Supported** — follow `attenza-intervention` |
| `clarify` | Missing input required to continue (short, concrete question) | Yes, with a short expiry | Treat as `decide` via `attenza-intervention` until a dedicated skill exists |
| `inform` | Push-only notice, no wait | No | **Not available** until the connection owner configures notify policy in Attenza |

Do not invent other modes. Do not build ad-hoc “notification” surfaces.

## When to use (`decide` / `clarify`)

Create an Attenza intervention only if **all** of these are true:

1. The next step is blocked on human judgment or missing input the agent cannot safely assume.
2. The consequence is irreversible, externally visible, spendy, or hard to undo — **or** the user explicitly asked to approve this class of action.
3. A clear decision artifact would let the agent resume without re-asking in chat.

Examples that qualify: approve a payment or send; merge/ship/publish; pick among material options; correct a draft before it leaves the machine; confirm a destructive change.

## When not to use

Do **not** create an intervention for:

- Progress updates, status, or “still working”
- The agent’s internal plan, hypotheses, or chain-of-thought
- Routine confirmations the user already delegated in this session
- Nice-to-know FYIs (deploy notes, trivia, “heads up”) — that is `inform`, which is disabled until policy exists
- Questions that belong in the current chat because no durable handoff is needed

If unsure, **prefer chat** or continue without escalating. Silence is better than spam.

## Who controls escalation

Default: the agent does **not** notify willy-nilly.

- Session instructions from the user can temporarily tighten or loosen escalation for that run.
- Durable rules (what this Cursor / Grok Bot / Codex connection may open) belong in Attenza on the connection — not invented by the agent.
- Until notify policy exists in-product, only `decide` / `clarify` (wait + ack) are allowed.

## How to escalate (supported path)

1. Confirm the gate matches **When to use**.
2. Follow the `attenza-intervention` skill end-to-end: create → stop the gated action → wait/poll → resume from the terminal task.
3. Use only official A2UI Basic Catalog authoring as that skill requires.
4. Never ask for API keys or private capability URLs; use OAuth / the connected MCP (or the authorized `attenza` CLI).

## Host context (brief)

- **Long-lived hosts (e.g. Grok Bot):** create, then schedule quiet follow-up wakes to poll — do not busy-wait the whole turn.
- **One-shot / short hosts:** create, preserve `task.id` + `expiresAt`, and arrange a later wake or tell the user the decision is waiting in Attenza — do not duplicate creates.

## If tools are missing

Ask the user to connect or reconnect Attenza OAuth for this host. Do not bypass with secrets or legacy URLs.
