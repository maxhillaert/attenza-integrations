# ChatGPT and Codex

ChatGPT and Codex consume the same shared package through its OpenAI plugin manifest and repository marketplace. Do not copy `SKILL.md` into this folder.

## Portable package

[`packages/attenza-plugin`](../../packages/attenza-plugin) remains an [Agent Plugins 1.0](https://github.com/agentplugins/agent-plugins-spec) root. Codex discovers the same package through the required [`.codex-plugin/plugin.json`](../../packages/attenza-plugin/.codex-plugin/plugin.json); that manifest exposes the shared skills directory and the OAuth MCP endpoint using Codex's native fields.

The package's [`.app.json`](../../packages/attenza-plugin/.app.json) maps Attenza to the OAuth MCP app registered in ChatGPT developer mode. The public repository includes [`.agents/plugins/marketplace.json`](../../.agents/plugins/marketplace.json). Add the marketplace and install Attenza:

```sh
codex plugin marketplace add maxhillaert/attenza-integrations
codex plugin add attenza@attenza-integrations
```

Restart the Codex app, open Plugins, select **Attenza integrations**, and enable **Attenza**. The first MCP use starts the browser OAuth flow; no API key or private capability URL is required.

For a ChatGPT developer test, enable developer mode, install Attenza from the local repository marketplace, and start a new conversation with the plugin enabled. The registered app mapping supplies the same `https://www.attenza.io/mcp` connection, while the bundled skills supply when-to-escalate guidance plus the polling, expiry, and A2UI decision workflow.

For development from a checkout, Codex also discovers the repo marketplace at `.agents/plugins/marketplace.json`. Run the repository gate after changing the native manifest:

```sh
mise run check
```

Read [`skills/attenza/SKILL.md`](../../packages/attenza-plugin/skills/attenza/SKILL.md) when deciding whether to escalate. The create/poll/resume path remains [`skills/attenza-intervention/SKILL.md`](../../packages/attenza-plugin/skills/attenza-intervention/SKILL.md). If a run must end before the task is terminal, preserve `task.id` so a later or scheduled wake polls that task instead of creating a duplicate.
