# Fluxo editorial / Editorial workflow

1. Identify the exact deliverable and source provenance: supplied, quoted, generated or translated proposal.
2. Choose explicit locale (pt, pt-BR, pt-PT, pt-AO, pt-MZ), audience, content role and medium (web, document, presentation, display).
3. Select explicit house style from locales/house-styles.json or inherit a verified project standard. Geography alone MUST NOT impose quotation marks, thousand separators, currency, timezone, address, or editorial tone.
4. Preserve UTF-8 bytes of supplied copy, accents and cedilla, brand names, quotes, dates, numerals, measurements, URLs, identifiers and original semantics.
5. Define the reading order, hierarchy, whitespace, type scale and responsive intent from the content; reject arbitrary AI-looking patterns, repetitive cards and decorative gradients when no editorial purpose exists.
6. Review mode is strictly non-destructive. In authorized production mode, return a clear diff; never silently modify source.
7. Run bounded offline checks with python runtime/checks.py original.txt --locale pt-PT. Findings are review candidates, not automatic corrections.
8. Report static observation separately from rendered browser/Office/PDF verification, native host execution and native Portuguese editorial review.
