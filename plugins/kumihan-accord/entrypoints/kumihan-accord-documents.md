---
name: kumihan-accord-documents
description: "Compone informes y presentaciones franceses preservando originales. | Lay out French reports and presentations while preserving sources."
---

# KUMIHAN｜Accord

Compone informes y presentaciones franceses preservando originales.

Lay out French reports and presentations while preserving sources.

Read [workflow](references/workflow.md), [documents](references/documents.md), [review](references/review.md), [house styles](locales/house-styles.json), [rules](rules/catalog.json) and [sources](sources.json) before acting. Four modes: study, build, audit and refine. Audit is read-only. Preserve source words, all whitespace, links, figures, names, accents, Unicode and protected spans. Never treat fr-FR editorial punctuation as mandatory for Québec, EU institutions or unknown Belgian/Swiss house styles. Do not fabricate visual evidence.

Optional static advisor: `python runtime/checks.py INPUT.txt --locale fr-FR --house-style fr-fr-editorial`. Native host, browser and document validation require separate checks.
