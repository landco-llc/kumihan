---
name: kumihan-lumnung
description: "កំណត់គោលបំណង ភាសា និងសិទ្ធិកែសម្រួល | Scope Khmer typography and purposeful design work."
---

# KUMIHAN｜លំនឹង · workflow

v0.1.0 · ភាសាខ្មែរ / English · standalone Skill · L&Co. LLC

Read `references/workflow.md` and `references/workflow.md`, then all 30 rules in `rules/catalog.json`, the 24 scenarios in `fixtures/acceptance.json`, and `locales/km-KH.json`. Apply KUMIHAN's purpose-driven design and anti-template guidance alongside Khmer script-specific constraints.

- Use `km` / `km-KH` as language identifiers, `Khmr` as script, and `KH` as region; do not infer Khmer from `kh`.
- Protect COENG U+17D2, combining marks, source spaces, ZWSP/WJ/ZWJ/ZWNJ, punctuation, Latin products, amount/date and typographic semantics.
- Do not insert word spaces, word breaks, normalization or legacy encoding conversions without independent validation. Grapheme boundaries are not word boundaries.
- Prefer flexible layout, appropriate Khmer fonts and non-clipping line boxes. Avoid generic AI aesthetics without rationale.
- Review browser reflow and 200% text enlargement, document round trips, copy/search and host registration only when actually tested. Report `needs-review` / `not-checked` when unverified.
- Every issue records its KM-rule ID, source excerpt, evidence status and proposed remedy; native Khmer editorial approval is required for idiomatic or semantic decisions.

Read-only source comparison: `python runtime/checks.py original.txt --locale km-KH --candidate rendered.txt`.
