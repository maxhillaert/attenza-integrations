# Attenza integrations

[![CI](https://github.com/maxhillaert/attenza-integrations/actions/workflows/ci.yml/badge.svg)](https://github.com/maxhillaert/attenza-integrations/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Public integrations for [Attenza](https://staging.attenza.io), the durable human-decision inbox for AI agents.

An agent can pause consequential work, post an interactive decision to its human owner's Attenza timeline, and resume from the recorded answer. Every user connects through OAuth; integrations contain one public MCP URL and never contain API keys, shared secrets, or private capability links.

> Attenza is currently in public beta. The canonical endpoint is `https://staging.attenza.io/mcp` until the production domain launches.

## Start here

If your agent supports remote MCP with OAuth, add:

```text
https://staging.attenza.io/mcp
```

The client discovers Attenza's OAuth server, opens sign-in and consent, and receives a revocable connection scoped to that user. A useful smoke test is:

> Ask me which environment to deploy to, send the choices to Attenza, and wait for my answer.

## Packages

| Package | Purpose |
| --- | --- |
| [`plugins/attenza`](plugins/attenza) | Codex plugin with OAuth MCP and intervention guidance |
| [`claude-plugins/attenza`](claude-plugins/attenza) | Claude Code plugin with the same behavior |
| [`agent-plugins/attenza`](agent-plugins/attenza) | Portable Agent Plugins 1.0 package |
| [`platforms`](platforms) | Copyable configuration and platform-specific instructions |
| [`skills/attenza-intervention`](skills/attenza-intervention) | Canonical, vendor-neutral agent behavior |

See the [platform support matrix](platforms/README.md) to choose an installation path.

## What the agent receives

The MCP server exposes three tools:

- `create_intervention` creates an idempotent, durable decision task.
- `get_intervention` reads its current state and final decision.
- `cancel_intervention` stops a task that is no longer needed.

Creating, reading, and canceling are separate OAuth scopes. Revoking a connection in Attenza immediately blocks its access tokens.

## Repository layout

```text
.
├── .agents/plugins/          # Codex marketplace catalog
├── .claude-plugin/           # Claude Code marketplace catalog
├── agent-plugins/attenza/    # Portable Agent Plugins package
├── claude-plugins/attenza/   # Claude Code package
├── config/endpoint.json      # Canonical public integration contract
├── platforms/                # Host-specific setup and config
├── plugins/attenza/          # Codex package
├── scripts/                  # Dependency-free validation
└── skills/                   # Canonical shared behavior
```

## Develop

Install [mise](https://mise.jdx.dev/) and run:

```sh
mise install
mise run check
```

The checks use only Python's standard library. Run `mise run sync` after changing the canonical skill, then commit all synchronized copies. Platform submissions and store publication are tracked separately from the open-source packages.

## Security

Do not open a public issue for a vulnerability or include tokens, authorization codes, private capability URLs, or personal task data in a report. See [SECURITY.md](SECURITY.md).

## Contributing

Small, platform-focused pull requests are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before adding a new host or changing the shared agent behavior.
