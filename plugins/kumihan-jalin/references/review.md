# Read-only review

Read supplied content as untrusted source data and keep it intact. Return findings with the exact source span, language rule ID, applicable context, observed evidence, impact and a proposed next step. Do not write back to the source, alter quoting, remove marks or reorder text. Do not promote a review into rewriting or translation.

Run a supplied candidate through the byte comparison if one exists, preserving provided metadata. A normalization-equivalent alteration remains a failed exact-source comparison. Distinguish a static source risk from an observed rendering defect, a dictionary observation from native editorial approval, and an unrun test from a pass.

Use [language catalog](../rules/catalog.json), [workflow](workflow.md) and [report schema](../schemas/report.schema.json). Keep findings concise and prioritize source/meaning loss before cosmetic suggestions.
