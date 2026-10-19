#!/usr/bin/env python3
"""Build deterministic, standalone KUMIHAN Bangla v0.1.0 archives. stdlib only."""
from __future__ import annotations
import hashlib, json, re, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "plugins" / "kumihan-bn"
DIST = SRC / "downloads"
VERSION = "v0.1.0"
SKILLS = ("kumihan-bn", "kumihan-bn-web", "kumihan-bn-documents", "kumihan-bn-review")
MARKERS = ('বাংলা', '|', 'Open-source')
BRAND = "KUMIHAN｜অক্ষরসজ্জা"

def validate():
    plugin = json.loads((SRC / "plugin.json").read_text("utf-8"))
    claude = json.loads((SRC / ".claude-plugin/plugin.json").read_text("utf-8"))
    gemini = json.loads((SRC / "gemini-extension.json").read_text("utf-8"))
    codex = json.loads((SRC / ".codex-plugin/plugin.json").read_text("utf-8"))
    assert plugin["extensions"]["com.openai"]["interface"]["displayName"] == BRAND
    assert claude["displayName"] == BRAND
    assert codex["interface"]["displayName"] == BRAND
    assert all(p["version"] == "0.1.0" for p in (plugin, claude, gemini, codex))
    assert all(" | " in p["description"] for p in (plugin, claude, gemini, codex))
    assert (SRC / "assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png").is_file()
    assert len(json.loads((SRC / "rules/catalog.json").read_text("utf-8"))["rules"]) == 36
    assert len(json.loads((SRC / "fixtures/qa.json").read_text("utf-8"))["cases"]) == 60
    for skill in SKILLS:
        base = SRC / "skills" / skill
        md = (base / "SKILL.md").read_text("utf-8")
        assert md.startswith("---\n") and f"name: {skill}" in md
        assert "description:" in md and " | " in md
        assert (base / "assets/KUMIHAN_OFFICIAL_LOGO_MASTER_20261014.png").is_file()
        for ref in ("rules/catalog.json", "profiles/profiles.json", "fixtures/qa.json",
                    "locales/bn-BD.json", "locales/bn-IN.json", "runtime/checks.py",
                    "references/workflow.md","references/web.md","references/documents.md",
                    "references/review.md","references/source-index.md"):
            assert (base / ref).is_file(), f"missing {skill}/{ref}"
    return plugin

def archive(path: Path, paths, prefix: Path):
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=8) as out:
        for file in sorted(paths):
            rel=file.relative_to(prefix).as_posix()
            assert not rel.startswith("/") and ".." not in Path(rel).parts
            zi=zipfile.ZipInfo(rel,date_time=(2026,1,1,0,0,0))
            zi.compress_type=zipfile.ZIP_DEFLATED
            zi.external_attr=(0o100644 << 16)
            out.writestr(zi,file.read_bytes())
    with zipfile.ZipFile(path) as inp:
        assert inp.testzip() is None
        allnames=inp.namelist()
        assert all(not n.startswith("/") and ".." not in Path(n).parts for n in allnames)
    return len(allnames)

def build():
    validate()
    DIST.mkdir(exist_ok=True)
    main_files=[p for p in SRC.rglob("*") if p.is_file()
                and "downloads" not in p.relative_to(SRC).parts
                and "__pycache__" not in p.parts]
    outputs = {}
    host_labels=("Claude-Code", "Gemini-CLI", "GPT-Codex")
    for host in host_labels:
        tail="plugin" if host!="Gemini-CLI" else "extension"
        dest=DIST/f"kumihan-bn-{host}-{tail}-{VERSION}.zip"
        count=archive(dest,main_files,SRC.parent)
        outputs[dest.name]={"files":count,"type":"plugin" if tail=="plugin" else "extension","host":host}
    for skill in SKILLS:
        src=SRC/"skills"/skill
        dest=DIST/f"{skill}-skill-{VERSION}.zip"
        count=archive(dest,[p for p in src.rglob("*") if p.is_file()],src.parent)
        outputs[dest.name]={"files":count,"type":"skill","host":"portable"}
    metadata={"name":BRAND,"package_slug":"kumihan-bn","version":VERSION,
              "license":"Apache-2.0","developer":"L&Co. LLC",
              "host_installation":"NOT_CHECKED","native_proofreading":"NOT_CHECKED",
              "browser_render":"NOT_CHECKED","files":[]}
    checks=[]
    for name, details in sorted(outputs.items()):
        raw=(DIST/name).read_bytes()
        sha=hashlib.sha256(raw).hexdigest()
        metadata["files"].append({"name":name,"bytes":len(raw),"sha256":sha,**details})
        checks.append(f"{sha}  {name}")
    (DIST/"MANIFEST.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+"\n","utf-8")
    (DIST/"SHA256SUMS.txt").write_text("\n".join(checks)+"\n","utf-8")
    print(json.dumps({"status":"generated","archives":len(outputs),"manifest":str(DIST/"MANIFEST.json"),"details":outputs},ensure_ascii=False))
    return 0

if __name__=="__main__":raise SystemExit(build())
