# GrokBot

GrokBot is the second planned integration target.

The current Grok iOS plugin settings do not expose a field for installing a bespoke remote MCP server. A user-specific URL is not an acceptable publication mechanism, so this repository intentionally does not contain a speculative Grok manifest or a private capability link.

The intended public integration will use the shared OAuth endpoint:

```text
https://staging.attenza.io/mcp
```

Next steps:

1. Identify xAI's supported public plugin submission and manifest format.
2. Add only the required GrokBot artifact here.
3. Test OAuth, tool discovery, intervention creation, waiting, and revocation end to end.
4. Update the status table in the root README with evidence.
