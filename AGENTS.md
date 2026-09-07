# Repository guidance

This repository contains public discovery, configuration, and behavior packages for Attenza integrations.

## Invariants

- The root `mcp.json` is the single MCP configuration and uses the canonical public URL.
- OAuth is the public authentication path. Never add user API keys, bearer tokens, authorization codes, client secrets, private capability URLs, personal email addresses, or real task data.
- `skills/attenza-intervention/SKILL.md` is the only skill copy.
- Only `integrations/cursor` and `integrations/grokbot` are currently in scope.
- Keep vendor-specific setup under `integrations/<vendor>` and shared behavior out of vendor documentation.
- Do not claim support for an installation or marketplace format that the platform does not publicly document.
- Update changed package versions and `CHANGELOG.md` together.

Run `mise run check` before opening a pull request.
