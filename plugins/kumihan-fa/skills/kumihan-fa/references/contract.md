# Persian source, scope and evidence contract

Product: KUMIHAN｜تراز, version 0.1.0. The research baseline is the Drive document in sources.json. Scope: modern Iranian standard Persian fa-IR as the proposed default for newly created Iranian content. fa-AF (Dari), Arabic and Tajik Cyrillic are not interchangeable. Explicit user selection takes precedence over metadata and inference.

Modes: study investigates options; build/refine change only permitted materials; audit is strictly read-only. Choose medium (web, copy, document, presentation, print, logo, social), reader, brand and protected text spans before design. Preserve original UTF-8 bytes, source metadata, logical order and formatting intent. NFC/NFKC normalization, Arabic Kaf/Yeh substitution, digit conversion, locale, calendar and currency adjustments require explicit editing authority and contextual checking; never rewrite original by default.

Fa-specific: Persian Kaf ک U+06A9 and Yeh ی U+06CC are distinct from Arabic ك U+0643 and ي U+064A. ZWNJ U+200C (Persian half-space) is distinct from ZWSP U+200B, ZWJ U+200D and regular spaces. Preserve joining and combining marks, ezafe هٔ, presentation forms from source, and all protected names and numbers. Candidate findings are not automatic corrections.

Bidirectional layout: markup is preferred to inserting directional controls; for known Latin identifiers use bdi dir="ltr", for unknown user text consider bdi dir="auto". Do not reverse strings for display or mirror all images and charts.

Design is guided by meaning, medium, reader and brand—not a default three-card page, gradients, generic Nastaliq ornament or mechanized spacing. Consider available licensed fonts only. Rendering, copy/select, browsers, mobile, PDF, Office and native-language acceptance must be verified in their actual host. Do not invent passes.

Evidence status: passed / failed / needs-review / not-checked / unsupported / waived / not-applicable. Record rule_id, scope, host, evidence and remediation. Research fixtures begin not-run.
