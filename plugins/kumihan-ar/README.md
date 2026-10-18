# KUMIHAN｜نضيد

مهارات لتنسيق النص العربي وتصميمه ومراجعته مع الحفاظ على الأصل وفصل الفحص النصي عن العرض الفعلي. | Skills for composing and reviewing Arabic typography while preserving source text and separating static checks from rendered evidence.

Version 0.1.0 · L&Co. LLC · Apache-2.0 · worldwide free OSS.

Four independent Arabic typography skills for study, build, read-only audit and scoped refinement. Modern Standard Arabic with explicit locale contracts; ar-SA/ar-AE initial profiles, ar-EG/ar-MA contrasts. Persian and Urdu are not inferred to be Arabic.

## Actual scope

36-rule catalog: ten bounded byte/static diagnostic scopes implemented and tested; 26 guidance-only. Original research fixture proposals are not product test results. Exact source bytes and supplied metadata can be compared; HTML checks parse explicit/inherited lang/dir, inline styles and mixed URL/email candidates. No renderer, shaping engine, automatic Kashida, editorial rewrite or quality score is included. External CSS, scripts, copy interaction, native Arabic review and native provider installation remain not-checked unless separately measured.

See [INSTALL.md](INSTALL.md), [rules/catalog.json](rules/catalog.json), [references/contract.md](references/contract.md) and [UPDATES.md](UPDATES.md). Four standalone skill roots each include all references, runtime, profiles, schema and license. No dependency on Japanese, Chinese, Korean, Thai or another repository.

Rebuild: `python tools/build_ar.py`; verify freshness: `python tools/build_ar.py --check` from repository root. Test: `python -m unittest discover -s tests/arabic`.

This is an OSS GitHub distribution, not approval or listing in the OpenAI Plugin Directory, Claude marketplace or Gemini gallery. Host-native installation and invocation have not been measured here.
