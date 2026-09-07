# Attenza plugin

Portable [Agent Plugins 1.0](https://github.com/agentplugins/agent-plugins-spec) package for Attenza. Hosts that implement the standard load **this directory** as the plugin root. The repository also contains a CLI and host-specific notes; those are siblings, not part of this package.

This package is the only copy of the skill and the only MCP configuration. Do not fork `SKILL.md` or `mcp.json` into `integrations/` or another host tree.

## Contents

| Path | Role |
| --- | --- |
| [`plugin.json`](plugin.json) | Agent Plugins 1.0 identity |
| [`mcp.json`](mcp.json) | Public OAuth MCP endpoint |
| [`skills/attenza-intervention/SKILL.md`](skills/attenza-intervention/SKILL.md) | When to pause, how to poll, how to resume |

The MCP URL is `https://staging.attenza.io/mcp`. Authentication is OAuth. Do not add API keys, bearer tokens, or private capability URLs.

## How hosts consume it

Point the host at this package directory, not the repository root.

| Host | Documented install path |
| --- | --- |
| [Cursor](../../integrations/cursor) | Symlink or copy this folder to `~/.cursor/plugins/local/attenza` |
| [GrokBot](../../integrations/grokbot) | Same Cursor plugin; GrokBot installs from the Cursor account marketplace |
| [Codex](../../integrations/codex) | Load this Agent Plugins 1.0 root as-is. Add a `.codex-plugin` overlay later only if Codex requires the vendor manifest or hooks |
| [Claude Code](../../integrations/claude-code) | Needs a `.claude-plugin/plugin.json` plus `.mcp.json` shim later. Until then, connect the shared MCP URL and follow the skill in this package |

Vendor-specific setup lives under `integrations/<host>/`. Shared behavior stays here.
