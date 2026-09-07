from __future__ import annotations

import ast
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://staging.attenza.io/mcp"
CANONICAL_SKILL = "packages/attenza-plugin/skills/attenza-intervention/SKILL.md"
CANONICAL_MCP = "packages/attenza-plugin/mcp.json"
CANONICAL_PLUGIN = "packages/attenza-plugin/plugin.json"
REQUIRED = (
    CANONICAL_PLUGIN,
    CANONICAL_MCP,
    "packages/attenza-plugin/README.md",
    "integrations/cursor/README.md",
    "integrations/grokbot/README.md",
    "integrations/codex/README.md",
    "integrations/claude-code/README.md",
    CANONICAL_SKILL,
    "src/attenza_cli/cli.py",
    "schemas/intervention.schema.json",
    "examples/release-approval.json",
)
ALLOWED_INTEGRATIONS = {"cursor", "grokbot", "codex", "claude-code"}
FORBIDDEN_PRIVATE_ROOTS = {"apps", "deploy", "infrastructure", "migrations", "terraform"}
FORBIDDEN_OLD_ROOTS = {".agents", ".claude-plugin", "agent-plugins", "claude-plugins", "platforms", "plugins"}
FORBIDDEN_ROOT_PLUGIN_PATHS = ("plugin.json", "mcp.json", "skills")
GENERATED_PARTS = {".git", ".venv", "__pycache__", "build", "dist"}
SECRET_PATTERNS = (
    re.compile(r"https://staging\.attenza\.io/mcp/[A-Za-z0-9_-]+"),
    re.compile(r"\b(?:ata|sk|ghp|github_pat)_[A-Za-z0-9_-]{16,}"),
    re.compile(r'"(?:access_token|refresh_token|client_secret)"\s*:\s*".+"', re.I),
)


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(relative_path: str) -> Any:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def tracked_files(pattern: str) -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob(pattern)
        if path.is_file() and not GENERATED_PARTS.intersection(path.relative_to(ROOT).parts)
    )


def main() -> None:
    for relative_path in REQUIRED:
        if not (ROOT / relative_path).is_file():
            fail(f"required file is missing: {relative_path}")

    for leftover in FORBIDDEN_ROOT_PLUGIN_PATHS:
        if (ROOT / leftover).exists():
            fail(f"{leftover} must live only under packages/attenza-plugin/")

    for directory in FORBIDDEN_PRIVATE_ROOTS | FORBIDDEN_OLD_ROOTS:
        if (ROOT / directory).exists():
            fail(f"out-of-scope directory must not enter this repository: {directory}/")

    integration_root = ROOT / "integrations"
    integration_names = {
        path.name for path in integration_root.iterdir() if path.is_dir()
    }
    if integration_names != ALLOWED_INTEGRATIONS:
        fail(f"integrations must be exactly: {', '.join(sorted(ALLOWED_INTEGRATIONS))}")
    for path in sorted(integration_root.rglob("*")):
        if path.is_file() and path.name != "README.md":
            fail(
                "integrations may only contain README.md files, "
                f"found {path.relative_to(ROOT)}"
            )

    skill_files = [path.relative_to(ROOT).as_posix() for path in tracked_files("SKILL.md")]
    if skill_files != [CANONICAL_SKILL]:
        fail(f"skill copies must be exactly {CANONICAL_SKILL}; found {skill_files}")

    mcp_files = [path.relative_to(ROOT).as_posix() for path in tracked_files("mcp.json")]
    if mcp_files != [CANONICAL_MCP]:
        fail(f"MCP manifests must be exactly {CANONICAL_MCP}; found {mcp_files}")

    plugin_files = [path.relative_to(ROOT).as_posix() for path in tracked_files("plugin.json")]
    if plugin_files != [CANONICAL_PLUGIN]:
        fail(f"plugin manifests must be exactly {CANONICAL_PLUGIN}; found {plugin_files}")

    json_files = tracked_files("*.json")
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")

    for path in sorted((ROOT / "scripts").glob("*.py")):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            fail(f"invalid Python in {path.relative_to(ROOT)}: {exc}")
    for path in sorted((ROOT / "src").rglob("*.py")) + sorted(
        (ROOT / "tests").glob("*.py")
    ):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            fail(f"invalid Python in {path.relative_to(ROOT)}: {exc}")

    mcp = load_json(CANONICAL_MCP)
    try:
        configured_endpoint = mcp["mcpServers"]["attenza"]["url"]
    except (KeyError, TypeError) as exc:
        fail(f"plugin MCP manifest has an invalid shape: {exc}")
    if configured_endpoint != ENDPOINT:
        fail("plugin MCP manifest does not contain the canonical endpoint")

    package = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
        "project"
    ]
    plugin = load_json(CANONICAL_PLUGIN)
    source_version = re.search(
        r'^__version__ = "([^"]+)"$',
        (ROOT / "src/attenza_cli/__init__.py").read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if (
        plugin.get("name") != "attenza"
        or plugin.get("version") != package["version"]
        or source_version is None
        or source_version.group(1) != package["version"]
    ):
        fail("plugin identity or version has drifted from the CLI package")

    for path in ROOT.rglob("*"):
        relative_path = path.relative_to(ROOT)
        if not path.is_file() or GENERATED_PARTS.intersection(relative_path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(f"possible credential or private capability URL in {relative_path}")

    print(
        f"ok: {len(json_files)} JSON files, one skill, and "
        f"{len(integration_names)} focused integrations validated"
    )


if __name__ == "__main__":
    main()
