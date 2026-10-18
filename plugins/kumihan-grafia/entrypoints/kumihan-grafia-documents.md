---
name: kumihan-grafia-documents
description: "Estructura documentos y presentaciones en español sin modificar cifras ni citas. | Structure Spanish documents and slides while preserving figures and quotations."
---

# KUMIHAN｜Grafía

Skill independiente de español / Independent Spanish skill, v0.1.0. No sibling plugin is required.

1. Determinar el modo y los límites del encargo con [flujo](references/workflow.md). Inherit unknown region; never infer currency, timezone or tú/vos/usted from country.
2. Leer [guía de la tarea](references/documents.md), [revisión](references/review.md) y [cobertura](references/coverage.md). For entry scope choose the requested medium and use the local web/documents guidance directly; no sibling runtime dependency.
3. Consultar [reglas](rules/catalog.json), [fuentes públicas](sources/public-sources.json), el archivo `locales/<locale>.json` explícito y el perfil `profiles/<medium>.json`. Read only the relevant records, not unrelated private documents.
4. Preserve original UTF-8 bytes, quotations, brands, numbers, dates and IDs. No normalization or content edits in review. For authorized production/refinement, keep original and show bounded diff.
5. Separar candidatos estáticos, observación real y decisiones editoriales. Return findings using [schema](schemas/report.schema.json), actual environment, source hash and unchecked scope. Never infer successful render or host installation.

Optional offline helper: `python runtime/checks.py original.txt --locale es --candidate candidate.txt`. It only reads files and prints JSON. It does not render, translate, normalize or fix text. Standalone resources include [original case coverage](fixtures/acceptance-ledger.json).

Ejemplo: Usa kumihan-grafia-documents con el contexto de mi proyecto; conserva las cifras, los nombres y el original. / Use kumihan-grafia-documents with my project context; preserve figures, names and source text.
