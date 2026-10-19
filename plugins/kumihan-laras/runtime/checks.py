#!/usr/bin/env python3
"""KUMIHAN｜Laras v0.1.0: read-only and advisory. Never rewrites source."""
import argparse, hashlib, json, re
from pathlib import Path
LOCALES=("id","id-ID")
RULES=(
 ("ID-31",r"\blang\s*=\s*[\"']in(?:-ID)?[\"']","Legacy language tag; review lang=id."),
 ("ID-32",r"word-break\s*:\s*break-all","Arbitrary word breaking may violate Indonesian words."),
 ("ID-32",r"hyphens\s*:\s*auto","Verify actual Indonesian dictionary and rendered output."),
 ("ID-05",r"\bdi\s{2,}(?:toko|rumah|tempat)\b","Check preposition spacing in context."),
 ("ID-06",r"\b\w+[\u2013\u2014]\w+\b","Possible lexical reduplication hyphen changed to dash."),
 ("ID-24",r"\bRp\s*\d[\d.,]*","Verify IDR fraction digits and existing source notation."),
 ("ID-26",r"\b(?:[01]\d|2[0-3])[.:][0-5]\d\b","Dot and colon clock formats may both be valid."),
 ("ID-28",r"\b(?:kami|kita)\b","Inclusive/exclusive pronoun requires context."),
)
def inspect(raw,locale="id-ID",candidate=None,house_style=None):
 if locale not in LOCALES: raise ValueError("Unsupported locale")
 text=raw.decode("utf-8")
 findings=[{"rule_id":rid,"status":"needs-review","offset":m.start(),"evidence":m.group(),"note":note}
           for rid,pattern,note in RULES for m in re.finditer(pattern,text,re.I)]
 return {"product":"KUMIHAN｜Laras","version":"0.1.0","locale":locale,"house_style":house_style,
   "source_sha256":hashlib.sha256(raw).hexdigest(),"source_bytes":len(raw),
   "preservation":"not-checked" if candidate is None else ("passed" if raw==candidate else "failed"),
   "findings":findings,"rendering":"not-checked","native_host":"not-checked","language_editor":"not-checked"}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("--candidate",type=Path)
 p.add_argument("--locale",choices=LOCALES,default="id-ID");p.add_argument("--house-style")
 a=p.parse_args();out=inspect(a.source.read_bytes(),a.locale,a.candidate.read_bytes() if a.candidate else None,a.house_style)
 print(json.dumps(out,ensure_ascii=False,indent=2));raise SystemExit(1 if out["preservation"]=="failed" else 0)
