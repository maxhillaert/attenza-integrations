# Cursor

Cursor is the first active integration target.

This file is human setup and verification documentation; Cursor does not load it as behavioral guidance. When Attenza is installed as an Agent Plugin, Cursor loads the canonical skill and its A2UI authoring references from [`packages/attenza-plugin/skills/attenza-intervention`](../../packages/attenza-plugin/skills/attenza-intervention). A raw remote MCP connection exposes tools but does not add the skill. Add shared agent behavior to the package, not here.

## Remote MCP test

Add [`packages/attenza-plugin/mcp.json`](../../packages/attenza-plugin/mcp.json) to Cursor's MCP configuration. It contains only the public endpoint:

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

[`packages/attenza-plugin`](../../packages/attenza-plugin) is the portable Agent Plugin: [`plugin.json`](../../packages/attenza-plugin/plugin.json), [`mcp.json`](../../packages/attenza-plugin/mcp.json), and [`skills/attenza-intervention`](../../packages/attenza-plugin/skills/attenza-intervention). The skill teaches Cursor to preserve the task id, poll with bounded backoff, honor the expiry deadline, and resume only from the recorded terminal result. There is no separate Cursor copy to keep synchronized.

For local testing, symlink or copy **that package directory** (not the repository root) to `~/.cursor/plugins/local/attenza`:

```sh
mkdir -p ~/.cursor/plugins/local
ln -sfn /path/to/attenza-integrations/packages/attenza-plugin ~/.cursor/plugins/local/attenza
```

Reload Cursor, then confirm Attenza appears under Customize with one MCP server and one skill.

Cursor's [plugin reference](https://cursor.com/docs/reference/plugins) requires a repository-root marketplace manifest when a plugin lives in a subdirectory. This repository provides [`.cursor-plugin/marketplace.json`](../../.cursor-plugin/marketplace.json), which points discovery at `packages/attenza-plugin`. Submit the public repository URL through the [Cursor marketplace form](https://cursor.com/marketplace/publish).
