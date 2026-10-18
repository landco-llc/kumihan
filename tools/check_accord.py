#!/usr/bin/env python3
"""Accord package, icon, integrity and metadata verification (no native host claims)."""
import hashlib
import json
import re
import struct
import sys
from pathlib import Path
from zipfile import ZipFile

LOGO = "KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"
SKILLS = ("kumihan-accord", "kumihan-accord-web", "kumihan-accord-documents", "kumihan-accord-review")
ROOT = "kumihan-accord/"
PNG_SIGNATURE = bytes.fromhex("89504e470d0a1a0a")


def png_ok(data):
    if len(data) > 5 * 1024 * 1024 or not data.startswith(PNG_SIGNATURE):
        return False
    if len(data) < 24 or data[12:16] != b"IHDR":
        return False
    width, height = struct.unpack(">II", data[16:24])
    return width == height and 48 <= width <= 4096


def skill_icons(archive, skill_root, members):
    yaml_path = skill_root + "/agents/openai.yaml"
    logo_path = skill_root + "/assets/" + LOGO
    assert yaml_path in members and logo_path in members, (yaml_path, logo_path)
    yaml = archive.read(yaml_path).decode("utf-8")
    assert "interface:\n" in yaml
    assert "display_name:" in yaml and "short_description:" in yaml
    assert 'icon_small: "./assets/' + LOGO + '"' in yaml
    assert 'icon_large: "./assets/' + LOGO + '"' in yaml
    img = archive.read(logo_path)
    assert png_ok(img), logo_path
    return hashlib.sha256(img).hexdigest()


def check(out):
    manifest = json.loads((out / "MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["product"] == "KUMIHAN｜Accord" and manifest["version"] == "0.1.1"
    assert manifest["tag"] == "kumihan-fr-v0.1.1"
    packs = manifest["packages"]
    assert len(packs) == 15 and len({p["name"] for p in packs}) == 15
    checksums = (out / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
    assert len(checksums) == 15
    assert {line.split("  ", 1)[1]: line.split("  ", 1)[0] for line in checksums} == {
        p["name"]: p["sha256"] for p in packs
    }
    canonical_logo_digest = None
    inspected = 0
    for pkg in packs:
        filename = pkg["name"]
        assert filename.endswith("-v0.1.1.zip")
        archive_bytes = (out / filename).read_bytes()
        assert hashlib.sha256(archive_bytes).hexdigest() == pkg["sha256"]
        with ZipFile(out / filename) as zipfile:
            assert zipfile.testzip() is None
            members = zipfile.namelist()
            assert len(members) == len(set(members)) and members
            assert not any(p.startswith("/") or ".." in Path(p).parts for p in members)
            assert any(p.endswith("/LICENSE") for p in members)
            assert any(p.endswith("/rules/catalog.json") for p in members)
            skills = [p.removesuffix("/SKILL.md") for p in members if p.endswith("/SKILL.md")]
            if "-skill-" in filename:
                assert len(skills) == 1
                assert skills[0] in SKILLS
                assert any(p.endswith("/runtime/checks.py") for p in members)
                sha = skill_icons(zipfile, skills[0], members)
                digests = [sha]
            else:
                assert len(skills) == 4
                assert set(skills) == {ROOT + s for s in SKILLS}
                root_logo = ROOT + "assets/" + LOGO
                assert root_logo in members and png_ok(zipfile.read(root_logo))
                digests = [hashlib.sha256(zipfile.read(root_logo)).hexdigest()]
                for s in SKILLS:
                    digests.append(skill_icons(zipfile, ROOT + "skills/" + s, members))
                name = "plugin.json" if "chatgpt-codex" in filename else (
                    ".claude-plugin/plugin.json" if "claude-code" in filename else "gemini-extension.json"
                )
                assert ROOT + name in members
                data = json.loads(zipfile.read(ROOT + name))
                assert data["name"] == "kumihan-accord" and data["version"] == "0.1.1"
                assert " | " in data["description"]
                if "chatgpt-codex" in filename:
                    for m in (data, json.loads(zipfile.read(ROOT + ".codex-plugin/plugin.json"))):
                        ui = m["extensions"]["com.openai"]["interface"] if "extensions" in m else m["interface"]
                        assert ui["displayName"] == "KUMIHAN｜Accord"
                        for key in ("logo", "composerIcon"):
                            icon_ref = ui[key]
                            assert icon_ref == "./assets/" + LOGO
                            assert ROOT + icon_ref[2:] in members
                elif "claude-code" in filename:
                    assert data["displayName"] == "KUMIHAN｜Accord"
                    assert data["icon"] == "./assets/" + LOGO
                    assert ROOT + data["icon"][2:] in members
                else:
                    # Gemini CLI docs do not define a standard icon UI field.
                    # Include the asset, but never claim Gemini displays it.
                    assert "gemini-extension.json" in name
            for sha in digests:
                if canonical_logo_digest is None:
                    canonical_logo_digest = sha
                assert sha == canonical_logo_digest, "Images differ across bundles"
                inspected += 1
    assert inspected == 27, inspected  # 12 standalone + 3*(1 plugin + 4 skills)
    print("PASS: 15 ZIPs, 27 embedded image copies, 15 SHA256, OpenAI skill/icon metadata, Claude icon, Gemini image")


if __name__ == "__main__":
    check(Path(sys.argv[1]))
