#!/usr/bin/env python3
"""Accord v0.1.0: non-destructive French typography candidates, not a renderer."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

VERSION = "0.1.0"
STYLES = {
  "fr-fr-editorial": {"!":"\u202f","?":"\u202f",";":"\u202f",":":"\u00a0","quotes":"\u202f"},
  "fr-ca-oqlf": {"!":None,"?":None,";":None,":":"\u00a0","quotes":"\u00a0"},
  "eu-interinstitutional": {"!":"","?":"",";":"",":":"","quotes":""}
}
LOCALES = ("fr-FR","fr-CA","fr-BE","fr-CH")
SPACES = " \u00a0\u202f"
PROTECT = re.compile(r"(?s)\x60{3}.*?\x60{3}|\x60[^\x60\n]+\x60|https?://[^\s<>]+|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|<[^>]+>|\$\{[^{}]+\}|\{\{[^{}]+\}\}")

def protected(a,b,ranges):
  return any(a<end and b>start for start,end in ranges)

def inspect(text,locale="fr-FR",house_style=None,candidate=None):
  if locale not in LOCALES: raise ValueError("Unsupported locale")
  if house_style is not None and house_style not in STYLES: raise ValueError("Unknown house style")
  raw=text.encode("utf-8")
  report={"version":VERSION,"mode":"audit","locale":locale,"house_style":house_style,
          "house_style_status":"explicit" if house_style else "unresolved",
          "source_sha256":hashlib.sha256(raw).hexdigest(),"source_bytes":len(raw),
          "preservation":{"status":"not-checked" if candidate is None else
                          ("passed" if text==candidate else "failed"),
                          "method":"exact UTF-8; no normalization"},
          "findings":[],"rendered_evidence":"not-checked",
          "limitations":"Bounded advisory checks only; not a text editor, PDF/Office renderer, font/accessibility checker or native host test."}
  if not house_style: return report
  ranges=[m.span() for m in PROTECT.finditer(text)]
  style=STYLES[house_style]
  for m in re.finditer(r"([ \u00a0\u202f]*)([!?;:])",text):
    if protected(*m.span(),ranges):continue
    before,mark=m.groups()
    wanted=style[mark]
    if wanted is None or wanted==before or m.start()==0:continue
    report["findings"].append({"rule_id":"FR-GUIL-01" if False else "FR-FR-01" if house_style=="fr-fr-editorial" else
                                "FR-CA-02" if house_style=="fr-ca-oqlf" else "FR-EU-01",
                               "status":"needs-review","offset":m.start(),"evidence":m.group(),
                               "expected_space":"U+202F" if wanted=="\u202f" else
                               "U+00A0" if wanted=="\u00a0" else "none"})
  for m in re.finditer(r"«([^«»]*)»",text):
    if protected(*m.span(),ranges):continue
    inner=m.group(1);wanted=style["quotes"]
    if not inner:continue
    bad=((not inner.startswith(wanted) or not inner.endswith(wanted))
         if wanted else (inner[:1] in SPACES or inner[-1:] in SPACES))
    if bad:report["findings"].append({"rule_id":"FR-GUIL-01","status":"needs-review",
          "offset":m.start(),"evidence":m.group(),"note":"Context and house style must be verified."})
  return report

def propose_generated_plain(text,house_style):
  if house_style not in STYLES:raise ValueError("Choose explicit house style")
  if PROTECT.search(text) or "\n" in text or "\r" in text:
    raise ValueError("Only one-line unstructured generated copy is eligible")
  style=STYLES[house_style]
  def punct(m):
    prior,mark=m.groups(); required=style[mark]
    return (prior if required is None else required)+mark
  out=re.sub(r"([ \u00a0\u202f]*)([!?;:])",punct,text)
  def quote(m):
    middle=m.group(1).strip(SPACES)
    return "«"+style["quotes"]+middle+style["quotes"]+"»"
  return re.sub(r"«([^«»]*)»",quote,out)

def main(argv=None):
  parser=argparse.ArgumentParser(description=__doc__)
  parser.add_argument("source",type=Path)
  parser.add_argument("--locale",choices=LOCALES,default="fr-FR")
  parser.add_argument("--house-style",choices=tuple(STYLES))
  parser.add_argument("--candidate",type=Path)
  parser.add_argument("--source-origin",choices=("supplied","quoted","generated","translation-proposal"),default="supplied")
  parser.add_argument("--propose",action="store_true")
  args=parser.parse_args(argv)
  if args.propose and (args.source_origin!="generated" or not args.house_style):
    parser.error("--propose requires --source-origin generated and --house-style")
  try:
    raw=args.source.read_bytes();text=raw.decode("utf-8")
    cand=args.candidate.read_bytes() if args.candidate else None
    result=inspect(text,args.locale,args.house_style,cand.decode("utf-8") if cand is not None else None)
    result["source_sha256"]=hashlib.sha256(raw).hexdigest()
    if args.propose:
      result["proposal_only"]=propose_generated_plain(text,args.house_style)
      result["proposal_scope"]="generated plain text only; no file modification"
  except (OSError,UnicodeError,ValueError) as e:parser.error(str(e))
  print(json.dumps(result,ensure_ascii=False,indent=2))
  return 1 if result["preservation"]["status"]=="failed" else 0

if __name__=="__main__":sys.exit(main())
