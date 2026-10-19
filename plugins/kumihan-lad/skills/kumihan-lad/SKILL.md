---
name: kumihan-lad
description: "Русская типографика и дизайн по смыслу текста с сохранением оригинала. | Russian typography and content-led design with source preservation."
---

# KUMIHAN｜Лад / entry

v0.1.0 · Русский / English

1. Определите цель, аудиторию, язык, носитель и разрешённые изменения. Identify purpose, audience, context and existing edit authorization.
2. Read `references/contract.md`, `references/typography.md` and `rules/catalog.json`. Use rule authority, applicability and exception fields; 48 entries are not 48 automatic repairs.
3. Preserve ё, й, accents, proper names, quotation, copy, IDs, numbers, URLs and code. NFC comparison does not authorize updating input; never auto NFKC, replace homoglyphs or add ё.
4. Match typography and page structure to information priorities, brand voice and audience. Avoid repeated generic cards, purposeless gradients and artificial rhythm.
5. For Russian copy: handle «…»/„…“, short prepositions, dashes, inflection and hyphenation contextually; do not insert global NBSP or rewrite all punctuation.
6. `runtime/checks.py` provides limited read-only candidates only. Real font rendering, 320px/200% browser output, Office/PDF, native host and native editorial review are `not-checked` until observed.
7. Return original excerpts, rule IDs, suggested actions, evidence classes and remaining exceptions. Make changes only within current authorized edit scope.

Research: https://drive.google.com/drive/folders/12l8XF3yMYHpfP80aAkmhUVO4LYFxXYQP
