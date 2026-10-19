---
name: kumihan-hlela-web
description: "Hlela amawebhusayithi ngesiZulu ngaphandle kokulahla umongo. | Design and review isiZulu websites and interfaces with accessible typography."
---

# KUMIHAN｜Hlela · web

v0.1.0 · isiZulu / English · standalone skill · L&Co. LLC

1. Read references/workflow.md and references/web.md, plus all 24 rules in rules/catalog.json, 20 fixtures in fixtures/acceptance.json, sources/public-sources.json, and locales/zu-ZA.json.
2. Produce responsive HTML/CSS; protect original words and verify actual rendering.
3. Preserve exact original UTF-8 text, isiZulu internal capitalization, long words, prefixes, names, quote marks and date/number meanings. Do not normalize or change source silently.
4. Set lang=zu or zu-ZA on isiZulu text. Do not mistake xh, ss, sw, nd, nr or the KUMIHAN Zilu edition for Zulu.
5. Prefer normal word wrapping and flexible elements to clipping. Do not claim hyphens:auto is supported without an actual verified language dictionary; use editor-approved manual breaks only.
6. Apply purposeful design, not generic AI templates. For web test 320px and native 200% font zoom; for documents test page flow, font fallback and extracted text. Do not claim those tests passed unless executed.
7. Every issue includes source excerpt, location, ZU-rule ID, evidence, proposed correction and observed/needs-review/not-checked. Grammar and typography proposals require native isiZulu editorial review.

Read-only comparison: python runtime/checks.py original.txt --locale zu-ZA --candidate extracted.txt
