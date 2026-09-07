# Cursor

Cursor is the first active integration target.

## Remote MCP test

Add the repository's root [`mcp.json`](../../mcp.json) to Cursor's MCP configuration. It contains only the public endpoint:

```json
{
  "mcpServers": {
    "attenza": {
      "type": "streamable-http",
      "url": "https://staging.attenza.io/mcp"
    }
  }
}
```

Enable `attenza`, complete the browser OAuth flow, and verify the tools `create_intervention`, `get_intervention`, and `cancel_intervention` appear.

Then ask Cursor:

> Ask me which environment to deploy to, post the choices to Attenza, and wait for my answer.

## Agent Plugin

The repository root is also a portable Agent Plugin: [`plugin.json`](../../plugin.json), [`mcp.json`](../../mcp.json), and [`skills/attenza-intervention`](../../skills/attenza-intervention). There is no separate Cursor copy to keep synchronized.
