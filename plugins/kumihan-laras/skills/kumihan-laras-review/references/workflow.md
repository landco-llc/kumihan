# Alur kerja / Workflow

1. Set language=id and (only when appropriate) numberLocale=id-ID, medium, textRole, audience, editing permission, house style, voice, currency and time zone.
2. Preserve names, UTF-8 text, quotes, prices, dates, identifiers, brand spellings, reduplication hyphens and terms. Do not rewrite without approval and diff.
3. Read rules/catalog.json and sources/public-sources.json; apply EYD V and KBBI with relevant context. Do not use broad regex to equate di toko/dikirim, ke luar/keluar, apa pun/walaupun, kami/kita.
4. Use semantic hierarchy and real content rather than repetitive AI cards or meaningless decoration. Avoid global word-break:break-all and do not claim automatic hyphenation without dictionary/render evidence.
5. Classify findings needs-review where semantics or brand voice are ambiguous, not-checked for untested browser/PDF/native/editor conditions, passed/failed only with evidence.
6. Optional local read-only analyzer: python runtime/checks.py original.txt --locale id-ID; never writes files.
