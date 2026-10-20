#!/usr/bin/env python3
"""Create three host-specific KUMIHAN plugin bundles after the real HTTPS MCP URL is verified."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
from urllib.parse import urlparse
import zipfile

ROOT = Path(__file__).resolve().parents[2]
VERSION = "0.1.0-preview"
DESCRIPTION = "多言語文字組・デザインガイダンスを提供。 / Multilingual typography and purposeful design guidance."


def validate_endpoint(value: str) -> str:
    parsed = urlparse(value)
    host = parsed.hostname or ""
    if (parsed.scheme != "https" or not host or parsed.username or parsed.password
            or parsed.query or parsed.fragment or not parsed.path.endswith("/mcp")
            or host in ("localhost", "127.0.0.1")
            or host.endswith((".example", ".invalid", ".test", ".localhost"))
            or "YOUR" in value.upper()):
        raise ValueError("Provide the VERIFIED real HTTPS endpoint ending in /mcp")
    return value


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def text_guidance() -> str:
    return """---
name: kumihan-universal
description: "多言語文字組とデザインを支援。 | Guide typography and design across languages."
---

# KUMIHAN Universal

Use the shared KUMIHAN MCP to list installed languages and choose the appropriate language module.

- Respect an explicit requested locale before document metadata; use conservative automatic routing otherwise.
- If language, script or regional house style is ambiguous, ask only when the choice materially affects typography.
- For mixed documents, preserve original segments and select separate language rules; never silently translate.
- Use kumihan_get_guidance for language/medium-appropriate source-backed guidance.
- kumihan_review_text is an advisory read-only check. Do not call any text layout 'verified' without actual rendered evidence.
- Preserve all original names, prices, links, values, Unicode and protected content.
- Do not invent availability for unregistered or preview-only language modules.
"""


def copy_common(root: Path) -> None:
    target = root / "skills" / "kumihan-universal" / "SKILL.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text_guidance(), encoding="utf-8")


def build(endpoint: str, outdir: Path) -> list[Path]:
    endpoint = validate_endpoint(endpoint)
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    result = []

    openai = outdir / "openai"
    copy_common(openai)
    write_json(openai / "plugin.json", {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": "kumihan", "version": VERSION, "description": DESCRIPTION,
        "author": {"name": "L&Co. LLC"}, "license": "Apache-2.0",
        "repository": "https://github.com/landco-llc/kumihan",
        "extensions": {"com.openai": {"interface": {
            "displayName": "KUMIHAN",
            "shortDescription": DESCRIPTION,
            "longDescription": "Source-preserving multilingual typography guidance. Modules update on the MCP server; installed Skill updates still require package updates.",
            "developerName": "L&Co. LLC", "category": "Productivity",
            "websiteURL": "https://github.com/landco-llc/kumihan",
        }}},
    })
    write_json(openai / "mcp.json", {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
        "mcpServers": {"kumihan": {"type": "streamable-http", "url": endpoint}},
    })
    logo = ROOT / "assets" / "KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"
    if logo.is_file():
        (openai / "assets").mkdir()
        shutil.copy2(logo, openai / "assets" / "logo.png")
        manifest_path = openai / "plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["extensions"]["com.openai"]["interface"]["logo"] = "./assets/logo.png"
        manifest["extensions"]["com.openai"]["interface"]["composerIcon"] = "./assets/logo.png"
        write_json(manifest_path, manifest)

    claude = outdir / "claude-code"
    copy_common(claude)
    write_json(claude / ".claude-plugin" / "plugin.json", {
        "name": "kumihan", "version": VERSION, "description": DESCRIPTION,
        "author": {"name": "L&Co. LLC"},
    })
    write_json(claude / ".mcp.json", {
        "mcpServers": {"kumihan": {"type": "http", "url": endpoint}},
    })

    gemini = outdir / "gemini-cli"
    copy_common(gemini)
    write_json(gemini / "gemini-extension.json", {
        "name": "kumihan", "version": VERSION, "description": DESCRIPTION,
        "contextFileName": "GEMINI.md",
        "mcpServers": {"kumihan": {"httpUrl": endpoint}},
    })
    (gemini / "GEMINI.md").write_text(
        "Use the kumihan-universal Skill and remote KUMIHAN tools for source-preserving multilingual typography. "
        "Never infer region from script or treat guidance-only as validated rendering.\n", encoding="utf-8"
    )

    for app in (openai, claude, gemini):
        archive = outdir / f"kumihan-universal-{app.name}-{VERSION}.zip"
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for file in sorted(app.rglob("*")):
                if not file.is_file():
                    continue
                zip_path = file.relative_to(app).as_posix()
                info = zipfile.ZipInfo(zip_path, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                zf.writestr(info, file.read_bytes())
        result.append(archive)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--output", type=Path, default=ROOT / "universal" / "dist")
    args = parser.parse_args()
    for path in build(args.endpoint, args.output):
        print(path)
