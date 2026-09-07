# Claude

For Claude Code, prefer the repository marketplace plugin because it installs both the MCP server and the intervention skill:

```text
/plugin marketplace add maxhillaert/attenza-integrations
/plugin install attenza@attenza
```

For a direct local test, add the public endpoint:

```sh
claude mcp add --transport http attenza https://staging.attenza.io/mcp
```

Claude.ai users can add the same URL as a custom remote connector where their plan and workspace policy permit it.
