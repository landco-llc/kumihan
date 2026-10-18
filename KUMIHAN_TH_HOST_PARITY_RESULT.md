# KUMIHAN｜ดุลอักษร — host parity correction result

Document: KUMI-TH-HOST-PARITY-CORRECTION-20261018-R2 · 2026-10-18 JST
Status: IMPLEMENTED SOURCE CANDIDATE / DRAFT PR #48. **NOT Release READY; NOT PUBLISHED.**

## Source identity and scope

- Fresh base main: `651a361ac6920ca4061d8f4781ef2c9649fa404e` (includes Korean host parity PR #45).
- Implementation: `e030f42193bb51def6bc587b3b632f3f2d6b6a34`.
- Verified code candidate before this receipt: `ae9f81586e611813e7476ae36bce0f322297514c`. Receipt/evidence-only commits and browser locale configuration follow; the final PR HEAD is recorded in the PR description.
- Branch: `feat/kumihan-th-host-parity-20261018`; isolated worktree; one writer.
- PR: https://github.com/landco-llc/kumihan/pull/48 (`isDraft=true`). No merge or release authorization inferred.
- Receipt/evidence snapshot HEAD: `21d514d680a85c649c63b5e4e038f56578dcef7b`; GitHub potential merge commit at that HEAD: `6dae6ee3e23788b615dd1521d2cc9419f793b9ac` (ephemeral preview, not an actual merge). This final receipt update follows; exact final HEAD/merge-preview and CI are recorded in the PR description.
- PR #42 remains merged at `51a31418fadcd3713875b1805cb15dbc332b2600`.
- Existing `kumihan-th-v0.1.0` tag still points to that older SHA. Never moved, deleted or recreated.
- Existing Release ID `416435873`: `draft=true`, `assets=[]`, `published_at=null` at fresh read.
- Other active work, including ZiHeng PR #46, untouched.

The original feature set remains four independent skills (entry/web/documents/read-only review), 32 rules, six media profiles, exact-source/protected-span checking, official logo, th-TH locale, and three landing plus nine installation pages. The missing ten host artifacts arose from the previous narrow contract of one portable plugin plus four Skills, rather than a complete three-host distribution contract.

## Fifteen artifact matrix

All metadata versions remain 0.1.0 **only as an unapproved source candidate**, with literal `-v0.1.0.zip` names. These are not assets of the old immutable tag. Original five ZIP bytes changed because bilingual Skill descriptions, documentation and inventories changed; no byte-preservation claim is made. Combined manifest precisely maps source path, release asset basename, byte length and SHA256. Each added host also has its own MANIFEST and SHA256SUMS; each ZIP has a complete hashed inventory.

| Host | Artifact/source path | Bytes | SHA256 |
| --- | --- | ---: | --- |
| Claude | `plugins/kumihan-th/downloads/claude/plugins/kumihan-th-Claude-Code-plugin-v0.1.0.zip` | 921674 | `283af5374e967107a5efc1807c12c3786a7c75881824eb1269a8c000827037dc` |
| Claude | `plugins/kumihan-th/downloads/claude/skills/kumihan-th-Claude-skill-v0.1.0.zip` | 28819 | `4a405756ca9ff79778f096c2af6d707f169563c83bcea1b74ed6f3c5268969df` |
| Claude | `plugins/kumihan-th/downloads/claude/skills/kumihan-th-documents-Claude-skill-v0.1.0.zip` | 29236 | `a97b6b8313dd49c16c76761f3da0570262174a3c2229091b0a8749f3068333fa` |
| Claude | `plugins/kumihan-th/downloads/claude/skills/kumihan-th-review-Claude-skill-v0.1.0.zip` | 29120 | `07425585511b71ebdb0708f10f57c58230fc23c4e9a73fea9bc58297f301baa2` |
| Claude | `plugins/kumihan-th/downloads/claude/skills/kumihan-th-web-Claude-skill-v0.1.0.zip` | 29005 | `8cd7e7cd05f0906e5d6d16d9c082206709187c8759a8b244331247175e21e972` |
| Gemini | `plugins/kumihan-th/downloads/gemini/plugins/kumihan-th-Gemini-CLI-extension-v0.1.0.zip` | 922148 | `4ad5223cdd580b17274618252c204d546ec85fd7a2587799959633df3ba0fd5a` |
| Gemini | `plugins/kumihan-th/downloads/gemini/skills/kumihan-th-Gemini-Apps-skill-v0.1.0.zip` | 28819 | `4a405756ca9ff79778f096c2af6d707f169563c83bcea1b74ed6f3c5268969df` |
| Gemini | `plugins/kumihan-th/downloads/gemini/skills/kumihan-th-documents-Gemini-Apps-skill-v0.1.0.zip` | 29236 | `a97b6b8313dd49c16c76761f3da0570262174a3c2229091b0a8749f3068333fa` |
| Gemini | `plugins/kumihan-th/downloads/gemini/skills/kumihan-th-review-Gemini-Apps-skill-v0.1.0.zip` | 29120 | `07425585511b71ebdb0708f10f57c58230fc23c4e9a73fea9bc58297f301baa2` |
| Gemini | `plugins/kumihan-th/downloads/gemini/skills/kumihan-th-web-Gemini-Apps-skill-v0.1.0.zip` | 29005 | `8cd7e7cd05f0906e5d6d16d9c082206709187c8759a8b244331247175e21e972` |
| ChatGPT/Codex | `plugins/kumihan-th/downloads/plugins/kumihan-th-plugin-v0.1.0.zip` | 923908 | `8e73fcbb5d67db210dab8250e32ea53ff3bc80133fd4c4f1ae49f9ad26e349e5` |
| ChatGPT/Codex | `plugins/kumihan-th/downloads/skills/kumihan-th-documents-v0.1.0.zip` | 29236 | `a97b6b8313dd49c16c76761f3da0570262174a3c2229091b0a8749f3068333fa` |
| ChatGPT/Codex | `plugins/kumihan-th/downloads/skills/kumihan-th-review-v0.1.0.zip` | 29120 | `07425585511b71ebdb0708f10f57c58230fc23c4e9a73fea9bc58297f301baa2` |
| ChatGPT/Codex | `plugins/kumihan-th/downloads/skills/kumihan-th-v0.1.0.zip` | 28819 | `4a405756ca9ff79778f096c2af6d707f169563c83bcea1b74ed6f3c5268969df` |
| ChatGPT/Codex | `plugins/kumihan-th/downloads/skills/kumihan-th-web-v0.1.0.zip` | 29005 | `8cd7e7cd05f0906e5d6d16d9c082206709187c8759a8b244331247175e21e972` |

## Checks actually run

- Baseline Thai 16 tests passed before changes. Expanded contract tests initially failed for 5 instead of 15 ZIPs, missing literal v links, and monolingual descriptions; implementation made them pass. Archive-wide Markdown closure regression exposed absent download links in bundled INSTALL; replaced with candidate absolute URLs. Relative `..` links are normalized within ZIP names by the checker.
- Final Thai unit/contract tests: 19 passed (distribution bytes, 15 unique paths, archive inventories/checksums, safe member names and regular-file modes, all Markdown link closure, standalone runtime outside repository, Thai-first + English description rejection, source and protected spans, twelve-page links/hreflang and host-specific download names).
- Japanese: 5 passed. ZiHeng: 16 passed. `build_dist.py --check` 128 files; `build_ziheng.py --check` 110; `check_ja_type_011_cases.py` 11 internally consistent fixtures, not rendered acceptance.
- Thai `build_th.py --check`: 105 generated files; second deterministic check stable. `build_th_site.py --check`: twelve existing URLs, no duplicate pages.
- Node Intl.Segmenter Thai probes passed; sample reconstruction and UTF-16 offsets only, not universal linguistic acceptance.
- 309 tracked Japanese distribution / ZiHeng / Korean source files compared byte-for-byte with base; SHA256 list in `docs/thai/host-parity-evidence/protected-source-digests.json`. Japanese core source/builders also absent from diff. No original non-Thai ZIP was regenerated.
- Logo SHA256 remains `1d1ae2cb4f7f69f7b5f54b050ff8c6fb2c315b75ded8003f8b605855d633f96e`; author L&Co. LLC and Apache-2.0 retained.
- Each archive checked for traversal, duplicate members and symlink modes; packaged Markdown/JSON/Python scanned for private Drive URLs and private-key markers. No runtime dependency on Japanese, ZiHeng or sibling installations.
- Independent bounded read-only review: `parity_review`, one pass, Critical 0 / Important 0. Minor archive reference issue regraded as required standalone closure and fixed with RED→GREEN regression; candidate documentation URLs aligned; generated bytecode excluded. No second review requested.

## Browser evidence and limits

Initial Chromium matrix: 84/96 passed, 12 enlarged Claude/Gemini installation cases overflowed. Root cause: long literal command paths in ordinary paragraphs with normal wrapping. Added `.guide p{{overflow-wrap:anywhere}}`; DOM text unchanged, no clipping hacks.
Second Chromium run: 96/96 passed across 12 pages × 320/375/768/1280px × 100/200% CSS text enlargement. Final explicit th-TH browser locale run: **96/96 passed**, with navigator.language=th-TH recorded for every case in browser-final.json. This is CSS text enlargement, not browser-native text zoom or WCAG certification. Existing static keyboard/language anchor checks passed; inherited interactive keyboard/clipboard claims were not rerun and are not promoted. Mobile Thai screenshot and enlarged English Claude guide visually inspected; no missing glyphs or clipped marks observed in that bounded scope. CDP confirms Noto Sans Thai Bold on inspected Thai h1, with fallback fonts for Latin/fullwidth bar; no universal font prescription. Browser report includes actual fonts; no fonts redistributed.

32 rule statuses remain 4 bounded implemented / 23 assisted / 5 guidance-only. Forty fixture proposals remain 5 bounded static subchecks passed / 35 not-checked, not forty full acceptances. Native Thai editorial review: needs-review. Native Office/PDF and vertical Thai: not-checked.

## Host contracts and native outcomes

Official provider references read 2026-10-18 through the connected web tool:
[Claude manifest](https://code.claude.com/docs/en/plugins-reference), [Gemini extension reference](https://geminicli.com/docs/extensions/reference/).

Claude archive: `.claude-plugin/plugin.json`, supported versionless displayName exactly `KUMIHAN｜ดุลอักษร`, ASCII name `kumihan-th`, four default `skills/` directories. Local load instructions use `claude --plugin-dir /absolute/path/kumihan-th`. No marketplace is required for this local candidate; Japanese marketplace is unchanged.
Gemini archive: `gemini-extension.json`, `GEMINI.md`, four default `skills/` directories; local instructions use `gemini extensions link /absolute/path/kumihan-th`. Gemini reference documents ASCII `name` but no dedicated displayName field. Product title in context/docs is exact and versionless; CLI technical label is `kumihan-th`. Native UI display-name parity is **not established**; no invented supported displayName field is claimed. Author/license are in bundled documentation and LICENSE because Gemini does not document those manifest fields.

All twelve Skill instances have Thai-first + English frontmatter descriptions; plugin/extension descriptions also bilingual. No Japanese mixed into those metadata fields.

Native ChatGPT/Codex plugin/Skill import/invocation: not-checked. Claude Code validation/install/invocation: not-checked (CLI unavailable). Claude Apps import: not-checked. Gemini CLI install/invocation: not-checked (CLI unavailable). Gemini Apps upload/import: not-checked; structural skill ZIPs do not establish Apps support. Public provider marketplace listing: not-checked. Attaching ZIP to chat is not installation.

## HTTP / deployed state

All fifteen branch-source ZIPs fetched with HTTP 200 and exact byte length/SHA256 match against combined manifest. See `candidate-http.json` for each source URL and actual status. These are GitHub source assets, not Release attachments.

Existing Pages URLs were fetched from one managed executor; status per URL below. They serve the currently deployed earlier source, not this unmerged correction. HTTP 200 is not proof of corrected content or a published Release. The draft Release URL was reachable in this execution context; public anonymous Release visibility is not established. No second independent outside execution environment was available for GET verification. No Jekyll/Pages deployment was performed.

| URL | Actual HTTP status |
| --- | ---: |
| https://landco-llc.github.io/kumihan/kumihan-th.html | 200 |
| https://landco-llc.github.io/kumihan/kumihan-th-en.html | 200 |
| https://landco-llc.github.io/kumihan/kumihan-th-ja.html | 200 |
| https://landco-llc.github.io/kumihan/docs/install-kumihan-th-chatgpt.html | 200 |
| https://landco-llc.github.io/kumihan/docs/install-kumihan-th-chatgpt.en.html | 200 |
| https://landco-llc.github.io/kumihan/docs/install-kumihan-th-chatgpt.ja.html | 200 |
| https://landco-llc.github.io/kumihan/docs/install-kumihan-th-claude.html | 200 |
| https://landco-llc.github.io/kumihan/docs/install-kumihan-th-claude.en.html | 200 |
| https://landco-llc.github.io/kumihan/docs/install-kumihan-th-claude.ja.html | 200 |
| https://landco-llc.github.io/kumihan/docs/install-kumihan-th-gemini.html | 200 |
| https://landco-llc.github.io/kumihan/docs/install-kumihan-th-gemini.en.html | 200 |
| https://landco-llc.github.io/kumihan/docs/install-kumihan-th-gemini.ja.html | 200 |
| https://github.com/landco-llc/kumihan/releases/tag/kumihan-th-v0.1.0 | 200 |

## Publication handoff and Owner gate

**BLOCKED for publication only.** Preserve old v0.1.0 tag and draft provenance. Recommended next release: **v0.1.1**, tagged from the approved merged correction, after explicit Owner exact-candidate/version approval. If selected, change all metadata/inventories/manifests and all fifteen names to `-v0.1.1.zip`, update guides and release URLs, rebuild deterministically and revalidate the exact merged source before attaching assets. Do not upload these 0.1.0 candidate bytes as v0.1.1.

Alternative: explicit Owner approval for a controlled unpublished-v0.1.0 retag, recording old SHA `51a31418fadcd3713875b1805cb15dbc332b2600`, exact new approved SHA, rollback to old SHA and draft state, and fresh complete artifact checks. No such approval was supplied here.

Observed provider permissions: GitHub reads and feature-branch push succeeded; Draft PR #48 creation succeeded. CI state for the exact final HEAD is recorded in the PR description; it was still running at this receipt snapshot. Upload/publication permissions were not exercised. No API upload or publish attempted, so no upload 403 is claimed. If a later authorized upload returns 403, preserve Draft/assets and stop that operation without credential bypass.

At the gate, obtain Owner selection between v0.1.1 and controlled v0.1.0 retag; then approve the exact resulting source/label. No release-ready or publication statement is warranted by merge/CI/Pages alone.
