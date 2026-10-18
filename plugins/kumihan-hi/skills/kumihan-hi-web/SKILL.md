---
name: kumihan-hi-web
description: "हिंदी वेबसाइट और UI के अक्षर-विन्यास, फ़ॉन्ट और responsive डिज़ाइन के लिए उपयोग करें। | Use to build or refine source-preserving Hindi web typography and UI."
---

# KUMIHAN｜अक्षर-संगति

Web: author or refine semantic HTML/CSS with source fidelity, Indic shaping, responsive lines, font fallback and operation-specific browser evidence.

## First record intent and authority
Read [workflow](references/workflow.md). Record language/script/market/locale, reader, purpose, medium, profile, task mode (study/build/audit/refine), and content policy (preserve/propose/rewrite). Default preserve; build does not authorize rewriting supplied copy. Audit never changes targets. Use ui/editorial/marketing/report/slides/display from [profiles](profiles/profiles.json).

## Apply the typography contract
Read [24 rules](rules/catalog.json), [locale](locales/hi-IN.json), [source index](references/source-index.md) and [sources](sources.json). Preserve logical order, ZWJ/ZWNJ, nukta, nasal marks, punctuation, quantities, identifiers and names. NFC comparisons are derived only. Hindi is not synonymous with Devanagari or India. No automatic Hinglish, gender guesses, danda conversion or native-digit conversion.

Read [web](references/web.md), [documents](references/documents.md) and [review](references/review.md) for the requested medium. Choose hierarchy, spacing and type roles from the message, not a generic template or script stereotype. Explain reference choices; do not promise AI detection or improved sales.

## Verify and report
Use [24 QA cases](fixtures/qa.json) with exact source text. Optional offline Python 3.12: `python runtime/checks.py original.txt --candidate candidate.txt`. Exit 1 means byte mismatch, even when NFC-derived comparison agrees. This does not inspect rendering, grammar or segmentation. No files are rewritten.

Keep static observations, actual rendering, interaction, editorial proposals and NOT_CHECKED separate. Report location/rule_id/evidence_kind/severity/impact/recommendation/environment/unresolved. Never invent native-speaker, host-install, IME, Office or accessibility results.

## Examples
- “Review क्षि क्षी त्रि ज्ञ श्र स्त्री without editing”: audit + preserve; record source comparison and separate browser shaping findings.
- “Build a 320px Hindi UI; keep OTP 012345 and KUMIHAN”: build + preserve; semantic lang=hi, local ID wrapping, actual reflow and fallback checks.
- “Improve this report”: refine + preserve until wording changes are explicitly scoped; retain master and compare PDF extraction separately.

All supporting files are inside this standalone package. No sibling Skill or network fetch is required.
