#!/usr/bin/env python3
"""Operator-safe public HTTPS / MCP probe for KUMIHAN (no secrets, no document payloads).

Usage:
  python3 universal/tools/probe_remote.py --mode tls
  python3 universal/tools/probe_remote.py --mode mcp

The endpoint defaults to universal/deployment/target.json and MUST NOT be
assumed available merely because the manifest or DNS entry exists.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import socket
import ssl
import sys
import urllib.error
import urllib.request
from urllib.parse import urlparse

TARGET_FILE = Path(__file__).resolve().parents[1] / "deployment" / "target.json"
TIMEOUT = 12


def target() -> str:
    return json.loads(TARGET_FILE.read_text(encoding="utf-8"))["endpoint"]


def secure_endpoint(value: str) -> tuple[str, str]:
    parsed = urlparse(value)
    if (parsed.scheme != "https" or not parsed.hostname or parsed.port not in (None, 443)
        or parsed.username or parsed.password or parsed.query or parsed.fragment
        or parsed.path != "/mcp"):
        raise ValueError("Only exact HTTPS MCP paths without embedded credentials are supported")
    return parsed.hostname, value


def tls_preflight(endpoint: str) -> None:
    hostname, _ = secure_endpoint(endpoint)
    # Default SSL context validates a trusted chain and exact server name.
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with ssl.create_default_context().wrap_socket(sock, server_hostname=hostname) as wrapped:
            certificate = wrapped.getpeercert()
            print("TLS_VALID hostname=" + hostname
                  + " version=" + str(wrapped.version())
                  + " notAfter=" + str(certificate.get("notAfter", "(unknown)")))


def decode_rpc_response(raw: bytes, content_type: str) -> dict:
    text = raw.decode("utf-8")
    if "text/event-stream" in content_type or text.lstrip().startswith("event:") or text.lstrip().startswith("data:"):
        packets = [json.loads(line[5:].strip()) for line in text.splitlines() if line.startswith("data:")]
        if not packets:
            raise ValueError("SSE body has no JSON-RPC message")
        return packets[-1]
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("JSON-RPC response must be an object")
    return parsed


def rpc(endpoint: str, payload: dict, session: str = "") -> tuple[dict, str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": "2025-11-25",
    }
    if session:
        headers["Mcp-Session-Id"] = session
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            message = decode_rpc_response(
                response.read(1024 * 1024),
                response.headers.get("Content-Type", "application/json"),
            )
            new_session = response.headers.get("Mcp-Session-Id", "")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"MCP_HTTP_{exc.code} (may require deployment/configuration)") from exc
    if "error" in message:
        raise RuntimeError("MCP_JSON_RPC_ERROR: " + str(message["error"].get("code", "unknown")))
    return message, new_session or session


def mcp_probe(endpoint: str) -> None:
    _, endpoint = secure_endpoint(endpoint)
    request_id = 1
    init, session = rpc(endpoint, {
        "jsonrpc": "2.0", "id": request_id, "method": "initialize",
        "params": {
            "protocolVersion": "2025-11-25",
            "capabilities": {},
            "clientInfo": {"name": "kumihan-deploy-smoke", "version": "0.1.0"},
        },
    })
    server = init.get("result", {}).get("serverInfo", {}).get("name")
    if server != "KUMIHAN Universal":
        raise RuntimeError(f"MCP server identity unexpected: {server!r}")
    tools, session = rpc(endpoint, {
        "jsonrpc": "2.0", "id": request_id + 1,
        "method": "tools/list", "params": {},
    }, session)
    names = {item["name"] for item in tools.get("result", {}).get("tools", [])}
    required = {"kumihan_list_languages", "kumihan_detect_language",
                "kumihan_get_guidance", "kumihan_review_text"}
    if not required.issubset(names):
        raise RuntimeError("MCP tool list incomplete")
    result, _ = rpc(endpoint, {
        "jsonrpc": "2.0", "id": request_id + 2,
        "method": "tools/call",
        "params": {"name": "kumihan_list_languages", "arguments": {}},
    }, session)
    if "result" not in result or "21" not in json.dumps(result["result"]):
        raise RuntimeError("MCP language list was not returned as expected")
    print("MCP_PASS endpoint=" + endpoint + " server=" + server
          + " tools=" + str(len(names)) + " registry=present")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("tls", "mcp"), default="tls")
    parser.add_argument("--endpoint", default=target())
    args = parser.parse_args()
    try:
        secure_endpoint(args.endpoint)
        if args.mode == "tls":
            tls_preflight(args.endpoint)
        else:
            tls_preflight(args.endpoint)
            mcp_probe(args.endpoint)
        return 0
    except (OSError, ssl.SSLError, ValueError, RuntimeError, UnicodeError) as exc:
        print(f"{args.mode.upper()}_NOT_VERIFIED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
