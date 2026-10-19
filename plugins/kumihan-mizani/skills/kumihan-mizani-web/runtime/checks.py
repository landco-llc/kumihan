#!/usr/bin/env python3
"""KUMIHAN｜Mizani v0.1.0 advisory, source-preserving Swahili checker."""
import argparse, hashlib, json, re
from pathlib import Path
LOCALES=("sw","sw-TZ","sw-KE","sw-UG","sw-CD")
RULES=(
 ("SW-03",r"ng\\u2018|ng\\u201c","Suspicious opening quote where a lexical apostrophe may belong."),
 ("SW-05",r"word-break\\s*:\\s*break-all","Arbitrary breaking can damage Swahili words."),
 ("SW-13",r"hyphens\\s*:\\s*auto","Verify actual dictionary and rendered hyphenation first."),
 ("SW-06",r"\\blang\\s*=\\s*['\\\"]sw_[A-Za-z]+['\\\"]","Use BCP 47 hyphens (e.g. sw-TZ), not underscores."),
 ("SW-07",r"\\b(?:TZS|KES|UGX|CDF)\\s*[0-9][0-9., ]*","Check currency digits, spacing and explicit locale."),
 ("SW-08",r"\\bsaa\\s+(?:moja|mbili|tatu|nne|tano|sita|saba|nane|tisa|kumi)\\b","Distinguish Swahili colloquial clock from civil clock."),
)
def inspect(raw,locale="sw-TZ",candidate=None,house_style=None):
 if locale not in LOCALES: raise ValueError("Unsupported locale")
 source=raw.decode("utf-8")
 findings=[{"rule_id":rid,"status":"needs-review","offset":m.start(),"evidence":m.group(),"note":note}
     for rid,pattern,note in RULES for m in re.finditer(pattern,source,re.I)]
 return {"product":"KUMIHAN｜Mizani","version":"0.1.0","locale":locale,
    "source_sha256":hashlib.sha256(raw).hexdigest(),"source_bytes":len(raw),
    "house_style":house_style,"preservation":"not-checked" if candidate is None else ("passed" if raw==candidate else "failed"),
    "findings":findings,"rendering":"not-checked","native_host":"not-checked","native_editor":"not-checked"}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("--candidate",type=Path)
 p.add_argument("--locale",choices=LOCALES,default="sw-TZ");p.add_argument("--house-style")
 a=p.parse_args();r=inspect(a.source.read_bytes(),a.locale,a.candidate.read_bytes() if a.candidate else None,a.house_style)
 print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(1 if r["preservation"]=="failed" else 0)
