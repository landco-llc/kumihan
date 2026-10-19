#!/usr/bin/env python3
"""KUMIHAN｜Szyk: bounded read-only Polish checker, NOT a full spelling engine."""
from pathlib import Path
import argparse, hashlib, json, re
def inspect(original, locale="pl", candidate=None, source_role="authored_source"):
    if locale not in ("pl","pl-PL"):raise ValueError("Only pl and pl-PL are supported")
    src=original.decode("utf-8")
    candidate=original if candidate is None else candidate
    candidate.decode("utf-8")
    checksum=hashlib.sha256(original).hexdigest()
    items=[]
    def finding(rule,match,proposed):
        items.append({"rule_id":rule,"status":"needs-review","method":"bounded-static-candidate",
          "evidence":{"offset":match.start(),"text":match.group(0)},"proposal":proposed,"source_sha256":checksum})
    for match in re.finditer(r"word-break\s*:\s*break-all\b",src,re.I):
        finding("PL-TYPE-08",match,"Sprawdź łamanie polskich słów i nawigacji. | Review possible word splits.")
    if re.search(r"<html\b",src,re.I) and not re.search(r"<html[^>]*\blang\s*=\s*['\"]pl(?:-PL)?['\"]",src,re.I):
        finding("PL-I18N-01",re.search(r"<html\b",src,re.I),"Ustaw język pl dla polskiego dokumentu. | Set lang=pl for Polish content.")
    if source_role=="new_copy":
        for match in re.finditer(r"[“”][^“”\n]{1,120}[“”]",src):
            finding("PL-TYPE-03",match,"Rozważ polskie „…” w nowym tekście. | Review new-copy quote style.")
    if source_role=="observed_layout":
        for match in re.finditer(r"(?<!\w)[aiouwzAIUOWZ][ \t]*\r?\n",src):
            finding("PL-TYPE-01",match,"Sprawdź samotną literę na końcu rzeczywistego wiersza. | Check observed dangling word.")
    return {
     "product":"KUMIHAN｜Szyk","version":"0.1.0","locale":locale,"source_role":source_role,
     "original_sha256":checksum,"original_bytes":len(original),
     "source_preservation":{"status":"passed" if candidate==original else "failed",
       "candidate_sha256":hashlib.sha256(candidate).hexdigest(),"method":"exact-byte-comparison"},
     "findings":items,"rendering":"not-checked","editorial_review":"needs-review",
     "native_host":"not-checked","complete_spellcheck":False,"research_fixtures_executed":0}
def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("original",type=Path);a.add_argument("--candidate",type=Path)
    a.add_argument("--locale",default="pl")
    a.add_argument("--source-role",default="authored_source",choices=["authored_source","new_copy","observed_layout","code"])
    opts=a.parse_args()
    try:
        r=inspect(opts.original.read_bytes(),opts.locale,opts.candidate.read_bytes() if opts.candidate else None,opts.source_role)
    except (OSError,UnicodeError,ValueError) as exc:a.error(str(exc))
    print(json.dumps(r,ensure_ascii=False,indent=2))
    return int(r["source_preservation"]["status"]=="failed")
if __name__=="__main__":raise SystemExit(main())
