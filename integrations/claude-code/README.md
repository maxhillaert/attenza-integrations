# Claude Code

Claude Code consumes the shared package through its native manifest and repository marketplace. Do not copy `SKILL.md` into this folder.

## Why a shim is required

[`packages/attenza-plugin`](../../packages/attenza-plugin) follows Agent Plugins 1.0 while also containing Claude Code's native [`.claude-plugin/plugin.json`](../../packages/attenza-plugin/.claude-plugin/plugin.json). [Claude Code plugins](https://code.claude.com/docs/en/plugins-reference) discover:

- metadata and native MCP wiring from `.claude-plugin/plugin.json`
- the existing skill under `skills/<name>/SKILL.md`

The native manifest keeps the MCP server inline because Agent Plugins and Claude Code use different transport names. Repository validation ensures both native URLs match the portable `mcp.json` URL.

## Install

Add the public marketplace, then install the plugin:

```sh
claude plugin marketplace add maxhillaert/attenza-integrations
claude plugin install attenza@attenza-integrations
```

For local development, validate and load the package directly:

```sh
claude plugin validate packages/attenza-plugin --strict
claude --plugin-dir packages/attenza-plugin
```

The first MCP use starts the browser OAuth flow. Follow [`skills/attenza-intervention/SKILL.md`](../../packages/attenza-plugin/skills/attenza-intervention/SKILL.md) for create, poll, expiry, and resume behavior. If a session must end before the task is terminal, preserve `task.id` so a later or scheduled wake polls that task instead of creating a duplicate.

See the [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference) and [marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces) for the underlying formats.
