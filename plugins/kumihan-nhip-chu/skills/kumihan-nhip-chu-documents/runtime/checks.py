#!/usr/bin/env python3
"""KUMIHAN Nhịp Chữ: bounded, read-only Vietnamese typography advisor (stdlib)."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

VERSION = "0.1.0"
CSS_BREAK = re.compile(r"\\bword-break\\s*:\\s*break-all\\b", re.I)
CSS_HYPHENS = re.compile(r"\\bhyphens\\s*:\\s*auto\\b", re.I)
def inspect(raw, locale="vi-VN", candidate=None, style_text=None):
    if locale not in ("vi", "vi-VN"):
        raise ValueError("Unsupported locale")
    text = raw.decode("utf-8")
    if candidate is not None:
        candidate.decode("utf-8")
    findings = []
    def note(rule, message, status="needs-review", offset=None):
        findings.append({"rule_id":rule,"status":status,"message":message,"offset":offset})
    if unicodedata.normalize("NFC", text) != text:
        note("VI-03","Source contains canonically decomposed sequences; compare normalized copies but do not rewrite original.")
    for i, char in enumerate(text):
        if unicodedata.combining(char) and (i == 0 or text[i-1].isspace() or text[i-1] in "<>"):
            note("VI-04","Combining mark at a potential detached boundary; review actual grapheme sequence.",offset=i)
    if style_text:
        for match in CSS_BREAK.finditer(style_text):
            note("VI-15","CSS word-break:break-all candidate in inspected stylesheet; scope correction to intended Vietnamese text.",offset=match.start())
        for match in CSS_HYPHENS.finditer(style_text):
            note("VI-13","CSS automatic hyphenation requires locale/dictionary and rendered verification.",offset=match.start())
    return {"product":"KUMIHAN｜Nhịp Chữ","version":VERSION,"locale":locale,"mode":"audit",
       "source_sha256":hashlib.sha256(raw).hexdigest(),"source_bytes":len(raw),
       "preservation":{"status":"not-checked" if candidate is None else ("passed" if candidate==raw else "failed"),
           "method":"exact bytes (no normalization or edits)"},
       "findings":findings,"rendered_evidence":"not-checked","native_speaker_review":"not-checked",
       "host_activation":"not-checked",
       "limitations":"Static candidates only; not grammar correction, rendered font verification or host certification."}
def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--candidate", type=Path)
    parser.add_argument("--css", type=Path, help="Optional CSS for advisory checks")
    parser.add_argument("--locale", choices=("vi","vi-VN"), default="vi-VN")
    args=parser.parse_args(argv)
    try:
        data=args.source.read_bytes()
        other=args.candidate.read_bytes() if args.candidate else None
        css=args.css.read_text(encoding="utf-8") if args.css else None
        result=inspect(data,args.locale,other,css)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["preservation"]["status"]=="failed" else 0
if __name__ == "__main__":
    sys.exit(main())
