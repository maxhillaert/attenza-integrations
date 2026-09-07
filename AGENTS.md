# Repository guidance

This repository contains public discovery, configuration, and behavior packages for Attenza integrations.

## Invariants

- Every remote MCP configuration uses the canonical URL in `config/endpoint.json`.
- OAuth is the public authentication path. Never add user API keys, bearer tokens, authorization codes, client secrets, private capability URLs, personal email addresses, or real task data.
- `skills/attenza-intervention/SKILL.md` is canonical. After editing it, run `mise run sync` and commit all package copies.
- Keep vendor-specific setup under `platforms/<vendor>` and shared behavior out of vendor documentation.
- Do not claim support for an installation or marketplace format that the platform does not publicly document.
- Update changed package versions and `CHANGELOG.md` together.

Run `mise run check` before opening a pull request.
