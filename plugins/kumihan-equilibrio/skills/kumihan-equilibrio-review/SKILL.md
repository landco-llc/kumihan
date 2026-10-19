---
name: kumihan-equilibrio-review
description: "Esaminare tipografia e layout italiani in sola lettura, distinguendo prove e proposte. | Review Italian typography and layouts read-only, distinguishing evidence and proposals."
---

# KUMIHAN｜Equilibrio

Skill indipendente / Independent skill; no sibling or plugin is required.

1. Resolve the independent context axes and edit permission in [workflow](references/workflow.md).
2. Read [task guidance](references/review.md), [web](references/web.md), [documents](references/documents.md) and [read-only review](references/review.md) as relevant. Review never edits targets.
3. Consult [rules](rules/catalog.json), [sources](sources/public-sources.json), [coverage](references/coverage.md), [research](references/research.md), [cases](fixtures/acceptance-ledger.json), [it-IT](locales/it-IT.json), [it-CH](locales/it-CH.json) and [report schema](schemas/report.schema.json). All resources are local.
4. Preserve accents, original quotes/names/foreign text, code/URLs/IDs, NFC/NFD bytes, numeric values and timestamps. Separate typesetting_only/proofread/rewrite; changes need scoped permission and a separate proposed diff.
5. Record rule ID, reference, scope, before/after proposal, edit permission, status and environment. Static checks do not prove rendering, dictionary hyphenation or editorial correctness.

Esempio / Example: Usa kumihan-equilibrio-review; conserva nomi, valori e testo originale. / Use kumihan-equilibrio-review; preserve names, values and original content.

Optional offline helper: `python runtime/checks.py original.txt --locale it-CH --candidate candidate.txt`. It only reads and reports; it never rewrites, normalizes or installs. See [license](LICENSE) and [notices](THIRD_PARTY_NOTICES.md).
