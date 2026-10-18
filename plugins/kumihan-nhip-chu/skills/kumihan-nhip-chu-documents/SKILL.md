---
name: kumihan-nhip-chu-documents
description: "Dàn trang tài liệu và bản trình bày tiếng Việt, bảo toàn nguyên bản. | Lay out Vietnamese reports and presentations without changing source content."
---

# KUMIHAN｜Nhịp Chữ

Dàn trang tài liệu và bản trình bày tiếng Việt, bảo toàn nguyên bản.

Lay out Vietnamese reports and presentations without changing source content.

## Before acting

Read [workflow](references/workflow.md), [documents](references/documents.md), [review](references/review.md), [rules](rules/catalog.json), [locale](locales/vi-VN.json) and [sources](sources.json). This Skill is self-contained and does not require the Japanese edition.

## Work modes

- **study**: research design and standards, no edits.
- **build**: create new assets within authorized scope only.
- **audit**: always read-only, evidence with observed / needs-review / not-checked.
- **refine**: change only explicitly authorized sources and show the diff.

## Rules

Protect every original syllable, character, tone mark, number, link, proper noun, price, line break and protected span. Do not silently normalize, translate, proofread or invent claims. Vietnamese spaces can separate syllables, not necessarily whole lexical words; body wrapping and headline phrase decisions are different. Never apply French punctuation spacing or Japanese kinsoku wholesale. Check font glyph coverage and real rendering for accent collisions. Avoid generic AI-looking design: choose visual treatment according to audience, purpose and content rather than forbidding all decoration. Mark any absent rendered or native-host evidence **not-checked**.

Optional non-destructive checker: `python runtime/checks.py input.txt --locale vi-VN`.
