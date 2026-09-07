# Contributing

Thank you for improving Attenza's agent integrations.

## Before opening a pull request

1. Keep one platform or one shared behavior change per pull request.
2. Never commit credentials, OAuth tokens, authorization codes, private capability URLs, personal email addresses, or real task payloads.
3. Put reusable behavior in `skills/attenza-intervention/SKILL.md`, then run `mise run sync` so packaged copies cannot drift.
4. Use the canonical endpoint from `config/endpoint.json`; do not create platform-specific service URLs.
5. Run `mise run check`.

For a new platform, add a directory under `platforms/` containing a short README and the smallest supported configuration file. State honestly when a platform requires marketplace review or does not support user-installed remote MCP.

## Releases

Packages use semantic versions. Update every changed package manifest and `CHANGELOG.md` in the same pull request. Tags use `vMAJOR.MINOR.PATCH`.
