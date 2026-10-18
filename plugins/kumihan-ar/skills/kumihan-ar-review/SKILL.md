---
name: kumihan-ar-review
description: مراجعة قرائية دون تعديل ملفات المصدر أو ادعاء نتائج لم تُختبر. | Read-only review without modifying source files or claiming untested results.
---
# KUMIHAN｜نضيد

Audit only: read references/review.md and the medium-specific reference. Never modify the target, normalize source or silently repair characters. Emit findings and scoped remediation proposals.

1. Read references/contract.md and confirm study / build / audit / refine, explicit language, region, audience and protected original content.
2. Read rules/catalog.json for all 36 rule scopes; implemented-and-tested means only its stated static/byte scope. Read sources.json for public citations, not claims of native execution.
3. Choose the locale profile in locales/. Do not convert digits, punctuation, dates, prices, controls or Tatweel by default; fa/ur specialized Arabic review is unsupported.
4. Read the relevant bundled medium reference. Make semantic direction and logical-order decisions before visual styling. Never prescribe a fixed font pair or reverse Arabic strings.
5. Use runtime/check_source.py only for its documented bounded checks. Preserve raw inputs and supplied metadata; derived NFC is evidence only. Run real rendering/copy/export checks separately when available.
6. Report per-rule status using schemas/report.schema.json. Distinguish observed, guidance-only, not-checked and needs-native-review; give host and reproducible evidence. Audit is read-only.

All supporting files are relative to this skill root; no other language package or network service is required. Native provider import/invocation remains not-checked until actually performed.
