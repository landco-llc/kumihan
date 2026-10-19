#!/usr/bin/env python3
"""Read-only Bangla source fidelity checks; not a shaping renderer."""
import argparse, hashlib, json, unicodedata
from pathlib import Path

def check(source: bytes, candidate: bytes):
    a=source.decode("utf-8"); b=candidate.decode("utf-8")
    equal=(source==candidate)
    return {
        "rule_id":"BN-002", "status":"passed" if equal else "failed",
        "source_sha256":hashlib.sha256(source).hexdigest(),
        "candidate_sha256":hashlib.sha256(candidate).hexdigest(),
        "bytes_equal":equal,
        "derived_nfc_equal":unicodedata.normalize("NFC",a)==unicodedata.normalize("NFC",b),
        "join_control_preserved": [(i,ord(x)) for i,x in enumerate(a) if x in ("\u200c","\u200d")] == [(i,ord(x)) for i,x in enumerate(b) if x in ("\u200c","\u200d")],
        "rendering":"not-checked", "translation":"not-checked", "native_review":"not-checked",
        "note":"Byte differences require authorization even when normalized text compares equal."
    }

def inspect(source: bytes):
    a=source.decode("utf-8")
    return {
        "source_sha256":hashlib.sha256(source).hexdigest(),
        "bytes":len(source),
        "join_controls":[{"index":i,"codepoint":f"U+{ord(c):04X}"} for i,c in enumerate(a) if c in ("\u200c","\u200d")],
        "nfc_is_equal":unicodedata.normalize("NFC",a)==a,
        "status":"observed", "rendering":"not-checked", "grapheme_segmentation":"not-checked", "native_review":"not-checked"
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("source",type=Path);p.add_argument("--candidate",type=Path)
    args=p.parse_args()
    src=args.source.read_bytes()
    result=check(src,args.candidate.read_bytes()) if args.candidate else inspect(src)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if result.get("status")=="failed" else 0

if __name__=="__main__": raise SystemExit(main())
