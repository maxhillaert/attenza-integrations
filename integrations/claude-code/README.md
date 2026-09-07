# Claude Code

Claude Code is a planned host for the same portable plugin. Do not copy `SKILL.md` or `mcp.json` into this folder.

## Why a shim is required

[`packages/attenza-plugin`](../../packages/attenza-plugin) follows Agent Plugins 1.0 (`plugin.json` and `mcp.json` at the package root). [Claude Code plugins](https://code.claude.com/docs/en/plugins) document a different discovery layout:

- Manifest at `.claude-plugin/plugin.json` (not root `plugin.json`)
- MCP servers at `.mcp.json` (not `mcp.json`)
- Skills still under `skills/<name>/SKILL.md` at the plugin root

Until those shims exist, Claude Code will not treat the portable package as a native plugin.

## Planned approach

Add the Claude overlay **inside** `packages/attenza-plugin/` so there is still one skill and one canonical MCP URL:

1. `.claude-plugin/plugin.json` mirroring the portable identity (`name`, `version`, `description`).
2. `.mcp.json` as a twin of `mcp.json` that keeps the same server name and `https://staging.attenza.io/mcp` URL. CI would then assert the two MCP files agree, rather than maintaining a second skill.
3. No copy of `SKILL.md`. Claude Code already discovers `skills/` next to `.claude-plugin/`.

Those files are intentionally not added in this pass. A twin `.mcp.json` is a follow-up so the URL cannot drift by hand.

## Meanwhile

Connect the shared OAuth endpoint as a remote MCP server:

```text
https://staging.attenza.io/mcp
```

Follow [`packages/attenza-plugin/skills/attenza-intervention/SKILL.md`](../../packages/attenza-plugin/skills/attenza-intervention/SKILL.md) for create, poll, expiry, and resume behavior. If a Claude Code session must end before the task is terminal, preserve `task.id` so a later or scheduled wake can poll that task instead of creating a duplicate.

See the [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference) before claiming a marketplace or `--plugin-dir` install path.
