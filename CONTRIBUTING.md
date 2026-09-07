# Contributing

Thank you for improving Attenza's agent integrations.

## Before opening a pull request

1. Keep one platform or one shared behavior change per pull request.
2. Never commit credentials, OAuth tokens, authorization codes, private capability URLs, personal email addresses, or real task payloads.
3. Put reusable behavior only in `packages/attenza-plugin/skills/attenza-intervention/SKILL.md`; do not create vendor copies.
4. Use the canonical endpoint from `packages/attenza-plugin/mcp.json`. A host-native manifest may repeat that public URL only when its format requires different MCP syntax; add it to the drift checks in `scripts/check.py`.
5. Keep `integrations/<vendor>/` as human documentation only. Put executable discovery metadata in the shared package or the host's repository marketplace.
6. New hosts need a README, a native manifest or documented portable path, and an `ALLOWED_INTEGRATIONS` update in `scripts/check.py`.
7. Run `mise run check`.

CLI changes must remain dependency-free unless a dependency brings a clear interoperability or security benefit. Add unit tests for token handling, transport parsing, and payload behavior without calling the live service.

Do not claim support for an installation or marketplace format that the platform does not publicly document. State honestly when a platform requires marketplace review, a vendor overlay (`.claude-plugin`, `.codex-plugin`), or does not support user-installed remote MCP.

## Releases

Packages use semantic versions. Update every changed package manifest and `CHANGELOG.md` in the same pull request. Tags use `vMAJOR.MINOR.PATCH`.
