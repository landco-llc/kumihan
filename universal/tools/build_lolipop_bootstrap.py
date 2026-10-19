#!/usr/bin/env python3
"""Build a secure Lolipop kmhn document-root bootstrap; NO server writes.

Important: Lolipop's FTP-root may itself be publicly served by the account's
default domain. Never place src, vendor, registry or config in an FTP-root sibling.
This generator requires an explicit ABSOLUTE server directory OUTSIDE FTP root.
Output contains ONLY the public bootstrap and .htaccess.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "universal" / "deployment" / "target.json"
REWRITE_RULES = ROOT / "universal" / "server" / "public" / ".htaccess"


def safe_absolute_path(value: str, label: str) -> Path:
    if not value or not Path(value).is_absolute() or any(ord(ch) < 32 for ch in value):
        raise ValueError(f"{label} must be a non-empty absolute path without control characters")
    resolved = Path(value).resolve(strict=False)
    if resolved == Path("/"):
        raise ValueError(f"{label} cannot be filesystem root")
    return resolved


def resolve_layout(ftp_root: str, private_server_root: str) -> dict[str, Path]:
    config = json.loads(TARGET.read_text(encoding="utf-8"))
    folder = config["production_upload_directory"]
    if folder != "kmhn":
        raise ValueError("The Owner-confirmed public folder must be kmhn")
    ftp = safe_absolute_path(ftp_root, "ftp_root")
    private = safe_absolute_path(private_server_root, "private_server_root")
    public = ftp / folder
    if private == ftp or private.is_relative_to(ftp):
        raise ValueError("Private server root is inside the potentially public Lolipop FTP root")
    if public == private or public.is_relative_to(private):
        raise ValueError("Public and private directories must be separate")
    # The private path must be an owned, SSH-accessible non-web path, verified on host.
    return {"ftp": ftp, "public": public, "private": private, "entrypoint": private / "public" / "index.php"}


def php_literal(value: str) -> str:
    if "\x00" in value or "\r" in value or "\n" in value:
        raise ValueError("Invalid PHP string")
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def build(ftp_root: str, private_server_root: str, output_dir: Path) -> dict:
    layout = resolve_layout(ftp_root, private_server_root)
    out = Path(output_dir)
    if not out.is_absolute():
        raise ValueError("output_dir must be absolute")
    out = out.resolve(strict=False)
    # Refuse to write directly into host root, even if invoked on SSH.
    if out == layout["ftp"] or out.is_relative_to(layout["ftp"]) or out.is_relative_to(layout["private"]):
        raise ValueError("output_dir must be an offline build area outside FTP and private server root")
    docroot = out / "kmhn"
    docroot.mkdir(parents=True, exist_ok=True)

    php = """<?php
declare(strict_types=1);

// KUMIHAN Universal bootstrap. THIS FILE HAS NO PASSWORDS.
// The actual MCP app is outside the public FTP root.
$entrypoint = %s;
if (!is_file($entrypoint)) {
    http_response_code(503);
    header('Content-Type: application/json; charset=utf-8');
    echo '{"error":"KUMIHAN_MCP_NOT_DEPLOYED"}';
    exit;
}
require $entrypoint;
""" % php_literal(str(layout["entrypoint"]))
    (docroot / "index.php").write_text(php, encoding="utf-8")
    (docroot / ".htaccess").write_bytes(REWRITE_RULES.read_bytes())
    details = {
        "status": "offline_generated_not_deployed",
        "target": "https://mcp-kmhn.landco.co.jp/mcp",
        "public_ftp_relative": "kmhn",
        "public_ssh_absolute": str(layout["public"]),
        "private_server_ssh_absolute": str(layout["private"]),
        "private_entrypoint": str(layout["entrypoint"]),
        "public_files": ["kmhn/index.php", "kmhn/.htaccess"],
        "upload_plan": "Copy ONLY two generated public files into existing FTP root/kmhn. Unpack staging artifact under private_server_ssh_absolute. Ensure private path is NOT in ANY other domain's public root.",
        "caution": "Do not treat this build output as evidence of live configuration or a successful PHP/MCP connection.",
    }
    (out / "placement.json").write_text(
        json.dumps(details, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return details


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ftp-root", required=True, help="Absolute SSH filesystem path of Lolipop FTP root (not the kmhn folder)")
    p.add_argument("--private-server-root", required=True, help="Absolute SSH path OUTSIDE FTP root for server/public, src, vendor, runtime")
    p.add_argument("--output-dir", required=True, type=Path, help="Absolute OFFLINE build output path (not the hosting directories)")
    args = p.parse_args()
    try:
        details = build(args.ftp_root, args.private_server_root, args.output_dir)
        print(json.dumps(details, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"NO_BOOTSTRAP: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
