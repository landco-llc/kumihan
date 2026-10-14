#!/usr/bin/env python3
"""Rebuild KUMIHAN skill inventories and distribution archives.

Usage:
  python3 tools/build_dist.py                      # sync, rebuild everything
  python3 tools/build_dist.py --check              # verify the tree is up to date
  python3 tools/build_dist.py --set-version X.Y.Z  # bump the version, then rebuild

`skills/kumihan` is the canonical copy of every shared file. The other skill
folders differ only in SKILL.md and inventory.json. Standard library only.
"""

import argparse
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["kumihan", "kumihan-web", "kumihan-documents", "kumihan-review"]
CANONICAL = "kumihan"
PER_SKILL = {"SKILL.md", "inventory.json"}
VERSION_FILES = [
    "plugin.json",
    ".codex-plugin/plugin.json",
    ".claude-plugin/plugin.json",
    "gemini-extension.json",
]
VERSION_TEXT_FILES = ["README.md", "docs/*.md"]
ZIP_DATE = (2026, 10, 14, 0, 0, 0)
PUBLISHER = "L&Co.LLC"
REPOSITORY = "landco-llc/kumihan"
COMMON_EXTRAS = ["LICENSE", "THIRD_PARTY_NOTICES.md", "docs/development.md", "sources/public-sources.json"]
SKILL_LABELS = {
    "kumihan": "最初の入口 / starting point",
    "kumihan-web": "Webページ / web pages",
    "kumihan-documents": "報告書・スライド / reports and slides",
    "kumihan-review": "レビュー / review",
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_version():
    versions = {f: json.loads((ROOT / f).read_text())["version"] for f in VERSION_FILES}
    if len(set(versions.values())) != 1:
        sys.exit(f"Version mismatch across manifests: {versions}")
    return next(iter(versions.values()))


def set_version(new):
    old = read_version()
    for f in VERSION_FILES:
        p = ROOT / f
        data = json.loads(p.read_text())
        data["version"] = new
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    for pattern in VERSION_TEXT_FILES:
        for p in ROOT.glob(pattern):
            text = p.read_text()
            if old in text:
                p.write_text(text.replace(old, new))
    print(f"Version {old} -> {new}")


def skill_files(name):
    base = ROOT / "skills" / name
    return sorted(p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file())


def planned_tree():
    """Return {relative repo path: bytes} for every generated file under skills/."""
    out = {}
    shared = [f for f in skill_files(CANONICAL) if f not in PER_SKILL]
    for name in SKILLS:
        base = ROOT / "skills" / name
        files = {}
        for f in shared:
            files[f] = (ROOT / "skills" / CANONICAL / f).read_bytes()
        files["SKILL.md"] = (base / "SKILL.md").read_bytes()
        out.update({f"skills/{name}/{f}": b for f, b in files.items()})
        inventory = {
            "format": "kumihan-standalone-inventory-2",
            "skill": name,
            "version": VERSION,
            "path_base": "skill-folder-root",
            "self_digest": "inventory.json lists every other file; its own hash is in the distribution SHA256SUMS.",
            "files": [
                {"path": f, "bytes": len(b), "sha256": sha256(b)} for f, b in sorted(files.items())
            ],
        }
        out[f"skills/{name}/inventory.json"] = (json.dumps(inventory, ensure_ascii=False, indent=2) + "\n").encode()
    return out


def stale_skill_files():
    """Files present in a skill folder that the canonical copy does not have."""
    expected = set(skill_files(CANONICAL)) | PER_SKILL
    return [
        ROOT / "skills" / name / f
        for name in SKILLS
        for f in skill_files(name)
        if f not in expected
    ]


def make_zip(members):
    """members: list of (archive path, bytes). Deterministic output."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for path, data in sorted(members):
            info = zipfile.ZipInfo(path, ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data, compresslevel=9)
    return buf.getvalue()


def skill_members(tree, name, prefix):
    base = f"skills/{name}/"
    return [(prefix + p[len(base):], b) for p, b in tree.items() if p.startswith(base)]


def plugin_members(tree, prefix, extras):
    members = [(prefix + p, b) for p, b in tree.items()]
    members += [(prefix + f, (ROOT / f).read_bytes()) for f in extras]
    return members


def downloads_readme(folder, title, guide_ja, guide_en, bundle_heading, bundle_desc, bundle_file, skills_heading, skills_desc, skill_pattern, layout):
    lines = [
        f"# KUMIHAN ダウンロード：{title}",
        "",
        f"[導入ガイド（日本語）]({guide_ja}) ・ [Installation guide (English)]({guide_en}) ・ [トップに戻る / Back to top](../README.md)",
        "",
        "<br>",
        "",
        f"プレビュー版 **{VERSION}** です。導入の手順は、上の導入ガイドをご覧ください。",
        "",
        f"Preview version **{VERSION}**. See the installation guide above for setup steps.",
        "",
        "<br>",
        "",
        f"## {bundle_heading}",
        "",
        *bundle_desc,
        "",
        f"- [{Path(bundle_file).name}]({bundle_file})",
        "",
        "<br>",
        "",
        f"## {skills_heading}",
        "",
        *skills_desc,
        "",
        *[f"- [{n}]({skill_pattern.format(name=n)}) — {SKILL_LABELS[n]}" for n in SKILLS],
        "",
        "<br>",
        "",
        "## ファイルの確認（任意） / Verify downloads (optional)",
        "",
        f"ダウンロードしたファイルが壊れていないかを確認できます。このページと同じフォルダー構成（{layout}）でファイルを置き、macOSのターミナルで次を実行してください。すべての行に `OK` と表示されれば問題ありません。",
        "",
        "To check your downloads, keep the same folder layout as this page and run the following in the macOS Terminal. Every line should show `OK`.",
        "",
        "```sh",
        f'cd "{folder}"',
        "shasum -a 256 -c SHA256SUMS.txt",
        "```",
        "",
        "[SHA256SUMS.txt](SHA256SUMS.txt) ・ [MANIFEST.json](MANIFEST.json)",
        "",
    ]
    return "\n".join(lines).encode()


def planned_downloads(tree):
    """Return {relative repo path: bytes} for every file under the downloads folders."""
    v = VERSION
    dists = [
        {
            "folder": "downloads Claude",
            "product": "KUMIHAN for Claude",
            "bundle": (f"plugins/kumihan-Claude-Code-plugin-{v}.zip",
                       plugin_members(tree, "kumihan/", [".claude-plugin/plugin.json"] + COMMON_EXTRAS)),
            "skill_file": "skills/{name}-Claude-skill-" + v + ".zip",
            "skill_prefix": "{name}/",
            "readme": dict(
                title="Claude", guide_ja="../docs/installation.claude.ja.md", guide_en="../docs/installation.claude.md",
                bundle_heading="Claude Code用プラグイン / Plugin for Claude Code",
                bundle_desc=["4つのスキルをまとめたパッケージです。Claude Codeで使います。", "", "All four skills in one package, for Claude Code."],
                skills_heading="Claudeチャット用スキル / Skills for Claude chat",
                skills_desc=["claude.aiやClaudeアプリに、1つずつアップロードして使います。", "", "Upload one at a time to claude.ai or the Claude apps."],
                layout="`plugins/` と `skills/`"),
        },
        {
            "folder": "downloads GPT-Codex",
            "product": "KUMIHAN for ChatGPT and Codex",
            "bundle": (f"plugins/kumihan-GPT-Codex-plugin-{v}.zip",
                       plugin_members(tree, "kumihan-private-install-preview/",
                                      [".codex-plugin/plugin.json", "plugin.json", "assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png"] + COMMON_EXTRAS)),
            "skill_file": "skills/{name}-GPT-Codex-skill-" + v + ".zip",
            "skill_prefix": "{name}/",
            "readme": dict(
                title="ChatGPT・Codex", guide_ja="../docs/installation.ja.md", guide_en="../docs/installation.md",
                bundle_heading="プラグイン / Plugin",
                bundle_desc=["4つのスキルをまとめたパッケージです。", "", "All four skills in one package."],
                skills_heading="スキル / Skills",
                skills_desc=["1つずつ追加して使います。", "", "Add them one at a time."],
                layout="`plugins/` と `skills/`"),
        },
        {
            "folder": "downloads Gemini",
            "product": "KUMIHAN for Gemini",
            "bundle": (f"extensions/kumihan-Gemini-CLI-extension-{v}.zip",
                       plugin_members(tree, "", ["gemini-extension.json"] + COMMON_EXTRAS)),
            "skill_file": "skills/{name}-Gemini-Apps-skill-" + v + ".zip",
            "skill_prefix": "",
            "readme": dict(
                title="Gemini", guide_ja="../docs/installation.gemini.ja.md", guide_en="../docs/installation.gemini.md",
                bundle_heading="Gemini CLI用拡張機能 / Extension for Gemini CLI",
                bundle_desc=["4つのスキルをまとめたパッケージです。", "", "All four skills in one package."],
                skills_heading="Geminiアプリ用スキル / Skills for the Gemini app",
                skills_desc=["1つずつアップロードして使います。", "", "Upload them one at a time."],
                layout="`extensions/` と `skills/`"),
        },
    ]
    out = {}
    for d in dists:
        archives = [d["bundle"]]
        for name in SKILLS:
            archives.append((d["skill_file"].format(name=name),
                             skill_members(tree, name, d["skill_prefix"].format(name=name))))
        manifest = {
            "format": 2,
            "product": d["product"],
            "publisher": PUBLISHER,
            "version": v,
            "source_repository": REPOSITORY,
            "status": "Preview. Behavior in each host has not been fully verified.",
            "archives": [],
        }
        sums = []
        for file, members in archives:
            data = make_zip(members)
            out[f"{d['folder']}/{file}"] = data
            sums.append((sha256(data), file))
            manifest["archives"].append({
                "file": file,
                "sha256": sha256(data),
                "bytes": len(data),
                "members": [{"path": p, "bytes": len(b), "sha256": sha256(b)} for p, b in sorted(members)],
            })
        manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode()
        out[f"{d['folder']}/MANIFEST.json"] = manifest_bytes
        sums.insert(0, (sha256(manifest_bytes), "MANIFEST.json"))
        out[f"{d['folder']}/SHA256SUMS.txt"] = "".join(f"{h}  {f}\n" for h, f in sums).encode()
        r = d["readme"]
        out[f"{d['folder']}/README.md"] = downloads_readme(
            d["folder"], r["title"], r["guide_ja"], r["guide_en"],
            r["bundle_heading"], r["bundle_desc"], d["bundle"][0],
            r["skills_heading"], r["skills_desc"], d["skill_file"], r["layout"])
    return out


def stale_download_files(planned):
    stale = []
    for folder in {p.split("/")[0] for p in planned}:
        for p in (ROOT / folder).rglob("*"):
            if p.is_file() and p.relative_to(ROOT).as_posix() not in planned:
                stale.append(p)
    return stale


def main():
    global VERSION
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="exit 1 if any generated file is out of date")
    parser.add_argument("--set-version", metavar="VERSION")
    args = parser.parse_args()

    if args.set_version:
        if args.check:
            sys.exit("--check cannot be combined with --set-version")
        set_version(args.set_version)
    VERSION = read_version()

    tree = planned_tree()
    planned = dict(tree)
    planned.update(planned_downloads(tree))
    stale = stale_skill_files() + stale_download_files(planned)

    changed = [p for p, b in planned.items() if not (ROOT / p).is_file() or (ROOT / p).read_bytes() != b]

    if args.check:
        for p in changed:
            print(f"out of date: {p}")
        for p in stale:
            print(f"stale: {p.relative_to(ROOT)}")
        if changed or stale:
            sys.exit("Run python3 tools/build_dist.py to regenerate.")
        print(f"OK: version {VERSION}, {len(planned)} generated files up to date.")
        return

    for p in changed:
        target = ROOT / p
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(planned[p])
        print(f"wrote {p}")
    for p in stale:
        p.unlink()
        print(f"removed {p.relative_to(ROOT)}")
    for folder in {p.split("/")[0] for p in planned} | {f"skills/{n}" for n in SKILLS}:
        for d in sorted((ROOT / folder).rglob("*"), reverse=True):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
    print(f"Done: version {VERSION}.")


VERSION = None

if __name__ == "__main__":
    main()
