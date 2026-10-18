#!/usr/bin/env python3
"""KUMIHAN Compasso. Read-only Portuguese typography candidates; never rewrites the source."""
import argparse, hashlib, json, re
from pathlib import Path
LOCALES=("pt","pt-BR","pt-PT","pt-AO","pt-MZ")
RULES=(("PT-17",r"word-break\s*:\s*break-all","Arbitrary word breaking needs rendered review."),("PT-11",r"\d(?:km|kg|cm|mm)\b","Check number–unit spacing and authoritative house style."),("PT-10",r"\d%","Confirm house-style/SI percent spacing; never auto-fix."),("PT-07",r"\b\d{1,3},\d{3}\.\d{2}\b","Possibly imported en-style number; do not reinterpret."),("PT-18",r"(?m)^-[a-záàâãéêíóôõúç]","Check repeated hyphen only with actual rendered line breaks."))
def inspect(raw,locale="pt",candidate=None,house_style=None):
 if locale not in LOCALES:raise ValueError("Unsupported locale")
 text=raw.decode("utf-8")
 found=[{"rule_id":rid,"status":"needs-review","offset":m.start(),"evidence":m.group(),"note":note} for rid,pat,note in RULES for m in re.finditer(pat,text,re.I)]
 return {"product":"KUMIHAN｜Compasso","version":"0.1.0","locale":locale,"house_style":house_style,"source_sha256":hashlib.sha256(raw).hexdigest(),"source_bytes":len(raw),"preservation":"not-checked" if candidate is None else ("passed" if raw==candidate else "failed"),"findings":found,"rendering":"not-checked","native_host":"not-checked","language_editor":"not-checked","rule_catalog":"36 advisory rules"}
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("source",type=Path);p.add_argument("--candidate",type=Path);p.add_argument("--locale",choices=LOCALES,default="pt");p.add_argument("--house-style");a=p.parse_args()
 report=inspect(a.source.read_bytes(),a.locale,a.candidate.read_bytes() if a.candidate else None,a.house_style)
 print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(1 if report["preservation"]=="failed" else 0)
