from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from attenza_cli.client import (
    AttenzaError,
    Credentials,
    clear_credentials,
    extract_tool_value,
    load_credentials,
    pkce_pair,
    save_credentials,
    validate_server_url,
)
from attenza_cli.cli import _load_object, _task_expiry, _task_state, build_parser


ROOT = Path(__file__).resolve().parents[1]


class ClientTests(unittest.TestCase):
    def test_public_mcp_url_is_accepted(self) -> None:
        self.assertEqual(
            validate_server_url("https://www.attenza.io/mcp/"),
            "https://www.attenza.io/mcp",
        )
        with self.assertRaises(AttenzaError):
            validate_server_url("https://www.attenza.io/mcp/" + "private-token")
        with self.assertRaises(AttenzaError):
            validate_server_url("http://www.attenza.io/mcp")

    def test_pkce_values_have_required_shape(self) -> None:
        verifier, challenge = pkce_pair()
        self.assertGreaterEqual(len(verifier), 43)
        self.assertEqual(len(challenge), 43)

    def test_credentials_round_trip_and_logout(self) -> None:
        with tempfile.TemporaryDirectory() as directory, patch.dict(
            os.environ, {"ATTENZA_CONFIG_HOME": directory}
        ):
            expected = Credentials(
                server_url="https://www.attenza.io/mcp",
                client_id="public-client",
                access_token="test-access-token",
                refresh_token="test-refresh-token",
                expires_at=123,
                scope="tasks:read",
            )
            save_credentials(expected)
            self.assertEqual(load_credentials(), expected)
            self.assertTrue(clear_credentials())
            self.assertFalse(clear_credentials())

    def test_tool_result_prefers_structured_content(self) -> None:
        self.assertEqual(
            extract_tool_value({"structuredContent": {"task": {"id": "123"}}}),
            {"task": {"id": "123"}},
        )
        self.assertEqual(
            extract_tool_value({"content": [{"type": "text", "text": '{"created":true}'}]}),
            {"created": True},
        )

    def test_example_is_a_valid_cli_request(self) -> None:
        value = _load_object(str(ROOT / "examples" / "release-approval.json"))
        self.assertEqual(value["source"], "release-agent")
        self.assertEqual(len(value["a2ui_messages"]), 3)

    def test_terminal_state_and_cli_surface(self) -> None:
        self.assertEqual(
            _task_state({"task": {"status": {"state": "TASK_STATE_COMPLETED"}}}),
            "TASK_STATE_COMPLETED",
        )
        parser = build_parser()
        self.assertEqual(parser.parse_args(["get", "task-1"]).task_id, "task-1")

    def test_task_expiry_reads_a2a_metadata(self) -> None:
        self.assertEqual(
            _task_expiry({"task": {"metadata": {"expiresAt": "2026-09-07T12:00:00Z"}}}),
            1788782400.0,
        )
        self.assertIsNone(_task_expiry({"task": {"metadata": {}}}))


if __name__ == "__main__":
    unittest.main()
