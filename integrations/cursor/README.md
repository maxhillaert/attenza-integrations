# Cursor

Cursor is the first active integration target.

This file is human setup and verification documentation; Cursor does not load it as behavioral guidance. When Attenza is installed as an Agent Plugin, Cursor loads the shared skills from [`packages/attenza-plugin/skills`](../../packages/attenza-plugin/skills): `attenza` (when to escalate) and `attenza-intervention` (create, poll, resume) plus A2UI authoring references. A raw remote MCP connection exposes tools but does not add the skills. Add shared agent behavior to the package, not here.

## How a Cursor test works

Cursor can load Attenza in four ways. They are not equivalent.

| Setup | What Cursor loads | What you can prove |
| --- | --- | --- |
| Remote MCP only | The `attenza` server at `https://www.attenza.io/mcp` | OAuth, tool list, create/get/cancel |
| Cloud Agent MCP | The same server attached under [cursor.com/agents](https://cursor.com/agents) | The same MCP contract from a Cloud Agent VM |
| Desktop local plugin | MCP **plus** the `attenza` and `attenza-intervention` skills from `~/.cursor/plugins/local` | IDE Customize discovery |
| Marketplace plugin | MCP **plus** the skills from a team or public catalog | GrokBot Plugins and other cloud hosts |

The installable plugin is [`packages/attenza-plugin`](../../packages/attenza-plugin), not this repository root. Cursor identifies an [Agent Plugin](https://cursor.com/docs/plugins.md) by a root `plugin.json` sitting next to `mcp.json` and `skills/`. Those files live only under that package.

Desktop Cursor discovers in-development plugins from `~/.cursor/plugins/local/<name>/`. That folder is IDE-only.

[Cloud Agents](https://cursor.com/docs/cloud-agent) and [GrokBot](https://cursor.com/help/grok-bot/connect-plugins) consume Cursor's **cloud catalog**, not the local folder and not a repo checkout. A Cloud Agent can call MCP servers you attach under [cursor.com/agents](https://cursor.com/agents). GrokBot can install the plugin only after it appears in a marketplace that account can see (team import of this repo, or the public Cursor Marketplace). Checking out `packages/attenza-plugin` in a Cloud Agent VM does not install it. See [`integrations/grokbot`](../grokbot) for that path.

## Local Agent Plugin test

Cursor's [local plugin docs](https://cursor.com/docs/plugins.md#test-plugins-locally) load either an Agent Plugin (`plugin.json` at the plugin root) or a Cursor Plugin (`.cursor-plugin/plugin.json`) from `~/.cursor/plugins/local`.

Attenza is an Agent Plugin. Symlink or copy **the package directory**:

```sh
mkdir -p ~/.cursor/plugins/local
ln -sfn /path/to/attenza-integrations/packages/attenza-plugin ~/.cursor/plugins/local/attenza
```

After that link, `~/.cursor/plugins/local/attenza/plugin.json`, `mcp.json`, `skills/attenza/SKILL.md`, and `skills/attenza-intervention/SKILL.md` must all exist. Pointing Cursor at the repository root fails because those files are not there.

If a symlink is ignored, copy the directory instead of linking it.

Then:

1. On Teams or Enterprise, confirm an admin has enabled **Allow Local Plugin Imports** under Dashboard → Settings → Security & Identity → Marketplace and Plugins. The setting is off by default on Enterprise; when it is off, Cursor skips `~/.cursor/plugins/local` and lists no local plugin.
2. If a marketplace copy of `attenza` is already installed, uninstall or disable it. Marketplace installs take precedence over the local folder.
3. Restart Cursor, or run **Developer: Reload Window**.
4. Open **Customize** and confirm Attenza appears with one MCP server (`attenza`) and two skills (`attenza` and `attenza-intervention`).
5. Enable `attenza`, complete the browser OAuth flow, and verify the tools `create_intervention`, `get_intervention`, and `cancel_intervention`.
6. Ask Cursor:

> Ask me which environment to deploy to, post the choices to Attenza, and wait for my answer.

The skill should create one intervention, keep `task.id`, poll `get_intervention` with bounded backoff until a terminal state or expiry, and resume from that recorded result instead of asking you to restate the answer in chat.

## Remote MCP test

Add [`packages/attenza-plugin/mcp.json`](../../packages/attenza-plugin/mcp.json) to Cursor's MCP configuration. It contains only the public endpoint:

```json
{
  "mcpServers": {
    "attenza": {
      "type": "streamable-http",
      "url": "https://www.attenza.io/mcp"
    }
  }
}
```

Enable `attenza`, complete the browser OAuth flow, and verify the tools `create_intervention`, `get_intervention`, and `cancel_intervention` appear. This proves the OAuth MCP contract. It does not load the skills, so the agent may not poll or honor expiry on its own.

## Agent Plugin package and marketplace

[`packages/attenza-plugin`](../../packages/attenza-plugin) is the portable Agent Plugin: [`plugin.json`](../../packages/attenza-plugin/plugin.json), [`mcp.json`](../../packages/attenza-plugin/mcp.json), [`skills/attenza`](../../packages/attenza-plugin/skills/attenza), and [`skills/attenza-intervention`](../../packages/attenza-plugin/skills/attenza-intervention). The overview skill teaches when to escalate; the intervention skill teaches Cursor to preserve the task id, poll with bounded backoff, honor the expiry deadline, and resume only from the recorded terminal result. There is no separate Cursor copy to keep synchronized.

Cursor's [plugin reference](https://cursor.com/docs/reference/plugins) requires a repository-root marketplace manifest when a plugin lives in a subdirectory. This repository provides [`.cursor-plugin/marketplace.json`](../../.cursor-plugin/marketplace.json), which points discovery at `packages/attenza-plugin` and names the shared `skills/` and `mcp.json` paths. That file is for installing this repo as a Cursor marketplace (team import or public submission). It is not a substitute for the `~/.cursor/plugins/local` folder during first local discovery.

To test the plugin in GrokBot or another cloud host before public review, import this repository as a [team marketplace](https://cursor.com/docs/plugins.md#add-a-team-marketplace) and install Attenza from that catalog. Submit the public repository URL through the [Cursor marketplace form](https://cursor.com/marketplace/publish) when you want it listed for every Cursor account.
