#!/usr/bin/env python3
"""KUMIHAN Khmer: read-only source-preservation and bounded style checks."""
import argparse
import hashlib
import json
import re
from pathlib import Path

LOCALES = ("km", "km-KH")
STYLES = (
    ("KM-01", r'lang\s*=\s*["\x27]kh(?:-KH)?["\x27]', "Use Khmer language tag km / km-KH; kh is not Khmer."),
    ("KM-09", r'word-break\s*:\s*break-all', "Avoid break-all for natural Khmer prose."),
    ("KM-09", r'line-break\s*:\s*anywhere', "Avoid broad arbitrary breaks."),
    ("KM-13", r'line-height\s*:\s*(?:1(?:\.0)?|normal)\s*[;}]', "Inspect vertical marks and rendering; this is not an automatic failure."),
    ("KM-14", r'(?:max-)?height\s*:\s*\d+(?:px|rem)', "Review clipped multiline Khmer UI and controls."),
    ("KM-15", r'letter-spacing\s*:\s*[-+]?[0-9.]+(?:em|px|rem)', "Review tracking for Khmer-script text."),
    ("KM-23", r'text-overflow\s*:\s*ellipsis', "Check that meaningful Khmer copy is not hidden."),
)

def inspect(source, locale="km-KH", candidate=None, context=None):
    if locale not in LOCALES:
        raise ValueError("Unsupported Khmer locale: "+str(locale))
    text = source.decode("utf-8")
    findings = [
        {"rule_id": rid, "status": "needs-review", "offset": match.start(),
         "evidence": match.group(0), "note": note}
        for rid, pattern, note in STYLES
        for match in re.finditer(pattern, text, flags=re.I)
    ]
    for codepoint in ("\u17a3", "\u17a4"):
        for m in re.finditer(codepoint, text):
            findings.append({"rule_id": "KM-07", "status": "needs-review", "offset": m.start(),
                             "evidence": f"U+{ord(codepoint):04X}",
                             "note": "Deprecated Khmer character; do not auto-replace."})
    for codepoint in ("\u17b4", "\u17b5", "\u17d8"):
        for m in re.finditer(codepoint, text):
            findings.append({"rule_id": "KM-07", "status": "needs-review", "offset": m.start(),
                             "evidence": f"U+{ord(codepoint):04X}",
                             "note": "Discouraged Khmer character; do not auto-replace."})
    for m in re.finditer("\u17d2(?=$|[\\s])", text):
        findings.append({"rule_id": "KM-04", "status": "needs-review", "offset": m.start(),
                         "evidence": "U+17D2", "note": "Possible dangling COENG; requires native inspection."})
    findings.sort(key=lambda v: (v["offset"], v["rule_id"]))
    return {"product": "KUMIHAN｜លំនឹង", "version": "0.1.0", "locale": locale,
            "source_sha256": hashlib.sha256(source).hexdigest(),
            "source_bytes": len(source),
            "preservation": "not-checked" if candidate is None
                else ("passed" if candidate == source else "failed"),
            "khmer_codepoints": sum(0x1780 <= ord(ch) <= 0x17FF for ch in text),
            "coeng_count": text.count("\u17d2"),
            "context": context, "findings": findings, "auto_fixes": 0,
            "rendering": "not-checked", "native_host": "not-checked",
            "editorial_review": "needs-review"}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("--candidate", type=Path)
    p.add_argument("--locale", choices=LOCALES, default="km-KH")
    p.add_argument("--context")
    args = p.parse_args()
    result = inspect(args.source.read_bytes(), args.locale,
        args.candidate.read_bytes() if args.candidate else None, args.context)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if result["preservation"] == "failed" else 0)
