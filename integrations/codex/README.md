# ChatGPT and Codex

ChatGPT and Codex consume the same shared package through its OpenAI plugin manifest and repository marketplace. Do not copy `SKILL.md` into this folder.

## Portable package

[`packages/attenza-plugin`](../../packages/attenza-plugin) remains an [Agent Plugins 1.0](https://github.com/agentplugins/agent-plugins-spec) root. Codex discovers the same package through the required [`.codex-plugin/plugin.json`](../../packages/attenza-plugin/.codex-plugin/plugin.json); that manifest exposes the shared skills directory and the OAuth MCP endpoint using Codex's native fields.

The package's [`.app.json`](../../packages/attenza-plugin/.app.json) maps Attenza to the OAuth MCP app registered in ChatGPT developer mode. It uses the underlying `asdk_app_...` ID, not the `plugin_asdk_app_...` URL identifier, and marks the app as required so the complete plugin cannot be installed without its tools.

The public repository includes [`.agents/plugins/marketplace.json`](../../.agents/plugins/marketplace.json). The repository being public does not make the plugin listing public. There are two private test routes.

### Personal local marketplace

Add the repository marketplace and install Attenza on the development computer:

```sh
codex plugin marketplace add maxhillaert/attenza-integrations
codex plugin add attenza@attenza-integrations
```

Restart the Codex app, open Plugins, select **Attenza integrations**, and enable **Attenza**. The first MCP use starts the browser OAuth flow; no API key or private capability URL is required.

This installs the complete package locally: the registered app mapping supplies `https://www.attenza.io/mcp`, while the bundled skills supply when-to-escalate guidance plus the polling, expiry, and A2UI decision workflow. Start a new ChatGPT Work or Codex conversation after every install or update. A raw developer-mode MCP connection tests the tools only and is not a substitute for this package test.

### Private workspace marketplace

A ChatGPT workspace admin can import this repository without submitting Attenza to the public plugin directory:

1. Open **Admin > Plugins > Add > Import marketplace**.
2. Set **Source** to `https://github.com/maxhillaert/attenza-integrations`.
3. Leave **Path** empty so ChatGPT discovers `.agents/plugins/marketplace.json` at the repository root.
4. Select the branch or commit to test, import the marketplace, and review the import result.
5. Make Attenza available to the intended role, enable its required app, install it, authenticate, and start a new chat.

The repository can be public or private; workspace import does not publish the plugin to the universal directory. Use **Sync now** after pushing a test update. The importing GitHub account must be able to read the repository.

The shared portable package also contains `mcp.json` for Cursor and other direct MCP hosts. OpenAI currently marks a workspace-imported package that declares `mcp.json` as desktop-only, even when it uses remote HTTPS. Therefore this shared package is suitable for private desktop testing today, but a mobile-capable workspace listing will need an OpenAI-specific package that references only the registered `.app.json` and bundled skills, without portable MCP configuration.

For development from a checkout, Codex also discovers the repo marketplace at `.agents/plugins/marketplace.json`. Run the repository gate after changing the native manifest:

```sh
mise run check
```

Read [`skills/attenza/SKILL.md`](../../packages/attenza-plugin/skills/attenza/SKILL.md) when deciding whether to escalate. The create/poll/resume path remains [`skills/attenza-intervention/SKILL.md`](../../packages/attenza-plugin/skills/attenza-intervention/SKILL.md). If a run must end before the task is terminal, preserve `task.id` so a later or scheduled wake polls that task instead of creating a duplicate.
