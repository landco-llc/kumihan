---
name: kumihan-bn
description: "কাজের উদ্দেশ্য, অঞ্চল, মাধ্যম ও সম্পাদনার অনুমতি নির্ধারণ করুন। | Scope the brief and route to the web, documents or review Skill. Record locale and edit authority."
---

# KUMIHAN｜অক্ষরসজ্জা — kumihan-bn

**Version:** 0.1.0 · বাংলা / English

কাজের উদ্দেশ্য, অঞ্চল, মাধ্যম ও সম্পাদনার অনুমতি নির্ধারণ করুন।
Scope the brief and route to the web, documents or review Skill. Record locale and edit authority.

## Start with the original
1. Read [workflow](references/workflow.md) and [workflow](references/workflow.md).
2. Record `bn-BD`, `bn-IN` or `bn` without inventing the region. Choose media [profiles](profiles/profiles.json) and applicable [36 rules](rules/catalog.json).
3. Treat any protected text as immutable. No silent Unicode normalization, numeral conversion, correction or ZWJ/ZWNJ cleanup. Preserve Bengali combining signs, virama, reph and joint letters.
4. Keep decisions grounded in audience, meaning, hierarchy and the actual medium. Avoid unreasoned AI design conventions.
5. Distinguish static source checks from browser/print rendering and native linguistic review. Use [60 scenarios](fixtures/qa.json) as NOT_CHECKED candidates until executed. Run `python runtime/checks.py source.txt --candidate output.txt` for read-only source comparisons only.
6. Report rule ID, location, evidence, exact text, severity, environment, suggested action, and uncertainty. In review mode, do not write.

**Important:** `Intl.Segmenter` cannot be assumed to preserve every Bangla orthographic syllable for typographic editing or per-letter effects. See `references/web.md` and the W3C [Bengali Layout Requirements](https://www.w3.org/International/ilreq/bengali/). Full host installation and live glyph rendering are not guaranteed by this package.

All referenced resources and the licensed KUMIHAN logo are included in this standalone Skill folder.
