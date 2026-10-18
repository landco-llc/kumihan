#!/usr/bin/env python3
"""Rebuild host-specific ZiHeng archives, independent from Japanese KUMIHAN.

Canonical skill inputs: plugins/kumihan-ziheng/skills/* (first run the regular
tools/build_ziheng.py builder to sync these). No network or runtime dependency.
Outputs: the ZiHeng product's Claude and Gemini distributions only.
"""
import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = "plugins/kumihan-ziheng"
NAMES = ("kumihan-ziheng", "kumihan-ziheng-web",
         "kumihan-ziheng-documents", "kumihan-ziheng-review")
DATE = (2026, 10, 18, 0, 0, 0)
HOSTS = {
    "Claude": ("downloads Claude", "plugins", "Claude-Code-plugin", "Claude-skill"),
    "Gemini": ("downloads Gemini", "extensions", "Gemini-CLI-extension", "Gemini-Apps-skill"),
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def makezip(entries):
    """Stable ZIP order, timestamp and modes, like the Japanese KUMIHAN builder."""
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as z:
        for name, data in sorted(entries.items()):
            if name.startswith("/") or ".." in Path(name).parts:
                raise ValueError("Unsafe member path")
            info = zipfile.ZipInfo(name, DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data, compresslevel=9)
    return out.getvalue()


def skill_source_files(root, name, version):
    base = root / PRODUCT / "skills" / name
    files = {p.relative_to(base).as_posix(): p.read_bytes()
             for p in sorted(base.rglob("*")) if p.is_file()}
    inventory = json.loads(files["inventory.json"])
    if inventory["skill"] != name or inventory["version"] != version:
        raise ValueError(f"Outdated skill inventory: {name}")
    expected = {entry["path"] for entry in inventory["files"]}
    if expected != set(files) - {"inventory.json"}:
        raise ValueError(f"Incomplete inventory: {name}")
    for entry in inventory["files"]:
        data = files[entry["path"]]
        if sha(data) != entry["sha256"] or len(data) != entry["bytes"]:
            raise ValueError(f"Changed skill file: {name}/{entry['path']}")
    if not files["SKILL.md"].startswith(b"---\n"):
        raise ValueError(f"Missing Skill front matter: {name}")
    return files


def plan_outputs(root=ROOT):
    root = Path(root)
    base = root / PRODUCT
    manifest = json.loads((base / "plugin.json").read_text(encoding="utf-8"))
    version = manifest["version"]
    if manifest["name"] != "kumihan-ziheng" or not re.fullmatch(
        r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?", version
    ):
        raise ValueError("Unexpected ZiHeng identity or version")
    assets = {name: skill_source_files(root, name, version) for name in NAMES}
    license_data = (base / "LICENSE").read_bytes()
    notices = (base / "THIRD_PARTY_NOTICES.md").read_bytes()
    description = manifest["description"]

    claude_plugin = {
        "name": "kumihan-ziheng", "version": version,
        "description": description,
        "author": {"name": "L&Co. LLC"},
        "repository": "https://github.com/landco-llc/kumihan",
        "license": "Apache-2.0",
    }
    gemini_extension = {
        "name": "kumihan-ziheng", "version": version,
        "description": description,
    }
    outputs = {
        f"{PRODUCT}/.claude-plugin/plugin.json": encoded(claude_plugin),
        f"{PRODUCT}/gemini-extension.json": encoded(gemini_extension),
    }

    readme_claude = (
        "# KUMIHAN｜字衡 — Claude Code\n\n"
        "臺灣（zh-Hant-TW）與香港（zh-Hant-HK）的繁體中文文字組版。\n"
        "Traditional Chinese typography guidance for Taiwan and Hong Kong.\n\n"
        f"Version {version}. Four skills in `skills/`. The plugin is independently installable.\n"
        "Use Claude Code's plugin import or local `claude --plugin-dir` on the extracted folder.\n"
        "To install individual skills in Claude chat, use the four separately packaged skill ZIPs.\n"
        "The original source text is protected; this is guidance, not a renderer.\n"
    ).encode("utf-8")
    readme_gemini = (
        "# KUMIHAN｜字衡 — Gemini CLI\n\n"
        "臺灣（zh-Hant-TW）及香港（zh-Hant-HK）繁體中文文字組版。\n"
        "Traditional Chinese typography guidance for Taiwan and Hong Kong.\n\n"
        f"Version {version}. Four skills in `skills/`.\n"
        "Extract the extension ZIP into an empty local folder, then run "
        "`gemini extensions install /absolute/path/to/folder`.\n"
        "The Japanese KUMIHAN GitHub repository root is a different Gemini extension: "
        "do NOT install its root URL expecting ZiHeng.\n"
        "For Gemini app imports, use the four independent flat skill ZIPs.\n"
        "Actual host discovery and invocation require separate acceptance testing.\n"
    ).encode("utf-8")

    for platform, (folder, bundle_dir, bundle_kind, skill_kind) in HOSTS.items():
        bundle_members = {}
        if platform == "Claude":
            prefix = "kumihan-ziheng/"
            bundle_members[prefix + ".claude-plugin/plugin.json"] = outputs[
                f"{PRODUCT}/.claude-plugin/plugin.json"
            ]
            bundle_members[prefix + "README.md"] = readme_claude
        else:
            prefix = ""
            bundle_members["gemini-extension.json"] = outputs[f"{PRODUCT}/gemini-extension.json"]
            bundle_members["README.md"] = readme_gemini
        bundle_members[prefix + "LICENSE"] = license_data
        bundle_members[prefix + "THIRD_PARTY_NOTICES.md"] = notices
        for name, files in assets.items():
            for path, content in files.items():
                bundle_members[prefix + f"skills/{name}/{path}"] = content

        downloads = {}
        bundle_name = f"kumihan-ziheng-{bundle_kind}-{version}.zip"
        downloads[f"{bundle_dir}/{bundle_name}"] = makezip(bundle_members)
        for name, files in assets.items():
            path = f"skills/{name}-{skill_kind}-{version}.zip"
            # Claude: parent folder as standard Claude upload; Gemini Apps: flat, like the Japanese build.
            skill_prefix = f"{name}/" if platform == "Claude" else ""
            downloads[path] = makezip({skill_prefix + key: value for key, value in files.items()})

        dist_manifest = {
            "format": 2,
            "product": f"KUMIHAN｜字衡 for {platform}",
            "publisher": "L&Co. LLC",
            "version": version,
            "source_repository": "landco-llc/kumihan",
            "status": "Preview. Host-native installation and invocation not yet verified.",
            "archives": [],
        }
        for path, data in sorted(downloads.items()):
            with zipfile.ZipFile(io.BytesIO(data)) as zipf:
                members = [
                    {"path": name, "bytes": len(zipf.read(name)), "sha256": sha(zipf.read(name))}
                    for name in sorted(zipf.namelist())
                ]
            dist_manifest["archives"].append({
                "file": path, "sha256": sha(data), "bytes": len(data), "members": members
            })
        downloads["MANIFEST.json"] = encoded(dist_manifest)
        downloads["SHA256SUMS.txt"] = "".join(
            f"{sha(data)}  {path}\n" for path, data in sorted(downloads.items())
        ).encode("utf-8")
        skill_list = "\n".join(
            f"- [{name}]"
            f"(skills/{name}-{skill_kind}-{version}.zip)"
            for name in NAMES
        )
        if platform == "Claude":
            lead = (
                "Claude Code: marketplace entry `kumihan-ziheng@kumihan-marketplace`, "
                "or extract the full plugin ZIP and use "
                "`claude --plugin-dir /absolute/path/kumihan-ziheng`.\n\n"
                "Claude chat: use an individual skill ZIP for skill import; "
                "host availability varies.\n"
            )
        else:
            lead = (
                "Gemini CLI: extract the extension ZIP into a new folder, then run "
                "`gemini extensions install /absolute/path/to/folder`. "
                "Direct install from this monorepo's root selects **Japanese KUMIHAN**, "
                "not ZiHeng.\n\nGemini app: use an individual skill ZIP if the "
                "Skills import feature is available.\n"
            )
        downloads["README.md"] = (
            f"# KUMIHAN｜字衡 for {platform} / {platform} 版本\n\n"
            f"v{version} (preview). 臺灣 / 香港繁體中文文字組版 — "
            "Traditional Chinese typography and read-only review.\n\n"
            + lead + "\n"
            + f"## Full bundle / 整包\n\n"
            + f"- [{bundle_name}]({bundle_dir}/{bundle_name})\n\n"
            + "## Four independent skills / 四個獨立技能\n\n"
            + skill_list + "\n\n"
            + "## SHA-256 verification / 校驗\n\n"
            + "`shasum -a 256 -c SHA256SUMS.txt` (or equivalent) "
            "from this download folder.\n\n"
            + "No automatic rendering, regional glyph, Office/PDF, or native-host "
            "compatibility guarantee. No public marketplace listing is implied.\n"
        ).encode("utf-8")
        for path, data in downloads.items():
            outputs[f"{PRODUCT}/{folder}/{path}"] = data

    return outputs


def generated_files(root=ROOT):
    base = Path(root) / PRODUCT
    paths = [base / ".claude-plugin" / "plugin.json", base / "gemini-extension.json"]
    for folder, *_ in HOSTS.values():
        path = base / folder
        if path.exists():
            paths.extend(p for p in path.rglob("*") if p.is_file())
    return {p.relative_to(root).as_posix() for p in paths if p.is_file()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = plan_outputs()
    changed = [p for p, value in outputs.items()
               if not (ROOT / p).exists() or (ROOT / p).read_bytes() != value]
    stale = generated_files() - set(outputs)
    if args.check:
        for p in sorted(set(changed) | stale):
            print(f"out of date: {p}")
        if changed or stale:
            return 1
        print(f"OK: ZiHeng Claude/Gemini {len(outputs)} generated files current")
        return 0
    for p in changed:
        dest = ROOT / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(outputs[p])
    for p in sorted(stale):
        (ROOT / p).unlink()
    print(f"Built ZiHeng host outputs: {len(outputs)}; updated {len(changed)}; stale {len(stale)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
