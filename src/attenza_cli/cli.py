from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from . import __version__
from .client import AttenzaError, Client, DEFAULT_SERVER, clear_credentials, load_credentials, login


TERMINAL_STATES = {
    "TASK_STATE_COMPLETED",
    "TASK_STATE_CANCELED",
    "TASK_STATE_FAILED",
    "TASK_STATE_REJECTED",
}


def _print(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False))


def _load_object(path: str) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AttenzaError(f"cannot read intervention JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise AttenzaError("intervention JSON must contain an object")
    value.pop("$schema", None)
    required = {"title", "summary", "source", "message_id", "a2ui_messages"}
    missing = sorted(required - value.keys())
    if missing:
        raise AttenzaError(f"intervention JSON is missing: {', '.join(missing)}")
    return value


def _task_state(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    task = value.get("task")
    if not isinstance(task, dict):
        return None
    status = task.get("status")
    return str(status.get("state")) if isinstance(status, dict) and status.get("state") else None


def _task_expiry(value: Any) -> float | None:
    if not isinstance(value, dict) or not isinstance(value.get("task"), dict):
        return None
    metadata = value["task"].get("metadata")
    expires_at = metadata.get("expiresAt") if isinstance(metadata, dict) else None
    if not isinstance(expires_at, str):
        return None
    try:
        return datetime.fromisoformat(expires_at.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create and monitor Attenza human decisions")
    parser.add_argument("--version", action="version", version=f"attenza {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    login_parser = commands.add_parser("login", help="Authorize this CLI through Attenza OAuth")
    login_parser.add_argument("--server", default=DEFAULT_SERVER)
    login_parser.add_argument("--no-browser", action="store_true")
    commands.add_parser("logout", help="Delete locally stored OAuth credentials")
    commands.add_parser("status", help="Verify the current connection")
    commands.add_parser("tools", help="List available Attenza MCP tools")

    create_parser = commands.add_parser("create", help="Create an intervention from JSON")
    create_parser.add_argument("request_json")
    get_parser = commands.add_parser("get", help="Read an intervention")
    get_parser.add_argument("task_id")
    wait_parser = commands.add_parser("wait", help="Poll until an intervention is terminal")
    wait_parser.add_argument("task_id")
    wait_parser.add_argument("--deadline", type=int, default=86_400)
    wait_parser.add_argument("--interval", type=float, default=5.0)
    cancel_parser = commands.add_parser("cancel", help="Cancel a pending intervention")
    cancel_parser.add_argument("task_id")
    return parser


def run(args: argparse.Namespace) -> None:
    if args.command == "login":
        credentials = login(args.server, open_browser=not args.no_browser)
        print(f"Authorized Attenza with scopes: {credentials.scope}")
        return
    if args.command == "logout":
        print("Deleted local Attenza credentials." if clear_credentials() else "No local credentials found.")
        return

    client = Client()
    if args.command == "status":
        credentials = load_credentials()
        tools = client.tools()
        _print({"connected": True, "server": credentials.server_url, "scopes": credentials.scope.split(), "tools": [tool.get("name") for tool in tools]})
    elif args.command == "tools":
        _print(client.tools())
    elif args.command == "create":
        _print(client.call("create_intervention", _load_object(args.request_json)))
    elif args.command == "get":
        _print(client.call("get_intervention", {"task_id": args.task_id}))
    elif args.command == "cancel":
        _print(client.call("cancel_intervention", {"task_id": args.task_id}))
    elif args.command == "wait":
        deadline = time.time() + args.deadline
        value: Any = {}
        while time.time() < deadline:
            value = client.call("get_intervention", {"task_id": args.task_id})
            if _task_state(value) in TERMINAL_STATES:
                _print(value)
                return
            task_expiry = _task_expiry(value)
            if task_expiry is not None:
                deadline = min(deadline, task_expiry)
            time.sleep(max(0, min(args.interval, deadline - time.time())))
        _print(value)
        raise AttenzaError("deadline elapsed before the intervention became terminal")


def main() -> None:
    try:
        run(build_parser().parse_args())
    except AttenzaError as exc:
        print(f"attenza: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
