# Attenza plugin

Portable [Agent Plugins 1.0](https://github.com/agentplugins/agent-plugins-spec) package for Attenza. Hosts that implement the standard load **this directory** as the plugin root. The repository also contains a CLI and host-specific notes; those are siblings, not part of this package.

This package is the only copy of the skill and the only portable MCP configuration. Native host manifests may express the same public endpoint in their own syntax; repository checks prevent those thin shims from drifting. Do not fork `SKILL.md` or `mcp.json` into `integrations/` or another host tree.

## Contents

| Path | Role |
| --- | --- |
| [`plugin.json`](plugin.json) | Agent Plugins 1.0 identity |
| [`mcp.json`](mcp.json) | Agent Plugins 1.0 public OAuth MCP endpoint |
| [`skills/attenza-intervention/SKILL.md`](skills/attenza-intervention/SKILL.md) | When to pause, how to poll, how to resume |
| [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) | Codex-native discovery and MCP wiring |
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | Claude Code-native discovery and MCP wiring |

The MCP URL is `https://staging.attenza.io/mcp`. Authentication is OAuth. Do not add API keys, bearer tokens, or private capability URLs.

## How hosts consume it

Point the host at this package directory, not the repository root.

| Host | Documented install path |
| --- | --- |
| [Cursor](../../integrations/cursor) | Symlink or copy this folder to `~/.cursor/plugins/local/attenza` |
| [GrokBot](../../integrations/grokbot) | Same Cursor plugin; GrokBot installs from the Cursor account marketplace |
| [Codex](../../integrations/codex) | Install `attenza` from the repository's `.agents/plugins/marketplace.json` |
| [Claude Code](../../integrations/claude-code) | Install `attenza` from the repository's `.claude-plugin/marketplace.json` |

Vendor-specific setup lives under `integrations/<host>/`. The native manifests contain only discovery metadata and the host-specific spelling of the public MCP connection; shared behavior stays in the single skill.
