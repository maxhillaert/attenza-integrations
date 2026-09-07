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

The repository root is a portable Agent Plugin: [`plugin.json`](../../plugin.json), [`mcp.json`](../../mcp.json), and [`skills/attenza-intervention`](../../skills/attenza-intervention). The skill teaches Cursor to preserve the task id, poll with bounded backoff, honor the expiry deadline, and resume only from the recorded terminal result. There is no separate Cursor copy to keep synchronized.

For local testing, place or symlink this repository at `~/.cursor/plugins/local/attenza`, reload Cursor, then confirm Attenza appears under Customize with one MCP server and one skill. The public [Cursor marketplace submission](https://cursor.com/marketplace/publish) uses this repository URL; see Cursor's [plugin reference](https://cursor.com/docs/reference/plugins) for the review checklist.
