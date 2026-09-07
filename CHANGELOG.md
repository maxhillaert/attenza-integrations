# Changelog

## [Unreleased]

## [0.3.0] - 2026-09-07

- Moved the portable Agent Plugin from the repository root to `packages/attenza-plugin/` so multiple hosts can share one skill and one MCP config.
- Updated Cursor local testing to symlink or copy that package directory to `~/.cursor/plugins/local/attenza` instead of the repository root.
- Added Codex and Claude Code integration notes. Vendor overlays (`.codex-plugin`, `.claude-plugin` / `.mcp.json`) are documented as follow-ups, not copied trees.
- Taught the intervention skill to preserve `task.id` for a later or scheduled wake when the host must end before a terminal state.
- This is a breaking path change for anyone who installed the repository root as a Cursor plugin.

## [0.2.0] - 2026-09-07

- Made the portable Agent Plugin ready for Cursor marketplace and GrokBot discovery.
- Taught the intervention skill to poll immediately with bounded backoff and resume only from a terminal result.
- Documented absolute and relative expiry, and made the CLI wait honor the server deadline.
- Recorded the successful GrokBot custom OAuth MCP round trip.

## [0.1.0] - 2026-09-07

- Added the public OAuth MCP manifest and intervention skill.
- Added the dependency-free Attenza CLI, JSON Schema, and synthetic example.
- Added focused Cursor integration instructions.
- Recorded GrokBot as the next planned public integration.

[Unreleased]: https://github.com/maxhillaert/attenza-integrations/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/maxhillaert/attenza-integrations/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/maxhillaert/attenza-integrations/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/maxhillaert/attenza-integrations/releases/tag/v0.1.0
