#!/usr/bin/env python3
"""Real HTTP MCP invocation smoke (CI only, after Composer and PHP server startup)."""
import json
import os
import sys
import urllib.request

ENDPOINT = os.environ.get("KUMIHAN_MCP_LOCAL_URL", "http://127.0.0.1:8989/index.php")


def post(payload: dict, headers: dict | None = None):
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            **(headers or {}),
        },
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        body = response.read().decode("utf-8")
        session = response.headers.get("Mcp-Session-Id", "")
    if body.strip().startswith("{"):
        msg = json.loads(body)
    else:
        packets = [json.loads(line[5:].strip()) for line in body.splitlines() if line.startswith("data:")]
        if not packets:
            raise AssertionError("No JSON-RPC packet: " + body[:200])
        msg = packets[-1]
    if "error" in msg:
        raise AssertionError("JSON-RPC: " + json.dumps(msg["error"]))
    return msg, session


def check(ok: bool, message: str):
    if not ok:
        raise AssertionError(message)


def run():
    initialized, session = post({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "kumihan-ci", "version": "0.1"}}
    })
    check(initialized.get("result", {}).get("serverInfo", {}).get("name") == "KUMIHAN Universal", "handshake result")
    headers = {"MCP-Protocol-Version": "2025-11-25"}
    if session:
        headers["Mcp-Session-Id"] = session

    listed, _ = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, headers)
    tools = {tool["name"] for tool in listed["result"]["tools"]}
    check({"kumihan_list_languages", "kumihan_detect_language", "kumihan_get_guidance", "kumihan_review_text"} <= tools, "four tools")

    invoked, _ = post({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
        "name": "kumihan_list_languages", "arguments": {}
    }}, headers)
    check("21" in json.dumps(invoked["result"]), "module list tool call")

    detection, _ = post({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {
        "name": "kumihan_detect_language", "arguments": {"text": "日本語とEnglish"}
    }}, headers)
    check("needs_review" in json.dumps(detection["result"]), "real language route tool call")

    modern_meta = {
        "io.modelcontextprotocol/protocolVersion": "2026-07-28",
        "io.modelcontextprotocol/clientCapabilities": {},
    }
    modern, _ = post({"jsonrpc": "2.0", "id": 5, "method": "server/discover", "params": {"_meta": modern_meta}}, {
        "MCP-Protocol-Version": "2026-07-28",
        "Mcp-Method": "server/discover",
    })
    check("result" in modern, "modern protocol discovery")
    print("MCP real HTTP smoke PASS: handshake, 4 tools, tools/call, modern stateless discover")


if __name__ == "__main__":
    run()
