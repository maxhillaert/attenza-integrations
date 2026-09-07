# Platform support

Attenza has one public OAuth MCP endpoint. Platform packages add discovery and behavior guidance; they do not create different Attenza credentials.

| Platform | Installation path | Status |
| --- | --- | --- |
| ChatGPT | Add the remote MCP server as a custom connector/app | Ready for developer testing |
| Claude.ai | Add the remote MCP connector | Ready where custom connectors are enabled |
| Claude Code | Install the `attenza@attenza` marketplace plugin | Ready |
| Codex | Install `plugins/attenza` from the repository marketplace | Ready |
| Cursor | Add the checked-in `mcp.json` or portable Agent Plugin | Ready |
| GitHub Copilot | Add the repository MCP configuration | Ready |
| Gemini CLI | Add the checked-in settings fragment | Ready |
| VS Code | Add the workspace MCP configuration | Ready |
| Windsurf | Add the checked-in MCP configuration | Ready |
| Grok | Public plugin listing is required; Grok iOS does not expose bespoke MCP setup | Publication adapter pending |

Every ready path points to `https://staging.attenza.io/mcp` and relies on the host to complete OAuth. If a host cannot perform OAuth for remote MCP, do not paste a private capability URL into a public or shared configuration.
