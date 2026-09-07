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
REQUIRED = (
    ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json",
    "plugins/attenza/.codex-plugin/plugin.json",
    "plugins/attenza/.mcp.json",
    "claude-plugins/attenza/.claude-plugin/plugin.json",
    "claude-plugins/attenza/.mcp.json",
    "agent-plugins/attenza/plugin.json",
    "agent-plugins/attenza/mcp.json",
    "skills/attenza-intervention/SKILL.md",
    "pyproject.toml",
    "src/attenza_cli/cli.py",
    "schemas/intervention.schema.json",
    "examples/release-approval.json",
)
SKILL_COPIES = (
    "plugins/attenza/skills/attenza-intervention/SKILL.md",
    "claude-plugins/attenza/skills/attenza-intervention/SKILL.md",
    "agent-plugins/attenza/skills/attenza-intervention/SKILL.md",
)
FORBIDDEN_PRIVATE_ROOTS = ("apps", "deploy", "infrastructure", "migrations", "terraform")
GENERATED_PARTS = {".git", ".venv", "__pycache__", "build", "dist"}
SECRET_PATTERNS = (
    re.compile(r"https://staging\.attenza\.io/mcp/[A-Za-z0-9_-]+"),
    re.compile(r"\b(?:ata|sk|ghp|github_pat)_[A-Za-z0-9_-]{16,}"),
    re.compile(r'"(?:access_token|refresh_token|client_secret)"\s*:\s*".+"', re.I),
)


def load_json(relative_path: str) -> Any:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    for directory in FORBIDDEN_PRIVATE_ROOTS:
        if (ROOT / directory).exists():
            fail(f"private application surface must not enter this repository: {directory}/")

    for relative_path in REQUIRED:
        if not (ROOT / relative_path).is_file():
            fail(f"required file is missing: {relative_path}")

    json_files = sorted(ROOT.rglob("*.json"))
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
    for path in sorted((ROOT / "src").rglob("*.py")) + sorted((ROOT / "tests").glob("*.py")):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            fail(f"invalid Python in {path.relative_to(ROOT)}: {exc}")

    endpoint = load_json("config/endpoint.json")
    if endpoint.get("mcpUrl") != ENDPOINT:
        fail("config/endpoint.json does not contain the canonical MCP endpoint")

    mcp_files = (
        "plugins/attenza/.mcp.json",
        "claude-plugins/attenza/.mcp.json",
        "agent-plugins/attenza/mcp.json",
        "platforms/claude-code/mcp.json",
        "platforms/cursor/mcp.json",
        "platforms/github-copilot/mcp.json",
        "platforms/gemini-cli/settings.json",
        "platforms/vscode/mcp.json",
        "platforms/windsurf/mcp_config.json",
    )
    for relative_path in mcp_files:
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if ENDPOINT not in text:
            fail(f"canonical endpoint is missing from {relative_path}")

    source_skill = (ROOT / "skills/attenza-intervention/SKILL.md").read_bytes()
    for relative_path in SKILL_COPIES:
        if (ROOT / relative_path).read_bytes() != source_skill:
            fail(f"skill copy has drifted: {relative_path}; run mise run sync")

    codex_manifest = load_json("plugins/attenza/.codex-plugin/plugin.json")
    package = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    package_version = package["version"]
    if codex_manifest.get("name") != "attenza" or codex_manifest.get("version") != package_version:
        fail("Codex manifest identity or version is invalid")
    if codex_manifest.get("mcpServers") != "./.mcp.json":
        fail("Codex manifest must reference its packaged MCP configuration")

    codex_marketplace = load_json(".agents/plugins/marketplace.json")
    if codex_marketplace.get("name") != "attenza":
        fail("Codex marketplace must be named attenza")
    codex_source = codex_marketplace["plugins"][0]["source"]["path"]
    if not (ROOT / codex_source).is_dir():
        fail("Codex marketplace source does not exist")

    claude_marketplace = load_json(".claude-plugin/marketplace.json")
    if claude_marketplace.get("name") != "attenza":
        fail("Claude marketplace must be named attenza")
    if not (ROOT / claude_marketplace["plugins"][0]["source"]).is_dir():
        fail("Claude marketplace source does not exist")

    versioned_manifests = (
        "claude-plugins/attenza/.claude-plugin/plugin.json",
        "agent-plugins/attenza/plugin.json",
    )
    for relative_path in versioned_manifests:
        if load_json(relative_path).get("version") != package_version:
            fail(f"package version has drifted in {relative_path}")

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

    print(f"ok: {len(json_files)} JSON files and {len(SKILL_COPIES)} skill copies validated")


if __name__ == "__main__":
    main()
