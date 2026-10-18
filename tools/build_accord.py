#!/usr/bin/env python3
"""Build 15 reproducible Accord v0.1.0 archives and checksums (stdlib only)."""
import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"plugins/kumihan-accord"
SKILLS=("kumihan-accord","kumihan-accord-web","kumihan-accord-documents","kumihan-accord-review")
HOSTS=("chatgpt","claude","gemini")
PLUGINS={"chatgpt":"chatgpt-codex-plugin","claude":"claude-code-plugin","gemini":"gemini-cli-extension"}
META={"chatgpt":{"plugin.json",".codex-plugin/plugin.json"},
      "claude":{".claude-plugin/plugin.json"},
      "gemini":{"gemini-extension.json","GEMINI.md"}}
COMMON={"README.md","INSTALL.md","LICENSE","RELEASE_NOTES.md","THIRD_PARTY_NOTICES.md","UPDATES.md","LIGHT_REVIEW.md"}

def write_zip(path,entries):
    with ZipFile(path,"w",compression=ZIP_DEFLATED) as archive:
        for src,name in sorted(entries,key=lambda p:p[1]):
            info=ZipInfo(name,date_time=(2026,10,19,0,0,0))
            info.compress_type=ZIP_DEFLATED
            info.external_attr=0o100644<<16
            archive.writestr(info,src.read_bytes(),compress_type=ZIP_DEFLATED,compresslevel=9)

def build(out):
    out.mkdir(parents=True,exist_ok=True)
    all_files=[f for f in SOURCE.rglob("*") if f.is_file() and
               not any(segment in {"__pycache__",".DS_Store","downloads"} for segment in f.parts)]
    hashes=[]
    for host in HOSTS:
        for name in SKILLS:
            root=SOURCE/"skills"/name
            entries=[(f,(Path(name)/f.relative_to(root)).as_posix()) for f in all_files if root in f.parents]
            assert any(f.name=="SKILL.md" for f,_ in entries)
            target=out/f"{name}-{host}-skill-v0.1.0.zip"
            write_zip(target,entries)
            hashes.append((target.name,hashlib.sha256(target.read_bytes()).hexdigest()))
        entries=[]
        for f in all_files:
            rel=f.relative_to(SOURCE).as_posix()
            include=rel.startswith(("skills/","rules/","locales/","references/","schemas/","runtime/","entrypoints/")) or rel in COMMON or rel=="sources.json" or rel in META[host]
            if include:entries.append((f,"kumihan-accord/"+rel))
        target=out/f"kumihan-accord-{PLUGINS[host]}-v0.1.0.zip"
        write_zip(target,entries)
        hashes.append((target.name,hashlib.sha256(target.read_bytes()).hexdigest()))
    hashes.sort()
    (out/"SHA256SUMS.txt").write_text("".join(f"{digest}  {name}\n" for name,digest in hashes),encoding="utf-8")
    (out/"MANIFEST.json").write_text(json.dumps({"product":"KUMIHAN｜Accord","version":"0.1.0",
          "tag":"kumihan-fr-v0.1.0","packages":[{"name":n,"sha256":h} for n,h in hashes]},
          ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return len(hashes)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,default=ROOT/"dist"/"accord-v0.1.0")
    args=parser.parse_args()
    print(f"Built {build(args.out)} ZIPs")
