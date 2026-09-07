# Attenza integrations

[![CI](https://github.com/maxhillaert/attenza-integrations/actions/workflows/ci.yml/badge.svg)](https://github.com/maxhillaert/attenza-integrations/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

The small public integration kit for [Attenza](https://staging.attenza.io). It contains only the client-side pieces needed to connect agents to Attenza: a CLI, one agent skill, one portable plugin manifest, and focused setup notes.

The Attenza application, API implementation, database, deployment, and infrastructure remain in a separate private repository.

## Integration status

| Integration | Available now | Currently tested | Next step |
| --- | --- | --- | --- |
| Cursor remote MCP | [`mcp.json`](mcp.json) points to the public OAuth endpoint | Live OAuth discovery and unauthenticated MCP challenge; repository validation | Complete a real Cursor OAuth login and intervention round trip |
| Cursor Agent Plugin | Root [`plugin.json`](plugin.json), MCP manifest, and skill form one portable package | Manifest structure and CI checks | Install from GitHub in Cursor and verify skill discovery |
| GrokBot | Public OAuth MCP endpoint is ready for a future listing | Current Grok iOS UI has no bespoke MCP field; no end-to-end test yet | Establish xAI's public plugin submission format and publish it |
| Attenza CLI | Browser OAuth, create, get, wait, cancel, and token refresh | Six unit tests, clean wheel build, and isolated install | Complete one interactive OAuth and intervention smoke test |

We are intentionally taking integrations one at a time. Other agent platforms are out of scope until Cursor and GrokBot are working end to end.

## What every folder is for

| Path | Why it exists |
| --- | --- |
| [`integrations/cursor`](integrations/cursor) | Cursor-specific setup and testing notes |
| [`integrations/grokbot`](integrations/grokbot) | GrokBot publication status and next steps |
| [`skills/attenza-intervention`](skills/attenza-intervention) | The single canonical instruction set that teaches an agent when to pause and how to resume |
| [`src/attenza_cli`](src/attenza_cli) | The dependency-free `attenza` command-line client |
| [`examples`](examples) | Synthetic intervention payloads for testing |
| [`schemas`](schemas) | The public JSON shape accepted by the CLI |
| [`scripts`](scripts) | Repository boundary, manifest, and secret-leak checks |
| [`tests`](tests) | CLI unit tests; they do not contact a live account |

At the repository root, `plugin.json`, `mcp.json`, and `skills/` together are the portable Agent Plugin. Keeping them at the root means there is no second copied plugin tree and no duplicated skill. `.github`, `mise.toml`, `pyproject.toml`, and the policy files are ordinary public-repository maintenance files.

## Public endpoint

OAuth-capable MCP clients connect to:

```text
https://staging.attenza.io/mcp
```

The client discovers Attenza OAuth, opens sign-in and consent, and receives revocable user-scoped access. Do not publish API keys, OAuth tokens, authorization codes, or legacy capability URLs.

## CLI

```sh
uv tool install git+https://github.com/maxhillaert/attenza-integrations.git
attenza login
attenza create examples/release-approval.json
attenza wait TASK_ID
```

The CLI stores its OAuth tokens only in the user's local configuration directory. Run `attenza logout` locally and revoke the connection in Attenza when it is no longer required.

## Develop

```sh
mise install
mise run check
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) before contributing.
