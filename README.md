# Attenza integrations

[![CI](https://github.com/maxhillaert/attenza-integrations/actions/workflows/ci.yml/badge.svg)](https://github.com/maxhillaert/attenza-integrations/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

The public multi-host integration kit for [Attenza](https://www.attenza.io). It contains only the client-side pieces needed to connect agents to Attenza: a CLI, one portable Agent Plugin, and focused setup notes per host.

The Attenza application, API implementation, database, deployment, and infrastructure remain in a separate private repository.

## Integration status

| Integration | Available now | Currently tested | Next step |
| --- | --- | --- | --- |
| Cursor remote MCP | [`packages/attenza-plugin/mcp.json`](packages/attenza-plugin/mcp.json) points to the public OAuth endpoint | OAuth and MCP contract tested by Attenza; repository validation | Complete a real Cursor intervention round trip |
| Cursor Agent Plugin | [`packages/attenza-plugin`](packages/attenza-plugin) plus a repository [`marketplace.json`](.cursor-plugin/marketplace.json) | Manifest/schema checks; local-test layout and marketplace skill/MCP paths | Desktop Customize **or** a team-marketplace install; then public marketplace submission |
| GrokBot custom connector | Shared OAuth endpoint works without a private URL | OAuth, tool discovery, intervention creation, human decision, and result retrieval tested end to end | Retain as the direct integration path |
| GrokBot plugin | The same Agent Plugin adds polling and expiry behavior to the MCP endpoint | Package validation; raw MCP round trip tested | Import this repo as a Cursor team marketplace (or wait for public listing) and install from GrokBot Plugins |
| ChatGPT / Codex | Native [`.codex-plugin`](packages/attenza-plugin/.codex-plugin/plugin.json) manifest, registered [`.app.json`](packages/attenza-plugin/.app.json), and repo marketplace | ChatGPT developer-mode OAuth and discovery of all three Attenza actions; repository validation | Install the complete package from the local marketplace and complete an intervention round trip |
| Claude Code | Native [`.claude-plugin`](packages/attenza-plugin/.claude-plugin/plugin.json) manifest and repo marketplace | Manifest validation and repository discovery wiring | Install from the repo marketplace and complete an OAuth round trip |
| Attenza CLI | Browser OAuth, create, get, wait, cancel, and token refresh | Seven unit tests, clean wheel build, isolated install, and live production DCR + PKCE + token + authenticated `tools/list` smoke test | Complete a live create/wait intervention round trip |

Cursor and GrokBot remain the end-to-end tested hosts. ChatGPT developer-mode OAuth and tool discovery are recorded; a ChatGPT/Codex package install plus intervention round trip, and Claude Code's live OAuth round trip, remain.

## What every folder is for

| Path | Why it exists |
| --- | --- |
| [`packages/attenza-plugin`](packages/attenza-plugin) | Portable Agent Plugin: one manifest, one MCP config, one skill, and its shared A2UI authoring references. Hosts consume this directory. |
| [`.cursor-plugin`](.cursor-plugin) | Cursor repository marketplace pointing at the shared package |
| [`.agents/plugins`](.agents/plugins) | ChatGPT/Codex repository marketplace pointing at the shared package |
| [`.claude-plugin`](.claude-plugin) | Claude Code repository marketplace pointing at the shared package |
| [`integrations/cursor`](integrations/cursor) | Human-facing Cursor setup and local test notes; not agent instructions |
| [`integrations/grokbot`](integrations/grokbot) | Human-facing GrokBot publication status and test notes; not agent instructions |
| [`integrations/codex`](integrations/codex) | ChatGPT/Codex installation and test notes |
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
https://www.attenza.io/mcp
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

For a desktop Cursor plugin test, symlink or copy the portable package rather than the repository root. Desktop Cursor loads that folder from `~/.cursor/plugins/local`. GrokBot and Cloud Agents do not; they install from a Cursor marketplace or an attached MCP server. See [integrations/cursor](integrations/cursor) and [integrations/grokbot](integrations/grokbot).

```sh
mkdir -p ~/.cursor/plugins/local
ln -sfn "$PWD/packages/attenza-plugin" ~/.cursor/plugins/local/attenza
```

Codex and Claude Code install from the public repository marketplaces:

```sh
codex plugin marketplace add maxhillaert/attenza-integrations
codex plugin add attenza@attenza-integrations

claude plugin marketplace add maxhillaert/attenza-integrations
claude plugin install attenza@attenza-integrations
```

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) before contributing.
