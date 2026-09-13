# Attenza plugin

Portable [Agent Plugins 1.0](https://github.com/agentplugins/agent-plugins-spec) package for Attenza. Hosts that implement the standard load **this directory** as the plugin root. The repository also contains a CLI and host-specific notes; those are siblings, not part of this package.

This package is the only copy of the skills and the only portable MCP configuration. Native host manifests may express the same public endpoint in their own syntax; repository checks prevent those thin shims from drifting. Do not fork `SKILL.md` or `mcp.json` into `integrations/` or another host tree.

## Contents

| Path | Role |
| --- | --- |
| [`plugin.json`](plugin.json) | Agent Plugins 1.0 identity |
| [`mcp.json`](mcp.json) | Agent Plugins 1.0 public OAuth MCP endpoint |
| [`.app.json`](.app.json) | ChatGPT's registered development-app mapping for the same public MCP endpoint |
| [`skills/attenza/SKILL.md`](skills/attenza/SKILL.md) | When to use Attenza (`decide` / `clarify`) versus chat; `inform` is unavailable until in-product notify policy |
| [`skills/attenza-intervention/SKILL.md`](skills/attenza-intervention/SKILL.md) | Shared decide workflow: create, wait contract, host adapters, poll, expiry, and resume |
| [`skills/attenza-intervention/references`](skills/attenza-intervention/references) | Shared A2UI schema profile and decision-interface guidance loaded by the skill when authoring a surface |
| [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) | ChatGPT/Codex-native discovery, app mapping, and MCP wiring |
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | Claude Code-native discovery and MCP wiring |

The MCP URL is `https://www.attenza.io/mcp`. Authentication is OAuth. Do not add API keys, bearer tokens, or private capability URLs.

## How hosts consume it

Point the host at this package directory, not the repository root.

| Host | Documented install path |
| --- | --- |
| [Cursor](../../integrations/cursor) | Desktop: symlink or copy this folder to `~/.cursor/plugins/local/attenza`. Cloud Agents: attach the MCP server in cursor.com/agents; they do not load this folder from a repo checkout. |
| [GrokBot](../../integrations/grokbot) | Same Cursor plugin, installed from a Cursor marketplace the account can see (team import or public listing). GrokBot does not read `~/.cursor/plugins/local`. |
| [ChatGPT and Codex](../../integrations/codex) | Install `attenza` from the repository's `.agents/plugins/marketplace.json` |
| [Claude Code](../../integrations/claude-code) | Install `attenza` from the repository's `.claude-plugin/marketplace.json` |

Vendor-specific setup lives under `integrations/<host>/`. The native manifests contain only discovery metadata and the host-specific spelling of the public MCP connection; shared behavior stays in the skills.

## Where guidance belongs

- Put behavior that every agent should follow in the shared skills or their references. When-to-escalate guidance belongs in `skills/attenza`. A2UI construction, decision design, wait contract, host wait adapters, polling, expiry, and terminal-result handling belong in `skills/attenza-intervention`.
- Put human-facing installation, publication, and host verification steps in `integrations/<host>/README.md`. Hosts do not load these README files as agent instructions.
- Add a host-specific skill reference only when that host requires genuinely different runtime behavior. Link it conditionally from the shared skill; do not copy the whole skill into a host folder. Host wait adapters for `decide` already live in `skills/attenza-intervention`; do not duplicate them under `integrations/`.
- Keep discovery-only differences in the native manifest or marketplace file that requires them.
