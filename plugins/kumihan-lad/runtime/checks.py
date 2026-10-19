#!/usr/bin/env python3
"""Limited read-only Russian typography checks: does not rewrite input."""
import argparse, hashlib, json, re, unicodedata
from pathlib import Path
LOCALES = ("ru", "ru-RU")
RULES = (
  ("RU-022", r"word-break\s*:\s*break-all", "Arbitrary Cyrillic word breaks require actual render review."),
  ("RU-025", r"\d(?:кг|км|см|мм|°C)\b", "Review value–unit spacing; never change numeric values."),
  ("RU-025", r"\d%", "Confirm percentage spacing by house style."),
  ("RU-023", r"\b\d{1,3},\d{3}\.\d{2}\b", "Possible imported locale format; do not reinterpret the value."),
  ("RU-009", r'["][А-Яа-яЁё ]{2,}["]', "Quotes may follow a house style; exclude code or intentional quotation."),
  ("RU-014", r"\.{3}", "Review ellipsis style by context."),
)
def inspect(raw, locale="ru-RU", candidate=None, house_style=None):
  if locale not in LOCALES: raise ValueError("Unsupported locale")
  text = raw.decode("utf-8",errors="strict")
  found = [{"rule_id":rid,"status":"needs-review","offset":m.start(),"evidence":m.group(),
            "note_en":note} for rid,pat,note in RULES for m in re.finditer(pat,text,re.I)]
  for m in re.finditer(r"(?<!\w)[A-Za-zА-Яа-яЁё]{3,}(?!\w)",text):
    token=m.group()
    if re.search("[A-Za-z]",token) and re.search("[А-Яа-яЁё]",token):
      found.append({"rule_id":"RU-008","status":"needs-review","offset":m.start(),"evidence":token,
                    "note_en":"Mixed Latin/Cyrillic token. Verify by context; never auto-replace."})
  if unicodedata.normalize("NFC",text) != text:
    found.append({"rule_id":"RU-005","status":"needs-review","offset":None,"evidence":"non-NFC source",
                  "note_en":"NFC comparison is not permission to modify original bytes."})
  if unicodedata.normalize("NFKC",text) != text:
    found.append({"rule_id":"RU-006","status":"needs-review","offset":None,"evidence":"NFKC changes bytes",
                  "note_en":"Compatibility folding may change № or no-break spaces."})
  return {"product":"KUMIHAN｜Лад","version":"0.1.0","locale":locale,"house_style":house_style,
          "source_sha256":hashlib.sha256(raw).hexdigest(),"source_bytes":len(raw),
          "preservation":"not-checked" if candidate is None else ("passed" if raw==candidate else "failed"),
          "findings":found,"rendering":"not-checked","native_host":"not-checked",
          "language_editor":"not-checked","rule_catalog":"48 contextual advisory rules"}
if __name__ == "__main__":
  p=argparse.ArgumentParser()
  p.add_argument("source",type=Path);p.add_argument("--candidate",type=Path)
  p.add_argument("--locale",choices=LOCALES,default="ru-RU");p.add_argument("--house-style")
  a=p.parse_args()
  report=inspect(a.source.read_bytes(),a.locale,a.candidate.read_bytes() if a.candidate else None,a.house_style)
  print(json.dumps(report,ensure_ascii=False,indent=2))
  raise SystemExit(1 if report["preservation"]=="failed" else 0)
