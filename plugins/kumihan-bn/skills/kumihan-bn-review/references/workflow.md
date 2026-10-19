# Workflow / কাজের ধারা

1. Establish a brief and Design Contract: target locale (bn-BD/bn-IN/unknown), original, permission to edit, audience, medium, references, constraints, house style and accessibility expectations.
2. Select rule IDs from `rules/catalog.json`. Preserve source byte-for-byte unless rewrite explicitly approved. Avoid replacing source with NFC or regex cleanup; show NFC comparisons only as diagnostics.
3. Choose typefaces with Bengali shaping (Noto Sans Bengali, Hind Siliguri, Noto Serif Bengali or an approved licensed font). Compare fonts by role, do not infer aesthetic quality from a script stereotype.
4. Use `lang="bn-BD"` or `lang="bn-IN"` as appropriate. If locale unknown, use `lang="bn"` and ask before changing currency, numerals or orthography.
5. Keep Bangla word-breaking normal initially. Avoid global `word-break:break-all`, arbitrary per-grapheme DOM splits, letter spacing on conjuncts and overflow clipping.
6. Preserve organization-specific design, information priority and originality; do not automatically impose a decorative traditional motif or a generic hero+cards+CTA template.
7. Separate reports into static, rendering, editorial and host-install evidence. Record `passed`, `failed`, `needs-review`, `not-checked`, `unsupported`, `waived`, `not-applicable` exactly. Never report browser or native-language passes without performing them.

Sources: https://www.w3.org/TR/beng-lreq/ (2026 draft), https://www.w3.org/International/ilreq/bengali/ (working draft), https://unicode.org/versions/latest/core-spec/chapter-12/ ; KUMIHAN Drive `/RESEARCH/BN` research report 2026-10-19.
