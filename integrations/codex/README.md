# Codex

Codex consumes the same shared package through its native plugin manifest and repository marketplace. Do not copy `SKILL.md` into this folder.

## Portable package

[`packages/attenza-plugin`](../../packages/attenza-plugin) remains an [Agent Plugins 1.0](https://github.com/agentplugins/agent-plugins-spec) root. Codex discovers the same package through the required [`.codex-plugin/plugin.json`](../../packages/attenza-plugin/.codex-plugin/plugin.json); that manifest exposes the canonical skill and the OAuth MCP endpoint using Codex's native fields.

The public repository includes [`.agents/plugins/marketplace.json`](../../.agents/plugins/marketplace.json). Add the marketplace and install Attenza:

```sh
codex plugin marketplace add maxhillaert/attenza-integrations
codex plugin add attenza@attenza-integrations
```

Restart the Codex app, open Plugins, select **Attenza integrations**, and enable **Attenza**. The first MCP use starts the browser OAuth flow; no API key or private capability URL is required.

For development from a checkout, Codex also discovers the repo marketplace at `.agents/plugins/marketplace.json`. Run the repository gate after changing the native manifest:

```sh
mise run check
```

The canonical behavior remains [`skills/attenza-intervention/SKILL.md`](../../packages/attenza-plugin/skills/attenza-intervention/SKILL.md). If a run must end before the task is terminal, preserve `task.id` so a later or scheduled wake polls that task instead of creating a duplicate.
