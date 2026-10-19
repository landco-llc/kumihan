---
name: kumihan-laras
description: "Definisikan tujuan, bahasa, medium, merek dan izin sunting. | Define purpose, language, medium, brand voice and edit permissions."
---

# KUMIHAN｜Laras · entry

v0.1.0 · Bahasa Indonesia / English · Standalone skill (no sibling language edition required).

1. Read [workflow](references/workflow.md), [34 rules](rules/catalog.json), [65 research sources](sources/public-sources.json), [locale](locales/id-ID.json), and the [acceptance scenarios](fixtures/acceptance.json).
2. Resolve the actual user goal, text role, medium, Indonesian `id` vs number `id-ID`, house style, audience, currency, time zone and authorized edits. Never infer a currency or voice from language alone.
3. Preserve provided UTF-8 source, brand names, prices, dates, IDs, quotes and conditions. Do not silently edit di/ke/dari, reduplication hyphens, `pun`, `kami/kita`, `Anda/kamu` or atypical promotional spellings.
4. Follow EYD V and KBBI for scoped proposals, not universal regex fixes. For headings and body prioritize meaning, reading order, content-specific hierarchy and coherent design rather than generic AI styling.
5. For web start with normal word breaks and `hyphens:manual`; browser dictionaries, PDF, native applications, 320px and 200% layouts require **actual** tests. Static checks remain advisory.
6. In review mode never write to the target. In production mode, change supplied content only with explicit permission and an inspectable diff.
7. Deliver exact evidence, the relevant rule IDs and sources, an implementation or review result, and `needs-review` / `not-checked` where warranted.

Optional offline check: `python runtime/checks.py original.txt --locale id-ID --candidate candidate.txt` (read only; never rewrites source).
