---
name: kumihan-mizani-web
description: "Upangaji wa Kiswahili kwenye tovuti, ukurasa wa kutua na kiolesura. | Swahili website, landing page and interface typography with source fidelity."
---

# KUMIHAN｜Mizani · web

v0.1.0 · Kiswahili / English · standalone skill, no other language edition required.

1. Read [workflow](references/workflow.md), [24 research rules](rules/catalog.json), [source references](sources/public-sources.json), [locale profile](locales/sw-TZ.json) and [24 research fixtures](fixtures/acceptance.json).
2. Read references/web.md; produce responsive HTML/CSS. Reflow at 320px, 200% zoom, image copy and accent/apostrophe preservation must be actually tested.
3. Preserve supplied UTF-8 source, proper names, codes, quotations, values, dates and apostrophe code points. `ng` and `ng’` are not interchangeable. Propose edits only when permitted and show their diff.
4. Do not change event timestamps based on the Swahili clock convention. Never infer currency or region from `sw`; support `sw-TZ`, `sw-KE`, `sw-UG`, and `sw-CD` explicitly.
5. Avoid generic AI layouts and decorative motifs when they serve no purpose. Preserve reader comprehension and the brand's documented design intent.
6. Record relevant SW-rule IDs, evidence, and unresolved `needs-review` / `not-checked` states. Do not assert verification of a browser, font, PDF or native host that was not executed.

Offline source check (read-only): `python runtime/checks.py source.txt --locale sw-TZ --candidate rendered-extract.txt`.
