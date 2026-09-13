# GrokBot

This file is human setup, publication, and verification documentation; GrokBot does not load it as behavioral guidance. When Attenza is installed as an Agent Plugin, GrokBot receives the same A2UI authoring, decision-design, polling, and expiry instructions as Cursor from [`packages/attenza-plugin/skills/attenza-intervention`](../../packages/attenza-plugin/skills/attenza-intervention). A raw custom MCP connector exposes tools but does not add the skill. A future GrokBot-only behavioral rule should be a conditionally loaded reference under that shared skill, not another skill copy here.

## How GrokBot loads Attenza

GrokBot runs in Cursor's cloud and installs [plugins from the same Cursor account catalog](https://cursor.com/help/grok-bot/connect-plugins). MCP authentication is shared with Cursor. There is no GrokBot copy of the skill, and GrokBot does **not** read `~/.cursor/plugins/local`.

That means a desktop local-plugin symlink is not a GrokBot test. A Cloud Agent checkout of this repository is also not a plugin install: Cloud Agents can call MCP servers attached in [cursor.com/agents](https://cursor.com/agents), but they do not load `packages/attenza-plugin` as a plugin just because the repo is cloned.

| Setup | Where you enable it | What GrokBot loads |
| --- | --- | --- |
| Custom OAuth connector | [Grok connectors](https://grok.com/connectors) → Custom | MCP tools only |
| Cloud Agent MCP | [cursor.com/agents](https://cursor.com/agents) MCP dropdown | MCP tools only (this is Cursor Cloud, not GrokBot Plugins) |
| Cursor plugin | A marketplace your Cursor account can see, then GrokBot → Plugins | MCP tools **plus** `attenza-intervention` |

The plugin is not in the public Cursor Marketplace yet. Until it is, the cloud plugin test is a **team marketplace** import of this repository, not the desktop local folder.

## Custom connector test (MCP only)

Attenza already works end to end in GrokBot as a custom OAuth MCP connector. Add the shared endpoint through [Grok connectors](https://grok.com/connectors) using New Connector → Custom:

```text
https://www.attenza.io/mcp
```

Complete browser OAuth, confirm `create_intervention`, `get_intervention`, and `cancel_intervention`, then run one intervention round trip. This proves the OAuth MCP contract. It does not load the skill, so the bot may not poll or honor expiry on its own.

## Cloud plugin test (MCP plus skill)

[`packages/attenza-plugin`](../../packages/attenza-plugin) is the same Agent Plugin GrokBot will install once it appears in a Cursor marketplace. [`.cursor-plugin/marketplace.json`](../../.cursor-plugin/marketplace.json) is the discovery file Cursor indexes.

On a Teams or Enterprise plan, import this public repository as a team marketplace instead of waiting for public review:

1. Open [Dashboard → Plugins](https://cursor.com/dashboard).
2. Under Team Marketplaces, add a marketplace and **Import from Repo** using `https://github.com/maxhillaert/attenza-integrations`.
3. Confirm the `attenza` plugin is listed from `packages/attenza-plugin`.
4. Enable it for the account. If the team uses an MCP allowlist, add `https://www.attenza.io/mcp`.
5. In GrokBot, open **Plugins**, install Attenza, and finish OAuth.
6. Ask the bot to post a decision to Attenza and wait for the answer. The skill should keep `task.id`, poll `get_intervention`, and resume from the terminal result.

Individuals without a team marketplace cannot load an unpublished plugin into GrokBot. The remaining cloud path is the custom connector above, then public submission at [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish).

A Cloud Agent with Attenza added as an HTTP MCP server can exercise the same three tools after OAuth. That still is not a plugin test: the `attenza-intervention` skill is not installed unless the plugin itself is in a marketplace that host consumes.

Publication checklist after the team-marketplace or public-catalog install succeeds:

1. Install Attenza from GrokBot Plugins and verify the skill-driven polling loop.
2. Revoke the test grant in Attenza and confirm subsequent calls are denied.
