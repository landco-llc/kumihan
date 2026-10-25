#!/usr/bin/env python3
"""Accord v0.1.2: non-destructive French typography candidates, not a renderer."""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

VERSION = "0.1.2"
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

def _rule(style, mark):
  if style == "fr-fr-editorial": return "FR-FR-02" if mark == ":" else "FR-FR-01", "FR01"
  if style == "fr-ca-oqlf": return "FR-CA-02" if mark == ":" else "FR-CA-01", "FR02"
  return "FR-EU-01", "FR03"


def _scan(text, house_style):
  """One source-coordinate scanner for both audit and generated-copy proposals.

  Numeric colons (time, ratios and similar values) are excluded conservatively.
  This is bounded plain-text analysis, not a parser for documents or markup.
  """
  ranges = [m.span() for m in PROTECT.finditer(text)]
  style = STYLES[house_style]
  evaluations, edits = [], []
  for m in re.finditer(r"([^\S\r\n]*)([!?;:])", text):
    gap, mark = m.groups()
    pos = m.end() - 1
    if protected(*m.span(), ranges): continue
    prior = text[m.start() - 1] if m.start() else ""
    numeric = mark == ":" and pos > 0 and pos + 1 < len(text) and text[pos-1].isdigit() and text[pos+1].isdigit()
    # A natural prose mark needs preceding text; opening delimiters and line starts do not qualify.
    attached_letter_mark = False
    if prior and unicodedata.category(prior).startswith("M"):
      base = m.start() - 1
      while base >= 0 and unicodedata.category(text[base]).startswith("M"):
        base -= 1
      attached_letter_mark = base >= 0 and text[base].isalpha()
    applicable = bool(prior and (prior.isalnum() or attached_letter_mark or prior in "»\"')]}")) and not numeric
    rid, source = _rule(house_style, mark)
    wanted = style[mark]
    allowed = ("", "\u202f") if wanted is None else (wanted,)
    status = "outside_supported_scope" if not applicable else "accepted" if gap in allowed else "nonconforming" if all(c in SPACES for c in gap) else "needs_review"
    record = {"rule_id": rid, "status": status, "offset": m.start(), "evidence": m.group(),
              "source_range": {"start": m.start(), "end": m.end(), "unit": "unicode_code_point"},
              "source_ref": {"catalog": "accord-source-catalog@0.1.0", "id": source},
              "accepted_spaces": list(allowed), "expected_space": "U+00A0" if wanted == "\u00a0" else "U+202F" if wanted == "\u202f" else "none",
              "reason": "numeric_or_syntax_colon" if numeric else "no_preceding_prose" if not applicable else None}
    evaluations.append(record)
    if status == "nonconforming": edits.append((m.start(), pos, "" if wanted is None else wanted))
  for m in re.finditer(r"«([^«»]*)»", text):
    if protected(*m.span(), ranges): continue
    inner = m.group(1)
    middle = inner.strip(SPACES)
    if not middle: continue
    left = len(inner) - len(inner.lstrip(SPACES))
    right = len(inner) - len(inner.rstrip(SPACES))
    wanted = style["quotes"]
    correct = inner[:left] == wanted and (inner[len(inner)-right:] if right else "") == wanted
    unknown_padding = any(c.isspace() and c not in SPACES for c in (inner[0], inner[-1]))
    status = "needs_review" if unknown_padding else "accepted" if correct else "nonconforming"
    evaluations.append({"rule_id": "FR-GUIL-01", "status": status, "offset": m.start(), "evidence": m.group(),
                        "source_range": {"start": m.start(), "end": m.end(), "unit": "unicode_code_point"},
                        "source_ref": {"catalog": "accord-source-catalog@0.1.0", "id": _rule(house_style, ":")[1]},
                        "note": "Explicit selected house style; plain-text quote spacing only."})
    if status == "nonconforming":
      edits.extend(((m.start()+1, m.start()+1+left, wanted), (m.end()-1-right, m.end()-1, wanted)))
  return evaluations, edits


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
          "findings":[],"evaluations":[],"rendered_evidence":"not-checked",
          "range_unit":"unicode_code_point",
          "proposal_policy":{"id":"accord-generated-plain-repair@0.1.0",
                             "accepted_forms":"preserve", "oqlf_nonconforming_known_space":"zero",
                             "unknown_whitespace":"review_without_change",
                             "authority":"product_policy; only explicit generated plain-text proposal"},
          "scope":"bounded plain-text advisory; markup tags are guarded, document/language structure is not parsed",
          "limitations":"Not a document editor, formatter, PDF/Office renderer, font/accessibility checker or native host test."}
  if not house_style:
    report["evaluation_status"] = "not_checked_unresolved_house_style"
    return report
  evaluations, _ = _scan(text, house_style)
  report["evaluations"] = evaluations
  report["findings"] = [dict(e, status="needs-review") for e in evaluations if e["status"] in ("nonconforming", "needs_review")]
  report["evaluation_status"] = "bounded_checks_completed"
  return report


def _has_structure(text):
  """Conservative exclusion, not a Markdown/HTML parser.

  A bracket may denote an inline, reference, collapsed or shortcut link,
  including a reference defined elsewhere. Such ambiguity is outside this
  plain-text helper. Leading block markers and inline markup are likewise
  rejected rather than flattened into editable copy.
  """
  return bool(re.search(
      r"<[^>]*>|\[|`|"
      r"^\s*(?:#{1,6}(?:\s|$)|[-+*](?:\s|$)|[0-9]{1,9}[.)](?:\s|$)|>|~{3,}|\|)|"
      r"(?<!\w)(?:\*{1,3}|_{1,3}|~~)\S",
      text, re.M))


def propose_generated_plain(text,house_style):
  if house_style not in STYLES:raise ValueError("Choose explicit house style")
  if PROTECT.search(text) or _has_structure(text) or "\n" in text or "\r" in text:
    raise ValueError("Only one-line unstructured generated copy is eligible")
  _, edits = _scan(text, house_style)
  out = text
  for start, end, value in sorted(edits, reverse=True):
    out = out[:start] + value + out[end:]
  return out

def inspect_context(text, context, *, raw_locale=None, source_sha256=None,
                    protected_ranges=(), typed_values=()):
  """Opt-in plain-text audit bridge for existing context axes and scalar ranges.

  This does not modify the closed common context schema, resolve regional
  profiles, format typed values or edit structured/mixed-language documents.
  Caller ranges require the exact UTF-8 hash of this source. No normalization
  or source-map reindexing is performed. Unknown critical extensions block.
  """
  digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
  result = {"adapter_id": "kumihan.accord.context-audit@0.1.0",
            "source_sha256": digest, "raw_locale": raw_locale,
            "resolved_module_id": None, "status": "blocked", "report": None,
            "source_preserved": True, "normalization": "none",
            "capabilities": ["plain_text_audit", "source_bound_scalar_protection"],
            "unsupported_capabilities": ["structured_edit", "mixed_language_resolution", "typed_value_format", "render"]}
  def stop(status, reason):
    result.update(status=status, reason=reason)
    return result
  if not isinstance(context, dict): return stop("blocked", "invalid_context")
  axes = {"language", "house_style", "region", "market", "register", "role", "medium",
          "norm_edition", "format_locale", "direction", "intent", "extensions"}
  if set(context) - axes: return stop("blocked", "unknown_context_axis")
  if any(value is not None and not isinstance(value, str) for key,value in context.items() if key != "extensions"):
    return stop("blocked", "invalid_context_axis")
  extensions = context.get("extensions", [])
  if not isinstance(extensions, list): return stop("blocked", "invalid_extensions")
  for extension in extensions:
    if not isinstance(extension, dict) or set(extension) != {"namespace", "version", "critical", "payload"} or not isinstance(extension["critical"], bool):
      return stop("blocked", "invalid_extension")
    if not isinstance(extension["namespace"], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", extension["namespace"]) or not isinstance(extension["version"], str) or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", extension["version"]):
      return stop("blocked", "invalid_extension_identity")
    if extension["critical"]: return stop("blocked", "unsupported_critical_extension")
  result["uninterpreted_extensions"] = extensions
  language = context.get("language")
  if language is None: return stop("needs_review", "unknown_language")
  if language != "fr": return stop("blocked", "resolved_language_conflict")
  result["resolved_module_id"] = "fr"
  if raw_locale is None: return stop("needs_review", "unknown_raw_locale")
  if raw_locale not in LOCALES: return stop("outside_supported_scope", "unsupported_raw_locale")
  if context.get("house_style") not in STYLES:
    return stop("needs_review" if context.get("house_style") is None else "outside_supported_scope", "unresolved_house_style")
  if context.get("norm_edition") is not None: return stop("needs_review", "norm_edition_not_connected")
  if not isinstance(protected_ranges, (list, tuple)) or not isinstance(typed_values, (list, tuple)):
    return stop("blocked", "invalid_range_or_typed_value_collection")
  if typed_values: return stop("outside_supported_scope", "typed_values_not_connected")
  if _has_structure(text):
    return stop("outside_supported_scope", "structured_input_not_parsed")
  if source_sha256 is not None and source_sha256 != digest: return stop("blocked", "source_hash_mismatch")
  if protected_ranges and source_sha256 is None: return stop("blocked", "source_hash_required_for_ranges")
  ranges = []
  for r in protected_ranges:
    if not isinstance(r, dict) or set(r) != {"start", "end", "coordinate"} or r["coordinate"] != "scalar":
      return stop("blocked", "unsupported_range_coordinates")
    if type(r["start"]) is not int or type(r["end"]) is not int or not 0 <= r["start"] < r["end"] <= len(text):
      return stop("blocked", "invalid_source_range")
    ranges.append((r["start"], r["end"]))
  report = inspect(text, raw_locale, context["house_style"])
  for item in report["evaluations"]:
    r = item["source_range"]
    if protected(r["start"], r["end"], ranges):
      item.update(status="outside_supported_scope", reason="caller_protected_source_range")
  report["findings"] = [dict(item, status="needs-review") for item in report["evaluations"] if item["status"] in ("nonconforming", "needs_review")]
  result["report"] = report
  result["context"] = dict(context)
  return stop("completed", "plain_text_audit_only")


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
