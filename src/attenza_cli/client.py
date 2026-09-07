from __future__ import annotations

import base64
import hashlib
import json
import os
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from dataclasses import asdict, dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any


DEFAULT_SERVER = "https://staging.attenza.io/mcp"
SCOPES = "tasks:create tasks:read tasks:cancel"
PROTOCOL_VERSION = "2025-11-25"


class AttenzaError(RuntimeError):
    """A safe, user-facing Attenza client error."""


@dataclass(slots=True)
class Credentials:
    server_url: str
    client_id: str
    access_token: str
    refresh_token: str
    expires_at: int
    scope: str


def validate_server_url(value: str) -> str:
    parsed = urllib.parse.urlsplit(value.rstrip("/"))
    if parsed.scheme != "https" or not parsed.hostname or parsed.query or parsed.fragment:
        raise AttenzaError("the MCP server URL must be an HTTPS URL")
    if parsed.path.rstrip("/") != "/mcp":
        raise AttenzaError("the MCP server URL must end with /mcp and contain no capability token")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "/mcp", "", ""))


def credentials_path() -> Path:
    override = os.getenv("ATTENZA_CONFIG_HOME")
    if override:
        return Path(override).expanduser() / "credentials.json"
    if os.name == "nt":
        root = Path(os.getenv("APPDATA", str(Path.home()))) / "Attenza"
    else:
        root = Path(os.getenv("XDG_CONFIG_HOME", str(Path.home() / ".config"))) / "attenza"
    return root / "credentials.json"


def load_credentials() -> Credentials:
    path = credentials_path()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return Credentials(**payload)
    except FileNotFoundError as exc:
        raise AttenzaError("not signed in; run `attenza login`") from exc
    except (json.JSONDecodeError, TypeError) as exc:
        raise AttenzaError("stored Attenza credentials are invalid; run `attenza login`") from exc


def save_credentials(credentials: Credentials) -> None:
    path = credentials_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(asdict(credentials), indent=2) + "\n", encoding="utf-8")
    try:
        os.chmod(temporary, 0o600)
    except OSError:
        pass
    temporary.replace(path)


def clear_credentials() -> bool:
    path = credentials_path()
    try:
        path.unlink()
        return True
    except FileNotFoundError:
        return False


def pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).decode().rstrip("=")
    return verifier, challenge


def _request_json(
    url: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    form: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[dict[str, Any], dict[str, str]]:
    body: bytes | None = None
    request_headers = {"Accept": "application/json", **(headers or {})}
    if payload is not None:
        body = json.dumps(payload).encode()
        request_headers["Content-Type"] = "application/json"
    elif form is not None:
        body = urllib.parse.urlencode(form).encode()
        request_headers["Content-Type"] = "application/x-www-form-urlencoded"
    request = urllib.request.Request(url, method=method, data=body, headers=request_headers)
    try:
        with urllib.request.urlopen(request, timeout=40) as response:
            result = json.load(response)
            return result, dict(response.headers.items())
    except urllib.error.HTTPError as exc:
        try:
            detail = json.load(exc)
        except (json.JSONDecodeError, UnicodeDecodeError):
            detail = {"error": exc.reason}
        message = detail.get("error_description") or detail.get("error") or exc.reason
        raise AttenzaError(f"Attenza returned HTTP {exc.code}: {message}") from exc
    except urllib.error.URLError as exc:
        raise AttenzaError(f"Attenza is unavailable: {exc.reason}") from exc


def _origin(server_url: str) -> str:
    parsed = urllib.parse.urlsplit(validate_server_url(server_url))
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))


def login(server_url: str = DEFAULT_SERVER, *, open_browser: bool = True) -> Credentials:
    server_url = validate_server_url(server_url)
    callback: dict[str, str] = {}

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            parsed = urllib.parse.urlsplit(self.path)
            if parsed.path != "/callback":
                self.send_error(404)
                return
            values = urllib.parse.parse_qs(parsed.query)
            callback.update({key: items[0] for key, items in values.items() if items})
            body = b"Attenza authorization received. You can close this window."
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, _format: str, *_args: object) -> None:
            return

    with HTTPServer(("127.0.0.1", 0), CallbackHandler) as callback_server:
        callback_server.timeout = 1
        redirect_uri = f"http://127.0.0.1:{callback_server.server_port}/callback"
        origin = _origin(server_url)
        registration, _ = _request_json(
            f"{origin}/oauth/register",
            method="POST",
            payload={
                "client_name": "Attenza CLI",
                "redirect_uris": [redirect_uri],
                "grant_types": ["authorization_code", "refresh_token"],
                "response_types": ["code"],
                "token_endpoint_auth_method": "none",
            },
        )
        client_id = str(registration["client_id"])
        verifier, challenge = pkce_pair()
        state = secrets.token_urlsafe(24)
        authorize_url = f"{origin}/oauth/authorize?" + urllib.parse.urlencode(
            {
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "response_type": "code",
                "scope": SCOPES,
                "state": state,
                "code_challenge": challenge,
                "code_challenge_method": "S256",
                "resource": server_url,
            }
        )
        print(f"Open this URL to authorize Attenza:\n{authorize_url}")
        if open_browser:
            webbrowser.open(authorize_url)
        deadline = time.monotonic() + 300
        while not callback and time.monotonic() < deadline:
            callback_server.handle_request()

    if not callback:
        raise AttenzaError("authorization timed out")
    if callback.get("state") != state:
        raise AttenzaError("authorization state did not match")
    if "error" in callback:
        raise AttenzaError(f"authorization was not granted: {callback['error']}")
    code = callback.get("code")
    if not code:
        raise AttenzaError("authorization response did not contain a code")
    tokens, _ = _request_json(
        f"{origin}/oauth/token",
        method="POST",
        form={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": verifier,
            "resource": server_url,
        },
    )
    credentials = Credentials(
        server_url=server_url,
        client_id=client_id,
        access_token=str(tokens["access_token"]),
        refresh_token=str(tokens["refresh_token"]),
        expires_at=int(time.time()) + int(tokens["expires_in"]),
        scope=str(tokens.get("scope", SCOPES)),
    )
    save_credentials(credentials)
    return credentials


def refresh(credentials: Credentials) -> Credentials:
    tokens, _ = _request_json(
        f"{_origin(credentials.server_url)}/oauth/token",
        method="POST",
        form={
            "grant_type": "refresh_token",
            "client_id": credentials.client_id,
            "refresh_token": credentials.refresh_token,
            "resource": credentials.server_url,
        },
    )
    updated = Credentials(
        server_url=credentials.server_url,
        client_id=credentials.client_id,
        access_token=str(tokens["access_token"]),
        refresh_token=str(tokens["refresh_token"]),
        expires_at=int(time.time()) + int(tokens["expires_in"]),
        scope=str(tokens.get("scope", credentials.scope)),
    )
    save_credentials(updated)
    return updated


def extract_tool_value(result: dict[str, Any]) -> Any:
    if result.get("isError"):
        content = result.get("content", [])
        message = content[0].get("text") if content and isinstance(content[0], dict) else "tool failed"
        raise AttenzaError(str(message))
    if "structuredContent" in result:
        return result["structuredContent"]
    for item in result.get("content", []):
        if isinstance(item, dict) and item.get("type") == "text":
            try:
                return json.loads(str(item.get("text", "")))
            except json.JSONDecodeError:
                return item.get("text")
    return result


class Client:
    def __init__(self, credentials: Credentials | None = None):
        self.credentials = credentials or load_credentials()

    def _rpc(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        if self.credentials.expires_at <= int(time.time()) + 30:
            self.credentials = refresh(self.credentials)
        payload = {"jsonrpc": "2.0", "id": secrets.randbelow(2**31), "method": method, "params": params}
        response, _ = _request_json(
            self.credentials.server_url,
            method="POST",
            payload=payload,
            headers={
                "Authorization": f"Bearer {self.credentials.access_token}",
                "Accept": "application/json, text/event-stream",
                "MCP-Protocol-Version": PROTOCOL_VERSION,
            },
        )
        if "error" in response:
            error = response["error"]
            raise AttenzaError(str(error.get("message", "MCP request failed")))
        result = response.get("result")
        if not isinstance(result, dict):
            raise AttenzaError("MCP response did not contain an object result")
        return result

    def tools(self) -> list[dict[str, Any]]:
        result = self._rpc("tools/list", {})
        tools = result.get("tools")
        if not isinstance(tools, list):
            raise AttenzaError("MCP server did not return a tools list")
        return tools

    def call(self, name: str, arguments: dict[str, Any]) -> Any:
        return extract_tool_value(self._rpc("tools/call", {"name": name, "arguments": arguments}))
