# Attenza integrations

[![CI](https://github.com/maxhillaert/attenza-integrations/actions/workflows/ci.yml/badge.svg)](https://github.com/maxhillaert/attenza-integrations/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

The public multi-host integration kit for [Attenza](https://staging.attenza.io). It contains only the client-side pieces needed to connect agents to Attenza: a CLI, one portable Agent Plugin, and focused setup notes per host.

The Attenza application, API implementation, database, deployment, and infrastructure remain in a separate private repository.

## Integration status

| Integration | Available now | Currently tested | Next step |
| --- | --- | --- | --- |
| Cursor remote MCP | [`packages/attenza-plugin/mcp.json`](packages/attenza-plugin/mcp.json) points to the public OAuth endpoint | OAuth and MCP contract tested by Attenza; repository validation | Complete a real Cursor intervention round trip |
| Cursor Agent Plugin | [`packages/attenza-plugin`](packages/attenza-plugin) is the portable package (`plugin.json`, MCP manifest, polling skill) | Manifest structure and CI checks | Symlink the package locally, verify skill discovery, then submit to the marketplace |
| GrokBot custom connector | Shared OAuth endpoint works without a private URL | OAuth, tool discovery, intervention creation, human decision, and result retrieval tested end to end | Retain as the direct integration path |
| GrokBot plugin | The same Agent Plugin adds polling and expiry behavior to the MCP endpoint | Package validation; raw MCP round trip tested | Publish through the Cursor marketplace and verify catalog installation |
| Codex | Portable Agent Plugins 1.0 root; see [`integrations/codex`](integrations/codex) | Documentation and package layout | Load the package as an Agent Plugins root; add `.codex-plugin` later only if required |
| Claude Code | Planned `.claude-plugin` plus `.mcp.json` shim; see [`integrations/claude-code`](integrations/claude-code) | Documentation only | Add host shims without copying the skill or MCP URL |
| Attenza CLI | Browser OAuth, create, get, wait, cancel, and token refresh | Seven unit tests, clean wheel build, and isolated install | Complete one interactive OAuth and intervention smoke test |

Cursor and GrokBot remain the tested hosts. Codex and Claude Code are documented so later overlays can attach to the same plugin package instead of forking it.

## What every folder is for

| Path | Why it exists |
| --- | --- |
| [`packages/attenza-plugin`](packages/attenza-plugin) | Portable Agent Plugin: one manifest, one MCP config, one skill. Hosts consume this directory. |
| [`integrations/cursor`](integrations/cursor) | Cursor-specific setup and local test notes |
| [`integrations/grokbot`](integrations/grokbot) | GrokBot publication status and next steps |
| [`integrations/codex`](integrations/codex) | Codex / Agent Plugins install notes |
| [`integrations/claude-code`](integrations/claude-code) | Planned Claude Code overlay notes |
| [`src/attenza_cli`](src/attenza_cli) | The dependency-free `attenza` command-line client |
| [`examples`](examples) | Synthetic intervention payloads for testing |
| [`schemas`](schemas) | The public JSON shape accepted by the CLI |
| [`scripts`](scripts) | Repository boundary, manifest, and secret-leak checks |
| [`tests`](tests) | CLI unit tests; they do not contact a live account |

The CLI, examples, schemas, tests, and scripts stay at the repository root as siblings of the plugin package. `.github`, `mise.toml`, `pyproject.toml`, and the policy files are ordinary public-repository maintenance files.

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

For a local Cursor plugin test, symlink or copy the portable package rather than the repository root:

```sh
mkdir -p ~/.cursor/plugins/local
ln -sfn "$PWD/packages/attenza-plugin" ~/.cursor/plugins/local/attenza
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) before contributing.
