---
name: kumihan-satzbild-web
description: "Deutschsprachige Websites und Oberflächen mit lesbarer Typografie, sinnvollen Umbrüchen und begründetem Design gestalten. | Design German websites and interfaces with readable typography, considered line breaks and purposeful layout."
---

# KUMIHAN｜Satzbild

Eigenständiger Skill / Independent German skill. No sibling skill or plugin is required.

1. Resolve explicit locale, purpose, medium and permitted edits using [workflow](references/workflow.md). Unknown context is recorded, never guessed.
2. Apply [task guidance](references/web.md), [web](references/web.md), [documents](references/documents.md) and [read-only review](references/review.md) as relevant. Review never edits the target.
3. Consult [rules](rules/catalog.json), [sources](sources/public-sources.json), [coverage](references/coverage.md) and [research cases](fixtures/acceptance-ledger.json). Local resources include locales/de-DE.json, locales/de-AT.json, locales/de-CH.json and profiles/*.json. No other language edition is required.
4. Preserve names, brands, prices, dates, numbers, quotations, ß/ẞ/SS, umlauts and original bytes. Separate typesetting_only/proofread/rewrite; show explicit diffs for authorized content edits.
5. Use [report schema](schemas/report.schema.json). Separate static/render/editorial evidence and actual environment. Record all unchecked scope honestly.

Optional offline helper: `python runtime/checks.py original.txt --locale de-CH --candidate candidate.txt`. It reads UTF-8 files and prints JSON; it never rewrites, normalizes, translates, renders or installs anything.

Anwendung / Example: Nutze kumihan-satzbild-web; bewahre Namen, Zahlen und Originaltext. / Use kumihan-satzbild-web; preserve names, figures and original text.
