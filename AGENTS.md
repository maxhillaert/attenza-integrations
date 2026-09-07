# Repository guidance

This repository contains public discovery, configuration, and behavior packages for Attenza integrations.

## Invariants

- `packages/attenza-plugin/` is the only Agent Plugin root. Do not leave `plugin.json`, `mcp.json`, or `skills/` at the repository root.
- `packages/attenza-plugin/mcp.json` is the single MCP configuration and uses the canonical public URL.
- OAuth is the public authentication path. Never add user API keys, bearer tokens, authorization codes, client secrets, private capability URLs, personal email addresses, or real task data.
- `packages/attenza-plugin/skills/attenza-intervention/SKILL.md` is the only skill copy. Never duplicate it per host.
- `integrations/` is human documentation only. Current hosts: `cursor`, `grokbot`, `codex`, and `claude-code`.
- Keep vendor-specific setup under `integrations/<vendor>` and shared behavior out of vendor documentation.
- Do not claim support for an installation or marketplace format that the platform does not publicly document.
- Update changed package versions and `CHANGELOG.md` together.

Run `mise run check` before opening a pull request.
