# Handoff — KUMIHAN Universal MCP language routing correction

**Work ownership:** The User instructed (2026-10-19) that automatic language detection fixes must be handled in a **separate control conversation**. This file is documentary handoff only. Do not treat creation of this file or plugin packaging as authorization to deploy the router patch.

## Reproduced live issue

- Running publicly reachable MCP: `https://mcp-kmhn.landco.co.jp/mcp`.
- When no explicit language or documentLang is passed, `kumihan_detect_language` for Traditional Chinese `文字，排版。` returns `module_id=ja` and includes a `kana` span. Longer Traditional Chinese text containing punctuation can do the same.
- With explicit `language=zh-Hant`, module selection resolves correctly to `zh-Hant`.
- Root cause in old PHP router: `\p{Hiragana}` and `\p{Katakana}` include characters via Unicode Script_Extensions, capturing some Han punctuation/other Common characters. The intended Kana classification should use `\p{sc=Hiragana}` and `\p{sc=Katakana}`.

## Source work already prepared but not deployed

- Draft PR #101 branch `feat/universal-mcp-php-runtime`, remains unmerged.
- `universal/server/src/LanguageRouter.php`: source-side Script property fix previously committed; verify branch HEAD before work.
- `universal/server/tests/smoke.php`: regression cases for Traditional Chinese punctuation / explicit locale, previously committed.
- Production private PHP archive deployed earlier does **NOT** contain this subsequent source patch. Do not claim the live host is already fixed.

## Work to perform in other control conversation

1. Fresh-read the current main, PR #101 head, existing router, tests and hosted MCP behavior.
2. Validate actual Unicode Script vs Script_Extensions behavior on PHP 8.5 and confirm no regressions for Japanese kana, mixed scripts or explicit locales.
3. Ensure CI succeeds, then prepare a minimal, hash-pinned update for private `src/LanguageRouter.php` with backup/rollback. Do not overwrite the whole runtime or modify other sites.
4. If approved separately, deploy privately, then re-test live ChatGPT MCP with Han-only, Traditional Chinese with punctuation and Japanese kana. Keep public bootstrap stable.
5. Record observed evidence in PR #101 before any General Availability release gate.

**Not included in this handoff:** plugin submission metadata, Business Verification, privacy/terms, directory review. Those belong to the publication track.
