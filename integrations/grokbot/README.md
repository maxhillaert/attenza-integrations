# GrokBot

Attenza works end to end in GrokBot today as a custom OAuth MCP connector. Add the shared endpoint through [Grok connectors](https://grok.com/connectors) using New Connector → Custom:

```text
https://staging.attenza.io/mcp
```

The repository root packages the same endpoint with the canonical `attenza-intervention` skill as a portable Agent Plugin. [GrokBot plugin connections](https://cursor.com/help/grok-bot/connect-plugins) use the Cursor account and marketplace available to that account, so publishing this repository through the Cursor marketplace is the route to a one-click GrokBot installation. The shared skill is deliberately not copied into this folder.

The skill corrects the important behavioral gap in a raw MCP connection: after `create_intervention`, GrokBot must preserve the returned task id and expiry, then poll `get_intervention` until completion, cancellation, or expiry.

Publication checklist:

1. Install this Agent Plugin locally in Cursor and verify its MCP server and skill are discovered.
2. Submit this public repository at `cursor.com/marketplace/publish`.
3. After review, install Attenza from GrokBot Plugins and verify the skill-driven polling loop.
4. Revoke the test grant in Attenza and confirm subsequent calls are denied.
