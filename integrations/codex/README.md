# Codex

Codex is a planned host for the same portable plugin. Do not copy `SKILL.md` or `mcp.json` into this folder.

## Portable package

[`packages/attenza-plugin`](../../packages/attenza-plugin) is an [Agent Plugins 1.0](https://github.com/agentplugins/agent-plugins-spec) root: `plugin.json`, `mcp.json`, and `skills/attenza-intervention/SKILL.md`. Hosts that load that layout can point at this directory as-is.

OpenAI's [plugin packaging docs](https://developers.openai.com/plugins/build/plugins) currently describe a Codex-specific overlay at `.codex-plugin/plugin.json`, with optional `.mcp.json`, `.app.json`, and a `hooks/` directory. This repository does **not** add those files yet:

- The portable root is the shared source of truth.
- Add `.codex-plugin` later only if Codex cannot load Agent Plugins 1.0 from `plugin.json` at the package root, or if Codex-specific hooks become necessary.
- Do not add hooks now, and do not fork the skill or MCP URL into a Codex tree.

## Try the shared MCP endpoint

Until a Codex overlay exists, register the public OAuth endpoint as a custom MCP server:

```text
https://staging.attenza.io/mcp
```

Follow [`packages/attenza-plugin/skills/attenza-intervention/SKILL.md`](../../packages/attenza-plugin/skills/attenza-intervention/SKILL.md) for create, poll, expiry, and resume behavior. If a Codex run must end before the task is terminal, preserve `task.id` so a later or scheduled wake can poll that task instead of creating a duplicate.
