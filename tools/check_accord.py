#!/usr/bin/env python3
"""Verify Accord ZIP content, manifest and checksums without host claims."""
import hashlib
import json
import sys
from pathlib import Path
from zipfile import ZipFile

def check(out):
    manifest=json.loads((out/"MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["product"]=="KUMIHAN｜Accord" and manifest["version"]=="0.1.0"
    entries=manifest["packages"]
    assert len(entries)==15 and len({a["name"] for a in entries})==15
    lines=(out/"SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
    assert len(lines)==15
    assert {line.split("  ",1)[1]:line.split("  ",1)[0] for line in lines}=={a["name"]:a["sha256"] for a in entries}
    for item in entries:
        name=item["name"]
        assert name.endswith("-v0.1.0.zip")
        assert hashlib.sha256((out/name).read_bytes()).hexdigest()==item["sha256"]
        with ZipFile(out/name) as arc:
            assert arc.testzip() is None
            paths=arc.namelist()
            assert len(paths)==len(set(paths)) and paths
            assert not any(p.startswith("/") or ".." in Path(p).parts for p in paths)
            assert any(p.endswith("/LICENSE") for p in paths)
            assert any(p.endswith("/rules/catalog.json") for p in paths)
            if "-skill-" in name:
                assert sum(p.endswith("/SKILL.md") for p in paths)==1
                assert any(p.endswith("/runtime/checks.py") for p in paths)
            else:
                assert sum(p.endswith("/SKILL.md") for p in paths)==4
                want="plugin.json" if "chatgpt-codex" in name else ".claude-plugin/plugin.json" if "claude-code" in name else "gemini-extension.json"
                assert "kumihan-accord/"+want in paths
                m=json.loads(arc.read("kumihan-accord/"+want))
                assert m["name"]=="kumihan-accord" and m["version"]=="0.1.0" and " | " in m["description"]
                if "chatgpt-codex" in name:
                    assert m["extensions"]["com.openai"]["interface"]["displayName"]=="KUMIHAN｜Accord"
    print("PASS: 15 valid packages, ES+EN descriptions, metadata and SHA256")
if __name__=="__main__":check(Path(sys.argv[1]))
