# GrokBot

This file is human setup, publication, and verification documentation; GrokBot does not load it as behavioral guidance. When Attenza is installed as an Agent Plugin, GrokBot receives the same A2UI authoring, decision-design, polling, and expiry instructions as Cursor from [`packages/attenza-plugin/skills/attenza-intervention`](../../packages/attenza-plugin/skills/attenza-intervention). A raw custom MCP connector exposes tools but does not add the skill. A future GrokBot-only behavioral rule should be a conditionally loaded reference under that shared skill, not another skill copy here.

Attenza works end to end in GrokBot today as a custom OAuth MCP connector. Add the shared endpoint through [Grok connectors](https://grok.com/connectors) using New Connector → Custom:

```text
https://www.attenza.io/mcp
```

[`packages/attenza-plugin`](../../packages/attenza-plugin) packages the same endpoint with the canonical `attenza-intervention` skill as a portable Agent Plugin. [GrokBot plugin connections](https://cursor.com/help/grok-bot/connect-plugins) use the Cursor account and marketplace available to that account, so publishing that plugin through the Cursor marketplace is the route to a one-click GrokBot installation. The shared skill is deliberately not copied into this folder.

The skill corrects the important behavioral gap in a raw MCP connection: after `create_intervention`, GrokBot must preserve the returned task id and expiry, then poll `get_intervention` until completion, cancellation, or expiry.

Publication checklist:

1. Symlink or copy `packages/attenza-plugin` to `~/.cursor/plugins/local/attenza` and verify its MCP server and skill are discovered.
2. Submit this public repository at `cursor.com/marketplace/publish`; `.cursor-plugin/marketplace.json` points Cursor at the shared package.
3. After review, install Attenza from GrokBot Plugins and verify the skill-driven polling loop.
4. Revoke the test grant in Attenza and confirm subsequent calls are denied.
