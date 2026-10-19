#!/usr/bin/env python3
"""KUMIHAN｜Hlela: non-writing source comparison + bounded advisory matches."""
import argparse, hashlib, json, re
from pathlib import Path
LOCALES=("zu","zu-ZA")
RULES=(
 ("ZU-03",r'lang\s*=\s*["\x27]zu_[A-Za-z]+["\x27]',"Use BCP47 hyphens, not underscore."),
 ("ZU-06",r'word-break\s*:\s*break-all',"Natural text should avoid break-all."),
 ("ZU-07",r'text-overflow\s*:\s*ellipsis',"Check that meaning is not clipped."),
 ("ZU-09",r'hyphens\s*:\s*auto',"Check actual language dictionary and rendering."),
 ("ZU-14",r'text-transform\s*:\s*uppercase',"Display casing is not stored spelling."),
)
def inspect(raw,locale="zu-ZA",candidate=None,house_style=None):
    if locale not in LOCALES: raise ValueError("Unsupported locale: "+str(locale))
    txt=raw.decode("utf-8")
    f=[{"rule_id":rid,"status":"needs-review","offset":m.start(),"evidence":m.group(),"note":note}
        for rid,pattern,note in RULES for m in re.finditer(pattern,txt,re.I)]
    return {"product":"KUMIHAN｜Hlela","version":"0.1.0","locale":locale,
            "source_sha256":hashlib.sha256(raw).hexdigest(),"source_bytes":len(raw),
            "preservation":"not-checked" if candidate is None else ("passed" if candidate==raw else "failed"),
            "house_style":house_style,"findings":f,"auto_fixes":0,
            "rendering":"not-checked","native_host":"not-checked","native_editor":"not-checked"}
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source",type=Path);p.add_argument("--candidate",type=Path)
    p.add_argument("--locale",choices=LOCALES,default="zu-ZA");p.add_argument("--house-style")
    a=p.parse_args()
    r=inspect(a.source.read_bytes(),a.locale,a.candidate.read_bytes() if a.candidate else None,a.house_style)
    print(json.dumps(r,ensure_ascii=False,indent=2))
    raise SystemExit(1 if r["preservation"]=="failed" else 0)
