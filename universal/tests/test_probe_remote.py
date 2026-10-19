#!/usr/bin/env python3
"""Offline tests for the production-safe external TLS/MCP probe parser."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "tools" / "probe_remote.py"
spec = importlib.util.spec_from_file_location("kumihan_remote_probe", path)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class RemoteProbeTests(unittest.TestCase):
    def test_selected_endpoint(self):
        self.assertEqual(module.target(), "https://mcp-kmhn.landco.co.jp/mcp")
        self.assertEqual(module.secure_endpoint(module.target())[0], "mcp-kmhn.landco.co.jp")
        for invalid in (
            "http://mcp-kmhn.landco.co.jp/mcp",
            "https://mcp-kmhn.landco.co.jp/other",
            "https://name:secret@mcp-kmhn.landco.co.jp/mcp",
            "https://mcp-kmhn.landco.co.jp/mcp?token=secret",
        ):
            with self.subTest(url=invalid), self.assertRaises(ValueError):
                module.secure_endpoint(invalid)

    def test_json_and_sse(self):
        self.assertEqual(module.decode_rpc_response(
            b'{"jsonrpc":"2.0","id":1,"result":{}}', "application/json"
        )["id"], 1)
        self.assertEqual(module.decode_rpc_response(
            b'event: message\ndata: {"jsonrpc":"2.0","id":2,"result":{}}\n\n',
            "text/event-stream"
        )["id"], 2)


if __name__ == "__main__":
    unittest.main()
